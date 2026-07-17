import random
import string
from django.db import transaction
from django.core.cache import cache


class InventoryService:
    @staticmethod
    def reserve_stock(product, quantity=1, session_id=None):
        """
        Attempts to lock and reserve inventory in real-time to prevent overselling.
        Uses Redis distributed lock via cache object or DB atomic select_for_update.
        """
        lock_key = f"lock_stock_{product.id}"
        lock_acquired = cache.add(lock_key, "LOCKED", timeout=10)

        try:
            with transaction.atomic():
                # Refresh product from DB with lock
                from apps.catalog.models import Product
                p = Product.objects.select_for_update().get(id=product.id)
                
                if p.stock_quantity >= quantity:
                    p.stock_quantity -= quantity
                    p.save(update_fields=['stock_quantity'])
                    
                    # Also update StockItem reservation if exists
                    for item in p.stock_items.all():
                        if item.available_quantity >= quantity:
                            item.quantity_reserved += quantity
                            item.save(update_fields=['quantity_reserved'])
                            break
                    return True
                return False
        finally:
            if lock_acquired:
                cache.delete(lock_key)

    @staticmethod
    def generate_sku(brand_code="ARM", cat_code="SYS"):
        random_suffix = ''.join(random.choices(string.digits, k=5))
        return f"{brand_code.upper()}-{cat_code.upper()}-{random_suffix}"

    @staticmethod
    def generate_ean13():
        prefix = "0840"  # Enterprise prefix
        body = ''.join(random.choices(string.digits, k=8))
        raw = prefix + body
        # Calculate checksum
        total = sum(int(digit) * (3 if i % 2 else 1) for i, digit in enumerate(raw))
        check = (10 - (total % 10)) % 10
        return raw + str(check)
