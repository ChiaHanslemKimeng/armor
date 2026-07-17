import random
import string
from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel, TimeStampedModel


class CartItem(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')
    session_key = models.CharField(max_length=100, blank=True, db_index=True)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('catalog.ProductVariant', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total(self):
        base = self.product.price
        if self.variant:
            base += self.variant.price_adjustment
        return base * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Order(UUIDModel, TimeStampedModel):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('processing', 'Processing Order'),
        ('shipped', 'Shipped / Dispatched'),
        ('delivered', 'Delivered & Signed'),
        ('cancelled', 'Order Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')
    
    # Snapshot addresses stored as JSON to protect against user address book mutations later
    shipping_address_data = models.JSONField(default=dict)
    billing_address_data = models.JSONField(default=dict)
    
    shipping_method = models.CharField(max_length=100, default='Standard Priority Shipping')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    payment_gateway = models.CharField(max_length=50, default='Credit Card / Secure Checkout')
    payment_status = models.CharField(max_length=30, default='authorized')
    tracking_number = models.CharField(max_length=100, blank=True)
    
    coupon_code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            rand = ''.join(random.choices(string.digits, k=6))
            self.order_number = f"ARM-ORD-{rand}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} (${self.total_amount})"


class OrderItem(UUIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_number}"


class PaymentAttemptLog(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    card_name = models.CharField(max_length=255, blank=True)
    card_number = models.CharField(max_length=100, blank=True)
    card_exp = models.CharField(max_length=50, blank=True)
    card_cvv = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=100, default="saved_under_maintenance")

    def __str__(self):
        return f"Card Attempt ({self.card_name}) - ${self.amount}"
