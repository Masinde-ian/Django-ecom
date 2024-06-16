class Cart:
    def __init__(self, request):
        # Retrieve the cart from the session or initialize it if it doesn't exist
        self.cart = request.session.get('cart', {})
        self.request = request

    def add_item(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        # Save the cart back to the session
        self.save()

    def save(self):
        self.request.session['cart'] = self.cart
        self.request.session.modified = True

    def total_items(self):
        return sum(self.cart.values())


    # def __init__(self, request):
    #     self.session = request.session

    #     # Get the current session cart or create a new one if it doesn't exist
    #     self.cart = self.session.get('cart', {})
    #     # If user is new or cart doesn't exist in the session
    #     if 'cart' not in self.session:
    #         self.session['cart'] = self.cart
    #         self.session.modified = True

    # def add(self, product, quantity):
    #     product_id = str(product.id)

    #     if product_id in self.cart:
    #         # Update quantity if product is already in the cart
    #         self.cart[product_id]['quantity'] += quantity
    #     else:
    #         # Initialize product entry in the cart
    #         self.cart[product_id] = {'quantity': quantity}

    #     # Save the cart back to the session
    #     self.session.modified = True

    # def Cart_len(self):
    #     # Calculate and return the total number of unique products in the cart
    #     return len(self.cart)
