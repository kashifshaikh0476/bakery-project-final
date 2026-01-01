from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('order/order', views.order, name='order'),
    path('order/admin_order', views.admin_order, name='admin_order'),
    path('order/create_order', views.create_order, name='create_order'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/edit/', views.update_order, name='update_order'),
    path('order/<int:order_id>/box/', views.box, name='box'),
    path('order/<int:order_id>/status/', views.status, name='status'),
    path('order/<int:order_id>/delete_box/<int:box_id>/', views.delete_box, name='delete_box'),
    path('accounts/signup', views.signup, name='signup'),

    # Below path takes us to the details of an order:
    path('order/<int:order_id>/', views.detail, name='detail')
    
]

# Steps to create a new page
# 1. Create the path in urls.py
# 2. Create a view function
# 3. Create the template for the page