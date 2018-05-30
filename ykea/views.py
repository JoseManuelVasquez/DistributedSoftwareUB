from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Item, Shoppingcart, Itemquantity, Customer, Bill, Linebill
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

"""
********************* ITEM AND BUY VIEWS *********************
"""

def index(request):
    return render(request, 'ykea/index.html', {})

# All categories in Database
def categories(request):
    categories = Item.CATEGORIES

    try:
        currentCustomer = User.objects.get(username=request.user).customer
        number_items = len(Shoppingcart.objects.get(user=currentCustomer).items.all())
    except(KeyError, User.DoesNotExist, AttributeError, Shoppingcart.DoesNotExist):
        number_items = 0

    try:
        currentMoney = Customer.objects.get(user=User.objects.get(username=request.user)).money
    except(KeyError, Customer.DoesNotExist, User.DoesNotExist):
        currentMoney = 0

    context = {
        'categories': categories,
        'number_items': number_items,
        'money': currentMoney
    }
    return render(request, 'ykea/categories.html', context)

# Category of items view
def items_category(request,category=""):
    items_by_category = Item.objects.filter(category=category)

    try:
        currentCustomer = User.objects.get(username=request.user).customer
        number_items = len(Shoppingcart.objects.get(user=currentCustomer).items.all())
    except(KeyError, User.DoesNotExist, AttributeError, Shoppingcart.DoesNotExist):
        number_items = 0

    try:
        currentMoney = Customer.objects.get(user=User.objects.get(username=request.user)).money
    except(KeyError, Customer.DoesNotExist, User.DoesNotExist):
        currentMoney = 0

    context = {
        'items': items_by_category,
        'category': category,
        'number_items': number_items,
        'money': currentMoney
    }
    return render(request, 'ykea/items_category.html', context)

# Item detail view
def item_detail(request, item_number=""):
    item = Item.objects.get(item_number=item_number)

    try:
        currentCustomer = User.objects.get(username=request.user).customer
        number_items = len(Shoppingcart.objects.get(user=currentCustomer).items.all())
    except(KeyError, User.DoesNotExist, AttributeError, Shoppingcart.DoesNotExist):
        number_items = 0

    try:
        currentMoney = Customer.objects.get(user=User.objects.get(username=request.user)).money
    except(KeyError, Customer.DoesNotExist, User.DoesNotExist):
        currentMoney = 0

    context = {
        'item': item,
        'number_items': number_items,
        'money': currentMoney
    }
    return render(request, 'ykea/item_detail.html', context)

# We look in the DB, and we add every item in the cart if exists, also the amount
@login_required
def shoppingcart(request):
    currentCustomer = User.objects.get(username=request.user).customer

    try:
        shopping = Shoppingcart.objects.get(user=currentCustomer)
    except(KeyError, Shoppingcart.DoesNotExist):
        shopping = Shoppingcart(user=currentCustomer)
    shopping.save()

    selectedItems = []
    amountItems = []
    for selected in Itemquantity.objects.filter(shoppingcart=Shoppingcart.objects.get(user=currentCustomer)):
        selectedItems.append(selected.item.item_number)
        amountItems.append(selected.item.item_number + "-" + selected.amountItem)

    for key in request.POST:
        if key.startswith("checkbox"):
            if request.POST[key] not in selectedItems:
                selectedItems.append(request.POST[key])
        if key.startswith("amount"):
            for amount in amountItems:
                if (key[6:] + "-") in amount:
                    amountItems.remove(amount)
            amountItems.append(key[6:] + "-" + request.POST[key])
    request.session["selectedItem"] = selectedItems
    request.session["amountItem"] = amountItems
    return HttpResponseRedirect(reverse('buy'))

