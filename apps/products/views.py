from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models import Product, ProductCategory
from apps.businesses.models import Business
from api.v1.serializers.products import (
    ProductListSerializer, ProductDetailSerializer, 
    ProductCreateSerializer, ProductCategorySerializer
)

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status='active')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'business', 'is_featured', 'business__city']
    search_fields = ['name', 'description', 'business__name']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-is_featured', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return ProductDetailSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'by_business']:
            return [permissions.AllowAny()]
        else:
            # Create, update, delete only for business owners
            return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by business owner for management actions
        if self.action not in ['list', 'retrieve', 'featured', 'by_business']:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(business__owner=self.request.user)
        
        return queryset.select_related('business', 'category').prefetch_related('images')
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        featured_products = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(featured_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_business(self, request):
        """Get products by business slug"""
        business_slug = request.query_params.get('business_slug')
        
        if not business_slug:
            return Response(
                {'error': 'business_slug parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            business = Business.objects.get(slug=business_slug, is_active=True)
            products = self.get_queryset().filter(business=business)
            
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
            
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock (business owners only)"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        low_stock_products = Product.objects.filter(
            business__owner=request.user,
            track_inventory=True,
            stock_quantity__lte=models.F('low_stock_threshold')
        )
        
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update product stock quantity"""
        product = self.get_object()
        new_quantity = request.data.get('quantity')
        
        if new_quantity is None:
            return Response(
                {'error': 'Quantity is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                raise ValueError()
        except ValueError:
            return Response(
                {'error': 'Quantity must be a non-negative integer'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock_quantity = new_quantity
        product.save()
        
        return Response({
            'message': 'Stock updated successfully',
            'new_quantity': new_quantity,
            'is_low_stock': product.is_low_stock
        })


# Base pagination for consistent responses
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100