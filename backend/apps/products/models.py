from django.contrib.gis.db import models
from apps.businesses.models import Business
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

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
    slug = models.SlugField()
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