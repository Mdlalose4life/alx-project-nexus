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
    ViewSet for managing user's shopping cart with consistent response patterns
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
    
    def create_success_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        """Helper method to create consistent success responses"""
        response_data = {
            'success': True,
            'message': message
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)
    
    def create_error_response(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Helper method to create consistent error responses"""
        response_data = {
            'success': False,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)
    
    @extend_schema(
        summary="Get user's cart",
        description="Retrieve the current user's shopping cart with all items",
        responses={
            200: {
                'description': 'Cart retrieved successfully',
                'example': {
                    'success': True,
                    'message': 'Cart retrieved successfully',
                    'data': {
                        'id': 1,
                        'items': [],
                        'total_items': 0,
                        'total_amount': '0.00'
                    }
                }
            }
        }
    )
    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return self.create_success_response(
            data=serializer.data,
            message="Cart retrieved successfully"
        )
    
    @extend_schema(
        summary="Add item to cart",
        request=AddToCartSerializer,
        responses={
            201: {
                'description': 'Item added to cart successfully',
                'example': {
                    'success': True,
                    'message': 'Item added to cart successfully',
                    'data': {
                        'item': {
                            'id': 1,
                            'product_name': 'Pizza Margherita',
                            'quantity': 2,
                            'unit_price': '15.99'
                        },
                        'cart_summary': {
                            'total_items': 2,
                            'total_amount': '31.98'
                        }
                    }
                }
            },
            400: {
                'description': 'Validation error',
                'example': {
                    'success': False,
                    'message': 'Invalid product or quantity',
                    'errors': {
                        'product_id': ['Product not found or inactive']
                    }
                }
            }
        }
    )
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return self.create_error_response(
                message="Invalid product or quantity",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
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
            
            action_message = "Item added to cart successfully"
            if not created:
                # Update existing item
                old_quantity = cart_item.quantity
                cart_item.quantity += quantity
                cart_item.notes = notes
                cart_item.save()
                action_message = f"Item quantity updated from {old_quantity} to {cart_item.quantity}"
            
            # Refresh cart to get updated totals
            cart.refresh_from_db()
            
            item_serializer = CartItemSerializer(cart_item, context={'request': request})
            
            response_data = {
                'item': item_serializer.data,
                'cart_summary': {
                    'total_items': cart.total_items,
                    'total_amount': str(cart.total_amount)
                }
            }
            
            return self.create_success_response(
                data=response_data,
                message=action_message,
                status_code=status.HTTP_201_CREATED
            )
            
        except Product.DoesNotExist:
            return self.create_error_response(
                message="Product not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to add item to cart",
                errors={'detail': [str(e)]}
            )
    
    @extend_schema(
        summary="Update cart item",
        request=UpdateCartItemSerializer,
        responses={
            200: {
                'description': 'Cart item updated successfully',
                'example': {
                    'success': True,
                    'message': 'Cart item updated successfully',
                    'data': {
                        'item': {
                            'id': 1,
                            'quantity': 3,
                            'total_price': '47.97'
                        },
                        'cart_summary': {
                            'total_items': 3,
                            'total_amount': '47.97'
                        }
                    }
                }
            },
            404: {
                'description': 'Cart item not found',
                'example': {
                    'success': False,
                    'message': 'Cart item not found'
                }
            }
        }
    )
    @action(detail=True, methods=['patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, pk=None, item_id=None):
        cart = self.get_object()
        
        try:
            cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        except CartItem.DoesNotExist:
            return self.create_error_response(
                message="Cart item not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return self.create_error_response(
                message="Invalid update data",
                errors=serializer.errors
            )
        
        try:
            old_quantity = cart_item.quantity
            cart_item.quantity = serializer.validated_data['quantity']
            cart_item.notes = serializer.validated_data.get('notes', cart_item.notes)
            cart_item.save()
            
            # Refresh cart to get updated totals
            cart.refresh_from_db()
            
            item_serializer = CartItemSerializer(cart_item, context={'request': request})
            
            response_data = {
                'item': item_serializer.data,
                'cart_summary': {
                    'total_items': cart.total_items,
                    'total_amount': str(cart.total_amount)
                }
            }
            
            return self.create_success_response(
                data=response_data,
                message=f"Cart item updated successfully (quantity: {old_quantity} → {cart_item.quantity})"
            )
            
        except Exception as e:
            return self.create_error_response(
                message="Failed to update cart item",
                errors={'detail': [str(e)]}
            )
    
    @extend_schema(
        summary="Remove item from cart",
        responses={
            200: {
                'description': 'Item removed from cart successfully',
                'example': {
                    'success': True,
                    'message': 'Item removed from cart successfully',
                    'data': {
                        'removed_item': 'Pizza Margherita',
                        'cart_summary': {
                            'total_items': 1,
                            'total_amount': '15.99'
                        }
                    }
                }
            },
            404: {
                'description': 'Cart item not found',
                'example': {
                    'success': False,
                    'message': 'Cart item not found'
                }
            }
        }
    )
    @action(detail=True, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        cart = self.get_object()
        
        try:
            cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
            removed_item_name = cart_item.product.name
            cart_item.delete()
            
            # Refresh cart to get updated totals
            cart.refresh_from_db()
            
            response_data = {
                'removed_item': removed_item_name,
                'cart_summary': {
                    'total_items': cart.total_items,
                    'total_amount': str(cart.total_amount)
                }
            }
            
            return self.create_success_response(
                data=response_data,
                message="Item removed from cart successfully"
            )
            
        except CartItem.DoesNotExist:
            return self.create_error_response(
                message="Cart item not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to remove item from cart",
                errors={'detail': [str(e)]}
            )
    
    @extend_schema(
        summary="Clear entire cart",
        responses={
            200: {
                'description': 'Cart cleared successfully',
                'example': {
                    'success': True,
                    'message': 'Cart cleared successfully',
                    'data': {
                        'items_removed': 5,
                        'cart_summary': {
                            'total_items': 0,
                            'total_amount': '0.00'
                        }
                    }
                }
            }
        }
    )
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        cart = self.get_object()
        
        try:
            items_count = cart.items.count()
            cart.items.all().delete()
            
            # Refresh cart to get updated totals
            cart.refresh_from_db()
            
            response_data = {
                'items_removed': items_count,
                'cart_summary': {
                    'total_items': cart.total_items,
                    'total_amount': str(cart.total_amount)
                }
            }
            
            return self.create_success_response(
                data=response_data,
                message=f"Cart cleared successfully ({items_count} items removed)"
            )
            
        except Exception as e:
            return self.create_error_response(
                message="Failed to clear cart",
                errors={'detail': [str(e)]}
            )
    
    @extend_schema(
        summary="Clear cart items for specific business",
        responses={
            200: {
                'description': 'Business items cleared from cart successfully',
                'example': {
                    'success': True,
                    'message': 'Items from Pizza Palace cleared from cart successfully',
                    'data': {
                        'business_name': 'Pizza Palace',
                        'items_removed': 3,
                        'cart_summary': {
                            'total_items': 2,
                            'total_amount': '25.98'
                        }
                    }
                }
            },
            404: {
                'description': 'Business not found',
                'example': {
                    'success': False,
                    'message': 'Business not found'
                }
            }
        }
    )
    @action(detail=True, methods=['delete'], url_path='clear-business/(?P<business_id>[^/.]+)')
    def clear_business(self, request, pk=None, business_id=None):
        cart = self.get_object()
        
        try:
            from apps.businesses.models import Business
            business = get_object_or_404(Business, id=business_id)
            
            business_items = cart.items.filter(product__business_id=business_id)
            items_count = business_items.count()
            
            if items_count == 0:
                return self.create_success_response(
                    data={
                        'business_name': business.name,
                        'items_removed': 0,
                        'cart_summary': {
                            'total_items': cart.total_items,
                            'total_amount': str(cart.total_amount)
                        }
                    },
                    message=f"No items from {business.name} found in cart"
                )
            
            business_items.delete()
            
            # Refresh cart to get updated totals
            cart.refresh_from_db()
            
            response_data = {
                'business_name': business.name,
                'items_removed': items_count,
                'cart_summary': {
                    'total_items': cart.total_items,
                    'total_amount': str(cart.total_amount)
                }
            }
            
            return self.create_success_response(
                data=response_data,
                message=f"Items from {business.name} cleared from cart successfully ({items_count} items removed)"
            )
            
        except Business.DoesNotExist:
            return self.create_error_response(
                message="Business not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to clear business items from cart",
                errors={'detail': [str(e)]}
            )


# Additional utility class for consistent responses across the entire orders app
class StandardResponseMixin:
    """
    Mixin to provide consistent response patterns across all order-related views
    """
    
    def create_success_response(self, data=None, message="Operation successful", status_code=status.HTTP_200_OK):
        """Create consistent success response"""
        response_data = {
            'success': True,
            'message': message
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)
    
    def create_error_response(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Create consistent error response"""
        response_data = {
            'success': False,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)
    
    def create_validation_error_response(self, serializer_errors):
        """Create consistent validation error response"""
        return self.create_error_response(
            message="Validation failed",
            errors=serializer_errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def create_not_found_response(self, resource_name="Resource"):
        """Create consistent not found response"""
        return self.create_error_response(
            message=f"{resource_name} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    def create_permission_denied_response(self, message="Permission denied"):
        """Create consistent permission denied response"""
        return self.create_error_response(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class OrderViewSet(StandardResponseMixin, ModelViewSet):
    """
    ViewSet for managing orders with consistent response patterns
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
        ],
        responses={
            200: {
                'description': 'Orders retrieved successfully',
                'example': {
                    'success': True,
                    'message': 'Orders retrieved successfully',
                    'data': {
                        'count': 25,
                        'results': []
                    }
                }
            }
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return self.create_success_response(
            data=response.data,
            message="Orders retrieved successfully"
        )
    
    @extend_schema(
        summary="Create new order",
        description="Create a new order from cart items for a specific business",
        responses={
            201: {
                'description': 'Order created successfully',
                'example': {
                    'success': True,
                    'message': 'Order created successfully',
                    'data': {
                        'id': 123,
                        'order_number': 'ORD-2024-123',
                        'status': 'pending',
                        'total_amount': '45.99'
                    }
                }
            }
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.create_validation_error_response(serializer.errors)
        
        try:
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
            return self.create_success_response(
                data=response_serializer.data,
                message="Order created successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to create order",
                errors={'detail': [str(e)]}
            )
    
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
            return self.create_permission_denied_response(
                "Only business owners can update order status"
            )
        
        serializer = UpdateOrderStatusSerializer(
            data=request.data, 
            context={'order': order, 'request': request}
        )
        
        if not serializer.is_valid():
            return self.create_validation_error_response(serializer.errors)
        
        try:
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
            return self.create_success_response(
                data=response_serializer.data,
                message=f"Order status updated from {old_status} to {new_status}"
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to update order status",
                errors={'detail': [str(e)]}
            )
    
    @extend_schema(
        summary="Cancel order",
        responses={200: OrderDetailSerializer}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        # Check if order can be cancelled
        if order.status not in ['pending', 'confirmed', 'preparing']:
            return self.create_error_response(
                message="Order cannot be cancelled at this stage",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions (customer can cancel their own order, business owner can cancel any order)
        if not (order.customer == request.user or 
                (request.user.user_type == 'business_owner' and order.business.owner == request.user)):
            return self.create_permission_denied_response(
                "You do not have permission to cancel this order"
            )
        
        try:
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
            return self.create_success_response(
                data=response_serializer.data,
                message="Order cancelled successfully"
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to cancel order",
                errors={'detail': [str(e)]}
            )
    
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
            return self.create_permission_denied_response(
                "Only the customer can rate the order"
            )
        
        if order.status != 'completed':
            return self.create_error_response(
                message="Order must be completed before rating",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already rated
        if hasattr(order, 'rating'):
            return self.create_error_response(
                message="Order has already been rated",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CreateOrderRatingSerializer(
            data=request.data, 
            context={'order': order, 'request': request}
        )
        
        if not serializer.is_valid():
            return self.create_validation_error_response(serializer.errors)
        
        try:
            rating = serializer.save()
            response_serializer = OrderRatingSerializer(rating, context={'request': request})
            return self.create_success_response(
                data=response_serializer.data,
                message="Order rated successfully",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to rate order",
                errors={'detail': [str(e)]}
            )


class DeliveryInfoViewSet(StandardResponseMixin, ModelViewSet):
    """
    ViewSet for managing delivery information with consistent response patterns
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
            return self.create_permission_denied_response(
                "Only business owners can update delivery information"
            )
        
        try:
            response = super().update(request, *args, **kwargs)
            return self.create_success_response(
                data=response.data,
                message="Delivery information updated successfully"
            )
        except Exception as e:
            return self.create_error_response(
                message="Failed to update delivery information",
                errors={'detail': [str(e)]}
            )


class OrderRatingViewSet(StandardResponseMixin, ModelViewSet):
    """
    ViewSet for managing order ratings with consistent response patterns
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
        response = super().list(request, *args, **kwargs)
        return self.create_success_response(
            data=response.data,
            message="Ratings retrieved successfully"
        )


# Business Analytics Views
class BusinessOrderAnalyticsView(StandardResponseMixin, generics.GenericAPIView):
    """
    Get order analytics for business owners with consistent response patterns
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Get business order analytics",
        description="Get order statistics and analytics for business owners",
        responses={
            200: {
                'description': 'Analytics retrieved successfully',
                'example': {
                    'success': True,
                    'message': 'Business analytics retrieved successfully',
                    'data': {
                        'business_id': 1,
                        'business_name': 'Pizza Palace',
                        'overview': {
                            'total_orders': 150,
                            'total_revenue': 3250.50,
                            'average_rating': 4.2,
                            'total_ratings': 45
                        },
                        'recent_stats': {
                            'today': {'orders': 5, 'revenue': 125.99},
                            'week': {'orders': 25, 'revenue': 650.75},
                            'month': {'orders': 100, 'revenue': 2100.25}
                        }
                    }
                }
            },
            403: {
                'description': 'Permission denied',
                'example': {
                    'success': False,
                    'message': 'Only business owners can access analytics'
                }
            }
        }
    )
    def get(self, request, business_id=None):
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        user = request.user
        if user.user_type != 'business_owner':
            return self.create_permission_denied_response(
                "Only business owners can access analytics"
            )
        
        try:
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
            
            return self.create_success_response(
                data=analytics_data,
                message="Business analytics retrieved successfully"
            )
            
        except Business.DoesNotExist:
            return self.create_not_found_response("Business")
        except Exception as e:
            return self.create_error_response(
                message="Failed to retrieve analytics",
                errors={'detail': [str(e)]}
            )
