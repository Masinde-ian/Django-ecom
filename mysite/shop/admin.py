from django.contrib import admin
from .models import Category,Customer,Product,Order,Condition,Profile,Sub_category
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Condition)
#admin.site.register(image)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)
