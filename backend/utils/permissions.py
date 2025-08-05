from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner
        return obj.owner == request.user

class IsBusinessOwner(permissions.BasePermission):
    """
    Custom permission for business owners
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == 'business_owner'

class IsBusinessOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow business owners to manage their own content
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_authenticated:
            return False
            
        return request.user.user_type in ['business_owner', 'admin']
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user owns the business (direct or through product)
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'business'):
            return obj.business.owner == request.user
        
        return False
