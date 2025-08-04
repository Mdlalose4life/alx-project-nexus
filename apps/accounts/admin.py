from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.gis import admin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.GISModelAdmin):
    """Custom User Admin with location support"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('username',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('LocalBiz Info', {
            'fields': ('user_type', 'phone_number', 'is_phone_verified', 
                      'location', 'preferred_language', 'date_of_birth')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('LocalBiz Info', {
            'fields': ('user_type', 'phone_number', 'preferred_language')
        }),
    )
