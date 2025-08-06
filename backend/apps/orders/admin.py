from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from django.utils import timezone

from apps.orders.models import (
    Cart, CartItem, Order, OrderItem, OrderStatusHistory, 
    DeliveryInfo, OrderRating
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['unit_price', 'total_price', 'created_at', 'updated_at']
    fields = ['product', 'quantity', 'unit_price', 'total_price', 'notes']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'product__business')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_amount', 'businesses_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_items', 'total_amount', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def businesses_count(self, obj):
        return len(obj.businesses)
    businesses_count.short_description = 'Businesses'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related(
            'items__product__business'
        )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'product_name', 'product_description', 'created_at']
    fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price', 'notes']


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['created_at']
    fields = ['status', 'notes', 'created_by', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


class DeliveryInfoInline(admin.StackedInline):
    model = DeliveryInfo
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Driver Information', {
            'fields': ('driver_name', 'driver_phone', 'vehicle_info')
        }),
        ('Timing', {
            'fields': ('estimated_arrival', 'actual_arrival')
        }),
        ('Delivery Proof', {
            'fields': ('delivery_photo', 'customer_signature', 'delivery_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        })
    )


class OrderRatingInline(admin.StackedInline):
    model = OrderRating
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = [
        'overall_rating', 'food_quality', 'delivery_speed', 'customer_service',
        'review_text', 'is_public', 'is_verified'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_link', 'business_link', 'status_badge', 
        'delivery_method', 'total_amount', 'payment_status', 'created_at'
    ]
    list_filter = [
        'status', 'delivery_method', 'payment_status', 'business__business_type',
        'created_at', 'confirmed_at', 'delivered_at'
    ]
    search_fields = [
        'order_number', 'customer__username', 'customer__email',
        'business__name', 'customer_name', 'customer_phone'
    ]
    readonly_fields = [
        'id', 'order_number', 'subtotal', 'total_amount', 'created_at', 
        'updated_at', 'confirmed_at', 'delivered_at', 'location_map'
    ]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'customer', 'business', 'status')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Delivery Information', {
            'fields': ('delivery_method', 'delivery_address', 'location_map', 'delivery_notes')
        }),
        ('Pricing', {
            'fields': (
                'subtotal', 'delivery_fee', 'service_fee', 'tax_amount', 
                'discount_amount', 'total_amount'
            )
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_method', 'payment_reference')
        }),
        ('Additional Information', {
            'fields': ('special_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'estimated_delivery_time', 'delivered_at'),
            'classes': ['collapse']
        })
    )
    
    inlines = [OrderItemInline, OrderStatusHistoryInline, DeliveryInfoInline, OrderRatingInline]
    
    actions = ['mark_confirmed', 'mark_preparing', 'mark_ready', 'mark_delivered', 'mark_completed']
    
    def customer_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', url, obj.customer.username)
    customer_link.short_description = 'Customer'
    
    def business_link(self, obj):
        url = reverse('admin:businesses_business_change', args=[obj.business.pk])
        return format_html('<a href="{}">{}</a>', url, obj.business.name)
    business_link.short_description = 'Business'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',      # yellow
            'confirmed': '#17a2b8',    # info blue
            'preparing': '#fd7e14',    # orange  
            'ready': '#20c997',        # teal
            'out_for_delivery': '#6f42c1',  # purple
            'delivered': '#28a745',    # green
            'completed': '#28a745',    # green
            'cancelled': '#dc3545',    # red
            'refunded': '#6c757d'      # gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def location_map(self, obj):
        if obj.delivery_location:
            lat, lon = obj.delivery_location.y, obj.delivery_location.x
            map_url = f"https://www.google.com/maps?q={lat},{lon}"
            return format_html(
                '<a href="{}" target="_blank">View on Map ({:.6f}, {:.6f})</a>',
                map_url, lat, lon
            )
        return "No location data"
    location_map.short_description = 'Delivery Location'
    
    def mark_confirmed(self, request, queryset):
        count = 0
        for order in queryset:
            if order.status == 'pending':
                order.status = 'confirmed'
                order.confirmed_at = timezone.now()
                order.save()
                
                OrderStatusHistory.objects.create(
                    order=order,
                    status='confirmed',
                    notes='Status updated via admin',
                    created_by=request.user
                )
                count += 1
        
        self.message_user(request, f'{count} orders marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected orders as confirmed'
    
    def mark_preparing(self, request, queryset):
        count = 0
        for order in queryset.filter(status='confirmed'):
            order.status = 'preparing'
            order.save()
            
            OrderStatusHistory.objects.create(
                order=order,
                status='preparing',
                notes='Status updated via admin',
                created_by=request.user
            )
            count += 1
        
        self.message_user(request, f'{count} orders marked as preparing.')
    mark_preparing.short_description = 'Mark selected orders as preparing'
    
    def mark_ready(self, request, queryset):
        count = 0
        for order in queryset.filter(status='preparing'):
            order.status = 'ready'
            order.save()
            
            OrderStatusHistory.objects.create(
                order=order,
                status='ready',
                notes='Status updated via admin',
                created_by=request.user
            )
            count += 1
        
        self.message_user(request, f'{count} orders marked as ready.')
    mark_ready.short_description = 'Mark selected orders as ready'
    
    def mark_delivered(self, request, queryset):
        count = 0
        for order in queryset.filter(status='out_for_delivery'):
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            
            OrderStatusHistory.objects.create(
                order=order,
                status='delivered',
                notes='Status updated via admin',
                created_by=request.user
            )
            count += 1
        
        self.message_user(request, f'{count} orders marked as delivered.')
    mark_delivered.short_description = 'Mark selected orders as delivered'
    
    def mark_completed(self, request, queryset):
        count = 0
        for order in queryset.filter(status='delivered'):
            order.status = 'completed'
            order.save()
            
            OrderStatusHistory.objects.create(
                order=order,
                status='completed',
                notes='Status updated via admin',
                created_by=request.user
            )
            count += 1
        
        self.message_user(request, f'{count} orders marked as completed.')
    mark_completed.short_description = 'Mark selected orders as completed'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'customer', 'business'
        ).prefetch_related('items')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'status_badge', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'created_by__username']
    readonly_fields = ['created_at']
    
    def order_number(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_number.short_description = 'Order'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107', 'confirmed': '#17a2b8', 'preparing': '#fd7e14',
            'ready': '#20c997', 'out_for_delivery': '#6f42c1', 'delivered': '#28a745',
            'completed': '#28a745', 'cancelled': '#dc3545', 'refunded': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'created_by')


