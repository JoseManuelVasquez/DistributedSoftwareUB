from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    id_customer = models.AutoField(db_index=False, primary_key=True)

    user = models.OneToOneField(User, db_index=False, on_delete=models.CASCADE)
    money = models.DecimalField(db_index=False, max_digits=8, decimal_places=2)

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
    item_number = models.CharField(db_index=False, max_length=10, unique=True)
    name = models.CharField(db_index=False, max_length=50)
    description = models.TextField()
    price = models.DecimalField(db_index=False, max_digits=8, decimal_places=2)
    is_new = models.BooleanField()
    size = models.CharField(db_index=False, max_length=40)
    instructions = models.FileField(upload_to="instructions")
    featured_photo = models.ImageField(upload_to="images")
    category = models.CharField(db_index=False, max_length=5, choices=CATEGORIES)
    def __str__(self):
        return  ('[**NEW**]' if self.is_new else '') + "[" + self.category + "] [" + self.item_number + "] " + self.name + " - " + self.description + " (" + self.size + ") : " + str(self.price) + " €"

class Shoppingcart(models.Model):

    id_shoppingcart = models.AutoField(db_index=False, primary_key=True)

    user = models.ForeignKey(Customer, db_index=False, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Item, db_index=False, through='Itemquantity')

    def __str__(self):
        return "ID: " + str(self.id_shoppingcart)

class Itemquantity(models.Model):

    id_itemquantity = models.AutoField(db_index=False, max_length=8, primary_key=True, unique=True)

    shoppingcart = models.ForeignKey(Shoppingcart, db_index=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, db_index=False, on_delete=models.CASCADE)

    amountItem = models.CharField(db_index=False, max_length=10, null=False)

class Bill(models.Model):

    id_bill = models.AutoField(primary_key=True)

    user = models.ForeignKey(Customer, db_index=False, on_delete=models.CASCADE, related_name='id')
    linebill = models.ManyToManyField(Item, db_index=False, through='Linebill')

    total = models.DecimalField(db_index=False, max_digits=8, decimal_places=2)

class Linebill(models.Model):

    id_linebill = models.AutoField(db_index=False, max_length=8, primary_key=True, unique=True)

    bill = models.ForeignKey(Bill, db_index=False, on_delete=models.CASCADE, related_name='Bill')
    item = models.ForeignKey(Item, db_index=False, on_delete=models.CASCADE)

    quantity = models.CharField(db_index=False, max_length=10, null=False)
    subtotal = models.DecimalField(db_index=False, max_digits=8, decimal_places=2)