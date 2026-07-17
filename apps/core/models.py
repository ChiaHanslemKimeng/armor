import uuid
from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    """An abstract base class model that provides self-updating created and modified fields."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """An abstract base class model that makes primary key UUIDv4."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """An abstract base class providing SEO fields for public entities."""
    meta_title = models.CharField(max_length=255, blank=True, help_text='SEO Title tag (60 chars max recommended)')
    meta_description = models.TextField(blank=True, help_text='SEO Meta description (160 chars max recommended)')
    og_image_url = models.URLField(max_length=500, blank=True, help_text='OpenGraph image URL')

    class Meta:
        abstract = True


class AuditLog(TimeStampedModel):
    """Records critical security events, admin actions, and transactions across the enterprise platform."""
    ACTION_TYPES = [
        ('LOGIN_SUCCESS', 'Login Success'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('2FA_VERIFIED', '2FA Verified'),
        ('ORDER_PLACED', 'Order Placed'),
        ('INVENTORY_ALERT', 'Inventory Alert'),
        ('SECURITY_VIOLATION', 'Security Violation'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_TYPES, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Enterprise Audit Log'
        verbose_name_plural = 'Enterprise Audit Logs'

    def __str__(self):
        return f"[{self.action}] {self.user} @ {self.created_at:%Y-%m-%d %H:%M}"
