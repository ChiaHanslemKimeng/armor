from django.contrib import admin
from .models import Coupon, FlashSale, LoyaltyPoint


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'min_order_amount', 'usage_limit', 'times_used', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('is_active', 'usage_limit')
    readonly_fields = ('times_used',)
    fieldsets = (
        ('Coupon Code & Type', {
            'fields': ('code', 'discount_type', 'discount_value', 'is_active')
        }),
        ('Restrictions & Limits', {
            'fields': ('min_order_amount', 'usage_limit', 'times_used')
        }),
        ('Validity Dates', {
            'fields': ('valid_from', 'valid_to')
        }),
    )


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'start_time', 'end_time')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('products',)


@admin.register(LoyaltyPoint)
class LoyaltyPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'points_balance', 'lifetime_points', 'tier_level')
    list_filter = ('tier_level',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('lifetime_points',)
