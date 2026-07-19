import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from django.contrib.auth import get_user_model
import random

User = get_user_model()
from apps.catalog.models import Product, Category, Brand
from apps.reviews.models import ProductReview, QuestionAnswer

user, _ = User.objects.get_or_create(email='reviewer@glocksandarmor.com', defaults={'first_name': 'Tactical', 'last_name': 'Reviewer', 'is_active': True, 'username': 'reviewer'})
admin_user, _ = User.objects.get_or_create(email='admin@glocksandarmor.com', defaults={'first_name': 'Admin', 'is_superuser': True, 'is_staff': True, 'username': 'admin'})

products = list(Product.objects.all())

if not products:
    print("No products found in DB. Creating dummy products...")
    slug_suffix = str(uuid.uuid4())[:8]
    category = Category.objects.create(name=f'Rifles {slug_suffix}', slug=f'rifles-{slug_suffix}')
    brand = Brand.objects.create(name=f'ArmoryWorks {slug_suffix}', slug=f'armoryworks-{slug_suffix}')
    
    p1 = Product.objects.create(name='Tactical AR-15 Base', slug='tactical-ar15-base', brand=brand, price=799.99, sku='AR15-BASE-01')
    p1.categories.add(category)
    p2 = Product.objects.create(name='Glock 19 Gen 5', slug='glock-19-gen-5', brand=brand, price=599.99, sku='GLK-19-G5')
    p2.categories.add(category)
    p3 = Product.objects.create(name='Level IV Ceramic Plate', slug='level-iv-plate', brand=brand, price=199.99, sku='ARMOR-L4-01')
    p3.categories.add(category)
    
    products = [p1, p2, p3]

review_data = [
    ("Exceptional Quality", "This is exactly what I was looking for. Machining is flawless, fits perfectly. Highly recommend Glocks And Armor for fast shipping.", 5),
    ("Solid Performer", "Good price for the quality. Has held up well after 500 rounds. No issues.", 4),
    ("Best in class", "I've tried multiple brands and this is by far the most reliable setup I've owned. Customer service was also top notch.", 5),
    ("Decent but could be better", "It works as advertised, but the finish was a bit rough on the edges. Overall satisfactory.", 3),
    ("Absolute Tank", "Ran this through the mud and it didn't skip a beat. Worth every penny.", 5)
]

qa_data = [
    ("Does this require an FFL to ship?", "Yes, this item is a serialized firearm/receiver and must be shipped to a valid FFL dealer."),
    ("Is this compatible with mil-spec parts?", "Yes, it is 100% mil-spec compatible out of the box."),
    ("What is the warranty on this?", "This product carries a lifetime manufacturer defect warranty through Glocks And Armor."),
    ("Will this run steel case ammo?", "While it can run steel case, we highly recommend brass for longevity and reliability."),
    ("Does it come with a magazine?", "Yes, one 30-round magazine is included in the box where state laws permit.")
]

reviews_created = 0
qa_created = 0

for product in products:
    num_reviews = random.randint(1, 3)
    samples = random.sample(review_data, num_reviews)
    for title, comment, rating in samples:
        review, created = ProductReview.objects.get_or_create(
            product=product,
            user=user,
            title=title,
            comment=comment,
            defaults={'rating': rating, 'helpful_votes': random.randint(0, 15)}
        )
        if created:
            reviews_created += 1

    num_qa = random.randint(1, 2)
    qa_samples = random.sample(qa_data, num_qa)
    for q, a in qa_samples:
        qa, created = QuestionAnswer.objects.get_or_create(
            product=product,
            question_text=q,
            defaults={'answer_text': a, 'user': user, 'answered_by': admin_user}
        )
        if created:
            qa_created += 1

print(f"Successfully seeded {reviews_created} new reviews and {qa_created} new FAQs across {len(products)} products.")
