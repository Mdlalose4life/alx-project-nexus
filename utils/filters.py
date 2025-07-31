import django_filters
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.db import models
from apps.businesses.models import Business
from apps.products.models import Product

class BusinessFilter(django_filters.FilterSet):
    """Custom filters for businesses"""
    min_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    max_distance = django_filters.NumberFilter(method='filter_by_distance')
    lat = django_filters.NumberFilter(method='filter_by_location')
    lon = django_filters.NumberFilter(method='filter_by_location')
    
    class Meta:
        model = Business
        fields = ['business_type', 'category', 'city', 'province', 'is_featured']
    
    def filter_by_distance(self, queryset, name, value):
        """Filter businesses within specified distance"""
        lat = self.request.GET.get('lat')
        lon = self.request.GET.get('lon')
        
        if lat and lon and value:
            try:
                user_location = Point(float(lon), float(lat))
                return queryset.filter(
                    location__distance_lte=(user_location, Distance(km=value))
                )
            except (ValueError, TypeError):
                pass
        
        return queryset
    
    def filter_by_location(self, queryset, name, value):
        """Helper method for location-based filtering"""
        # This method is called for both lat and lon parameters
        # The actual filtering is done in filter_by_distance
        return queryset

class ProductFilter(django_filters.FilterSet):
    """Custom filters for products"""
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    on_sale = django_filters.BooleanFilter(method='filter_on_sale')
    
    class Meta:
        model = Product
        fields = ['category', 'business', 'is_featured', 'status']
    
    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock"""
        if value:
            return queryset.filter(
                models.Q(track_inventory=False) | 
                models.Q(track_inventory=True, stock_quantity__gt=0)
            )
        return queryset
    
    def filter_on_sale(self, queryset, name, value):
        """Filter products that are on sale (have original_price > price)"""
        if value:
            return queryset.filter(
                original_price__isnull=False,
                original_price__gt=models.F('price')
            )
        return queryset
