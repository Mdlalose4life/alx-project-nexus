from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'address', 'city', 'province', 'postal_code']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'is_phone_verified', 
            'preferred_language', 'date_of_birth', 'profile',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_phone_verified']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type', 'phone_number'
        ]
    
    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile automatically
        UserProfile.objects.create(user=user)
        return user

# Authentication-specific serializers
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class TokensSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class LoginResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    tokens = TokensSerializer()
    message = serializers.CharField()

class LogoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class ChangePasswordRequestSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

class ChangePasswordResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()

class UserRegistrationResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    tokens = TokensSerializer()
    message = serializers.CharField()

class DashboardStatsSerializer(serializers.Serializer):
    # Business owner stats
    total_businesses = serializers.IntegerField(required=False)
    total_products = serializers.IntegerField(required=False)
    total_orders = serializers.IntegerField(required=False)
    monthly_revenue = serializers.FloatField(required=False)
    featured_businesses = serializers.IntegerField(required=False)
    verified_businesses = serializers.IntegerField(required=False)
    
    # Customer stats
    total_spent = serializers.FloatField(required=False)
    favorite_businesses = serializers.IntegerField(required=False)
    reviews_written = serializers.IntegerField(required=False)

class UserBusinessesResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    businesses = serializers.ListField(child=serializers.DictField())

class ProfileUpdateResponseSerializer(serializers.Serializer):
    user = UserSerializer()
    message = serializers.CharField()