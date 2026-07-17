from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Brand, Product, ProductImage, ProductVariant, ProductBundle, Schematic, SchematicPart, ScraperTask
from .tasks import execute_scraper_task

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'brand', 'get_categories', 'price', 'stock_quantity', 'is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'brand', 'categories')
    search_fields = ('name', 'sku', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('rating_average', 'reviews_count')
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(ProductBundle)
class ProductBundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'bundle_price', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('products',)


class SchematicPartInline(admin.TabularInline):
    model = SchematicPart
    extra = 1

@admin.register(Schematic)
class SchematicAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'schematic_id_number', 'is_active')
    list_filter = ('is_active', 'brand')
    search_fields = ('title', 'schematic_id_number')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SchematicPartInline]

from django.urls import path
from django.http import JsonResponse

@admin.register(ScraperTask)
class ScraperTaskAdmin(admin.ModelAdmin):
    list_display = ('from_url', 'to_url', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('status', 'logs')
    search_fields = ('from_url', 'to_url')
    
    class Media:
        js = ('js/scraper_terminal.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/live_logs/', self.admin_site.admin_view(self.live_logs_view), name='scraper_task_live_logs'),
        ]
        return custom_urls + urls

    def live_logs_view(self, request, object_id):
        task = self.get_object(request, object_id)
        if not task:
            return JsonResponse({'error': 'Task not found'}, status=404)
        return JsonResponse({'logs': task.logs, 'status': task.status})
    
    fieldsets = (
        ('Scraper Configuration', {
            'fields': ('from_url', 'to_url'),
            'description': 'Configure the crawler to extract catalog products automatically.'
        }),
        ('Status & Output', {
            'fields': ('status', 'logs'),
            'classes': ('collapse',),
            'description': 'Live terminal logs will stream here while the task runs.'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == 'pending':
            from django.db import transaction
            import threading
            def start_thread():
                thread = threading.Thread(target=execute_scraper_task, args=(obj.id,))
                thread.daemon = True
                thread.start()
            transaction.on_commit(start_thread)
