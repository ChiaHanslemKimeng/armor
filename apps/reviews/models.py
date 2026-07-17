from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel, TimeStampedModel


class ProductReview(UUIDModel, TimeStampedModel):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5, help_text='1 to 5 Stars')
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_buyer = models.BooleanField(default=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}* by {self.user.email} on {self.product.sku}"


class QuestionAnswer(UUIDModel, TimeStampedModel):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True)
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers_given')
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Q: {self.question_text[:50]}..."
