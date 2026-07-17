from django.db import models
from apps.core.models import UUIDModel, TimeStampedModel


class Warehouse(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True, help_text='e.g. US-EAST-01')
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='United States')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Supplier(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    lead_time_days = models.PositiveSmallIntegerField(default=14)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StockItem(UUIDModel, TimeStampedModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='stock_items')
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.CASCADE, null=True, blank=True, related_name='stock_items')
    
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    
    bin_location = models.CharField(max_length=50, blank=True, help_text='Aisle-Rack-Shelf')
    barcode_ean = models.CharField(max_length=30, unique=True, null=True, blank=True)

    class Meta:
        unique_together = ['warehouse', 'product', 'variant']

    @property
    def available_quantity(self):
        return max(0, self.quantity_on_hand - self.quantity_reserved)

    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.code}: {self.available_quantity} available"


class PurchaseOrder(UUIDModel, TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft PO'),
        ('submitted', 'Submitted to Supplier'),
        ('in_transit', 'In Transit'),
        ('received', 'Fully Received'),
        ('cancelled', 'Cancelled'),
    ]

    po_number = models.CharField(max_length=100, unique=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='purchase_orders')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    expected_delivery_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.po_number} [{self.get_status_display()}]"


class PurchaseOrderItem(UUIDModel):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT)
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity_ordered}x {self.product.sku} for {self.po.po_number}"
