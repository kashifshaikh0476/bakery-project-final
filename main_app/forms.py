from django import forms
from .models import Order

# BoxForm aur Box model ki ab zaroorat nahi hai

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Ye wo fields hain jo customer bharega
        fields = ('customer_name', 'customer_email', 'customer_phone', 'address', 'city', 'quantity')
        
        # Form ko sundar banane ke liye styling (Widgets)
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        }

class OrderTrackerForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status', )
