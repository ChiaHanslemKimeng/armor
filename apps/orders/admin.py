from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'sku', 'unit_price', 'total_price')


from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'tracking_number')
    readonly_fields = ('order_number', 'formatted_shipping', 'formatted_billing', 'subtotal', 'tax_amount', 'shipping_cost', 'total_amount', 'created_at', 'updated_at')
    exclude = ('shipping_address_data', 'billing_address_data')
    inlines = [OrderItemInline]

    def formatted_shipping(self, obj):
        data = obj.shipping_address_data
        if not data:
            return "-"
        return format_html(
            "<b>{}</b><br><a href='mailto:{}'>{}</a><br>Phone: {}<br>{}<br>{}, {} {}",
            data.get('full_name', ''),
            data.get('email', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('street', ''),
            data.get('city', ''),
            data.get('state', ''),
            data.get('postal_code', '')
        )
    formatted_shipping.short_description = "Shipping Address"

    def formatted_billing(self, obj):
        data = obj.billing_address_data
        if not data:
            return "-"
        return format_html(
            "<b>{}</b><br><a href='mailto:{}'>{}</a><br>Phone: {}<br>{}<br>{}, {} {}",
            data.get('full_name', ''),
            data.get('email', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('street', ''),
            data.get('city', ''),
            data.get('state', ''),
            data.get('postal_code', '')
        )
    formatted_billing.short_description = "Billing Address"
