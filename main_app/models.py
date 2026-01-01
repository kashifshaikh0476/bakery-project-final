from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields

# ==========================
# 1. CHOICE TUPLES (Constants)
# ==========================

# Packing Options
BOX = (
    ('1', 'Single Item'),
    ('4', '4 Pack'),
    ('6', '6 Pack'),
    ('12', '12 Pack'),
)

# Bakery Menu Items
ORDER_ITEMS = (
    ('BR', 'Bread'),
    ('DG', 'Dough'),
    ('CK', 'Cookies'),
    ('MF', 'Muffins'),
    ('BS', 'Biscuits'),
    ('CP', 'Cupcakes'),
    ('PT', 'Pastries'),
    ('DN', 'Donut'),
    ('CR', 'Cream Roll'),
    ('CB', 'Chess Bars'),
    ('CH', 'Cheesecake Bars'),
    ('KP', 'Cake Pops'),
    ('TC', 'Tea Cakes'),
    ('CHB', 'Shooseberry'),
    ('PT', 'Pattice'),
)

# Order Status 
STATUS = (
    ('sc', 'Scheduled'),
    ('ip', 'In Progress'),
    ('re', 'Ready For Pickup'),
    ('pu', 'Picked up'),
)

# ==========================
# 2. MODELS
# ==========================

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField('Name', max_length=100)
    customer_email = models.EmailField('Email', max_length=100)
    customer_phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(
        'Order Status',
        max_length=2, 
        choices=STATUS, 
        default=STATUS[0][0]
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class Box(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    date = models.DateField('Date Needed By')
    box = models.CharField(
        'Box Size',
        max_length=2,
        choices=BOX,
        default=BOX[0][0]
    )
    item_ordered = models.CharField(
        'Item Selected',
        max_length=3,
        choices=ORDER_ITEMS,
        default=ORDER_ITEMS[0][0]
    )

    def __str__(self):
        return f"{self.get_box_display()} - {self.get_item_ordered_display()}"


class Map(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def __str__(self):
        return self.address


class Feedback(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    rating = models.IntegerField(default=5, help_text="Rating out of 5")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating} Stars"