from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductCategory, ProductImage

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = [
        'name', 'business', 'category', 'price', 'stock_quantity',
        'status', 'is_featured', 'stock_status', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'category', 'business__business_type',
        'business__city', 'track_inventory'
    ]
    search_fields = ['name', 'description', 'business__name', 'sku']
    readonly_fields = ['slug', 'sku', 'created_at', 'updated_at', 'is_in_stock', 'is_low_stock']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business', 'name', 'slug', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'track_inventory', 'sku')
        }),
        ('Product Details', {
            'fields': ('weight', 'dimensions', 'status', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_in_stock', 'is_low_stock'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['feature_products', 'unfeature_products', 'mark_out_of_stock']
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure slug and SKU are generated"""
        # The model's save() method will handle slug and SKU generation
        # but we can add any admin-specific logic here if needed
        super().save_model(request, obj, form, change)
    
    def stock_status(self, obj):
        if not obj.track_inventory:
            return format_html('<span style="color: blue;">Not tracked</span>')
        elif obj.is_low_stock:
            return format_html('<span style="color: red;">Low stock</span>')
        elif obj.is_in_stock:
            return format_html('<span style="color: green;">In stock</span>')
        else:
            return format_html('<span style="color: red;">Out of stock</span>')
    stock_status.short_description = 'Stock Status'
    
    def feature_products(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products featured successfully.')
    feature_products.short_description = "Feature selected products"
    
    def unfeature_products(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products unfeatured successfully.')
    unfeature_products.short_description = "Unfeature selected products"
    
    def mark_out_of_stock(self, request, queryset):
        updated = queryset.update(status='out_of_stock', stock_quantity=0)
        self.message_user(request, f'{updated} products marked as out of stock.')
    mark_out_of_stock.short_description = "Mark as out of stock"