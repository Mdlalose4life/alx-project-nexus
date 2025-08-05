from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Business, BusinessCategory, BusinessImage

@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 1
    fields = ['image', 'is_primary']

@admin.register(Business)
class BusinessAdmin(GISModelAdmin):
    """Business admin with map support"""
    inlines = [BusinessImageInline]
    list_display = [
        'name', 'owner', 'business_type', 'category', 'city', 
        'verification_status', 'is_active', 'is_featured', 'get_total_reviews', 
        'get_average_rating', 'created_at'
    ]
    list_filter = [
        'business_type', 'category', 'verification_status', 
        'is_active', 'is_featured', 'city', 'province'
    ]
    search_fields = ['name', 'description', 'owner__username', 'address']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'get_total_reviews', 'get_average_rating']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'slug', 'description', 'business_type', 'category')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'whatsapp_number')
        }),
        ('Location', {
            'fields': ('location', 'address', 'city', 'province', 'postal_code')
        }),
        ('Business Details', {
            'fields': ('registration_number', 'tax_number', 'opens_at', 'closes_at')
        }),
        ('Status & Verification', {
            'fields': ('verification_status', 'is_active', 'is_featured')
        }),
        ('Media', {
            'fields': ('logo', 'cover_image')
        }),
        ('Statistics', {
            'fields': ('get_average_rating', 'get_total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_businesses', 'feature_businesses', 'unfeature_businesses']
    
    def get_total_reviews(self, obj):
        """Get total number of reviews for this business"""
        # Assuming you have a reviews relationship
        if hasattr(obj, 'reviews'):
            return obj.reviews.count()
        return 0
    get_total_reviews.short_description = 'Total Reviews'
    
    def get_average_rating(self, obj):
        """Get average rating for this business"""
        if hasattr(obj, 'reviews'):
            avg_rating = obj.reviews.aggregate(avg=Avg('rating'))['avg']
            return round(avg_rating, 1) if avg_rating else 'No ratings'
        return 'No ratings'
    get_average_rating.short_description = 'Average Rating'
    
    def verify_businesses(self, request, queryset):
        updated = queryset.update(verification_status='verified')
        self.message_user(request, f'{updated} businesses verified successfully.')
    verify_businesses.short_description = "Verify selected businesses"
    
    def feature_businesses(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} businesses featured successfully.')
    feature_businesses.short_description = "Feature selected businesses"
    
    def unfeature_businesses(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} businesses unfeatured successfully.')
    unfeature_businesses.short_description = "Unfeature selected businesses"