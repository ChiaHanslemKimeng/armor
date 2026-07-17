from django.contrib import admin
from .models import ProductReview, QuestionAnswer


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_verified_buyer', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_buyer', 'is_approved', 'created_at')
    search_fields = ('product__name', 'product__sku', 'user__email', 'title', 'comment')
    actions = ['approve_reviews', 'disapprove_reviews']

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Disapprove selected reviews')
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)

