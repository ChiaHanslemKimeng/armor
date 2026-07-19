from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        try:
            from apps.catalog.models import Product
            return Product.objects.filter(is_active=True)
        except Exception:
            return []

    def lastmod(self, obj):
        return getattr(obj, 'updated_at', None)

    def location(self, obj):
        return reverse('product_detail', kwargs={'slug': obj.slug})


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        try:
            from apps.catalog.models import Category
            return Category.objects.filter(is_active=True)
        except Exception:
            return []

    def location(self, obj):
        return f"/products/?category={obj.slug}"

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ['home', 'about', 'contact', 'faq', 'return_policy']

    def location(self, item):
        return reverse(item)
