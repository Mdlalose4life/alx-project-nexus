from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.auth import get_user_model
from apps.orders.models import (
    Cart, CartItem, Order, OrderItem, OrderStatusHistory, 
    DeliveryInfo, OrderRating
)
from api.v1.serializers.products import ProductListSerializer
from api.v1.serializers.businesses import BusinessListSerializer

User = get_user_model()

# Cart Serializers
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    business_name = serializers.CharField(source='product.business.name', read_only=True)
    business_slug = serializers.CharField(source='product.business.slug', read_only=True)
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_image', 
            'business_name', 'business_slug', 'quantity', 
            'unit_price', 'total_price', 'notes', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'unit_price', 'total_price', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
        return None
    
    @extend_schema_field(serializers.BooleanField())
    def get_is_available(self, obj):
        return obj.product.status == 'active' and obj.product.is_in_stock

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    businesses = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total_items', 'total_amount', 
            'businesses', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_businesses(self, obj):
        businesses = obj.businesses
        return [
            {
                'id': business.id,
                'name': business.name,
                'slug': business.slug,
                'item_count': obj.items.filter(product__business=business).count()
            }
            for business in businesses
        ]

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            product = Product.objects.get(id=value, status='active')
            if not product.is_in_stock:
                raise serializers.ValidationError("Product is out of stock")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive")

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)

# Order Serializers
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField()
    product_description = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_description',
            'quantity', 'unit_price', 'total_price', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at']

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'status', 'status_display', 'notes', 
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = [
            'id', 'driver_name', 'driver_phone', 'vehicle_info',
            'estimated_arrival', 'actual_arrival', 'delivery_photo',
            'customer_signature', 'delivery_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderRatingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    class Meta:
        model = OrderRating
        fields = [
            'id', 'order', 'customer', 'customer_name', 'business',
            'overall_rating', 'food_quality', 'delivery_speed', 
            'customer_service', 'review_text', 'is_public', 
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'customer', 'customer_name', 'business', 
            'is_verified', 'created_at', 'updated_at'
        ]

class OrderListSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    business_logo = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    delivery_method_display = serializers.CharField(source='get_delivery_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'business_name', 'business_logo',
            'status', 'status_display', 'delivery_method', 'delivery_method_display',
            'payment_status', 'payment_status_display', 'total_amount',
            'item_count', 'created_at', 'estimated_delivery_time'
        ]
    
    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_business_logo(self, obj):
        if obj.business.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.business.logo.url)
        return None
    
    @extend_schema_field(serializers.IntegerField())
    def get_item_count(self, obj):
        return obj.items.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    business = BusinessListSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    delivery_info = DeliveryInfoSerializer(read_only=True)
    rating = OrderRatingSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    delivery_method_display = serializers.CharField(source='get_delivery_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'business', 'status', 'status_display',
            'delivery_method', 'delivery_method_display', 'subtotal', 'delivery_fee',
            'service_fee', 'tax_amount', 'discount_amount', 'total_amount',
            'customer_name', 'customer_phone', 'customer_email',
            'delivery_address', 'delivery_notes', 'payment_status', 
            'payment_status_display', 'payment_method', 'payment_reference',
            'special_instructions', 'items', 'status_history', 'delivery_info',
            'rating', 'created_at', 'updated_at', 'confirmed_at',
            'estimated_delivery_time', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'order_number', 'customer', 'subtotal', 'total_amount',
            'created_at', 'updated_at', 'confirmed_at', 'delivered_at'
        ]

class CreateOrderSerializer(serializers.ModelSerializer):
    delivery_latitude = serializers.FloatField(write_only=True, required=False)
    delivery_longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Order
        fields = [
            'business', 'delivery_method', 'customer_name', 'customer_phone',
            'customer_email', 'delivery_address', 'delivery_latitude', 
            'delivery_longitude', 'delivery_notes', 'special_instructions'
        ]
    
    def validate(self, data):
        # Validate delivery method requirements
        if data['delivery_method'] == 'delivery':
            required_fields = ['delivery_address', 'delivery_latitude', 'delivery_longitude']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(
                        f"{field.replace('_', ' ').title()} is required for delivery orders"
                    )
        return data
    
    def create(self, validated_data):
        from django.contrib.gis.geos import Point
        from decimal import Decimal
        
        # Extract location data
        lat = validated_data.pop('delivery_latitude', None)
        lon = validated_data.pop('delivery_longitude', None)
        
        if lat and lon:
            validated_data['delivery_location'] = Point(lon, lat)
        
        # Set customer
        validated_data['customer'] = self.context['request'].user
        
        # Get cart items for this business
        user = self.context['request'].user
        business = validated_data['business']
        cart_items = user.cart.items.filter(product__business=business)
        
        if not cart_items.exists():
            raise serializers.ValidationError("No items in cart for this business")
        
        # Calculate totals
        subtotal = sum(item.total_price for item in cart_items)
        validated_data['subtotal'] = subtotal
        
        # Calculate fees (you can customize this logic)
        delivery_fee = Decimal('0.00')
        if validated_data['delivery_method'] == 'delivery':
            delivery_fee = Decimal('5.00')  # Fixed delivery fee
        
        validated_data['delivery_fee'] = delivery_fee
        validated_data['service_fee'] = subtotal * Decimal('0.05')  # 5% service fee
        validated_data['tax_amount'] = subtotal * Decimal('0.15')  # 15% tax
        
        # Calculate total
        validated_data['total_amount'] = (
            subtotal + delivery_fee + 
            validated_data['service_fee'] + validated_data['tax_amount'] -
            validated_data.get('discount_amount', Decimal('0.00'))
        )
        
        # Create order
        order = super().create(validated_data)
        
        # Create order items from cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                notes=cart_item.notes
            )
        
        # Clear cart items for this business
        cart_items.delete()
        
        return order

class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_status(self, value):
        order = self.context['order']
        current_status = order.status
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['preparing', 'cancelled'],
            'preparing': ['ready', 'cancelled'],
            'ready': ['out_for_delivery', 'completed', 'cancelled'],
            'out_for_delivery': ['delivered', 'cancelled'],
            'delivered': ['completed'],
            'completed': [],
            'cancelled': ['refunded'],
            'refunded': []
        }
        
        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}"
            )
        
        return value

class CreateOrderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRating
        fields = [
            'overall_rating', 'food_quality', 'delivery_speed',
            'customer_service', 'review_text', 'is_public'
        ]
    
    def create(self, validated_data):
        order = self.context['order']
        validated_data['order'] = order
        validated_data['customer'] = self.context['request'].user
        validated_data['business'] = order.business
        return super().create(validated_data)