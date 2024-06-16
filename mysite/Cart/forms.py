from django import forms
from .models import CartItem
from  .shop import Product

product_quantity=Product.models(in_stock)
class cartAdd(froms.ModelField):
    quantity=forms.TypedChoiceField(choices=product_quantity, coerce=int)