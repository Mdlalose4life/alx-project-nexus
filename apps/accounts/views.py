from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from api.v1.serializers.accounts import (
    UserSerializer, UserCreateSerializer, LoginRequestSerializer,
    LoginResponseSerializer, LogoutRequestSerializer, LogoutResponseSerializer,
    ChangePasswordRequestSerializer, ChangePasswordResponseSerializer,
    ErrorResponseSerializer, UserRegistrationResponseSerializer,
    DashboardStatsSerializer, UserBusinessesResponseSerializer,
    ProfileUpdateResponseSerializer
)

User = get_user_model()

@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="Get a list of users (admin only)",
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve user profile information",
        tags=["Users"]
    ),
    create=extend_schema(
        summary="Register new user",
        description="Create a new user account",
        tags=["Authentication"],
        request=UserCreateSerializer,
        responses={
            201: UserRegistrationResponseSerializer,
            400: ErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                'Business Owner Registration',
                summary='Register as business owner',
                description='Example registration for a business owner',
                value={
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'password': 'securepassword123',
                    'password_confirm': 'securepassword123',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'user_type': 'business_owner',
                    'phone_number': '+27812345678'
                }
            ),
            OpenApiExample(
                'Customer Registration',
                summary='Register as customer',
                description='Example registration for a customer',
                value={
                    'username': 'jane_smith',
                    'email': 'jane@example.com',
                    'password': 'securepassword123',
                    'password_confirm': 'securepassword123',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'user_type': 'customer',
                    'phone_number': '+27823456789'
                }
            ),
        ]
    ),
    update=extend_schema(
        summary="Update user profile",
        description="Update user profile information (authenticated users only)",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Partially update user profile",
        description="Partially update user profile information (authenticated users only)",
        tags=["Users"]
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management and authentication.
    
    Provides user registration, authentication, and profile management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'login']:
            # Allow anyone to register or login
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            # Only admin can list all users
            permission_classes = [permissions.IsAdminUser]
        else:
            # All other actions require authentication
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Optionally restricts the returned users to the current user,
        by filtering against the current user.
        """
        if self.action == 'list' and self.request.user.is_staff:
            return User.objects.all()
        elif hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            # For unauthenticated requests (like registration)
            return User.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Register a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        # refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserSerializer(user, context={'request': request}).data,
            # 'tokens': {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # },
            'message': 'User registered successfully'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="User login",
        description="Authenticate user and return JWT tokens",
        tags=["Authentication"],
        request=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
        },
        examples=[
            OpenApiExample(
                'Login Example',
                summary='User login',
                description='Authenticate with username and password',
                value={
                    'username': 'john_doe',
                    'password': 'securepassword123'
                }
            ),
        ]
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """User login"""
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if not user.is_active:
                return Response(
                    {'error': 'Account is disabled'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user, context={'request': request}).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Login successful'
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid username or password'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @extend_schema(
        summary="User logout",
        description="Logout user by blacklisting refresh token",
        tags=["Authentication"],
        request=LogoutRequestSerializer,
        responses={
            200: LogoutResponseSerializer,
            400: ErrorResponseSerializer,
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """User logout"""
        try:
            serializer = LogoutRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        summary="Get/Update current user profile",
        description="Get or update the profile of the currently authenticated user",
        tags=["Users"],
        responses={
            200: UserSerializer,
            401: ErrorResponseSerializer,
        }
    )
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get or update current user profile"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = UserSerializer(
                request.user, 
                data=request.data, 
                partial=partial,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({
                'user': serializer.data,
                'message': 'Profile updated successfully'
            })
    
    @extend_schema(
        summary="Change password",
        description="Change user password",
        tags=["Authentication"],
        request=ChangePasswordRequestSerializer,
        responses={
            200: ChangePasswordResponseSerializer,
            400: ErrorResponseSerializer,
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        
        if not request.user.check_password(old_password):
            return Response(
                {'error': 'Invalid old password'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != confirm_password:
            return Response(
                {'error': 'New passwords do not match'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate new password
        try:
            validate_password(new_password, request.user)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({'message': 'Password changed successfully'})
    
    @extend_schema(
        summary="Get user businesses",
        description="Get all businesses owned by the current user",
        tags=["Users"],
        responses={
            200: UserBusinessesResponseSerializer
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_businesses(self, request):
        """Get current user's businesses"""
        from api.v1.serializers.businesses import BusinessListSerializer
        
        businesses = request.user.businesses.filter(is_active=True)
        serializer = BusinessListSerializer(
            businesses, 
            many=True, 
            context={'request': request}
        )
        
        return Response({
            'count': businesses.count(),
            'businesses': serializer.data
        })
    
    @extend_schema(
        summary="Get user dashboard stats",
        description="Get dashboard statistics for business owners",
        tags=["Users"],
        responses={
            200: DashboardStatsSerializer
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def dashboard_stats(self, request):
        """Get dashboard statistics for the current user"""
        user = request.user
        
        if user.user_type == 'business_owner':
            businesses = user.businesses.filter(is_active=True)
            total_businesses = businesses.count()
            
            # Calculate total products across all businesses
            total_products = sum(
                business.products.filter(status='active').count() 
                for business in businesses
            )
            
            # Basic stats (implement order tracking as needed)
            stats = {
                'total_businesses': total_businesses,
                'total_products': total_products,
                'total_orders': 0,  # Implement when order system is ready
                'monthly_revenue': 0.0,  # Implement when order system is ready
                'featured_businesses': businesses.filter(is_featured=True).count(),
                'verified_businesses': businesses.filter(verification_status='verified').count(),
            }
        else:
            # Customer stats
            stats = {
                'total_orders': 0,  # Implement when order system is ready
                'total_spent': 0.0,  # Implement when order system is ready
                'favorite_businesses': 0,  # Implement favorites system
                'reviews_written': 0,  # Implement when review system is ready
            }
        
        return Response(stats)