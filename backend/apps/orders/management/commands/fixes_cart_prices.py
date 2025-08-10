
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.orders.models import CartItem
from decimal import Decimal

class Command(BaseCommand):
    help = 'Fix cart items with None unit_price'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Find cart items with None unit_price
            problem_items = CartItem.objects.filter(unit_price__isnull=True)
            
            self.stdout.write(f"Found {problem_items.count()} cart items with None unit_price")
            
            fixed_count = 0
            removed_count = 0
            
            for item in problem_items:
                try:
                    if item.product.price is not None:
                        # Fix the price
                        item.unit_price = item.product.price
                        item.save()
                        fixed_count += 1
                        self.stdout.write(f"Fixed item {item.id}: {item.product.name} - ${item.unit_price}")
                    else:
                        # Product has no price, remove the cart item or set to 0
                        self.stdout.write(f"Product {item.product.name} has no price. Removing cart item {item.id}")
                        item.delete()
                        removed_count += 1
                except Exception as e:
                    self.stdout.write(f"Error processing item {item.id}: {e}")
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed {fixed_count} items, removed {removed_count} items"
                )
            )