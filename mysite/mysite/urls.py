"""
URL configuration for ryche_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from shop import views as auth_views


app_name='mysite'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('payment/',include('payment.urls')),
    path('cart/',include('Cart.urls')),
    path('login/', auth_views.login_user, name='login'),
    path('logout/', auth_views.logout_user, name='logout'),
    path('register/', auth_views.register_user, name='register'),   
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) 