# Method for going through the session and add new items if so
@login_required
def buy(request):
    currentCustomer = User.objects.get(username=request.user).customer
    currentMoney = currentCustomer.money

    try:
        shopping = Shoppingcart.objects.get(user=currentCustomer)
    except(KeyError, Shoppingcart.DoesNotExist):
        shopping = Shoppingcart(user=currentCustomer)
    shopping.save()

    items = []
    try:
        for item in request.session["selectedItem"]:
            for amount in request.session["amountItem"]:
                amountItem = amount.split("-")[0]
                am = 1
                if amountItem == item:
                    am = amount.split("-")[1]
                    break
            try:
                inter = Itemquantity.objects.get(shoppingcart=shopping, item=Item.objects.get(item_number=item))
                inter.amountItem = am
            except(KeyError, Itemquantity.DoesNotExist):
                inter = Itemquantity(shoppingcart=shopping, item=Item.objects.get(item_number=item), amountItem=am)
            inter.save()
            items.append((Item.objects.get(item_number=item), inter.amountItem))
    except(KeyError):
        pass

    context = {
        'items': items,
        'number_items': len(Shoppingcart.objects.get(user=currentCustomer).items.all()),
        'money': currentMoney
    }

    return render(request, "ykea/shoppingcart.html", context)

# Kind of listener for delete and checkout buttons
@login_required
def process(request):
    for item in request.POST:
        if item.startswith("delete"):
            item_number = item[6:]
            return HttpResponseRedirect(reverse('delete', kwargs={'item_number': item_number}))
        elif item == "checkout":
            return HttpResponseRedirect(reverse('checkout'))

# Method for deleting an item
@login_required
def delete(request, item_number):
    currentCustomer = User.objects.get(username=request.user).customer
    Itemquantity.objects.get(shoppingcart=Shoppingcart.objects.get(user=currentCustomer), item=Item.objects.get(item_number=item_number)).delete()

    items = [item for item in request.session["selectedItem"] if item != item_number]
    request.session["selectedItem"] = items

    return HttpResponseRedirect(reverse('buy'))

# We check all the items in the cart, and we make a bill
@login_required
def checkout(request):
    currentCustomer = User.objects.get(username=request.user).customer

    # New bill for current user
    bill = Bill(user=currentCustomer, total=0)
    bill.save()

    totalPrice = 0
    items = []
    inters = [item for item in Itemquantity.objects.filter(shoppingcart=Shoppingcart.objects.get(user=currentCustomer))]
    for inter in inters:
        for amount in request.session["amountItem"]:
            amountItem = amount.split("-")[0]
            am = 1
            if amountItem == inter.item.item_number:
                am = amount.split("-")[1]
                break

        # Partial bill
        linebill = Linebill(bill=bill, item=inter.item, quantity=am, subtotal=float(int(am) * inter.item.price))
        linebill.save()

        totalPrice += linebill.subtotal
        items.append((linebill.item, linebill.quantity))

    bill.total = totalPrice
    bill.save()

    # If current user has enough money, he can buy items
    if totalPrice > currentCustomer.money:
        bill.delete()
        return render(request, "ykea/not_enough_money.html", {})

    currentCustomer.money = float(currentCustomer.money) - totalPrice
    currentCustomer.save()

    context = {
        'items': items,
        'totalPrice': totalPrice
    }

    request.session["selectedItem"] = []
    Itemquantity.objects.filter(shoppingcart=Shoppingcart.objects.get(user=currentCustomer)).delete()

    return render(request, "ykea/checkout.html", context)

"""
********************* USER VIEWS *********************
"""

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_customer = Customer(user=User.objects.get(username=request.POST['username']), money=4000) # 4000 money for new customer
            new_customer.save()
            return HttpResponseRedirect(reverse("categories"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

"""
********************* API Django Rest Framework *********************
"""

# Filtering of items
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('item_number')
    serializer_class = ItemSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        new = self.request.query_params.get('new', None)
        price = self.request.query_params.get('price', None)

        if category and not new and not price:
            return Item.objects.filter(category=category)

        if not category and new and not price:
            return Item.objects.filter(is_new=(new == "yes"))

        if not category and not new and price:
            return Item.objects.filter(price__lt=price)

        if category and new and not price:
            return Item.objects.filter(category=category, is_new=(new == "yes"))

        if category and not new and price:
            return Item.objects.filter(category=category, price__lt=price)

        if not category and new and price:
            return Item.objects.filter(is_new=(new == "yes"), price__lt=price)

        if category and new and price:
            return Item.objects.filter(category=category, is_new=(new == "yes"), price__lt=price)

        return Item.objects.all()

"""
********************* Comparator *********************
"""

def comparator(request, ips):
    context = {
        'ips': ips,
        'categories': categories
    }

    return render(request, "ykea/comparator.html", context)