# Replace your apps/products/admin.py with this enhanced version

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from cloudinary import CloudinaryImage
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
    fields = ['image_preview', 'image', 'alt_text', 'is_primary', 'sort_order', 'cloudinary_url']
    readonly_fields = ['image_preview', 'cloudinary_url']
    
    def image_preview(self, obj):
        """Show image preview in inline"""
        if obj.image:
            try:
                # Use Cloudinary transformation for thumbnail
                thumbnail_url = CloudinaryImage(str(obj.image)).build_url(
                    width=100, height=100, crop='fill', gravity='center', quality='auto'
                )
                return format_html(
                    '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                    thumbnail_url
                )
            except Exception as e:
                return format_html('<span style="color: red;">Error: {}</span>', str(e))
        return "No image"
    
    image_preview.short_description = "Preview"
    
    def cloudinary_url(self, obj):
        """Show full Cloudinary URL"""
        if obj.image:
            try:
                url = obj.image.url
                return format_html(
                    '<a href="{}" target="_blank" style="font-size: 11px;">{}</a>',
                    url, url[:60] + '...' if len(url) > 60 else url
                )
            except Exception as e:
                return format_html('<span style="color: red;">URL Error: {}</span>', str(e))
        return "No URL"
    
    cloudinary_url.short_description = "Cloudinary URL"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = [
        'name', 'business', 'category', 'price', 'stock_quantity',
        'status', 'is_featured', 'stock_status', 'image_count', 'primary_image_preview', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'category', 'business__business_type',
        'business__city', 'track_inventory'
    ]
    search_fields = ['name', 'description', 'business__name', 'sku']
    readonly_fields = [
        'slug', 'sku', 'created_at', 'updated_at', 'is_in_stock', 'is_low_stock',
        'all_images_preview', 'cloudinary_test'
    ]
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
        ('Images Overview', {
            'fields': ('all_images_preview', 'cloudinary_test'),
            'classes': ('collapse',)
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
    
    actions = ['feature_products', 'unfeature_products', 'mark_out_of_stock', 'test_cloudinary_images']
    
    def image_count(self, obj):
        """Show number of images"""
        count = obj.images.count()
        primary_count = obj.images.filter(is_primary=True).count()
        
        if count == 0:
            return format_html('<span style="color: gray;">0 images</span>')
        elif primary_count == 0:
            return format_html('<span style="color: orange;">{} images (no primary)</span>', count)
        else:
            return format_html('<span style="color: green;">{} images</span>', count)
    
    image_count.short_description = "Images"
    
    def primary_image_preview(self, obj):
        """Show primary image preview in list"""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image and primary_image.image:
            try:
                thumbnail_url = CloudinaryImage(str(primary_image.image)).build_url(
                    width=50, height=50, crop='fill', gravity='center', quality='auto'
                )
                return format_html(
                    '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                    thumbnail_url
                )
            except Exception as e:
                return format_html('<span style="color: red;">Error</span>')
        return format_html('<span style="color: gray;">No primary image</span>')
    
    primary_image_preview.short_description = "Primary Image"
    
    def all_images_preview(self, obj):
        """Show all images in a grid in the edit form"""
        images = obj.images.all().order_by('sort_order', 'id')
        if not images:
            return format_html('<p style="color: gray;">No images uploaded yet. Use the inline form below to add images.</p>')
        
        html_parts = ['<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin: 10px 0;">']
        
        for img in images:
            try:
                # Get different sized URLs
                thumbnail_url = CloudinaryImage(str(img.image)).build_url(
                    width=200, height=150, crop='fill', gravity='center', quality='auto'
                )
                full_url = img.image.url
                
                primary_badge = '<span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; position: absolute; top: 5px; left: 5px;">PRIMARY</span>' if img.is_primary else ''
                
                html_parts.append(f'''
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; background: white; position: relative;">
                        {primary_badge}
                        <img src="{thumbnail_url}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px;" />
                        <div style="margin-top: 8px; font-size: 12px;">
                            <strong>ID:</strong> {img.id}<br>
                            <strong>Alt:</strong> {img.alt_text or "No alt text"}<br>
                            <strong>Order:</strong> {img.sort_order}<br>
                            <a href="{full_url}" target="_blank" style="color: #007cba; text-decoration: none;">View Full Size →</a>
                        </div>
                    </div>
                ''')
            except Exception as e:
                html_parts.append(f'''
                    <div style="border: 1px solid #dc3545; border-radius: 8px; padding: 10px; background: #f8d7da; color: #721c24;">
                        <strong>Image ID {img.id}: Error</strong><br>
                        {str(e)}
                    </div>
                ''')
        
        html_parts.append('</div>')
        return format_html(''.join(html_parts))
    
    all_images_preview.short_description = "All Images Preview"
    
    def cloudinary_test(self, obj):
        """Test Cloudinary connectivity for this product's images"""
        if not obj.images.exists():
            return format_html('<p style="color: gray;">No images to test</p>')
        
        html_parts = ['<div style="background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0;">']
        html_parts.append('<h4>Cloudinary Connection Test</h4>')
        
        for img in obj.images.all()[:3]:  # Test first 3 images
            try:
                # Try to access the image URL
                url = img.image.url
                public_id = str(img.image)
                
                # Generate different transformations to test
                test_urls = {
                    'Original': url,
                    'Thumbnail': CloudinaryImage(public_id).build_url(width=100, height=100, crop='fill'),
                    'Optimized': CloudinaryImage(public_id).build_url(quality='auto', fetch_format='auto')
                }
                
                html_parts.append(f'<p><strong>Image {img.id} ({public_id}):</strong></p>')
                html_parts.append('<ul>')
                
                for test_name, test_url in test_urls.items():
                    html_parts.append(f'''
                        <li>
                            {test_name}: <a href="{test_url}" target="_blank" style="color: green;">✓ URL Generated</a>
                            <br><small style="color: #666;">{test_url}</small>
                        </li>
                    ''')
                
                html_parts.append('</ul>')
                
            except Exception as e:
                html_parts.append(f'''
                    <p><strong>Image {img.id}:</strong> <span style="color: red;">✗ Error - {str(e)}</span></p>
                ''')
        
        html_parts.append('</div>')
        return format_html(''.join(html_parts))
    
    cloudinary_test.short_description = "Cloudinary Test"
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure slug and SKU are generated"""
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
    
    def test_cloudinary_images(self, request, queryset):
        """Test Cloudinary connectivity for selected products"""
        total_images = 0
        error_images = 0
        
        for product in queryset:
            for img in product.images.all():
                total_images += 1
                try:
                    # Test URL access
                    url = img.image.url
                    if not url:
                        error_images += 1
                except:
                    error_images += 1
        
        if error_images == 0:
            self.message_user(request, f'✓ All {total_images} images tested successfully!')
        else:
            self.message_user(request, f'⚠ {error_images} out of {total_images} images have issues.')
    
    test_cloudinary_images.short_description = "Test Cloudinary images"


# Register ProductImage separately for direct management
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_preview', 'alt_text', 'is_primary', 'sort_order']
    list_filter = ['is_primary', 'product__category']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['image_preview', 'cloudinary_info']
    
    fields = ['product', 'image', 'image_preview', 'cloudinary_info', 'alt_text', 'is_primary', 'sort_order']
    
    def image_preview(self, obj):
        if obj.image:
            try:
                thumbnail_url = CloudinaryImage(str(obj.image)).build_url(
                    width=200, height=150, crop='fill', gravity='center', quality='auto'
                )
                full_url = obj.image.url
                return format_html(
                    '''
                    <div>
                        <img src="{}" width="200" height="150" style="object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />
                        <br><a href="{}" target="_blank">View Full Size</a>
                    </div>
                    ''',
                    thumbnail_url, full_url
                )
            except Exception as e:
                return format_html('<span style="color: red;">Error: {}</span>', str(e))
        return "No image"
    
    image_preview.short_description = "Preview"
    
    def cloudinary_info(self, obj):
        if obj.image:
            try:
                public_id = str(obj.image)
                url = obj.image.url
                return format_html(
                    '''
                    <div style="background: #f8f9fa; padding: 10px; border-radius: 4px;">
                        <strong>Public ID:</strong> {}<br>
                        <strong>URL:</strong> <a href="{}" target="_blank">{}</a><br>
                        <strong>Status:</strong> <span style="color: green;">✓ Accessible</span>
                    </div>
                    ''',
                    public_id, url, url
                )
            except Exception as e:
                return format_html(
                    '<div style="background: #f8d7da; padding: 10px; border-radius: 4px; color: #721c24;">Error: {}</div>',
                    str(e)
                )
        return "No image data"
    
    cloudinary_info.short_description = "Cloudinary Info"