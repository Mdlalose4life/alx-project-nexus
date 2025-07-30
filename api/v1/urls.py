from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import ViewSets (we'll create these next)
from apps.accounts.views import UserViewSet
from apps.businesses.views import BusinessViewSet, BusinessCategoryViewSet
from apps.products.views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'business-categories', BusinessCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('apps.accounts.urls')),
    # Add other app URLs as needed
]