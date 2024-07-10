# context_processors.py

from .models import Cart

def cart(request):
    # Initialize or retrieve the cart for the current session
    cart = Cart(request)
    total_quantity = cart.total_quantity()
    # Pass the total number of items in the cart to the template context
    return {'total_quantity': total_quantity }
    # return 0
