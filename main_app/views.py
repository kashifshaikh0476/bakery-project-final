from django.shortcuts import render, redirect
from .models import Order, Map, Product, Feedback
from .forms import OrderForm, OrderTrackerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
# Ye line zaroori hai calculation ke liye
from django.db.models import Sum, F  

# --- CUSTOM LOGOUT ---
def custom_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def about(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        msg = request.POST.get('message')
        stars = request.POST.get('rating')
        if name and stars: 
            Feedback.objects.create(
                customer_name=name,
                message=msg,
                rating=stars
            )
        return redirect('about') 
    return render(request, 'about.html')

def shop(request):
    products = Product.objects.all() 
    return render(request, 'shop.html', {'products': products})

# --- STATUS FUNCTION (UPDATED) ---
# Ab ye check karega ki request kahan se aayi hai (Dashboard se ya Detail se)
# Aur wahi wapas bhejega.
def status(request, order_id):
    found_order = Order.objects.get(id=order_id)
    get_status = request.POST.get('status')
    
    if get_status:
        found_order.status = get_status
        found_order.save()
    
    # Check Previous Page URL
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
        
    return redirect('detail', order_id)

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = { 'orders': orders }
    return render(request,'order/order.html', context)

# --- ADMIN DASHBOARD (UPDATED) ---
# Isme ab Counting aur Revenue ka Logic hai
@user_passes_test(lambda u: u.is_superuser) 
def admin_order(request):
    orders = Order.objects.all().order_by('-id')
    
    # 1. Total Orders Count
    total_orders = orders.count()
    
    # 2. Pending Orders Count
    pending_count = Order.objects.filter(status='Pending').count()
    
    # 3. Revenue Calculation (Price * Quantity)
    revenue_data = Order.objects.aggregate(total=Sum(F('product__price') * F('quantity')))
    revenue = revenue_data['total'] if revenue_data['total'] else 0
    
    context = { 
        'orders': orders,
        'total_orders': total_orders,
        'pending_count': pending_count,
        'revenue': revenue
    }
    return render(request,'order/admin_dashboard.html', context)

@login_required
def detail(request, order_id):
    found_order = Order.objects.get(id=order_id)
    order_tracker = OrderTrackerForm()
    
    context = { 
        'order': found_order,
        'order_tracker': order_tracker
     }
    return render(request, 'order/order_detail.html', context)

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
            order.save()
            
            return redirect(f'/order/{order.id}/?placed=true') 
    
    context = { 'form': form, 'product': product }
    return render(request, 'order/create_order.html', context)

@login_required
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order')

def map_display(request):
    try:
        map = Map.objects.first() 
    except:
        map = None
    return render(request, 'about')

@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = { 'form': form }
        return render(request, 'order/update_order.html', context)
    else: 
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order=form.save()
            return redirect('detail', order.id)

@login_required
def order_tracker(request, order_id):
    form = OrderTrackerForm(request.POST)
    if form.is_valid():
        new_tracking = form.save(commit=False)
        new_tracking.order_id = order_id
        new_tracking.save()
        return redirect('detail', order_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm (request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('order')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
