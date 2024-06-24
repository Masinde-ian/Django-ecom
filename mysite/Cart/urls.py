from django.urls import path
from . import views

app_name = 'Cart'
urlpatterns = [
     path('summary/', views.cart_summary, name='cart_summary'),
     path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('process_quantity/', views.process_quantity, name='process_quantity'),
] 