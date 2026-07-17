from django.contrib import admin
from .models import StockItem


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity_on_hand', 'quantity_reserved', 'available_quantity', 'bin_location')
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'product__sku', 'bin_location', 'barcode_ean')
    readonly_fields = ('available_quantity',)

