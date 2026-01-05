from django.db import models
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields

# ==========================
# 1. CHOICE TUPLES (Updated)
# ==========================

# Professional Status Options (Admin Control)
STATUS_CHOICES = (
    ('Pending', 'Pending'),            # Order abhi aaya hai
    ('Scheduled', 'Scheduled'),        # Plan ho gaya
    ('In Progress', 'In Progress'),    # Ban raha hai
    ('Packed', 'Packed'),              # Pack ho gaya
    ('Shipped', 'Shipped'),            # Nikal gaya
    ('Ready For Pickup', 'Ready For Pickup'),
    ('Delivered', 'Delivered'),
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
    
    # 1. Product Link: Shop se jo select kiya wo yahan aayega
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    # 2. Quantity: Box size ki jagah ab quantity hai
    quantity = models.PositiveIntegerField(default=1)

    # 3. Customer Info
    customer_name = models.CharField('Name', max_length=100)
    customer_email = models.EmailField('Email', max_length=100)
    customer_phone = models.CharField(max_length=15)
    
    # 4. Address Fields (Form me the, isliye yahan zaroori hain)
    address = models.TextField(default="", blank=True) 
    city = models.CharField(max_length=100, default="", blank=True)

    # 5. Status (Default 'Pending' rahega, User change nahi kar payega)
    status = models.CharField(
        'Order Status',
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Admin panel me saaf dikhega: "Order #1 - Chocolate Cake (Qty: 2)"
        product_name = self.product.name if self.product else "Unknown Item"
        return f"Order #{self.id} - {product_name} (Qty: {self.quantity})"


# Box Model hata diya kyunki ab 'Quantity' aur 'Product' Order model me hi hain.

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
