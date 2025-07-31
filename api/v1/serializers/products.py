from rest_framework import serializers
from api.v1.serializers.businesses import BusinessListSerializer
from apps.products.models import Product, ProductCategory, ProductImage

class ProductCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'description', 'parent', 'parent_name', 'icon', 'is_active']
        read_only_fields = ['slug']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'sort_order']

class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""
    business_name = serializers.CharField(source='business.name', read_only=True)
    business_slug = serializers.CharField(source='business.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'original_price',
            'discount_percentage', 'business_name', 'business_slug',
            'category_name', 'primary_image', 'is_featured',
            'is_in_stock', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
        return None
    
    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0

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

