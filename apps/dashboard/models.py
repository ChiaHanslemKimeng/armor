from django.db import models
from apps.core.models import UUIDModel, TimeStampedModel


class AnalyticsSnapshot(UUIDModel, TimeStampedModel):
    date = models.DateField(unique=True, db_index=True)
    daily_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    orders_count = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    low_stock_alerts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Snapshot {self.date}: ${self.daily_revenue} ({self.orders_count} orders)"
