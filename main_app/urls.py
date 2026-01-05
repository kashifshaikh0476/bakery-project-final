from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    # UPDATED: Product ID ke sath link
    path('create_order/<int:product_id>/', views.create_order, name='create_order'),
    
    path('order/', views.order, name='order'),
    path('admin_order/', views.admin_order, name='admin_order'),
    path('order/<int:order_id>/', views.detail, name='detail'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/update/', views.update_order, name='update_order'),
    path('order/<int:order_id>/tracking/', views.order_tracker, name='order_tracker'),
    path('accounts/signup/', views.signup, name='signup'),
    
    # Status update path
    path('order/<int:order_id>/status/', views.status, name='status'),
]
