from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from apps.businesses.models import Business, BusinessCategory
from api.v1.serializers.businesses import (
    BusinessListSerializer, BusinessDetailSerializer, 
    BusinessCreateSerializer, BusinessCategorySerializer,
    BusinessWithProductsSerializer
)

class BusinessCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusinessCategory.objects.filter(is_active=True)
    serializer_class = BusinessCategorySerializer
    permission_classes = [permissions.AllowAny]

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business_type', 'category', 'city', 'province', 'is_featured']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'created_at', 'average_rating']
    ordering = ['-is_featured', '-created_at']
    
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
        if self.request.user.is_authenticated and self.request.user.location:
            context['user_location'] = self.request.user.location
        
        return context
    
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
    
    @action(detail=False, methods=['get'])
    def with_products(self, request):
        """Get businesses with their featured products"""
        businesses = self.get_queryset()[:10]  # Limit for performance
        serializer = self.get_serializer(businesses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
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
