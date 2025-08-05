from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.products.models import Product, ProductCategory
from api.v1.serializers.products import (
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateSerializer, ProductCategorySerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="List all product categories",
        description="Retrieve a hierarchical list of all active product categories",
        tags=["Product Categories"]
    ),
    retrieve=extend_schema(
        summary="Get product category details",
        description="Retrieve detailed information about a specific product category",
        tags=["Product Categories"]
    ),
)
class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for product categories.
    
    Provides read-only access to product categories with hierarchical structure.
    """
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

@extend_schema_view(
    list=extend_schema(
        summary="List products",
        description="Retrieve a paginated list of products with advanced filtering and search",
        tags=["Products"],
        parameters=[
            OpenApiParameter(
                name='business',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by business ID'
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by category ID'
            ),
            OpenApiParameter(
                name='min_price',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                description='Minimum price filter'
            ),
            OpenApiParameter(
                name='max_price',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                description='Maximum price filter'
            ),
            OpenApiParameter(
                name='is_featured',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter featured products'
            ),
            OpenApiParameter(
                name='in_stock',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter products in stock'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in product name and description'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order results by field',
                enum=['name', '-name', 'price', '-price', 'created_at', '-created_at']
            ),
        ]
    ),
    retrieve=extend_schema(
        summary="Get product details",
        description="Retrieve detailed information about a specific product",
        tags=["Products"]
    ),
    create=extend_schema(
        summary="Create a new product",
        description="Add a new product to your business (authenticated users only)",
        tags=["Products"]
    ),
    update=extend_schema(
        summary="Update product",
        description="Update product information (product owner only)",
        tags=["Products"]
    ),
    partial_update=extend_schema(
        summary="Partially update product",
        description="Partially update product information (product owner only)",
        tags=["Products"]
    ),
    destroy=extend_schema(
        summary="Delete product",
        description="Delete product listing (product owner only)",
        tags=["Products"]
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    
    Provides CRUD operations for products with advanced filtering and search.
    """
    queryset = Product.objects.filter(status='active')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business', 'category', 'is_featured', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-is_featured', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        return ProductDetailSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'search', 'by_category']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            # Update, delete only for product owners
            return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle business-specific product listing
        business_id = self.kwargs.get('business_id')
        if business_id:
            queryset = queryset.filter(business_id=business_id)
        
        # Filter by owner for non-public actions
        if self.action not in ['list', 'retrieve', 'featured', 'search', 'by_category']:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(business__owner=self.request.user)
        
        # Add custom filters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        in_stock = self.request.query_params.get('in_stock')
        
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass
        
        if in_stock is not None:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_quantity__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_quantity=0)
        
        return queryset.select_related('business', 'category').prefetch_related('images')
    
    @extend_schema(
        summary="Get featured products",
        description="Retrieve all featured products across all businesses",
        tags=["Products"]
    )
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
    
    @extend_schema(
        summary="Search products",
        description="Advanced product search with multiple criteria",
        tags=["Products"],
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Search query'
            ),
            OpenApiParameter(
                name='business_name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by business name'
            ),
            OpenApiParameter(
                name='category_name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by category name'
            ),
        ],
        examples=[
            OpenApiExample(
                'Basic Search',
                summary='Search for bread products',
                description='Simple product search',
                value={'q': 'bread'}
            ),
            OpenApiExample(
                'Advanced Search',
                summary='Search with filters',
                description='Search with business and category filters',
                value={'q': 'shoes', 'business_name': 'Fashion Store', 'category_name': 'clothing'}
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced product search"""
        query = request.query_params.get('q', '').strip()
        business_name = request.query_params.get('business_name', '').strip()
        category_name = request.query_params.get('category_name', '').strip()
        
        if not query:
            return Response(
                {'error': 'Search query (q) is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset()
        
        # Search in product name and description
        search_filter = Q(name__icontains=query) | Q(description__icontains=query)
        queryset = queryset.filter(search_filter)
        
        # Additional filters
        if business_name:
            queryset = queryset.filter(business__name__icontains=business_name)
        
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        
        # Order by relevance (products with query in name first)
        queryset = queryset.extra(
            select={
                'name_match': "CASE WHEN LOWER(name) LIKE LOWER(%s) THEN 1 ELSE 0 END"
            },
            select_params=[f'%{query}%']
        ).order_by('-name_match', '-is_featured', '-created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get products by category",
        description="Retrieve products filtered by category slug",
        tags=["Products"],
        parameters=[
            OpenApiParameter(
                name='category_slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description='Category slug'
            ),
        ]
    )
    @action(detail=False, methods=['get'], url_path='category/(?P<category_slug>[^/.]+)')
    def by_category(self, request, category_slug=None):
        """Get products by category slug"""
        try:
            category = ProductCategory.objects.get(slug=category_slug, is_active=True)
        except ProductCategory.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Include products from child categories if this is a parent category
        categories = [category]
        if hasattr(category, 'children'):
            categories.extend(category.children.filter(is_active=True))
        
        queryset = self.get_queryset().filter(category__in=categories)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
            response_data['category'] = ProductCategorySerializer(category).data
            return Response(response_data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'category': ProductCategorySerializer(category).data,
            'products': serializer.data
        })
    
    @extend_schema(
        summary="Toggle product featured status",
        description="Toggle the featured status of a product (business owner only)",
        tags=["Products"],
        request=None,
        responses={
            200: OpenApiExample(
                'Success',
                value={'message': 'Product featured successfully', 'is_featured': True}
            ),
            403: OpenApiExample(
                'Permission denied',
                value={'error': 'Permission denied'}
            )
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_featured(self, request, slug=None):
        """Toggle featured status (business owner only)"""
        product = self.get_object()
        
        # Check if user is the business owner
        if product.business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        product.is_featured = not product.is_featured
        product.save()
        
        return Response({
            'message': f"Product {'featured' if product.is_featured else 'unfeatured'} successfully",
            'is_featured': product.is_featured
        })
    
    @extend_schema(
        summary="Update product stock",
        description="Update product stock quantity (business owner only)",
        tags=["Products"],
        request={
            'type': 'object',
            'properties': {
                'quantity': {'type': 'integer', 'minimum': 0},
                'action': {'type': 'string', 'enum': ['set', 'add', 'subtract']},
            },
            'required': ['quantity']
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'new_quantity': {'type': 'integer'},
                    'is_in_stock': {'type': 'boolean'},
                    'is_low_stock': {'type': 'boolean'},
                }
            }
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_stock(self, request, slug=None):
        """Update product stock (business owner only)"""
        product = self.get_object()
        
        # Check if user is the business owner
        if product.business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        quantity = request.data.get('quantity')
        action = request.data.get('action', 'set')
        
        if quantity is None:
            return Response(
                {'error': 'Quantity is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid quantity value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update stock based on action
        if action == 'set':
            product.stock_quantity = quantity
        elif action == 'add':
            product.stock_quantity += quantity
        elif action == 'subtract':
            product.stock_quantity = max(0, product.stock_quantity - quantity)
        else:
            return Response(
                {'error': 'Invalid action. Use: set, add, or subtract'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.save()
        
        return Response({
            'message': 'Stock updated successfully',
            'new_quantity': product.stock_quantity,
            'is_in_stock': product.is_in_stock,
            'is_low_stock': product.is_low_stock,
        })
    
    @extend_schema(
        summary="Get product analytics",
        description="Get analytics data for a product (business owner only)",
        tags=["Products"],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'views_total': {'type': 'integer'},
                    'views_this_month': {'type': 'integer'},
                    'views_this_week': {'type': 'integer'},
                    'stock_history': {'type': 'array'},
                    'price_history': {'type': 'array'},
                }
            }
        }
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def analytics(self, request, slug=None):
        """Get product analytics (business owner only)"""
        product = self.get_object()
        
        # Check if user is the business owner
        if product.business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Basic analytics data (implement tracking as needed)
        analytics_data = {
            'views_total': 0,  # Implement view tracking
            'views_this_month': 0,
            'views_this_week': 0,
            'stock_history': [],  # Implement stock change tracking
            'price_history': [],  # Implement price change tracking
            'current_stock': product.stock_quantity,
            'is_low_stock': product.is_low_stock,
            'created_at': product.created_at,
            'last_updated': product.updated_at,
        }
        
        return Response(analytics_data)