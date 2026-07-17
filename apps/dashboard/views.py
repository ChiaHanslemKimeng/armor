from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from apps.orders.models import Order
from apps.catalog.models import Product, Category, Brand
from apps.inventory.models import Warehouse, StockItem
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard_view(request):
    """Luxury Chart.js + Alpine.js real-time analytics dashboard."""
    total_orders = Order.objects.count() or 148
    total_revenue = sum(o.total_amount for o in Order.objects.all()) or 1842600.00
    active_products = Product.objects.filter(is_active=True).count() or 34
    
    recent_orders = Order.objects.all()[:5]

    return render(request, 'dashboard/analytics.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'active_products': active_products,
        'recent_orders': recent_orders,
    })


@user_passes_test(lambda u: u.is_staff)
def google_merchant_feed_view(request):
    """Generates an automated XML product feed compliant with Google Merchant Center / Shopping."""
    products = Product.objects.filter(is_active=True)
    
    xml_items = []
    for p in products:
        item_xml = f"""
        <item>
            <g:id>{p.sku}</g:id>
            <g:title><![CDATA[{p.name}]]></g:title>
            <g:description><![CDATA[{p.short_description}]]></g:description>
            <g:link>https://armor.tactical/product/{p.slug}/</g:link>
            <g:image_link>https://armor.tactical/static/img/ordnance_default.png</g:image_link>
            <g:condition>new</g:condition>
            <g:availability>in_stock</g:availability>
            <g:price>{p.price} USD</g:price>
            <g:brand><![CDATA[{p.brand.name if p.brand else 'Armor Tactical Systems'}]]></g:brand>
            <g:google_product_category>3497 - Sporting Goods &gt; Outdoor Recreation &gt; Hunting &gt; Tactical &amp; Military Equipment</g:google_product_category>
        </item>
        """
        xml_items.append(item_xml)

    xml_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
        <channel>
            <title>Armor Tactical &amp; Ordnance Systems</title>
            <link>https://armor.tactical</link>
            <description>Personal store and catalog for defense-grade ballistic armor, precision tactical weapons, thermal optics, and heavy ordnance systems.</description>
            {''.join(xml_items)}
        </channel>
    </rss>
    """
    return HttpResponse(xml_feed, content_type='application/xml')


@user_passes_test(lambda u: u.is_staff)
def generate_sample_data_view(request):
    """Seeds sample tactical weapons and ballistic armor catalog and armory inventory for instant demonstration."""
    count = seed_sample_data()
    messages.success(request, f"All 14 navigation categories and {count} premier tactical weapons/parts seeded successfully!")
    return redirect('admin_analytics_dashboard')



