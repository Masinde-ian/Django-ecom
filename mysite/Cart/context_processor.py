# context_processors.py

from .models import Cart

def cart(request):
    # Initialize or retrieve the cart for the current session
    cart = Cart(request)
    # Pass the total number of items in the cart to the template context
    return {'cart.total_quantity': cart.total_quantity()}
