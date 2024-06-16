# context_processors.py

from .cart import Cart

def cart(request):
    # Initialize or retrieve the cart for the current session
    cart = Cart(request)
    # Pass the total number of items in the cart to the template context
    return {'cart_total_items': cart.total_items()}
