from django.urls import path
from .views import admin_dashboard_view, google_merchant_feed_view, generate_sample_data_view

urlpatterns = [
    path('', admin_dashboard_view, name='admin_analytics_dashboard'),
    path('feed/google.xml', google_merchant_feed_view, name='google_merchant_feed'),
    path('seed/', generate_sample_data_view, name='admin_seed_sample_data'),
]
