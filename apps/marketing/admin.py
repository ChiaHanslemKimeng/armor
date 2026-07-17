from django.contrib import admin
from .models import NewsletterSubscriber, PromotionalBanner, EmailCampaign


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)


@admin.register(PromotionalBanner)
class PromotionalBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'link_url', 'is_active', 'created_at')
    list_filter = ('position', 'is_active')
    search_fields = ('title', 'subtitle')


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('subject', 'body_html')
