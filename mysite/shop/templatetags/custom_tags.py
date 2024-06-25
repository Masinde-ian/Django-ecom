# custom_tags.py
from django import template
from shop.models import Category, Condition

register = template.Library()

@register.simple_tag
def get_categorys():
    return Category.objects.all()

@register.simple_tag
def get_conditions():
    return Condition.objects.all()
