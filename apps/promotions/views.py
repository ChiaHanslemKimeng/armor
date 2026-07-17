from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FlashSale, Coupon


def flash_sale_list_view(request):
    now = timezone.now()
    active_sales = FlashSale.objects.filter(is_active=True)
    return render(request, 'promotions/list.html', {'flash_sales': active_sales, 'now': now})
