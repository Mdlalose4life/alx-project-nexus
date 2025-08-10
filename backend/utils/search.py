from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q

class SearchManager:
    """
    Centralized search functionality
    """
    
    @staticmethod
    def search_businesses(query, queryset=None):
        """
        Full-text search for businesses
        """
        if queryset is None:
            from apps.businesses.models import Business
            queryset = Business.objects.filter(is_active=True)
        
        if not query:
            return queryset
        
        # PostgreSQL full-text search
        search_vector = SearchVector('name', weight='A') + \
                       SearchVector('description', weight='B') + \
                       SearchVector('address', weight='C')
        
        search_query = SearchQuery(query)
        
        return queryset.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

    @staticmethod
    def search_products(query, queryset=None):
        """
        Full-text search for products
        """
        if queryset is None:
            from apps.products.models import Product
            queryset = Product.objects.filter(status='active').select_related('business')
        
        if not query:
            return queryset
        
        search_vector = SearchVector('name', weight='A') + \
                    SearchVector('description', weight='B') + \
                    SearchVector('business__name', weight='C')
        
        search_query = SearchQuery(query)
        
        return queryset.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')