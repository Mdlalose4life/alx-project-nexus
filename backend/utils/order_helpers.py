from decimal import Decimal
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point

class OrderCalculationService:
    """
    Service class for order-related calculations
    """
    
    @staticmethod
    def calculate_delivery_fee(business_location, delivery_location, base_fee=Decimal('5.00')):
        """
        Calculate delivery fee based on distance
        """
        if not business_location or not delivery_location:
            return base_fee
        
        # Calculate distance in kilometers
        distance_km = business_location.distance(delivery_location) * 111
        
        if distance_km <= 5:
            return base_fee
        elif distance_km <= 10:
            return base_fee + Decimal('2.00')
        elif distance_km <= 20:
            return base_fee + Decimal('5.00')
        else:
            return base_fee + Decimal('10.00')
    
    @staticmethod
    def calculate_service_fee(subtotal, rate=Decimal('0.05')):
        """Calculate service fee as percentage of subtotal"""
        return subtotal * rate
    
    @staticmethod
    def calculate_tax(subtotal, rate=Decimal('0.15')):
        """Calculate tax as percentage of subtotal"""
        return subtotal * rate
    
    @staticmethod
    def calculate_total(subtotal, delivery_fee=None, service_fee=None, 
                       tax_amount=None, discount_amount=None):
        """Calculate total order amount"""
        total = subtotal
        
        if delivery_fee:
            total += delivery_fee
        if service_fee:
            total += service_fee
        if tax_amount:
            total += tax_amount
        if discount_amount:
            total -= discount_amount
            
        return max(total, Decimal('0.00'))  # Ensure non-negative total

class CartService:
    """
    Service class for cart-related operations
    """
    
    @staticmethod
    def merge_carts(source_cart, target_cart):
        """
        Merge items from source cart into target cart
        Used when user logs in and has items in both session and user cart
        """
        for source_item in source_cart.items.all():
            target_item, created = target_cart.items.get_or_create(
                product=source_item.product,
                defaults={
                    'quantity': source_item.quantity,
                    'notes': source_item.notes
                }
            )
            
            if not created:
                # If item already exists, add quantities
                target_item.quantity += source_item.quantity
                target_item.save()
        
        # Clear source cart
        source_cart.items.all().delete()
    
    @staticmethod
    def validate_cart_for_checkout(cart, business_id):
        """
        Validate cart items before checkout
        Returns tuple (is_valid, errors_list)
        """
        errors = []
        business_items = cart.items.filter(product__business_id=business_id)
        
        if not business_items.exists():
            errors.append("No items found for the specified business")
            return False, errors
        
        for item in business_items:
            # Check if product is still active
            if item.product.status != 'active':
                errors.append(f"{item.product.name} is no longer available")
            
            # Check stock if tracking inventory
            if item.product.track_inventory and not item.product.is_in_stock:
                errors.append(f"{item.product.name} is out of stock")
            
            # Check if quantity is still valid
            if (item.product.track_inventory and 
                item.quantity > item.product.stock_quantity):
                errors.append(
                    f"Only {item.product.stock_quantity} units of "
                    f"{item.product.name} available"
                )
        
        return len(errors) == 0, errors
