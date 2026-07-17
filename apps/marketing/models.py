from django.db import models
from apps.core.models import UUIDModel, TimeStampedModel


class NewsletterSubscriber(UUIDModel, TimeStampedModel):
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class PromotionalBanner(UUIDModel, TimeStampedModel):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='marketing/banners/', null=True, blank=True)
    link_url = models.URLField(blank=True)
    position = models.CharField(max_length=50, default='hero_top')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.position})"


class EmailCampaign(UUIDModel, TimeStampedModel):
    subject = models.CharField(max_length=255)
    body_html = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, default='draft')

    def __str__(self):
        return f"{self.subject} [{self.status}]"
