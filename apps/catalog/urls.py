from django.urls import path
from .views import (
    home_view, catalog_list_view, product_detail_view,
    about_view, faq_view, contact_view,
    trigger_times_view, resources_view, deals_view, brands_view,
    gun_schematics_view, schematic_detail_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('products/', catalog_list_view, name='catalog_list'),
    path('catalog/', catalog_list_view, name='catalog_list_alt'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
    path('about/', about_view, name='about'),
    path('faq/', faq_view, name='faq'),
    path('contact/', contact_view, name='contact'),
    path('trigger-times/', trigger_times_view, name='trigger_times'),
    path('resources/', resources_view, name='resources'),
    path('gun-schematics/', gun_schematics_view, name='gun_schematics'),
    path('gun-schematics/<slug:slug>/', schematic_detail_view, name='schematic_detail'),
    path('deals/', deals_view, name='deals'),
    path('brands/', brands_view, name='brands'),
]

