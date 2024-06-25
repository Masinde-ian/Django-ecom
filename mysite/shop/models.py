from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	County = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username

# Create a user Profile by default when user signs up
# def create_profile(sender, instance, created, **kwargs):
# 	if created:
# 		user_profile = Profile(user=instance)
# 		user_profile.save()
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Automate the profile thing
post_save.connect(create_profile, sender=User)



class Category(models.Model):
    name = models.CharField(max_length = 60)

    def __str__ (self):
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length = 60)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default=1)

    def __str__ (self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length = 60)

    def __str__ (self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 60)

    def __str__ (self):
        return f'{self.first_name} {self.last_name}'
                  

class Product(models.Model):
    name = models.CharField(max_length = 100)
    price =  models.DecimalField(default = 0, decimal_places = 2, max_digits = 8)
    discount = models.DecimalField(default = 0, decimal_places = 2, max_digits = 6)
    sub_category = models.ForeignKey(Sub_category, on_delete = models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default=1)
    condition = models.ForeignKey(Condition, on_delete = models.CASCADE, default=1)
    description = models.CharField(max_length = 500, default = '', blank = True, null = True)
    image = models.ImageField(upload_to = 'media/product/')
    image2 = models.ImageField(upload_to = 'media/product/', blank=True, null=True)
    new_price = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=8)
    precaution = models.CharField(max_length = 400, default = '', blank = True, null = True)
    use = models.CharField(max_length = 500, default = '', blank = True, null = True)
    in_stock = models.IntegerField(default=1)
    brand = models.CharField(max_length = 80, default = '', blank = True, null = True) 

    def __str__ (self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate the new price based on the discount
        self.new_price = self.price - self.discount

        # Retrieve the category associated with the sub_category
        if self.sub_category:
            self.category = self.sub_category.category

        # Call the superclass's save method
        super().save(*args, **kwargs)

        

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length = 100, default ='', blank=True)
    phone = models.CharField(max_length = 10) 
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default = False)

    def __str__ (self):
        return self.product

'''class image(models.Model):
    name = models.CharField(max_length = 50, null=False, default=1) 
    logo = models.ImageField(upload_to = 'media/design/', null=True)
    offer1 = models.ImageField(upload_to = 'media/design/', null=True)
    offer2 = models.ImageField(upload_to = 'media/design/', null=True)
    offer3 = models.ImageField(upload_to = 'media/design/', null=True)
    post1 = models.ImageField(upload_to = 'media/design/', null=True)
    post2 = models.ImageField(upload_to = 'media/design/', null=True)
    post3 = models.ImageField(upload_to = 'media/design/', null=True)
    pay1 = models.ImageField(upload_to = 'media/design/', null=True)
    pay2 = models.ImageField(upload_to = 'media/design/', null=True)
    pay3 = models.ImageField(upload_to = 'media/design/', null=True)

    def __str__ (self):
        return self.name'''


