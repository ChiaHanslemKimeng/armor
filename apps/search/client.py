import meilisearch
from django.conf import settings


class SearchEngineClient:
    """
    Enterprise search client integrating Meilisearch (primary) with fallback to
    database query search if Meilisearch container is unavailable.
    """
    def __init__(self):
        self.host = getattr(settings, 'MEILISEARCH_HOST', 'http://localhost:7700')
        self.key = getattr(settings, 'MEILISEARCH_KEY', 'masterKey')
        self._client = None

    @property
    def client(self):
        if not self._client:
            try:
                self._client = meilisearch.Client(self.host, self.key)
            except Exception:
                self._client = None
        return self._client

    def setup_index(self):
        if not self.client:
            return False
        try:
            index = self.client.index('products')
            index.update_filterable_attributes(['category', 'brand', 'price', 'is_active', 'rating_average'])
            index.update_searchable_attributes(['name', 'sku', 'short_description', 'specifications'])
            index.update_synonyms({
                'blade': ['server', 'node', 'chassis'],
                'quantum': ['neural', 'ai', 'processor'],
            })
            return True
        except Exception:
            return False

    def index_product(self, product):
        if not self.client:
            return False
        try:
            doc = {
                'id': str(product.id),
                'name': product.name,
                'slug': product.slug,
                'sku': product.sku,
                'price': float(product.price),
                'category': product.category.slug,
                'brand': product.brand.slug if product.brand else '',
                'short_description': product.short_description,
                'rating_average': float(product.rating_average),
                'is_active': product.is_active,
            }
            self.client.index('products').add_documents([doc])
            return True
        except Exception:
            return False