@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'driver_name', 'driver_phone', 'estimated_arrival', 
        'actual_arrival', 'has_photo', 'has_signature'
    ]
    list_filter = ['estimated_arrival', 'actual_arrival', 'created_at']
    search_fields = ['order__order_number', 'driver_name', 'driver_phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Driver Details', {
            'fields': ('driver_name', 'driver_phone', 'vehicle_info')
        }),
        ('Timing', {
            'fields': ('estimated_arrival', 'actual_arrival')
        }),
        ('Delivery Proof', {
            'fields': ('delivery_photo', 'customer_signature', 'delivery_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        })
    )
    
    def order_number(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_number.short_description = 'Order'
    
    def has_photo(self, obj):
        return bool(obj.delivery_photo)
    has_photo.boolean = True
    has_photo.short_description = 'Photo'
    
    def has_signature(self, obj):
        return bool(obj.customer_signature)
    has_signature.boolean = True
    has_signature.short_description = 'Signature'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')


@admin.register(OrderRating)
class OrderRatingAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'customer_name', 'business_name', 'overall_rating_stars',
        'is_public', 'is_verified', 'created_at'
    ]
    list_filter = ['overall_rating', 'is_public', 'is_verified', 'created_at']
    search_fields = [
        'order__order_number', 'customer__username', 'business__name', 'review_text'
    ]
    readonly_fields = ['customer', 'business', 'is_verified', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order', 'customer', 'business')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'food_quality', 'delivery_speed', 'customer_service')
        }),
        ('Review', {
            'fields': ('review_text', 'is_public', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        })
    )
    
    def order_number(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_number.short_description = 'Order'
    
    def customer_name(self, obj):
        return obj.customer.username
    customer_name.short_description = 'Customer'
    
    def business_name(self, obj):
        return obj.business.name
    business_name.short_description = 'Business'
    
    def overall_rating_stars(self, obj):
        stars = '⭐' * obj.overall_rating
        return f"{stars} ({obj.overall_rating}/5)"
    overall_rating_stars.short_description = 'Rating'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'customer', 'business')


# Custom admin site configuration
admin.site.site_header = "Orders Management"
admin.site.site_title = "Orders Admin"
admin.site.index_title = "Welcome to Orders Administration"
