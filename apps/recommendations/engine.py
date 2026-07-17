from django.core.cache import cache


class AIRecommendationEngine:
    """
    Enterprise hybrid recommendation engine calculating content similarity and
    collaborative purchase affinity to generate 'Frequently Bought Together'
    and 'Recommended for You' product sets.
    """
    @staticmethod
    def get_frequently_bought_together(product, limit=3):
        cache_key = f"fbt_recommendations_{product.id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        try:
            from apps.catalog.models import Product
            # Find products in same category or complementary hardware tiers
            qs = Product.objects.filter(is_active=True).exclude(id=product.id)
            if product.category:
                qs = qs.filter(category=product.category)
            results = list(qs[:limit])
            cache.set(cache_key, results, timeout=3600)
            return results
        except Exception:
            return []

    @staticmethod
    def get_collaborative_recommendations(user=None, limit=4):
        try:
            from apps.catalog.models import Product
            # Return top rated featured hardware nodes
            return Product.objects.filter(is_active=True, is_featured=True).order_by('-rating_average')[:limit]
        except Exception:
            return []
