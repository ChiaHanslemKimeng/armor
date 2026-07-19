import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import Schematic, SchematicPart, Product, Brand

def seed_schematics():
    brand = Brand.objects.first()
    if not brand:
        brand = Brand.objects.create(name=f'ArmoryWorks {uuid.uuid4().hex[:8]}', slug=f'armoryworks-{uuid.uuid4().hex[:8]}')

    # Create Schematic 1 (AR-15)
    sch1, created = Schematic.objects.get_or_create(
        slug='ar-15-lower-schematic',
        defaults={
            'title': 'AR-15 Lower Receiver Schematic',
            'brand': brand,
            'manufacturer_name': 'ArmoryWorks',
            'category_name': 'Rifles',
            'schematic_id_number': 'SCH-AR15-LWR-001',
            'is_active': True
        }
    )
    
    # Create Schematic 2 (Glock)
    sch2, created = Schematic.objects.get_or_create(
        slug='glock-19-schematic',
        defaults={
            'title': 'Glock 19 Gen 5 Schematic',
            'brand': brand,
            'manufacturer_name': 'Glock',
            'category_name': 'Handguns',
            'schematic_id_number': 'SCH-GLK19-001',
            'is_active': True
        }
    )
    
    products = list(Product.objects.all())
    p1 = products[0] if len(products) > 0 else None
    p2 = products[1] if len(products) > 1 else None
    
    if created:
        # AR-15 Parts
        SchematicPart.objects.create(schematic=sch1, diagram_number='1', part_name='Lower Receiver', product=p1)
        SchematicPart.objects.create(schematic=sch1, diagram_number='2', part_name='Trigger Assembly', product=p1)
        SchematicPart.objects.create(schematic=sch1, diagram_number='3', part_name='Magazine Catch', product=None)
        
        # Glock Parts
        SchematicPart.objects.create(schematic=sch2, diagram_number='1', part_name='Slide', product=p2)
        SchematicPart.objects.create(schematic=sch2, diagram_number='2', part_name='Barrel', product=p2)
        SchematicPart.objects.create(schematic=sch2, diagram_number='3', part_name='Recoil Spring', product=None)
        
    print("Schematics and parts seeded successfully.")

if __name__ == '__main__':
    seed_schematics()
