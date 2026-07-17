from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def robots_txt_view(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /users/wishlist/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def autocomplete_search_view(request):
    """
    HTMX endpoint returning live search suggestions as HTML cards or list items.
    """
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return HttpResponse("")

    results = []
    try:
        from apps.catalog.models import Product
        qs = Product.objects.filter(name__icontains=query, is_active=True)[:5]
        for p in qs:
            results.append({
                'name': p.name,
                'slug': p.slug,
                'price': str(p.price),
                'sku': p.sku,
            })
    except Exception:
        # Fallback sample response if DB not populated yet
        results = [
            {'name': f"Armor {query.title()} Blade Server Tier 1", 'slug': 'armor-blade-server', 'price': '4,850.00', 'sku': 'ARM-SRV-01'},
            {'name': f"Quantum {query.title()} Core Module", 'slug': 'quantum-core-module', 'price': '1,250.00', 'sku': 'QNT-MOD-09'},
        ]

    html = '<div class="list-group list-group-flush border-0">'
    for r in results:
        html += f'''
        <a href="/?product={r["slug"]}" class="list-group-item list-group-item-action bg-transparent border-glass py-3 d-flex justify-content-between align-items-center">
            <div>
                <h6 class="mb-0 fw-bold">{r["name"]}</h6>
                <small class="text-muted">SKU: {r["sku"]}</small>
            </div>
            <span class="badge bg-primary bg-opacity-10 text-primary fw-bold">${r["price"]}</span>
        </a>
        '''
    html += '</div>'
    return HttpResponse(html)
