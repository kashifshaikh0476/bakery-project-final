import os
import qrcode
import io
import base64
from django.shortcuts import render, redirect
from .models import Order, Map, Product, Feedback
from .forms import OrderForm, OrderTrackerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F 

# --- HELPER: DYNAMIC QR GENERATOR ---
def generate_upi_qr(amount, order_id):
    upi_id = "8421857457@ybl" 
    name = "A1%20Bakery"
    # Generating UPI Link for auto-price detection
    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn=Order_{order_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- AUTHENTICATION ---
def custom_logout(request):
    logout(request)
    return redirect('home')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/order/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})

# --- PUBLIC PAGES ---
def home(request):
    return render(request, 'home.html')

def about(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        msg = request.POST.get('message')
        stars = request.POST.get('rating')
        if name and stars: 
            Feedback.objects.create(customer_name=name, message=msg, rating=stars)
        return redirect('about') 
    return render(request, 'about.html')

def shop(request):
    products = Product.objects.all() 
    return render(request, 'shop.html', {'products': products})

# --- ORDER MANAGEMENT ---
@login_required
def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            
            pay_method = request.POST.get('payment_type') 
            trans_id = request.POST.get('transaction_id')

            if pay_method == 'online' and (not trans_id or len(trans_id) < 12):
                return render(request, 'order/create_order.html', {
                    'form': form, 'product': product, 'error': '12-digit Transaction ID is required!'
                })

            order.transaction_id = trans_id
            order.save()
            return redirect('detail', order_id=order.id) 
    
    return render(request, 'order/create_order.html', {'form': form, 'product': product})

@login_required
def detail(request, order_id):
    found_order = Order.objects.get(id=order_id)
    order_tracker = OrderTrackerForm()
    total_amount = found_order.product.price * found_order.quantity
    qr_code = generate_upi_qr(total_amount, found_order.id)
    
    return render(request, 'order/order_detail.html', {
        'order': found_order, 'order_tracker': order_tracker, 'qr_code': qr_code, 'total_amount': total_amount
    })

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request,'order/order.html', {'orders': orders})

@login_required
def delete_order(request, order_id):
    # This was the missing function causing the error
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order')

@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        return render(request, 'order/update_order.html', {'form': form})
    else: 
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order=form.save()
            return redirect('detail', order_id=order.id)

# --- ADMIN DASHBOARD ---
@user_passes_test(lambda u: u.is_superuser) 
def admin_order(request):
    orders = Order.objects.all().order_by('-id')
    total_orders = orders.count()
    pending_count = Order.objects.filter(status='Pending').count()
    revenue_data = Order.objects.aggregate(total=Sum(F('product__price') * F('quantity')))
    revenue = revenue_data['total'] if revenue_data['total'] else 0
    return render(request,'order/admin_dashboard.html', {
        'orders': orders, 'total_orders': total_orders, 'pending_count': pending_count, 'revenue': revenue
    })

def status(request, order_id):
    found_order = Order.objects.get(id=order_id)
    get_status = request.POST.get('status')
    if get_status:
        found_order.status = get_status
        found_order.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page if previous_page else 'detail', order_id=order_id)

@login_required
def order_tracker(request, order_id):
    form = OrderTrackerForm(request.POST)
    if form.is_valid():
        new_tracking = form.save(commit=False)
        new_tracking.order_id = order_id
        new_tracking.save()
    return redirect('detail', order_id=order_id)

def map_display(request):
    try:
        map = Map.objects.first() 
    except:
        map = None
    return render(request, 'about')
