# filters.py
import django_filters
from .models import Product
from django.db.models import ImageField

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gt')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lt')

    class Meta:
        model = Product
        fields = '__all__'
        filter_overrides = {
            ImageField: {
                'filter_class': django_filters.CharFilter,  # Example: using CharFilter for ImageField
                'extra': lambda f: {
                    'lookup_expr': 'icontains',  # Example: using 'icontains' lookup for CharFilter
                },
            },
        }
