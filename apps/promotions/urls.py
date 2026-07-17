from django.urls import path
from .views import flash_sale_list_view

urlpatterns = [
    path('', flash_sale_list_view, name='flash_sales_list'),
]
