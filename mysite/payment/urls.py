from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('payment_success/', views.payment_success, name = 'payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('Order_processing/', views.process_order, name='process_order')
]