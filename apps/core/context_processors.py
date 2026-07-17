from decimal import Decimal
from django.conf import settings
from apps.orders.models import CartItem


def global_settings_context(request):
    """Provides global enterprise settings, active currency, SEO defaults, and cart data across templates."""
    cart_items = []
    cart_count = 0
    cart_subtotal = Decimal('0.00')
    coupon_discount = Decimal('0.00')
    cart_total = Decimal('0.00')
    applied_coupon = None
    try:
        if request.user.is_authenticated:
            if request.session.session_key:
                CartItem.objects.filter(session_key=request.session.session_key, user__isnull=True).update(user=request.user)
            cart_items = list(CartItem.objects.filter(user=request.user).select_related('product'))
        elif request.session.session_key:
            cart_items = list(CartItem.objects.filter(session_key=request.session.session_key).select_related('product'))
        cart_count = sum(item.quantity for item in cart_items)
        cart_subtotal = round(sum(item.item_total for item in cart_items), 2)
        
        applied_coupon = request.session.get('applied_coupon')
        if applied_coupon == 'ARMOR25':
            coupon_discount = round(cart_subtotal * Decimal('0.25'), 2)
        elif applied_coupon == 'LEMIL10':
            coupon_discount = round(cart_subtotal * Decimal('0.10'), 2)
            
        discounted_subtotal = max(Decimal('0.00'), cart_subtotal - coupon_discount)
        cart_tax = round(discounted_subtotal * Decimal('0.08'), 2)
        cart_total = round(discounted_subtotal + cart_tax, 2)
    except Exception:
        pass

    return {
        'SITE_NAME': 'Armor Enterprise Systems',
        'DEFAULT_CURRENCY': 'USD ($)',
        'SUPPORT_PHONE': '+1 (800) 555-ARMOR',
        'IS_PRODUCTION': not settings.DEBUG,
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_subtotal': cart_subtotal,
        'coupon_discount': coupon_discount,
        'cart_total': cart_total,
        'applied_coupon': applied_coupon,
    }
