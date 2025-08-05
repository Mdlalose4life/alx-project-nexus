from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid

User = get_user_model()

class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def total_amount(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price
        return total
    
    @property
    def businesses(self):
        """Get all businesses in this cart"""
        return set(item.product.business for item in self.items.all())

class CartItem(models.Model):
    """Individual items in a shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, help_text="Special instructions for this item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['cart', 'product']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price
    
    def save(self, *args, **kwargs):
        # Save current product price
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

class Order(models.Model):
    """Main order model"""
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    DELIVERY_METHOD = (
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    # Order identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Relationships
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    business = models.ForeignKey('businesses.Business', on_delete=models.CASCADE, related_name='orders')
    
    # Order details
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(blank=True)
    
    # Delivery information
    delivery_address = models.TextField(blank=True)
    delivery_location = models.PointField(null=True, blank=True)
    delivery_notes = models.TextField(blank=True)
    
    # Payment
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Special instructions
    special_instructions = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['business', 'status']),
            models.Index(fields=['order_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        
        # Update status timestamps
        if self.status == 'confirmed' and not self.confirmed_at:
            self.confirmed_at = timezone.now()
        elif self.status == 'delivered' and not self.delivered_at:
            self.delivered_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        
        while True:
            # Format: ORD-YYYYMMDD-XXXX (e.g., ORD-20250804-A1B2)
            date_part = timezone.now().strftime('%Y%m%d')
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            order_number = f"ORD-{date_part}-{random_part}"
            
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

class OrderItem(models.Model):
    """Items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    
    # Product snapshot (in case product details change)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        
        # Save product snapshot
        if not self.product_name:
            self.product_name = self.product.name
            self.product_description = self.product.description
            
        super().save(*args, **kwargs)

class OrderStatusHistory(models.Model):
    """Track order status changes"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Order Status Histories"
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"

class DeliveryInfo(models.Model):
    """Detailed delivery information"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_info')
    driver_name = models.CharField(max_length=200, blank=True)
    driver_phone = models.CharField(max_length=15, blank=True)
    vehicle_info = models.CharField(max_length=100, blank=True)
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)
    delivery_photo = models.ImageField(upload_to='delivery_photos/', null=True, blank=True)
    customer_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    delivery_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery for {self.order.order_number}"

class OrderRating(models.Model):
    """Customer ratings and reviews for orders"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    
    # Ratings (1-5 stars)
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    food_quality = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    delivery_speed = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    customer_service = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    
    # Review
    review_text = models.TextField(blank=True)
    
    # Flags
    is_public = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)  # Since it's from actual order
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.overall_rating}⭐ - {self.order.order_number}"

# Custom managers
class OrderQuerySet(models.QuerySet):
    def for_customer(self, user):
        return self.filter(customer=user)
    
    def for_business(self, business):
        return self.filter(business=business)
    
    def active(self):
        return self.exclude(status__in=['cancelled', 'refunded'])
    
    def completed(self):
        return self.filter(status='completed')
    
    def pending(self):
        return self.filter(status='pending')

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)
    
    def for_customer(self, user):
        return self.get_queryset().for_customer(user)
    
    def for_business(self, business):
        return self.get_queryset().for_business(business)
    
    def active(self):
        return self.get_queryset().active()
    
    def completed(self):
        return self.get_queryset().completed()
    
    def pending(self):
        return self.get_queryset().pending()

# Add custom manager to Order model
Order.add_to_class('objects', OrderManager())
