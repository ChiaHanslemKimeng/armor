from django.urls import path
from .views import subscribe_newsletter_view

urlpatterns = [
    path('subscribe/', subscribe_newsletter_view, name='api_newsletter_subscribe'),
]
