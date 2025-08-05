from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from .models import Product
import logging

logger = logging.getLogger(__name__)

# Signal for auto-generating SKUs
@receiver(pre_save, sender=Product)
def generate_product_sku(sender, instance, **kwargs):
    """
    Auto-generates SKU if not provided using format:
    BUS-<business_id>-<category_initials>-<random_chars>
    """
    if not instance.sku:
        try:
            # Get category initials or default
            category_initials = ''.join(
                [word[0].upper() for word in instance.category.name.split()[:3]]
            ) if instance.category else 'GEN'
            
            # Generate random suffix
            random_suffix = get_random_string(4).upper()
            
            # Format the SKU
            instance.sku = f"BUS-{instance.business.id}-{category_initials}-{random_suffix}"
            
        except Exception as e:
            logger.error(f"Failed to generate SKU: {e}")
            # Fallback to simple random SKU
            instance.sku = f"PROD-{get_random_string(8).upper()}"

# Signal for low stock notifications
@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, created, **kwargs):
    """
    Sends notification when product stock falls below threshold
    """
    if not created and instance.track_inventory and instance.is_low_stock:
        try:
            # Get previous stock quantity from original instance if available
            original_stock = None
            if hasattr(instance, '_pre_save_instance'):
                original_stock = instance._pre_save_instance.stock_quantity
            
            # Only notify if stock just crossed the threshold
            if original_stock is None or original_stock > instance.low_stock_threshold:
                subject = f"Low Stock Alert: {instance.name}"
                message = (
                    f"Product: {instance.name}\n"
                    f"Current Stock: {instance.stock_quantity}\n"
                    f"Threshold: {instance.low_stock_threshold}\n"
                    f"Business: {instance.business.name}\n\n"
                    f"Please consider restocking soon."
                )
                
                # Send to business owner
                recipient_email = instance.business.owner.email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    fail_silently=False
                )
                
                logger.info(f"Low stock notification sent for {instance.name}")
                
        except Exception as e:
            logger.error(f"Failed to send low stock notification: {e}")

# Signal for search index updates
@receiver(post_save, sender=Product)
def update_search_index(sender, instance, **kwargs):
    """
    Updates search index when product changes
    """
    try:
        # Example using Django's built-in search (adjust for your search backend)
        from django.contrib.postgres.search import SearchVector
        from django.contrib.postgres.indexes import GinIndex
        
        # Update search vector if using PostgreSQL
        Product.objects.filter(pk=instance.pk).update(
            search_vector=(
                SearchVector('name', weight='A') +
                SearchVector('description', weight='B') +
                SearchVector('category__name', weight='B')
            )
        )
        
        # Alternative for other search backends like Elasticsearch
        # from search.utils import update_product_index
        # update_product_index(instance)
        
        logger.debug(f"Search index updated for product {instance.pk}")
        
    except Exception as e:
        logger.error(f"Failed to update search index: {e}")