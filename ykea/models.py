from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    id_customer = models.AutoField(primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=20, decimal_places=2)

class Item(models.Model):
    CATEGORIES = (
        ("beds", "Beds & mattressess"),
        ("furn", "Furniture, wardrobes & shelves"),
        ("sofa", "Sofas & armchairs"),
        ("table", "Tables & chairs"),
        ("texti","Textiles"),
        ("deco","Decoration & mirrors"),
        ("light","Lighting"),
        ("cook","Cookware"),
        ("tablw","Tableware"),
        ("taps","Taps & sinks"),
        ("org", "Organisers & storage accesories"),
        ("toys","Toys"),
        ("leis","Leisure"),
        ("safe","safety"),
        ("diy", "Do-it-yourself"),
        ("floor","Flooring"),
        ("plant","Plants & gardering"),
        ("food","Food & beverages")
    )
    item_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    is_new = models.BooleanField()
    size = models.CharField(max_length=40)
    instructions = models.FileField(upload_to="instructions")
    featured_photo = models.ImageField(upload_to="images")
    category = models.CharField(max_length=5, choices=CATEGORIES)
    def __str__(self):
        return  ('[**NEW**]' if self.is_new else '') + "[" + self.category + "] [" + self.item_number + "] " + self.name + " - " + self.description + " (" + self.size + ") : " + str(self.price) + " €"

class Shoppingcart(models.Model):

    id_shoppingcart = models.AutoField(primary_key=True)

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Item, through='Itemquantity')

    def __str__(self):
        return "ID: " + str(self.id_shoppingcart)

class Itemquantity(models.Model):

    id_itemquantity = models.AutoField(max_length=20, primary_key=True, unique=True)

    shoppingcart = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    amountItem = models.CharField(max_length=20, null=False)

class Bill(models.Model):

    id_bill = models.AutoField(primary_key=True)

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='id')
    linebill = models.ManyToManyField(Item, through='Linebill')

    total = models.DecimalField(max_digits=20, decimal_places=2)

class Linebill(models.Model):

    id_linebill = models.AutoField(max_length=20, primary_key=True, unique=True)

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='Bill')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    quantity = models.CharField(max_length=20, null=False)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)