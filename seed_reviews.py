import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import Product, Category, Brand
from apps.reviews.models import ProductReview
from django.contrib.auth import get_user_model

User = get_user_model()

print("Cleaning up old reviews...")
ProductReview.objects.all().delete()

products = list(Product.objects.all()[:50])
if not products:
    print("No products found, creating a dummy product for reviews...")
    brand = Brand.objects.first()
    if not brand:
        brand = Brand.objects.create(name="Armor Tactical", slug="armor-tactical-dummy")
    category = Category.objects.first()
    if not category:
        category = Category.objects.create(name="Accessories", slug="accessories-dummy")
    
    dummy_product = Product.objects.create(
        name="Tactical Carrier Plate",
        slug="tactical-carrier-plate",
        brand=brand,
        price=199.99,
        sku="TCP-001"
    )
    dummy_product.categories.add(category)
    products = [dummy_product]

titles = [
    "Solid replacement part",
    "Fits perfect",
    "Does the job",
    "Great product",
    "Machining is slightly off",
    "Will buy again",
    "Decent for the price",
    "Works flawlessly",
    "Highly recommended",
    "Average",
    "Very high quality",
    "Exceeded expectations"
]

comments = [
    "The build quality is very solid. Fits my setup perfectly.",
    "Installed it yesterday and took it to the range. No issues so far.",
    "This is a high quality component. Very satisfied with the purchase.",
    "I had to make some minor adjustments to get it to fit, but it works now.",
    "Exactly as described. Fast shipping and good customer service.",
    "Very easy to install. Took me less than 5 minutes.",
    "I've used this brand before and they always deliver good quality.",
    "Does exactly what it's supposed to do. No complaints.",
    "Machining tolerances are tight and the finish is excellent.",
    "Reliable and durable. Have put over 500 rounds through it.",
    "I was on the fence but glad I purchased this. Good value.",
    "A reliable addition to my custom build."
]

ratings_distribution = [
    3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5
]

first_names = ["John", "Sarah", "Michael", "David", "Jessica", "Robert", "William", "James", "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian"]
last_initials = ["A.", "B.", "C.", "D.", "F.", "G.", "H.", "K.", "M.", "P.", "R.", "S.", "T.", "V.", "W."]

print("Seeding 30 reviews...")
reviews_created = []

for i in range(30):
    product = random.choice(products)
    rating = random.choice(ratings_distribution)
    title = random.choice(titles)
    comment = random.choice(comments)
    
    # Create fake user
    fake_name = f"{random.choice(first_names)} {random.choice(last_initials)}"
    fake_email = f"user_{random.randint(10000, 99999)}@example.com"
    fake_user, created = User.objects.get_or_create(email=fake_email, defaults={'first_name': fake_name})
    if not created and not fake_user.first_name:
        fake_user.first_name = fake_name
        fake_user.save()
    
    review = ProductReview.objects.create(
        product=product,
        user=fake_user,
        rating=rating,
        title=title,
        comment=comment
    )
    reviews_created.append(review)

for review in reviews_created:
    random_days = random.randint(1, 365)
    random_date = timezone.now() - timedelta(days=random_days)
    ProductReview.objects.filter(id=review.id).update(created_at=random_date)

print(f"Successfully seeded {len(reviews_created)} reviews!")
