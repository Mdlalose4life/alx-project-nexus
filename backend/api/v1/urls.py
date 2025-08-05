from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Import ViewSets
from apps.accounts.views import UserViewSet
from apps.businesses.views import BusinessViewSet, BusinessCategoryViewSet
from apps.products.views import ProductViewSet, ProductCategoryViewSet
from apps.orders.views import (
    BusinessOrderAnalyticsView, CartViewSet, OrderViewSet, DeliveryInfoViewSet, OrderRatingViewSet
)

# Create router and register viewsets
router = DefaultRouter()

# User endpoints
router.register(r'users', UserViewSet, basename='user')

# Business endpoints
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'business-categories', BusinessCategoryViewSet, basename='businesscategory')

# Product endpoints  
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-categories', ProductCategoryViewSet, basename='productcategory')

# Nested routes for business products
# router.register(r'businesses/(?P<business_pk>[^/.]+)/products', ProductViewSet, basename='business-products')

# Order endpoints
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'delivery-info', DeliveryInfoViewSet, basename='deliveryinfo')
router.register(r'ratings', OrderRatingViewSet, basename='orderrating')


urlpatterns = [
    # API Schema and Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('', include(router.urls)),
    
    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom authentication endpoints
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='user_register'),
    path('auth/login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
    path('auth/logout/', UserViewSet.as_view({'post': 'logout'}), name='user_logout'),
    path('auth/me/', UserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'}), name='user_profile'),
    path('auth/change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change_password'),
    
    # Business specific endpoints
    path('businesses/nearby/', BusinessViewSet.as_view({'get': 'nearby'}), name='businesses_nearby'),
    path('businesses/featured/', BusinessViewSet.as_view({'get': 'featured'}), name='businesses_featured'),
    path('businesses/with-products/', BusinessViewSet.as_view({'get': 'with_products'}), name='businesses_with_products'),
    path('businesses/<int:pk>/toggle-featured/', BusinessViewSet.as_view({'post': 'toggle_featured'}), name='business_toggle_featured'),
    
    # Product specific endpoints
    path('products/featured/', ProductViewSet.as_view({'get': 'featured'}), name='products_featured'),
    path('products/search/', ProductViewSet.as_view({'get': 'search'}), name='products_search'),
    path('products/by-category/<slug:category_slug>/', ProductViewSet.as_view({'get': 'by_category'}), name='products_by_category'),
    
    # Business products nested endpoint
    path('businesses/<int:business_id>/products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='business_products'),
    
    # Order specific endpoints
    path('analytics/business/<int:business_id>/', BusinessOrderAnalyticsView.as_view(), name='business-order-analytics'),
]