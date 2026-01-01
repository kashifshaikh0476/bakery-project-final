from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Box, Map
from .forms import OrderForm, BoxForm, OrderTrackerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product 
from django.shortcuts import render, redirect
from .models import Feedback # Feedback model import karna zaroori hai

def home(request):
    return render(request, 'home.html')



def about(request):
    # Agar Form Submit hua hai (POST request)
    if request.method == 'POST':
        # 1. HTML se data nikalo
        name = request.POST.get('customer_name')
        msg = request.POST.get('message')
        stars = request.POST.get('rating')

        if name and stars: 
            Feedback.objects.create(
                customer_name=name,
                message=msg,
                rating=stars
            )
            print("Feedback Saved!") 
            
        return redirect('about') # Page reload 

    
    return render(request, 'about.html')


def shop(request):
    # Database se saare products laao
    products = Product.objects.all() 
    # In products ko HTML page (shop.html) par bhejo
    return render(request, 'shop.html', {'products': products})

def status(request, order_id):
    found_order = Order.objects.get(id=order_id)
    # print('hit the status view', order_id)
    get_status = request.POST.get('status')
    # print('$$$$$GET STATUS$$$$$', get_status)
    # found_order.status = get_status
    # form = OrderForm(found_order)
    # if form.is_valid():
    #  order=form.save(commit=False)
    found_order.status=get_status
    found_order.save()
    return redirect('detail', order_id)
    # form = OrderTrackerForm(request.POST)
    # print('==========================', form)
    # if form.is_valid():
    #     new_tracking = form.save(commit=False)
    #     new_tracking.order_id = order_id
    #     # new_tracking.save()
    #     print('***** NEW TRACKING*********', new_tracking)
    #     return redirect('detail', order_id)



# ---------------------------------------------------------
# 1. CUSTOMER SIDE (Sirf Apne Order Dikhenge)
# ---------------------------------------------------------
@login_required
def order(request):
    # Logic: Sirf wahi orders lao jisme user = current_user ho
    # .order_by('-id') ka matlab naya order sabse upar dikhega
    orders = Order.objects.filter(user=request.user).order_by('-id')
    
    # Customer ko 'order/order.html' dikhayenge
    context = { 'orders': orders }
    return render(request,'order/order.html', context)


# ---------------------------------------------------------
# 2. ADMIN SIDE (Sabke Order Dikhenge)
# ---------------------------------------------------------
# Ye check karega ki banda Superuser (Admin) hai ya nahi.
@user_passes_test(lambda u: u.is_superuser) 
def admin_order(request):
    # Logic: Saare orders le aao
    orders = Order.objects.all().order_by('-id')

    # Admin ko 'order/admin_dashboard.html' dikhayenge (Alag File)
    context = { 'orders': orders }
    return render(request,'order/admin_dashboard.html', context)
#ORDER DETAIL PAGE 
@login_required
def detail(request, order_id):
    found_order = Order.objects.get(id=order_id)
    print(found_order)
# THIS MAKES THE FORM SHOW UP :
    box_form = BoxForm()
    order_tracker = OrderTrackerForm()
    context = { 
        'order': found_order,
        'box_form': box_form,
        'order_tracker': order_tracker
    
     }

    

    return render(request, 'order/order_detail.html', context)
# CREATE ORDER is CUSTOMER INFO PAGE:  -----------------------
@login_required
def create_order(request):
    form = OrderForm()
    context = { 'form': form }
    if request.method == 'GET':
        return render(request, 'order/create_order.html', context)
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('detail', order.id)
        else:
            return render(request, 'order/create_order.html', context)

# Delete Order-------------
@login_required
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order')

def map_display(request):
    map = Map.objects.get()
    return render(request, 'about')


# Update Order-------
@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = {
            'form': form
        }
        return render(request, 'order/update_order.html', context)
    else: 
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order=form.save()
            return redirect('detail', order.id)
# Add Box Size Form:
@login_required
def box(request, order_id):
    form = BoxForm(request.POST)
    if form.is_valid():
        new_box_size = form.save(commit=False)
        new_box_size.order_id = order_id
        new_box_size.save()
        return redirect('detail', order_id)

#Delete Box:
@login_required
def delete_box(request, order_id, box_id):
    order = Order.objects.get(id=order_id)
    found_box = Box.objects.get(id=box_id)
    order.box_set.remove(found_box)

    return redirect('detail', order_id = order_id)


    
# Order Tracker Form------
@login_required
def order_tracker(request, order_id):
    form = OrderTrackerForm(request.POST)
    if form.is_valid():
        new_tracking = form.save(commit=False)
        new_tracking.order_id = order_id
        new_tracking.save()
        return redirect('detail', order_id)

# SIGN UP FORM:

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

 