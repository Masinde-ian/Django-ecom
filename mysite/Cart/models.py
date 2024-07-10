from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models import Sum

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other cart-related fields

    def total_quantity(self):
        # Calculate the total quantity of items in the cart
        total_quantity = CartItem.objects.aggregate(total=Sum('quantity'))['total']
        return total_quantity if total_quantity is not None else 0

    def total_price_sum(self):
        # Calculate the total price of items in the cart
        total_price = self.items.aggregate(total=Sum(models.F('quantity') * models.F('product__price')))['total']
        return total_price if total_price is not None else 0

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null = True, blank=True)
    # Other item-related fields

     # Define a method to calculate the total price for this item
    def total_price(self):
        return self.quantity * self.product.price

     # Define a method to calculate the total quantity
    def price_sum(self):
        # Calculate the total price of quantity of this items in the cart
        price = self.cart.items.aggregate(total=models.Sum('product.price'))['total']
        return price 