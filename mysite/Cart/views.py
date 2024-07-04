from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from .cart import Cart
from .forms import QuantityForm
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Cart

def process_quantity(request):
    if request.method == 'POST':
        # product = get_object_or_404(Product, id=product_id)
        product_id = request.POST.get('product_id')
        quant = request.POST.get('quant', '')
        return redirect(request.META.get('HTTP_REFERER', '/'))

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        quant = request.POST.get('quant', '')
        try:
            if quant:
                quantity = int(quant)
            else:
                quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, 'Invalid quantity value. Please enter a valid number.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        maximum = product.in_stock
        if quantity > maximum:
            messages.error(request, f'Reduce the quantity. Only {maximum} items in stock.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # If the item already exists in the cart, update its quantity
        if not item_created:
            cart_item.quantity += quantity  # Increase quantity by the submitted quantity
        else:
            cart_item.quantity = quantity  # Set quantity to the submitted quantity

        cart_item.save()
        messages.success(request, f'{product.name} {"added to" if item_created else "updated in"} the cart.')
    else:
        messages.error(request, "Invalid form submission")

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page       
        


def cart_summary(request):
    # cart = Cart.objects.get(user=request.user)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart_summary.html', {'cart': cart})
    else:
        # Handle the case where the user is not logged in
        return redirect('shop:home')


def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    item = CartItem.objects.get(cart=cart, product_id=product_id)
    item.delete()
    return redirect('Cart:cart_summary')


# Create your views here.
# def cart_info(request):
#		return render (request, "cart_info.html", {})



# @login_required
# def item_clear(request, id):


# @login_required
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")



