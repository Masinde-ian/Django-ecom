from django.shortcuts import render, redirect

from .models import Order,OrderItem

from Cart.cart import Cart
from Cart.models import CartItem, Cart
from shop.models import Profile

from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

from django.contrib import messages

import datetime

# Create your views here.


def view_order(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST.get('delivery_status')
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(deliverd=True, date_delivered=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(delivered=False)
			messages.success(request, "Delivery Status Updated")
			return redirect(request.META.get('HTTP_REFERER', '/'))
		return render(request, 'admin/orders.html', {"order":order, "items":items})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def undelivered_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(delivered = False)
		if request.POST:
			status = request.POST.get('delivery_status')
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(delivered = True, date_delivered = now)
			# redirect
			messages.success(request, "Delivery Status Updated")
			return redirect(request.META.get('HTTP_REFERER', '/'))

		return render(request, "admin/undelivered.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('shop:home')


def delivered_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(delivered = True)
		if request.POST:
			status = request.POST.get('delivery_status')
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(delivered = False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect(request.META.get('HTTP_REFERER', '/'))
		return render(request, "admin/delivered.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('shop:home')

def checkout(request):
    # Get the cart for the current user or create a new one
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Create a session with Shipping Info
        my_shipping = request.POST.dict()  # Convert POST QueryDict to a regular dictionary
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            # Checkout as logged-in user
            shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
            s_form = ShippingForm(request.POST, instance=shipping_user)
        else:
            # Checkout as guest
            s_form = ShippingForm(request.POST)
        
        if s_form.is_valid():
            return redirect('payment:process_order')
        else:
            messages.error(request, "Please correct the errors in the form.")

    else:
        if request.user.is_authenticated:
            shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
            s_form = ShippingForm(instance=shipping_user)
        else:
            s_form = ShippingForm()

    return render(request, "payment/checkout.html", {'cart': cart, 's_form': s_form})



def process_order(request):
    # if request.method == 'POST':
    if request.user.is_authenticated:
        # Get the cart for the current user or create a new one
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Check if 'my_shipping' exists in the session
        if not my_shipping:
            messages.error(request, "Shipping details are missing.")
            return redirect('payment:checkout')

        # Gather Order Info from session data
        full_name = my_shipping.get('shipping_full_name')
        phone = my_shipping.get('shipping_phone_number')

        # Check if necessary data is present
        if not full_name or not phone:
            messages.error(request, "Missing full name or phone number.")
            return redirect('payment:checkout')

        # Format the delivery address
        delivery_address = (
            f"{my_shipping.get('shipping_address1', '')}\n"
            f"{my_shipping.get('shipping_address2', '')}\n"
            f"{my_shipping.get('shipping_city', '')}\n"
            f"{my_shipping.get('shipping_county', '')}"
        )

        # Calculate total amount paid
        amount_paid = cart.total_price_sum()  # Assuming cart.total_price_sum() calculates the total amount

        # Create an Order
        try:
            create_order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                phone=phone,
                delivery_address=delivery_address,
                amount_paid=amount_paid
            )

            # Add order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=create_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price  # Assuming price is stored in each cart item's related product
                )

            # Clear session data
            request.session.pop('my_shipping', None)

            # Clear the cart
            cart.items.all().delete()

            # Update user's profile or related model (if necessary)
            if request.user.is_authenticated:
                Profile.objects.filter(user=request.user).update(old_cart="")

            messages.success(request, "Order Placed Successfully!")
            return redirect('shop:home')

        except IntegrityError:
            messages.error(request, "An error occurred while processing your order. Please try again.")
            return redirect('Cart:cart_summary')

    else:
         # Get the cart for the current user or create a new one
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Check if 'my_shipping' exists in the session
        if not my_shipping:
            messages.error(request, "Shipping details are missing.")
            return redirect('payment:checkout')

        # Gather Order Info from session data
        full_name = my_shipping.get('shipping_full_name')
        phone = my_shipping.get('shipping_phone_number')

        # Check if necessary data is present
        if not full_name or not phone:
            messages.error(request, "Missing full name or phone number.")
            return redirect('payment:checkout')

        # Format the delivery address
        delivery_address = (
            f"{my_shipping.get('shipping_address1', '')}\n"
            f"{my_shipping.get('shipping_address2', '')}\n"
            f"{my_shipping.get('shipping_city', '')}\n"
            f"{my_shipping.get('shipping_county', '')}"
        )

        # Calculate total amount paid
        amount_paid = cart.total_price_sum()  # Assuming cart.total_price_sum() calculates the total amount

        # Create an Order
        try:
            create_order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                phone=phone,
                delivery_address=delivery_address,
                amount_paid=amount_paid
            )

            # Add order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=create_order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price  # Assuming price is stored in each cart item's related product
                )

            # Clear session data
            request.session.pop('my_shipping', None)

            # Clear the cart
            cart.items.all().delete()

            # Update user's profile or related model (if necessary)
            if request.user.is_authenticated:
                Profile.objects.filter(user=request.user).update(old_cart="")

            messages.success(request, "Order Placed Successfully!")
            return redirect('shop:home')

        except IntegrityError:
            messages.error(request, "An error occurred while processing your order. Please try again.")
            return redirect('Cart:cart_summary')


def payment_success(request):
	return render(request, "payment/payment_success.html", {})
