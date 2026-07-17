import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import Category, Product, ProductImage

try:
    bad_cat = Category.objects.get(slug='scraped-products')
    good_cat = Category.objects.get(slug='rifles')
    Product.objects.filter(category=bad_cat).update(category=good_cat)
    bad_cat.delete()
    print("Deleted Scraped Products category and moved products.")
except Exception as e:
    print("Error moving categories:", e)

# Delete bad images
bad_imgs = ProductImage.objects.filter(image__icontains='privacyoptions')
count = bad_imgs.count()
bad_imgs.delete()
print(f"Deleted {count} privacyoptions images")

bad_imgs2 = ProductImage.objects.filter(image__icontains='icons')
count2 = bad_imgs2.count()
bad_imgs2.delete()
print(f"Deleted {count2} icon images")
