from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.businesses.models import Business, BusinessCategory
from api.v1.serializers.businesses import (
    BusinessListSerializer, BusinessDetailSerializer, 
    BusinessCreateSerializer, BusinessCategorySerializer,
    BusinessWithProductsSerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="List all business categories",
        description="Retrieve a list of all active business categories",
        tags=["Business Categories"]
    ),
    retrieve=extend_schema(
        summary="Get business category details",
        description="Retrieve detailed information about a specific business category",
        tags=["Business Categories"]
    ),
)
class BusinessCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for business categories.
    
    Provides read-only access to business categories.
    """
    queryset = BusinessCategory.objects.filter(is_active=True)
    serializer_class = BusinessCategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

@extend_schema_view(
    list=extend_schema(
        summary="List businesses",
        description="Retrieve a paginated list of businesses with filtering and search capabilities",
        tags=["Businesses"],
        parameters=[
            OpenApiParameter(
                name='business_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by business type',
                enum=['spaza_shop', 'restaurant', 'electronics', 'fashion', 'services', 'grocery', 'other']
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by category ID'
            ),
            OpenApiParameter(
                name='city',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by city'
            ),
            OpenApiParameter(
                name='is_featured',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter featured businesses'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in business name, description, and address'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order results by field',
                enum=['name', '-name', 'created_at', '-created_at', 'average_rating', '-average_rating']
            ),
        ]
    ),
    retrieve=extend_schema(
        summary="Get business details",
        description="Retrieve detailed information about a specific business including location data",
        tags=["Businesses"]
    ),
    create=extend_schema(
        summary="Create a new business",
        description="Register a new business listing",
        tags=["Businesses"]
    ),
    update=extend_schema(
        summary="Update business",
        description="Update business information (owners only)",
        tags=["Businesses"]
    ),
    partial_update=extend_schema(
        summary="Partially update business",
        description="Partially update business information (owners only)",
        tags=["Businesses"]
    ),
    destroy=extend_schema(
        summary="Delete business",
        description="Delete business listing (owners only)",
        tags=["Businesses"]
    ),
)
class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing businesses.
    
    Provides CRUD operations for businesses with location-based features.
    """
    queryset = Business.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_type', 'category', 'city', 'province', 'is_featured']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'created_at', 'average_rating']
    ordering = ['-is_featured', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BusinessListSerializer
        elif self.action == 'create':
            return BusinessCreateSerializer
        elif self.action == 'with_products':
            return BusinessWithProductsSerializer
        return BusinessDetailSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'nearby', 'featured', 'with_products']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            # Update, delete only for business owners
            return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by owner for non-public actions
        if self.action not in ['list', 'retrieve', 'nearby', 'featured', 'with_products']:
            if self.request.user.is_authenticated:
                queryset = queryset.filter(owner=self.request.user)
        
        return queryset.select_related('category', 'owner').prefetch_related('images')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        # Add user location for distance calculations
        if self.request.user.is_authenticated and hasattr(self.request.user, 'location') and self.request.user.location:
            context['user_location'] = self.request.user.location
        
        return context
    
    @extend_schema(
        summary="Get nearby businesses",
        description="Find businesses near a specific location",
        tags=["Businesses"],
        parameters=[
            OpenApiParameter(
                name='lat',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Latitude coordinate'
            ),
            OpenApiParameter(
                name='lon',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Longitude coordinate'
            ),
            OpenApiParameter(
                name='radius',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Search radius in kilometers (default: 10)',
                default=10
            ),
        ],
        examples=[
            OpenApiExample(
                'Cape Town Center',
                summary='Find businesses near Cape Town CBD',
                description='Example coordinates for Cape Town city center',
                value={'lat': -33.9249, 'lon': 18.4241, 'radius': 5}
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get businesses near user location"""
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        radius = request.query_params.get('radius', 10)  # Default 10km
        
        if not lat or not lon:
            return Response(
                {'error': 'Latitude and longitude are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_location = Point(float(lon), float(lat))
            nearby_businesses = self.get_queryset().filter(
                location__distance_lte=(user_location, Distance(km=int(radius)))
            ).distance(user_location).order_by('distance')
            
            # Add user location to context for distance calculation
            context = self.get_serializer_context()
            context['user_location'] = user_location
            
            page = self.paginate_queryset(nearby_businesses)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(nearby_businesses, many=True, context=context)
            return Response(serializer.data)
            
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid coordinates'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Get featured businesses",
        description="Retrieve all featured businesses",
        tags=["Businesses"]
    )
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured businesses"""
        featured_businesses = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(featured_businesses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(featured_businesses, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Get businesses with featured products",
        description="Retrieve businesses along with their featured products (limited to 10 businesses for performance)",
        tags=["Businesses"]
    )
    @action(detail=False, methods=['get'])
    def with_products(self, request):
        """Get businesses with their featured products"""
        businesses = self.get_queryset()[:10]  # Limit for performance
        serializer = self.get_serializer(businesses, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Toggle featured status",
        description="Toggle the featured status of a business (admin only)",
        tags=["Businesses"],
        request=None,
        responses={
            200: OpenApiExample(
                'Success',
                value={'message': 'Business featured successfully', 'is_featured': True}
            ),
            403: OpenApiExample(
                'Permission denied',
                value={'error': 'Permission denied'}
            )
        }
    )
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, slug=None):
        """Toggle featured status (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        business = self.get_object()
        business.is_featured = not business.is_featured
        business.save()
        
        return Response({
            'message': f"Business {'featured' if business.is_featured else 'unfeatured'} successfully",
            'is_featured': business.is_featured
        })
    
    @extend_schema(
        summary="Get business statistics",
        description="Get detailed statistics for a business (owner only)",
        tags=["Businesses"],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total_products': {'type': 'integer'},
                    'active_products': {'type': 'integer'},
                    'total_reviews': {'type': 'integer'},
                    'average_rating': {'type': 'number'},
                    'views_this_month': {'type': 'integer'},
                }
            }
        }
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def stats(self, request, slug=None):
        """Get business statistics (owner only)"""
        business = self.get_object()
        
        # Check if user is the owner
        if business.owner != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        stats = {
            'total_products': business.products.count(),
            'active_products': business.products.filter(status='active').count(),
            'total_reviews': getattr(business, 'reviews', None) and business.reviews.count() or 0,
            'average_rating': 0,  # Calculate from reviews if available
            'views_this_month': 0,  # Implement view tracking if needed
        }
        
        # Calculate average rating if reviews exist
        if hasattr(business, 'reviews') and business.reviews.exists():
            from django.db.models import Avg
            avg_rating = business.reviews.aggregate(avg=Avg('rating'))['avg']
            stats['average_rating'] = round(avg_rating, 1) if avg_rating else 0
        
        return Response(stats)