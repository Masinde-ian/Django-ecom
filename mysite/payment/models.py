from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
import datetime

# Create your models here.
class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255, null=True, blank=True)
	shipping_phone_number = models.CharField(max_length=255, null=True, blank=True)
	shipping_address1 = models.CharField(max_length=255, null=True, blank=True)
	shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
	shipping_city = models.CharField(max_length=255, null=True, blank=True)
	shipping_county = models.CharField(max_length=255, null=True, blank=True)


	# Don't pluralize address
	class Meta:
		verbose_name_plural = "Shipping Address"

	def __str__(self):
		return f'Shipping Address - {str(self.id)}'

# Create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)


# Create Order Model
class Order(models.Model):
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250)
	phone = models.CharField(max_length=250)
	delivery_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
	date_ordered = models.DateTimeField(auto_now_add=True)	
	delivered = models.BooleanField(default=False)
	date_delivered = models.DateTimeField(blank=True, null=True)
	
	def __str__(self):
		return f'Order - {str(self.id)}'

# Auto Add shipping Date
@receiver(pre_save, sender=Order)
def set_delivered_date_on_update(sender, instance, **kwargs):
	if instance.pk:
		now = datetime.datetime.now()
		obj = sender._default_manager.get(pk=instance.pk)
		if instance.delivered and not obj.delivered:
			instance.date_delivered = now


# Create Order Items Model
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2)


	def __str__(self):
		return f'Order Item - {str(self.id)}'

	# def save(self, *args, **kwargs):
	# 	# Call the superclass's save method
	# 	super().save(*args, **kwargs)

	# 	# Reduce the product's stock quantity
	# 	self.product.in_stock -= self.quantity
	# 	self.product.save()
