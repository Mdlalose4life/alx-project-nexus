from django.contrib.gis.db import models  # For PointField
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.contrib.gis.db import models


User = get_user_model()

class BusinessCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True) 
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Business Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Business(models.Model):
    # Constants
    VERIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    BUSINESS_TYPES = (
        ('spaza_shop', 'Spaza Shop'),
        ('restaurant', 'Restaurant'),
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion & Beauty'),
        ('services', 'Services'),
        ('grocery', 'Grocery Store'),
        ('other', 'Other'),
    )

    # Core Fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES)
    category = models.ForeignKey('BusinessCategory', on_delete=models.SET_NULL, null=True)

    # Contact Info
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)

    # Location Info
    location = models.PointField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True)

    # Business Identity
    registration_number = models.CharField(max_length=50, blank=True)
    tax_number = models.CharField(max_length=50, blank=True)

    # Status & Flags
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Operating Hours
    opens_at = models.TimeField(null=True, blank=True)
    closes_at = models.TimeField(null=True, blank=True)

    # Media
    logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='business_covers/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
        indexes = [
        models.Index(fields=['slug']),
        models.Index(fields=['category']),
        models.Index(fields=['business_type']),
        models.Index(fields=['city']),
        models.Index(fields=['province']),
        models.Index(fields=['owner']),
        models.Index(fields=['is_active']),
        models.Index(fields=['is_featured']),
        models.Index(fields=['created_at']),
    ]
        
    @property
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
    
    @property  
    def total_reviews(self):
        return self.reviews.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generate a smart and unique slug using multiple fallback strategies.
        """
        return self._generate_slug_strategy()

    def _generate_slug_strategy(self):
        """
        Strategy 3 (with fallback):
        Try combinations of name, city, business type, and fallback to random suffix.
        """
        base_slug = slugify(self.name)

        if not Business.objects.filter(slug=base_slug).exists():
            return base_slug

        city_slug = f"{base_slug}-{slugify(self.city)}"
        if not Business.objects.filter(slug=city_slug).exists():
            return city_slug

        type_slug = f"{base_slug}-{slugify(self.get_business_type_display())}"
        if not Business.objects.filter(slug=type_slug).exists():
            return type_slug

        # Final fallback with random suffix
        return f"{base_slug}-{get_random_string(6).lower()}"

    def _ensure_unique_slug(self, base_slug):
        """
        Ensure slug is unique by appending incrementing numbers.
        E.g., mama-sarahs, mama-sarahs-2, mama-sarahs-3
        """
        slug = base_slug
        counter = 2

        while Business.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'id']
        



class BusinessQuerySet(models.QuerySet):
    def with_stats(self):
        """Annotate businesses with review statistics"""
        return self.annotate(
            average_rating=models.Avg('reviews__rating', default=0.0),
            total_reviews=models.Count('reviews', distinct=True)
        )

class BusinessManager(models.Manager):
    def get_queryset(self):
        return BusinessQuerySet(self.model, using=self._db).with_stats()
    
    def with_stats(self):
        return self.get_queryset().with_stats()