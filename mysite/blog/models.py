from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		#return reverse('article-detail', args=(str(self.id)) )
		return reverse('blog:blog_home')


class Post(models.Model):
	title = models.CharField(max_length=255)
	header_image = models.ImageField(null=True, blank=True, upload_to="blog_images/")
	title_tag = models.CharField(max_length=255)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	body = CKEditor5Field(blank=True, null=True, config_name='extends')
	#body = models.TextField()
	post_date = models.DateField(auto_now_add=True)
	# category = models.CharField(max_length=255,)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	snippet = models.CharField(max_length=255)
	likes = models.ManyToManyField(User, related_name='blog_posts')

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		#return reverse('article-detail', args=(str(self.id)) )
		return reverse('blog:blog_home')


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.post.title, self.name)