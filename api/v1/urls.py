from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Import ViewSets
from apps.accounts.views import UserViewSet
from apps.businesses.views import BusinessViewSet, BusinessCategoryViewSet
from apps.products.views import ProductViewSet, ProductCategoryViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'business-categories', BusinessCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-categories', ProductCategoryViewSet)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom auth endpoints
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='user_register'),
    path('auth/login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
    path('auth/me/', UserViewSet.as_view({'get': 'me'}), name='user_profile'),
]