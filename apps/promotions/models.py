from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel, TimeStampedModel, SEOModel


class Coupon(UUIDModel, TimeStampedModel):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage Off'),
        ('fixed', 'Fixed Amount Off ($)'),
        ('free_shipping', 'Free Priority Shipping'),
    ]

    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=100)
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_value} {self.get_discount_type_display()})"


class FlashSale(UUIDModel, TimeStampedModel, SEOModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    banner_image = models.ImageField(upload_to='promotions/flash/', null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    products = models.ManyToManyField('catalog.Product', related_name='flash_sales')
    discount_percentage = models.PositiveSmallIntegerField(default=25)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}% OFF)"


class LoyaltyPoint(UUIDModel, TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loyalty_account')
    points_balance = models.PositiveIntegerField(default=500, help_text='100 points = $10 Store Credit')
    lifetime_points = models.PositiveIntegerField(default=500)
    tier_level = models.CharField(max_length=50, default='Gold Tier Customer')

    def __str__(self):
        return f"{self.user.email} - {self.points_balance} pts ({self.tier_level})"
