from django.urls import path
from . import views


app_name='shop'
urlpatterns = [
    path('',views.home, name = 'home'),
    path('product/<int:pk>', views.product, name = "product"),
    path('category/<str:cat>', views.category, name = "category"),
    path('offers/', views.offers, name = "offers"),
    path('condition/<str:cat>', views.condition, name = "condition"),
    # path('sub_category/<str:cat>', views.sub_category, name = "sub_category"),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_info/', views.update_info, name='update_info'),
    path('search/', views.search, name='search'),
    path('account_info/', views.account_info, name='account_info'),
    path('product/<int:pk>/add_review', views.add_review, name='add_review'),
    path('product/<int:pk>/remove_review', views.remove_review, name='remove_review'),
    path('favourites/', views.favourites, name='favourites'),
    path('process_email/', views.process_email, name='process_email'),
] 