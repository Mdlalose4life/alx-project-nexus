from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from apps.businesses.models import Business, BusinessCategory, BusinessImage

class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active']
        read_only_fields = ['slug']

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ['id', 'image', 'caption', 'is_primary', 'created_at']

class BusinessListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for business listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'business_type', 'category_name',
            'phone_number', 'address', 'city', 'province',
            'logo', 'average_rating', 'total_reviews', 'distance',
            'is_featured', 'opens_at', 'closes_at'
        ]
    
    def get_distance(self, obj):
        # Calculate distance if user location is provided in context
        user_location = self.context.get('user_location')
        if user_location and obj.location:
            # Return distance in kilometers
            from django.contrib.gis.measure import Distance
            return obj.location.distance(user_location) * 111  # Convert to km
        return None

class BusinessDetailSerializer(GeoFeatureModelSerializer):
    """Full business details with location data"""
    owner = serializers.StringRelatedField(read_only=True)
    category = BusinessCategorySerializer(read_only=True)
    images = BusinessImageSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        geo_field = 'location'
        fields = [
            'id', 'owner', 'name', 'slug', 'description', 'business_type',
            'category', 'phone_number', 'email', 'whatsapp_number',
            'address', 'city', 'province', 'postal_code',
            'registration_number', 'tax_number', 'verification_status',
            'is_active', 'is_featured', 'opens_at', 'closes_at',
            'logo', 'cover_image', 'images', 'average_rating',
            'total_reviews', 'product_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'owner', 'slug', 'verification_status', 
            'created_at', 'updated_at'
        ]
    
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()

class BusinessCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating businesses"""
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    class Meta:
        model = Business
        fields = [
            'name', 'description', 'business_type', 'category',
            'phone_number', 'email', 'whatsapp_number',
            'address', 'city', 'province', 'postal_code',
            'registration_number', 'tax_number',
            'opens_at', 'closes_at', 'logo', 'cover_image',
            'latitude', 'longitude'
        ]
    
    def create(self, validated_data):
        # Extract coordinates and create Point
        from django.contrib.gis.geos import Point
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)
        
        # Set owner from request user
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

# Nested serializers for combined views
class BusinessWithProductsSerializer(BusinessListSerializer):
    featured_products = serializers.SerializerMethodField()
    
    class Meta(BusinessListSerializer.Meta):
        fields = BusinessListSerializer.Meta.fields + ['featured_products']
    
    def get_featured_products(self, obj):
        from api.v1.serializers.products import ProductListSerializer  # Local import
        featured_products = obj.products.filter(
            status='active', 
            is_featured=True
        )[:4]
        return ProductListSerializer(featured_products, many=True, context=self.context).data