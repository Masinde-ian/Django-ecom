from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('payment_success/', views.payment_success, name = 'payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_processing/', views.process_order, name='process_order'),
    path('undelivered_dash', views.undelivered_dash, name='undelivered_dash'),
    path('delivered_dash/', views.delivered_dash, name='delivered_dash'),
    path('orders/<int:pk>', views.view_order, name='view_order'),
    path('access_token/', views.access_token, name='access_token'),
    path('stk-push/', views.stk_push, name='stk_push')
]