from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from .models import Product, Category, Condition, Profile, Sub_category, Brand, Like
from .filters import ProductFilter

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, SetPasswordForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, LoginForm, ReviewForm
from django import forms

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from Cart.cart import Cart

from django.db.models import Q

# Create your views here.

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')  # Safely get the search term from POST data

        if searched:
            # Query the database for matching products
            products = Product.objects.filter(
                Q(name__icontains=searched) | Q(description__icontains=searched)
            )

            if products.exists():
                return render(request, 'search.html', {
                    'searched': products,  # Pass the actual products to the template
                })
            else:
                messages.success(request, "No products found matching the search criteria.")
        else:
            messages.error(request, "Please enter a search term.")

        # Always redirect to home page after POST request processing
        return redirect('shop:home')

    # Handle GET requests or unexpected scenarios by redirecting to home
    return redirect('shop:home')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {
        'products':products,
    })


def account_info(request):
    return redirect("shop:update_info")

# def product(request,pk):
#     product = Product.objects.get(id = pk)
#     return render(request, 'product.html', {
#         'product':product,
#     })
def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    liked = False

    if request.user.is_authenticated:
        # Check if the user has already liked this product
        liked = Like.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST':
        # Handle like/unlike button click
        if liked:
            Like.objects.filter(user=request.user, product=product).delete()
        else:
            Like.objects.create(user=request.user, product=product)

        # Redirect back to the product page
        return redirect('product', pk=pk)

    return render(request, 'product.html', {
        'product': product,
        'liked': liked,
    })

def liked_page(request):
    user_likes = Like.objects.filter(user=request.user)
    liked_products = [like.product for like in user_likes]

    return render(request, 'liked_page.html', {'liked_products': liked_products})

def add_review(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.save()
            return redirect('home')  # Replace 'home' with your actual URL name
    else:
        form = CommentForm()

    return render(request, 'add_review.html', {'form': form})

from django.db.models import Max, Min

def category(request, cat):
    cat = cat.replace('-', ' ')
    try:
        category_obj = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category_obj)
        sub_categories = Sub_category.objects.filter(category=category_obj)
        brands = Brand.objects.filter(product__category=category_obj).distinct()

        # Handling brand and sub-category filtering
        selected_brands = request.POST.getlist('brands')
        selected_sub_categories = request.POST.getlist('sub_categories')

        if selected_brands:
            products = products.filter(brand__id__in=selected_brands)

        if selected_sub_categories:
            products = products.filter(sub_category__id__in=selected_sub_categories)

        # Get Max and Min Value of Queryset
        max_price = products.aggregate(Max('price'))['price__max']
        min_price = products.aggregate(Min('price'))['price__min']
        
        # Split the range into 4 (adjust as needed)
        range_step = (max_price - min_price) / 4

        return render(request, 'category.html', {
            'products': products,
            'category': category_obj,
            'sub_categories': sub_categories,
            'brands': brands,
            'selected_brands': [int(b) for b in selected_brands],
            'selected_sub_categories': [int(sc) for sc in selected_sub_categories],
            'min_price': min_price,
            'max_price': max_price,
            'range_step': range_step,
        })

    except Category.DoesNotExist:
        return redirect('shop:home')

# def sub_category(request,cat):
#     cat = cat.replace('-', ' ')
#     try:
#         category = Category.objects.get(name = cat)
#         products = Product.objects.filter(category = category,)
#         return render(request, 'sub_category.html', {
#             'products':products,
#             'category':category
#         })
#     except:
#         return redirect('home')

# def condition(request, cat):
#     cat = cat.replace('-', ' ')
#     try:
#         condition = Condition.objects.get(name = cat)
#         products = Product.objects.filter(condition = condition,)
#         return render(request, 'condition.html', {
#             'products':products,
#             'condition':condition
#         })
#     except:
#         return redirect('shop:home')

def condition(request, cat):
    cat = cat.replace('-', ' ')
    try:
        condition = Condition.objects.get(name = cat)
        products = Product.objects.filter(condition = condition,)
        brands = Brand.objects.filter(product__condition=condition).distinct()

        # Handling brand filtering
        selected_brands = request.POST.getlist('brands')

        if selected_brands:
            products = products.filter(brand__id__in=selected_brands)

        # Get Max and Min Value of Queryset
        max_price = products.aggregate(Max('price'))['price__max']
        min_price = products.aggregate(Min('price'))['price__min']
        
        # Split the range into 4 (adjust as needed)
        range_step = (max_price - min_price) / 4

        return render(request, 'condition.html', {
            'products': products,
            'condition': condition,
            'brands': brands,
            'selected_brands': [int(b) for b in selected_brands],
            'min_price': min_price,
            'max_price': max_price,
            'range_step': range_step,
        })

    except Condition.DoesNotExist:
        return redirect('shop:home')
        
from django.urls import reverse

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user: #is not None:
                login(request, user)
                # Redirect to the next URL after login, or to 'shop:home' if not set
                # next_url = request.GET.get('next', 'shop:home')
                messages.success(request, "You have been logged in.")
                # return redirect(next_url)
                return redirect('shop:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('login')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('shop:update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('shop:home')


# def update_info(request):
# 	if request.user.is_authenticated:
# 		# Get Current User
# 		current_user_profile = User.objects.get(id=request.user.id)
#         # current_user = Profile.objects.get(user_id=request.user.id)
#         # current_user = Profile.objects.get(user_id=request.user.id)
# 		# Get Current User's Shipping Info
# 		#shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
# 		# Get original User Form
# 		u_form = UserInfoForm(request.POST or None, instance=current_user_profile)
# 		# Get User's Shipping Form
# 		#shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
# 		if u_form.is_valid(): # or shipping_form.is_valid():
# 			# Save original form
# 			u_form.save()
# 			# Save shipping form
# 			#shipping_form.save()

# 			messages.success(request, "Your Info Has Been Updated!!")
# 			return redirect('shop:home')
# 		return render(request, "update_info.html", {'u_form':u_form,})
# 	else:
# 		messages.success(request, "You Must Be Logged In To Access That Page!!")
# 		return redirect('shop:home')

def update_info(request):
    # current_user = request.user
    current_user = Profile.objects.get(user__id=request.user.id)

    # Try to get the user's profile; create one if it doesn't exist
    # current_profile, created = Profile.objects.get_or_create(user=current_user)
    shipping_user, created = ShippingAddress.objects.get_or_create(user_id=request.user.id)

    if request.method == 'POST':
        u_form = UserInfoForm(request.POST, instance=current_user)
        s_form = ShippingForm(request.POST, instance = shipping_user)
        if u_form.is_valid() and s_form.is_valid():
            # saving info form
            u_form.save()
            # saving shipping form
            s_form.save()    
            messages.success(request, "Your info has been updated successfully.")
            return redirect('shop:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserInfoForm(instance=current_user)
        s_form = ShippingForm(instance=shipping_user)

    return render(request, 'update_info.html', {
        'u_form': u_form,
        's_form': s_form,
    })


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()
			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('shop:home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('shop:home')


def register_user(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})    
   
    if request.method == 'POST':
        form = SignUpForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have been registered successfully.')
            login(request, user)
            return redirect('shop:home')
        else:
            return render(request, 'register.html', {'form': form})

   
def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out.."))
    return redirect('shop:home')



