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


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length = 100)
    price =  models.DecimalField(default = 0, decimal_places = 2, max_digits = 8)
    discount = models.DecimalField(default = 0, decimal_places = 2, max_digits = 6)
    sub_category = models.ForeignKey(Sub_category, on_delete = models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, null=True,)
    condition = models.ForeignKey(Condition, on_delete = models.CASCADE, default=1, blank=True)
    description = models.CharField(max_length = 500, default = '', blank = True, null = True)
    image = models.ImageField(upload_to = 'product/')
    image2 = models.ImageField(upload_to = 'product/', blank=True, null=True)
    new_price = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=8)
    precaution = models.CharField(max_length = 400, default = '', blank = True, null = True)
    use = models.CharField(max_length = 500, default = '', blank = True, null = True)
    in_stock = models.IntegerField(default=1)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, default=1,  blank = True, null = True)

    def __str__ (self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate the new price based on the discount
        self.new_price = self.price - self.discount

        # Retrieve the category associated with the sub_category
        # if self.sub_category:
        self.category = self.sub_category.category

        # Call the superclass's save method
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.product}"


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

class Review(models.Model):
	product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.post.title, self.name)


class Email(models.Model):
    email = models.EmailField(max_length=70, unique=True)

    def __str__(self):
        return self.email


