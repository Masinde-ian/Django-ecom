from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('payment_success/', views.payment_success, name = 'payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_processing/', views.process_order, name='process_order'),
    path('orders', views.orders, name='orders'),
    path('delivered-orders/', views.delivered_orders, name='delivered_orders')
]