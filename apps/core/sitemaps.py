from django.contrib.sitemaps import Sitemap


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


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        try:
            from apps.catalog.models import Category
            return Category.objects.filter(is_active=True)
        except Exception:
            return []
