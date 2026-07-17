from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import UUIDModel, TimeStampedModel, SEOModel


class Category(MPTTModel, UUIDModel, TimeStampedModel, SEOModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon_class = models.CharField(max_length=100, blank=True, default='bi-shield-check')
    image = models.ImageField(upload_to='catalog/categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Brand(UUIDModel, TimeStampedModel, SEOModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='catalog/brands/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(UUIDModel, TimeStampedModel, SEOModel):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products')
    
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    stock_quantity = models.PositiveIntegerField(default=10)
    low_stock_threshold = models.PositiveIntegerField(default=3)
    
    short_description = models.CharField(max_length=500)
    rich_description = models.TextField()
    specifications = models.JSONField(default=dict, blank=True, help_text='Key-value specifications grid')
    
    # Media & 360 Viewer Architecture
    has_360_viewer = models.BooleanField(default=False)
    video_url = models.URLField(max_length=500, blank=True)
    download_manual_url = models.URLField(max_length=500, blank=True)
    
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=4.90)
    reviews_count = models.PositiveIntegerField(default=0)
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"

    @property
    def image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary and primary.image:
            return primary.image
        first_img = self.images.first()
        return first_img.image if first_img and first_img.image else None



class ProductImage(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='catalog/products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', '-is_primary']


class ProductVariant(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku_suffix = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True, help_text='e.g. Matte Black, FDE Flat Dark Earth, OD Green')
    size = models.CharField(max_length=50, blank=True, help_text='e.g. 16" Barrel, 30-Round, Large / SAPI')
    material = models.CharField(max_length=50, blank=True, help_text='e.g. 7075-T6 Aluminum, AR500 Steel, Kevlar / PE')
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.product.name} [{self.color} - {self.size}]"


class ProductBundle(UUIDModel, TimeStampedModel, SEOModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    products = models.ManyToManyField(Product, related_name='bundles')
    bundle_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.PositiveSmallIntegerField(default=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}% OFF)"


class Schematic(UUIDModel, TimeStampedModel, SEOModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name='schematics')
    manufacturer_name = models.CharField(max_length=150, blank=True, help_text="Used if Brand object doesn't exist")
    category_name = models.CharField(max_length=150, blank=True, help_text="Grouping header under the brand, e.g. 'Rifles' or 'Handguns'")
    schematic_id_number = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='catalog/schematics/')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class SchematicPart(UUIDModel, TimeStampedModel):
    schematic = models.ForeignKey(Schematic, on_delete=models.CASCADE, related_name='parts')
    diagram_number = models.CharField(max_length=20, help_text="The number/letter on the diagram (e.g. 21, 10A)")
    part_name = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='schematic_references', help_text="Link to a store product if available")
    
    class Meta:
        ordering = ['diagram_number']

    def __str__(self):
        return f"{self.schematic.title} - #{self.diagram_number} {self.part_name}"

class TriggerTimesVideo(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500)
    category = models.CharField(max_length=100)
    date_published = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_published']
        verbose_name = "Trigger Times Video"
        verbose_name_plural = "Trigger Times Videos"

class ScraperTask(UUIDModel, TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    from_url = models.URLField(max_length=500, blank=True, help_text="The URL to start scraping from")
    to_url = models.URLField(max_length=500, blank=True, help_text="The URL to end scraping (optional)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    logs = models.TextField(blank=True, help_text="Background logs and output from the scraping process")

    def __str__(self):
        return f"Scrape Task - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Scraper Task"
        verbose_name_plural = "Scraper Tasks"
