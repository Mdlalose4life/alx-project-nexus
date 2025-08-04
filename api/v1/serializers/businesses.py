from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from drf_spectacular.utils import extend_schema_field
from apps.businesses.models import Business, BusinessCategory, BusinessImage

class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active']
        read_only_fields = ['slug']

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ['id', 'image', 'is_primary', 'created_at']

class BusinessListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for business listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'slug', 'business_type', 'category_name',
            'phone_number', 'address', 'city', 'province',
            'logo', 'average_rating', 'total_reviews', 'distance',
            'is_featured', 'opens_at', 'closes_at'
        ]
    
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_distance(self, obj):
        # Calculate distance if user location is provided in context
        user_location = self.context.get('user_location')
        if user_location and obj.location:
            # Return distance in kilometers
            from django.contrib.gis.measure import Distance
            return obj.location.distance(user_location) * 111  # Convert to km
        return None
    
    @extend_schema_field(serializers.FloatField())
    def get_average_rating(self, obj):
        # Check if the business has the average_rating annotation
        if hasattr(obj, 'average_rating') and obj.average_rating is not None:
            return round(float(obj.average_rating), 1)
        # Fallback to calculating manually if no annotation
        # This assumes you have a reviews relationship
        try:
            from django.db.models import Avg
            avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
            return round(float(avg), 1) if avg else 0.0
        except:
            return 0.0
    
    @extend_schema_field(serializers.IntegerField())
    def get_total_reviews(self, obj):
        # Check if the business has the total_reviews annotation
        if hasattr(obj, 'total_reviews'):
            return obj.total_reviews
        # Fallback to calculating manually if no annotation
        try:
            return obj.reviews.count()
        except:
            return 0

class BusinessDetailSerializer(serializers.ModelSerializer):
    """Full business details with location data as separate fields"""
    owner = serializers.StringRelatedField(read_only=True)
    category = BusinessCategorySerializer(read_only=True)
    images = BusinessImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'owner', 'name', 'slug', 'description', 'business_type',
            'category', 'phone_number', 'email', 'whatsapp_number',
            'address', 'city', 'province', 'postal_code',
            'registration_number', 'tax_number', 'verification_status',
            'is_active', 'is_featured', 'opens_at', 'closes_at',
            'logo', 'cover_image', 'images', 'average_rating',
            'total_reviews', 'product_count', 'latitude', 'longitude',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'owner', 'slug', 'verification_status', 
            'created_at', 'updated_at'
        ]
    
    @extend_schema_field(serializers.IntegerField())
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()
    
    @extend_schema_field(serializers.FloatField())
    def get_average_rating(self, obj):
        # Check if the business has the average_rating annotation
        if hasattr(obj, 'average_rating') and obj.average_rating is not None:
            return round(float(obj.average_rating), 1)
        # Fallback to calculating manually if no annotation
        try:
            from django.db.models import Avg
            avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
            return round(float(avg), 1) if avg else 0.0
        except:
            return 0.0
    
    @extend_schema_field(serializers.IntegerField())
    def get_total_reviews(self, obj):
        # Check if the business has the total_reviews annotation
        if hasattr(obj, 'total_reviews'):
            return obj.total_reviews
        # Fallback to calculating manually if no annotation
        try:
            return obj.reviews.count()
        except:
            return 0
    
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_latitude(self, obj):
        if obj.location:
            return obj.location.y
        return None
    
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_longitude(self, obj):
        if obj.location:
            return obj.location.x
        return None

# Alternative GeoJSON serializer for when you specifically need GeoJSON format
class BusinessGeoJSONSerializer(GeoFeatureModelSerializer):
    """GeoJSON format serializer for mapping purposes"""
    owner = serializers.StringRelatedField(read_only=True)
    category = BusinessCategorySerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    
    class Meta:
        model = Business
        geo_field = 'location'
        auto_bbox = True
        fields = [
            'id', 'owner', 'name', 'slug', 'business_type',
            'category', 'phone_number', 'address', 'city', 'province',
            'is_active', 'is_featured', 'average_rating', 'total_reviews'
        ]

class BusinessCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating businesses"""
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    
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
    
    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_featured_products(self, obj):
        from api.v1.serializers.products import ProductListSerializer  # Local import
        featured_products = obj.products.filter(
            status='active', 
            is_featured=True
        )[:4]
        return ProductListSerializer(featured_products, many=True, context=self.context).data