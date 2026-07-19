from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from apps.core.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap
from apps.core.views import robots_txt_view

sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.core.api_urls')),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('robot.txt', robots_txt_view),  # Alias for common typo
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('return-policy/', TemplateView.as_view(template_name='pages/return_policy.html'), name='return_policy'),
    path('', include('apps.catalog.urls')),
    path('users/', include('apps.users.urls')),
    path('orders/', include('apps.orders.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('promotions/', include('apps.promotions.urls')),
    path('marketing/', include('apps.marketing.urls')),
    path('reviews/', include('apps.reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
