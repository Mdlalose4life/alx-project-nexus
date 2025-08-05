from rest_framework import generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from apps.orders.models import (
    Cart, CartItem, Order, OrderItem, OrderStatusHistory, 
    DeliveryInfo, OrderRating
)
from apps.products.models import Product
from api.v1.serializers.orders import (
    CartSerializer, CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer,
    OrderListSerializer, OrderDetailSerializer, CreateOrderSerializer,
    UpdateOrderStatusSerializer, OrderRatingSerializer, CreateOrderRatingSerializer,
    DeliveryInfoSerializer
)
from utils.permissions import IsOwnerOrReadOnly, IsBusinessOwnerOrReadOnly


class CartViewSet(ModelViewSet):
    """
    ViewSet for managing user's shopping cart
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related(
            'items__product__business',
            'items__product__images'
        )
    
    def get_object(self):
        # Get or create cart for current user
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @extend_schema(
        summary="Get user's cart",
        description="Retrieve the current user's shopping cart with all items"
    )
    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Add item to cart",
        request=AddToCartSerializer,
        responses={201: CartItemSerializer}
    )
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            notes = serializer.validated_data.get('notes', '')
            
            product = get_object_or_404(Product, id=product_id, status='active')
            
            # Check if item already exists in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity,
                    'notes': notes
                }
            )
            
            if not created:
                # Update existing item
                cart_item.quantity += quantity
                cart_item.notes = notes
                cart_item.save()
            
            serializer = CartItemSerializer(cart_item, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Update cart item",
        request=UpdateCartItemSerializer,
        responses={200: CartItemSerializer}
    )
    @action(detail=True, methods=['patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, pk=None, item_id=None):
        cart = self.get_object()
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        
        serializer = UpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item.quantity = serializer.validated_data['quantity']
            cart_item.notes = serializer.validated_data.get('notes', cart_item.notes)
            cart_item.save()
            
            response_serializer = CartItemSerializer(cart_item, context={'request': request})
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Remove item from cart",
        responses={204: None}
    )
    @action(detail=True, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        cart = self.get_object()
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        summary="Clear entire cart",
        responses={204: None}
    )
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        summary="Clear cart items for specific business",
        responses={204: None}
    )
    @action(detail=True, methods=['delete'], url_path='clear-business/(?P<business_id>[^/.]+)')
    def clear_business(self, request, pk=None, business_id=None):
        cart = self.get_object()
        cart.items.filter(product__business_id=business_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(ModelViewSet):
    """
    ViewSet for managing orders
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'delivery_method', 'business']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'business_owner':
            # Business owners see orders for their businesses
            return Order.objects.filter(
                business__owner=user
            ).select_related('customer', 'business').prefetch_related('items')
        else:
            # Customers see their own orders
            return Order.objects.filter(
                customer=user
            ).select_related('customer', 'business').prefetch_related('items')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return CreateOrderSerializer
        return OrderDetailSerializer
    
    @extend_schema(
        summary="List orders",
        description="List orders for the current user (customer orders or business orders)",
        parameters=[
            OpenApiParameter('status', OpenApiTypes.STR, description='Filter by order status'),
            OpenApiParameter('delivery_method', OpenApiTypes.STR, description='Filter by delivery method'),
            OpenApiParameter('business', OpenApiTypes.INT, description='Filter by business ID'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create new order",
        description="Create a new order from cart items for a specific business"
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            order = serializer.save()
            
            # Create initial status history
            OrderStatusHistory.objects.create(
                order=order,
                status='pending',
                notes='Order created',
                created_by=request.user
            )
        
        response_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Update order status",
        request=UpdateOrderStatusSerializer,
        responses={200: OrderDetailSerializer}
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        
        # Check permissions
        if request.user.user_type != 'business_owner' or order.business.owner != request.user:
            return Response(
                {'error': 'Only business owners can update order status'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UpdateOrderStatusSerializer(
            data=request.data, 
            context={'order': order, 'request': request}
        )
        
        if serializer.is_valid():
            with transaction.atomic():
                old_status = order.status
                new_status = serializer.validated_data['status']
                notes = serializer.validated_data.get('notes', '')
                
                order.status = new_status
                order.save()
                
                # Create status history entry
                OrderStatusHistory.objects.create(
                    order=order,
                    status=new_status,
                    notes=notes or f'Status changed from {old_status} to {new_status}',
                    created_by=request.user
                )
            
            response_serializer = OrderDetailSerializer(order, context={'request': request})
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Cancel order",
        responses={200: OrderDetailSerializer}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        # Check if order can be cancelled
        if order.status not in ['pending', 'confirmed', 'preparing']:
            return Response(
                {'error': 'Order cannot be cancelled at this stage'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions (customer can cancel their own order, business owner can cancel any order)
        if not (order.customer == request.user or 
                (request.user.user_type == 'business_owner' and order.business.owner == request.user)):
            return Response(
                {'error': 'You do not have permission to cancel this order'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        with transaction.atomic():
            order.status = 'cancelled'
            order.save()
            
            OrderStatusHistory.objects.create(
                order=order,
                status='cancelled',
                notes=f'Order cancelled by {request.user.username}',
                created_by=request.user
            )
        
        response_serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(response_serializer.data)
    
    @extend_schema(
        summary="Rate order",
        request=CreateOrderRatingSerializer,
        responses={201: OrderRatingSerializer}
    )
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        order = self.get_object()
        
        # Check if user is the customer and order is completed
        if order.customer != request.user:
            return Response(
                {'error': 'Only the customer can rate the order'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status != 'completed':
            return Response(
                {'error': 'Order must be completed before rating'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already rated
        if hasattr(order, 'rating'):
            return Response(
                {'error': 'Order has already been rated'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CreateOrderRatingSerializer(
            data=request.data, 
            context={'order': order, 'request': request}
        )
        
        if serializer.is_valid():
            rating = serializer.save()
            response_serializer = OrderRatingSerializer(rating, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryInfoViewSet(ModelViewSet):
    """
    ViewSet for managing delivery information
    """
    serializer_class = DeliveryInfoSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'business_owner':
            return DeliveryInfo.objects.filter(
                order__business__owner=user
            ).select_related('order')
        else:
            return DeliveryInfo.objects.filter(
                order__customer=user
            ).select_related('order')
    
    @extend_schema(
        summary="Update delivery information",
        description="Update delivery details (business owners only)"
    )
    def update(self, request, *args, **kwargs):
        delivery_info = self.get_object()
        
        # Check if user is business owner
        if request.user.user_type != 'business_owner' or delivery_info.order.business.owner != request.user:
            return Response(
                {'error': 'Only business owners can update delivery information'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


class OrderRatingViewSet(ModelViewSet):
    """
    ViewSet for managing order ratings
    """
    serializer_class = OrderRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['business', 'overall_rating', 'is_public']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'business_owner':
            # Business owners see ratings for their businesses
            return OrderRating.objects.filter(
                business__owner=user
            ).select_related('customer', 'order', 'business')
        else:
            # Customers see their own ratings
            return OrderRating.objects.filter(
                customer=user
            ).select_related('customer', 'order', 'business')
    
    @extend_schema(
        summary="List ratings",
        description="List ratings (business ratings for business owners, own ratings for customers)",
        parameters=[
            OpenApiParameter('business', OpenApiTypes.INT, description='Filter by business ID'),
            OpenApiParameter('overall_rating', OpenApiTypes.INT, description='Filter by overall rating'),
            OpenApiParameter('is_public', OpenApiTypes.BOOL, description='Filter by public visibility'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Business Analytics Views
class BusinessOrderAnalyticsView(generics.GenericAPIView):
    """
    Get order analytics for business owners
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get business order analytics",
        description="Get order statistics and analytics for business owners"
    )
    def get(self, request, business_id=None):
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        user = request.user
        if user.user_type != 'business_owner':
            return Response(
                {'error': 'Only business owners can access analytics'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get business
        from apps.businesses.models import Business
        business = get_object_or_404(Business, id=business_id, owner=user)
        
        # Date filters
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        orders_qs = Order.objects.filter(business=business)
        
        # Overall statistics
        total_orders = orders_qs.count()
        total_revenue = orders_qs.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Recent statistics
        today_orders = orders_qs.filter(created_at__date=today).count()
        week_orders = orders_qs.filter(created_at__date__gte=week_ago).count()
        month_orders = orders_qs.filter(created_at__date__gte=month_ago).count()
        
        today_revenue = orders_qs.filter(created_at__date=today).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        week_revenue = orders_qs.filter(created_at__date__gte=week_ago).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        month_revenue = orders_qs.filter(created_at__date__gte=month_ago).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Status breakdown
        status_breakdown = orders_qs.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Average ratings
        avg_rating = OrderRating.objects.filter(business=business).aggregate(
            avg=Avg('overall_rating')
        )['avg'] or 0
        
        # Popular products
        popular_products = OrderItem.objects.filter(
            order__business=business
        ).values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_orders=Count('order', distinct=True)
        ).order_by('-total_quantity')[:10]
        
        analytics_data = {
            'business_id': business.id,
            'business_name': business.name,
            'overview': {
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'average_rating': round(float(avg_rating), 2) if avg_rating else 0,
                'total_ratings': OrderRating.objects.filter(business=business).count()
            },
            'recent_stats': {
                'today': {
                    'orders': today_orders,
                    'revenue': float(today_revenue)
                },
                'week': {
                    'orders': week_orders,
                    'revenue': float(week_revenue)
                },
                'month': {
                    'orders': month_orders,
                    'revenue': float(month_revenue)
                }
            },
            'status_breakdown': [
                {
                    'status': item['status'],
                    'status_display': dict(Order.ORDER_STATUS)[item['status']],
                    'count': item['count']
                }
                for item in status_breakdown
            ],
            'popular_products': [
                {
                    'product_name': item['product__name'],
                    'total_quantity': item['total_quantity'],
                    'total_orders': item['total_orders']
                }
                for item in popular_products
            ]
        }
        
        return Response(analytics_data)