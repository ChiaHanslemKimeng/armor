import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor.settings')
django.setup()

from apps.catalog.models import Product, ProductImage

prod = Product.objects.filter(name__icontains="BXR").first()
if prod:
    print(f"Product: {prod.name}")
    for img in prod.images.all():
        print(img.image.path)
        print(f"URL: {img.image.url}")
else:
    print("BXR not found")
