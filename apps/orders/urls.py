from django.urls import path
from django.shortcuts import redirect
from .views import cart_view, cart_add_view, cart_remove_view, cart_update_view, checkout_view, order_tracking_view, invoice_pdf_view, apply_coupon_view, remove_coupon_view

urlpatterns = [
    path('history/', lambda r: redirect('/dashboard/#order-history'), name='order_history'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/', cart_add_view, name='cart_add'),
    path('cart/add/<str:product_id>/', cart_add_view, name='cart_add_by_id'),
    path('cart/add/<str:sku>/', cart_add_view, name='cart_add_by_sku'),
    path('cart/remove/<str:item_id>/', cart_remove_view, name='cart_remove'),
    path('cart/update/<str:item_id>/', cart_update_view, name='cart_update'),
    path('cart/apply-coupon/', apply_coupon_view, name='cart_apply_coupon'),
    path('cart/apply-coupon/<str:code>/', apply_coupon_view, name='cart_apply_coupon_code'),
    path('cart/remove-coupon/', remove_coupon_view, name='cart_remove_coupon'),
    path('checkout/', checkout_view, name='checkout'),
    path('track/<str:order_number>/', order_tracking_view, name='order_tracking'),
    path('invoice/<str:order_number>/', invoice_pdf_view, name='order_invoice'),
]
