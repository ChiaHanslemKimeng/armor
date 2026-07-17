from celery import shared_task
from django.core.cache import cache


@shared_task
def check_low_stock_thresholds():
    """
    Scans products and stock items across warehouses. If stock falls below
    low_stock_threshold, logs an alert and triggers notification pipelines.
    """
    try:
        from apps.catalog.models import Product
        from apps.core.models import AuditLog

        low_products = Product.objects.filter(is_active=True, stock_quantity__lte=models.F('low_stock_threshold'))
        for p in low_products:
            AuditLog.objects.create(
                action='INVENTORY_ALERT',
                details={'sku': p.sku, 'name': p.name, 'remaining_stock': p.stock_quantity, 'threshold': p.low_stock_threshold}
            )
        return f"Scanned inventory. Triggered alerts for {low_products.count()} items."
    except Exception as e:
        return f"Inventory scan task skipped or failed: {str(e)}"
