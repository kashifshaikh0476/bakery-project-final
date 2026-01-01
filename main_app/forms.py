from django import forms
from django.db.models.fields import DateField
from .models import Order, Box


class OrderForm (forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'customer_email', 'customer_phone')
        

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ('date', 'box', 'item_ordered')

class OrderTrackerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status', ) 
