from django.urls import path
from . import views

app_name = 'Cart'
urlpatterns = [
     # path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/add/', views.cart_add, name='cart_add'),
#     path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('summary/', views.cart_summary, name='cart_summary'),
     path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
#      path('cart/item_increment/<int:id>/',
#           views.item_increment, name='item_increment'),
#      path('cart/item_decrement/<int:id>/',
#           views.item_decrement, name='item_decrement'),
#      path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
#      path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
] 