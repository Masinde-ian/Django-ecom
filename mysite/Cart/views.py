from django.shortcuts import render, get_object_or_404, redirect
# from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CartItem, Cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the item already exists in the cart, increase its quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('Cart:cart_summary')  # Redirect to cart summary page

def cart_summary(request):
    # cart = Cart.objects.get(user=request.user)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart_summary.html', {'cart': cart})
    else:
        # Handle the case where the user is not logged in
        return render(request, 'shop:login_user')


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


# @login_required
# def cart_detail(request):
#     return render(request, 'cart_info.html')



# def cart_add(request):
#     # Get the cart
#     cart = Cart(request)
    
#     # Test for POST
#     if request.POST.get('action') == 'post':
#         # Get stuff
#         product_id = int(request.POST.get('product_id'))
#         # product_qty = int(request.POST.get('product_qty'))

#         # Lookup product in DB
#         product = get_object_or_404(Product, id=product_id)
        
#         # Save to session
#         # cart.add(product=product, quantity=product_qty)

#         # Get Cart Quantity
#         cart_quantity = cart.Cart_len()

#         # Return response
#         # response = JsonResponse({'Product Name: ': product.name})
#         response = JsonResponse({'qty': cart_quantity})
#         messages.success(request, ("Product Added To Cart..."))
#         return response
#         #return redirect("shop:home")
#     # else:
#     #     return redirect("shop:home")



# def cart_add(request):
#     # Get the cart
# 	cart = Cart(request)
# 	# test for POST
# 	if request.POST.get('action') == 'post':
# 		# Get stuff
# 		product_id = int(request.POST.get('product.id'))
# 		#product_qty = int(request.POST.get('product_qty'))

# 		# lookup product in DB
# 		product = get_object_or_404(Product, id=product_id)
		
# 		# Save to session
# 		#cart.add(product=product, quantity=product_qty)

# 		# Get Cart Quantity
# 		cart_quantity = cart.__len__()

# 		# Return resonse
# 		#response = JsonResponse({'Product Name: ': product.name})
# 		#response = JsonResponse({'qty': cart_quantity})
# 		messages.success(request, ("Product Added To Cart..."))
# 		#return response
#         return redirect("shop:home")
#         #return HttpResponse("Cart item added successfully")
