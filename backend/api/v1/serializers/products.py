from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from api.v1.serializers.businesses import BusinessListSerializer
from apps.products.models import Product, ProductCategory, ProductImage
from rest_framework import serializers
from cloudinary import CloudinaryImage


class ProductCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'description', 'parent', 'parent_name', 'icon', 'is_active']
        read_only_fields = ['slug']


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'thumbnail_url', 'alt_text', 'is_primary', 'sort_order']
    
    def get_cloudinary_public_id(self, obj):
        """Extracts the correct public_id from Cloudinary storage"""
        if not obj.image:
            return None
        
        public_id = str(obj.image)
        if '/upload/' in public_id:
            public_id = public_id.split('/upload/')[-1]
        public_id = public_id.split('/v1/')[-1]  # Remove version if present
        return public_id
    
    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_image_url(self, obj):
        """Get optimized image URL"""
        public_id = self.get_cloudinary_public_id(obj)
        if public_id:
            return CloudinaryImage(public_id).build_url(
                width=800,
                height=600,
                crop='limit',
                quality='auto',
                fetch_format='auto'
            )
        return None
    
    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_thumbnail_url(self, obj):
        """Get thumbnail URL"""
        public_id = self.get_cloudinary_public_id(obj)
        if public_id:
            return CloudinaryImage(public_id).build_url(
                width=300,
                height=300,
                crop='fill',
                gravity='center',
                quality='auto',
                fetch_format='auto'
            )
        return None
class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""
    business_name = serializers.CharField(source='business.name', read_only=True)
    business_slug = serializers.CharField(source='business.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'original_price',
            'discount_percentage', 'business_name', 'business_slug',
            'category_name', 'primary_image', 'is_featured',
            'is_in_stock', 'created_at'
        ]
    
    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image and primary_image.image:
            public_id = str(primary_image.image)
            if '/upload/' in public_id:
                public_id = public_id.split('/upload/')[-1]
            public_id = public_id.split('/v1/')[-1]
            
            return CloudinaryImage(public_id).build_url(
                width=300,
                height=300,
                crop='fill',
                quality='auto',
                fetch_format='auto'
            )
        return None
    
    @extend_schema_field(serializers.IntegerField())
    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0
    
    @extend_schema_field(serializers.BooleanField())
    def get_is_in_stock(self, obj):
        # Check if the product has the is_in_stock property/method
        if hasattr(obj, 'is_in_stock'):
            return obj.is_in_stock
        # Fallback to checking stock_quantity if available
        if hasattr(obj, 'stock_quantity'):
            return obj.stock_quantity > 0
        # Default to True if no stock tracking
        return True

class ProductDetailSerializer(serializers.ModelSerializer):
    """Full product details"""
    business = serializers.StringRelatedField(read_only=True)
    business_slug = serializers.CharField(source='business.slug', read_only=True)
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'business', 'business_slug', 'name', 'slug', 'description',
            'category', 'price', 'original_price', 'discount_percentage',
            'stock_quantity', 'low_stock_threshold', 'track_inventory',
            'sku', 'weight', 'dimensions', 'status', 'is_featured',
            'meta_title', 'meta_description', 'images',
            'is_in_stock', 'is_low_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'business', 'business_slug', 'slug', 'sku',
            'is_in_stock', 'is_low_stock', 'created_at', 'updated_at'
        ]
    
    @extend_schema_field(serializers.IntegerField())
    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0

class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating products"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'price', 'original_price',
            'stock_quantity', 'low_stock_threshold', 'track_inventory',
            'weight', 'dimensions', 'status', 'is_featured',
            'meta_title', 'meta_description'
        ]
    
    def create(self, validated_data):
        # Get business from URL or context
        business_id = self.context['view'].kwargs.get('business_pk')
        if business_id:
            from apps.businesses.models import Business
            validated_data['business'] = Business.objects.get(pk=business_id)
        else:
            # Fallback to user's first business
            validated_data['business'] = self.context['request'].user.businesses.first()
        
        return super().create(validated_data)