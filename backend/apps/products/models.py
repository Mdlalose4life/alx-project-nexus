from django.contrib.gis.db import models
from django.utils.text import slugify
from apps.businesses.models import Business
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
import uuid

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    )
    
    business = models.ForeignKey('businesses.Business', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    search_vector = SearchVectorField(null=True, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    track_inventory = models.BooleanField(default=True)
    
    # Product Details
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    
    # Status & Visibility
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS, default='active')
    is_featured = models.BooleanField(default=False)
    
    # SEO & Marketing
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['business', 'slug']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
            GinIndex(fields=['search_vector']), 
        ]
    
    def __str__(self):
        return f"{self.name} - {self.business.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        
        if not self.sku:
            self.sku = self.generate_unique_sku()
            
        super().save(*args, **kwargs)
    
    def generate_smart_slug(self):
        """More intelligent slug generation that prioritizes important words"""
        import re
        
        name = self.name.lower()
        
        # Remove common unimportant words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from'}
        words = [word for word in name.split() if word not in stop_words]
        
        # Take first few important words
        important_words = words[:6] 
        base_slug = slugify(' '.join(important_words))
        
        # Truncate if still too long
        max_base_length = 45
        if len(base_slug) > max_base_length:
            base_slug = base_slug[:max_base_length].rstrip('-')
        
        return self._make_slug_unique(base_slug)

    def generate_abbreviated_slug(self):
        """Create abbreviated slug using first letters of words"""
        words = self.name.split()
        
        if len(words) == 1:
            return slugify(self.name[:45])
        
        if len(words) > 3:
            first_word = slugify(words[0])
            abbreviations = ''.join([word[0] for word in words[1:] if word])
            base_slug = f"{first_word}-{abbreviations}".lower()
        else:
            base_slug = slugify(self.name)

        if len(base_slug) > 45:
            base_slug = base_slug[:45].rstrip('-')
        
        return self._make_slug_unique(base_slug)

    def _make_slug_unique(self, base_slug):
        """Helper method to ensure slug uniqueness"""
        slug = base_slug
        counter = 1
        
        while Product.objects.filter(business=self.business, slug=slug).exclude(pk=self.pk).exists():
            suffix = f"-{counter}"
            available_length = 50 - len(suffix)
            adjusted_base = base_slug[:available_length].rstrip('-')
            slug = f"{adjusted_base}{suffix}"
            counter += 1
            
        return slug

    def generate_unique_slug(self):
        """Generate a unique slug with multiple fallback strategies"""
        
        # Strategy 1: Smart slug generation
        try:
            return self.generate_smart_slug()
        except:
            pass
        
        # Strategy 2: Try abbreviated slug
        try:
            return self.generate_abbreviated_slug()
        except:
            pass
        
        # Strategy 3: Fallback to simple truncation (current approach)
        base_slug = slugify(self.name) or 'product'
        max_base_length = 45
        if len(base_slug) > max_base_length:
            base_slug = base_slug[:max_base_length].rstrip('-')
        
        return self._make_slug_unique(base_slug)
    
    def generate_unique_sku(self):
        """Generate a unique SKU for the product"""
        # Create SKU based on business name and product name
        business_prefix = slugify(self.business.name)[:3].upper()
        product_prefix = slugify(self.name)[:3].upper()
        
        # Add random suffix to ensure uniqueness
        random_suffix = str(uuid.uuid4())[:8].upper()
        sku = f"{business_prefix}-{product_prefix}-{random_suffix}"
        
        # Ensure uniqueness (though uuid should make collisions extremely rare)
        while Product.objects.filter(sku=sku).exclude(pk=self.pk).exists():
            random_suffix = str(uuid.uuid4())[:8].upper()
            sku = f"{business_prefix}-{product_prefix}-{random_suffix}"
            
        return sku
    
    @property
    def is_in_stock(self):
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        if not self.track_inventory:
            return False
        return self.stock_quantity <= self.low_stock_threshold

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.product.name} - Image"