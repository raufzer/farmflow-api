import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(lookup_expr='icontains')
    rating = django_filters.NumberFilter()
    price = django_filters.NumberFilter()
    status = django_filters.BooleanFilter()
    stock = django_filters.NumberFilter()
    keyword = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price' or 0 , lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price' or 100000000, lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('category', 'rating', 'price', 'status', 'stock','keyword','min_price','max_price')
