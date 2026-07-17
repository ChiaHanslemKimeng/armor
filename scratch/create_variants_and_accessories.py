import os
import sys
import django
import decimal
import json

sys.path.append(os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_store.settings')
django.setup()

from apps.catalog.models import Product, ProductVariant, Category, ProductImage

# 1. Populate exact, unique ProductVariant entries for all 5 rifles
variants_data = {
    'BRN-EXT-SPR-005': [
        {'name': 'SAINT Victor V2 16" 5.56 NATO Complete System', 'sku': 'BRN-EXT-SPR-005-STD', 'adj': '0.00', 'desc': '100% Factory Complete • 1x 30-Rd Mag Included'},
        {'name': 'SAINT Victor V2 Armorer Tuned & Suppressor Package', 'sku': 'BRN-EXT-SPR-005-TUNED', 'adj': '150.00', 'desc': 'Polished Match Action • Optimized Gas Dwell & Buffer'},
        {'name': 'SAINT Victor V2 Patrol Kit w/ 3 Extra PMAGs & Case', 'sku': 'BRN-EXT-SPR-005-PATROL', 'adj': '350.00', 'desc': 'Includes 3 Extra PMAGs • Waterproof Vault Hard Case • Sling'}
    ],
    'BRN-EXT-COL-004': [
        {'name': 'Colt M4A1 SOCOM 16.1" Combat Heavy Barrel System', 'sku': 'BRN-EXT-COL-004-STD', 'adj': '0.00', 'desc': 'True SOCOM Heavy Contour • KAC M4 Quad Rail'},
        {'name': 'Colt M4A1 SOCOM Geissele SSA Trigger Upgraded Package', 'sku': 'BRN-EXT-COL-004-SSA', 'adj': '200.00', 'desc': 'Factory Installed Geissele SSA 2-Stage Match Trigger'},
        {'name': 'Colt M4A1 SOCOM USGI Clone-Correct Deployment Kit', 'sku': 'BRN-EXT-COL-004-USGI', 'adj': '450.00', 'desc': 'Includes Matech BUIS • 4x USGI Mags • Pelican Hard Case'}
    ],
    'BRN-EXT-DAN-003': [
        {'name': 'Daniel Defense DD5 V4 7.62x51mm Complete Combat Rifle', 'sku': 'BRN-EXT-DAN-003-STD', 'adj': '0.00', 'desc': '4-Bolt Monolithic Rail • Adjustable Gas Block'},
        {'name': 'Daniel Defense DD5 V4 Sniper Dwell & Match Bore Tuned', 'sku': 'BRN-EXT-DAN-003-SNIPER', 'adj': '250.00', 'desc': 'Master Gunsmith Polished & Suppressor Dwell Calibrated'},
        {'name': 'Daniel Defense DD5 V4 DMR Tactical Package w/ Bipod', 'sku': 'BRN-EXT-DAN-003-DMR', 'adj': '550.00', 'desc': 'Includes Atlas BT10 QD Bipod • 3x Extra SR-25 Mags • Case'}
    ],
    'BRN-EXT-SIG-002': [
        {'name': 'Sig Sauer MCX-Spear 7.62x51 Dual Charging Complete Rifle', 'sku': 'BRN-EXT-SIG-002-STD', 'adj': '0.00', 'desc': 'Dual Charging Handles • 2-Position Adjustable Gas Piston'},
        {'name': 'Sig Sauer MCX-Spear Suppressor-Optimized SLX Gas Kit', 'sku': 'BRN-EXT-SIG-002-SLX', 'adj': '250.00', 'desc': 'Factory Tuned for Sig SLX Suppressors • Custom Dwell'},
        {'name': 'Sig Sauer MCX-Spear NGSW Military Operator Kit', 'sku': 'BRN-EXT-SIG-002-NGSW', 'adj': '600.00', 'desc': 'Includes 5 Extra Factory Steel Mags • Hard Case • Bi-Pod'}
    ],
    'BRN-EXT-GEI-001': [
        {'name': 'Geissele Super Duty Mod1 16" Nanoweapon Complete Rifle', 'sku': 'BRN-EXT-GEI-001-STD', 'adj': '0.00', 'desc': 'REBCG Nanoweapon Coated • SMR MK16 M-LOK Rail'},
        {'name': 'Geissele Super Duty Mod1 SSA-E X Lightning Bow Tuned Kit', 'sku': 'BRN-EXT-GEI-001-LIGHTNING', 'adj': '200.00', 'desc': 'Ultra-Crisp 3.5 lb SSA-E X Match Trigger Assembly'},
        {'name': 'Geissele Super Duty Mod1 Complete CQB/Patrol Vault Package', 'sku': 'BRN-EXT-GEI-001-VAULT', 'adj': '500.00', 'desc': 'Includes 4x Magpul PMAGs • Geissele Single-Point Sling • Case'}
    ]
}

for sku, vlist in variants_data.items():
    try:
        p = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        continue
    p.variants.all().delete()
    for v in vlist:
        ProductVariant.objects.create(
            product=p,
            color=v['name'],
            size=v['desc'],
            sku_suffix=v['sku'],
            price_adjustment=decimal.Decimal(v['adj']),
            stock_quantity=50
        )
    print(f"Created {len(vlist)} exact variants for {p.name}")

# 2. Populate distinct compliance and finish options right inside specifications dictionary
product_finishes_and_compliance = {
    'BRN-EXT-SPR-005': {
        'finishes': ['Melonite Black Anodized (Standard)', 'Armor FDE Tactical Cerakote', 'OD Green Combat Finish'],
        'origin': 'Geneseo, Illinois (USA) - Springfield Armory Facility',
        'itar': 'Yes (Category I(a) USML Regulated)',
        'ffl': 'Required (Class 1 FFL / SOT Firearms Transfer)',
        'warranty': 'Springfield Armory Limited Lifetime Replacement Guarantee',
        'manual_title': 'SAINT Victor V2 Operator Technical Manual Rev 4.2',
        'manual_meta': '68 Pages • Springfield Armory OEM Archive • 14.2 MB',
        'ballistic_title': '5.56x45mm NATO 62gr M855 Ballistic Trajectory Table',
        'ballistic_meta': 'Doppler Radar Velocity & Drop Profile • 4.2 MB',
        'qa': [
            {'q': 'What specific bolt carrier group (BCG) and steel specifications are used in the SAINT Victor V2?', 'a': 'The SAINT Victor V2 features an M16-profile bolt carrier group machined from 9310 steel with a Melonite finish. Every bolt is High-Pressure Tested (HPT) and Magnetic Particle Inspected (MPI) to guarantee zero structural fatigue.'},
            {'q': 'How does the Springfield Armory Accu-Tite tension system improve sub-MOA accuracy?', 'a': 'The Accu-Tite tension screw is embedded directly into the lower receiver beneath the rear takedown pin. Adjusting this tension removes 100% of upper-to-lower receiver play and rattle, locking the sighting plane directly to the bore.'},
            {'q': 'Is the 16" CMV Melonite-coated barrel optimized for both 5.56 NATO and .223 Remington ammunition?', 'a': 'Yes, the barrel features a true 5.56x45mm NATO chamber with a 1:8" twist rate, allowing flawless cycling and match accuracy with grain weights ranging from 55gr .223 Rem to 77gr MK262 OTM 5.56 NATO loads.'}
        ]
    },
    'BRN-EXT-COL-004': {
        'finishes': ['MIL-SPEC Type III Hardcoat Anodized Black', 'USGI Flat Dark Earth (FDE) Cerakote', 'SOPMOD Sniper Gray'],
        'origin': 'Hartford, Connecticut (USA) - Colt Defense Facility',
        'itar': 'Yes (Category I(a) USML Combat Weapon Regulated)',
        'ffl': 'Required (Class 1 FFL / SOT Firearms Transfer)',
        'warranty': 'Colt Defense MIL-SPEC Lifetime Factory Warranty',
        'manual_title': 'Colt M4A1 USGI Technical Manual TM 9-1005-319-23&P',
        'manual_meta': '184 Pages • Colt Military Ordnance Branch • 28.4 MB',
        'ballistic_title': 'Colt M4A1 SOCOM 16.1" Combat Heavy Barrel Trajectory Data',
        'ballistic_meta': 'US Army Ballistic Research Laboratory Data Table • 6.8 MB',
        'qa': [
            {'q': 'Does the Colt M4A1 SOCOM feature the authentic M203 heavy profile contour under the handguard?', 'a': 'Yes! Unlike standard lightweight M4 barrels, this SOCOM configuration features the true heavy combat barrel profile with the M203 grenade launcher flats, providing twice the heat dissipation during high-volume strings of fire.'},
            {'q': 'Are the KAC quad rails and Matech backup iron sights (BUIS) authentic military contract hardware?', 'a': 'Yes, this model comes equipped directly from Colt with authentic drop-in Knights Armament Company (KAC) quad rails with rib guards, paired with a Matech 200-600 meter elevation-adjustable folding rear iron sight.'},
            {'q': 'What gas system and buffer assembly are installed in the Colt SOCOM?', 'a': 'It utilizes a carbine-length gas system paired with a heavy H2 buffer and a Mil-Spec 4-position receiver extension to ensure smooth extraction and ejection reliability across varied ammunition pressures.'}
        ]
    },
    'BRN-EXT-DAN-003': {
        'finishes': ['Daniel Defense Black Hardcoat Anodized', 'DD Mil-Spec+ (Brown/FDE Cerakote)', 'Cobalt Tactical Gray'],
        'origin': 'Black Creek, Georgia (USA) - Daniel Defense Armory',
        'itar': 'Yes (Category I(a) USML Precision Rifle Regulated)',
        'ffl': 'Required (Class 1 FFL / SOT Firearms Transfer)',
        'warranty': 'Daniel Defense 100% Satisfaction & Lifetime Guarantee',
        'manual_title': 'Daniel Defense DD5 V4 Armorer & Operator Manual',
        'manual_meta': '92 Pages • Daniel Defense Precision Engineering • 19.8 MB',
        'ballistic_title': '7.62x51mm NATO 175gr Sierra MatchKing Ballistic Profile',
        'ballistic_meta': 'Long Range Precision Drop & Windage Archive • 5.1 MB',
        'qa': [
            {'q': 'How does the Daniel Defense 4-Bolt Monolithic connection differ from standard barrel nuts?', 'a': 'The patented 4-bolt attachment system clamps the free-floating handguard directly to a reinforced section of the upper receiver rather than the barrel nut. This completely isolates the cold-hammer-forged barrel from handguard flex or bipod loading.'},
            {'q': 'What does the user-adjustable gas block allow when shooting with a 7.62mm suppressor?', 'a': 'The integrated two-position adjustable gas block can be switched instantly between unsuppressed ("S" setting) and suppressed ("U" setting) operation, tuning carrier speed to eliminate excess gas blowback and carbon fouling.'},
            {'q': 'Is the DLC-coated bolt carrier group compatible with standard SR-25 / DPMS pattern magazines?', 'a': 'Yes, the DD5 V4 lower receiver accepts all SR-25 and DPMS pattern magazines, including Magpul PMAG LR/SR Gen M3 magazines and metal factory steel box magazines.'}
        ]
    },
    'BRN-EXT-SIG-002': {
        'finishes': ['Coyote Tan Anodized (Factory Standard NGSW)', 'Matte Black Tactical Finish', 'OD Green Elite Cerakote'],
        'origin': 'Newington, New Hampshire (USA) - Sig Sauer Defense',
        'itar': 'Yes (Category I(a) USML NGSW Weapon System)',
        'ffl': 'Required (Class 1 FFL / SOT Firearms Transfer)',
        'warranty': 'Sig Sauer Unlimited Lifetime Weapon System Warranty',
        'manual_title': 'Sig Sauer MCX-Spear NGSW Armorer Technical Guide',
        'manual_meta': '112 Pages • Sig Sauer Defense Systems • 24.1 MB',
        'ballistic_title': '7.62x51mm & .277 Fury Dual-Caliber Ballistic Tables',
        'ballistic_meta': 'Next Generation Squad Weapon Ballistic Data • 8.4 MB',
        'qa': [
            {'q': 'Can the charging handles on the MCX-Spear be used simultaneously or interchangeably?', 'a': 'Yes, the MCX-Spear is engineered with both a traditional AR-15 rear charging handle AND a folding, non-reciprocating left-side charging handle. Operators can manipulate either handle at any time depending on prone position or optic clearance.'},
            {'q': 'Can the barrel and caliber be swapped in the field between 7.62x51 NATO and .277 Sig Fury (6.8x51mm)?', 'a': 'Yes! By loosening the two captive Torx clamping screws on the right side of the receiver, an armorer can swap the cold-hammer-forged barrel assembly in under 60 seconds without altering receiver bedding or optic zero.'},
            {'q': 'Does the short-stroke gas piston eliminate carbon build-up in the receiver?', 'a': 'Unlike direct impingement AR systems, the MCX-Spear short-stroke gas piston vents excess propellant gases at the gas block at the front of the handguard. The bolt carrier and trigger group remain completely cool and clean even after hundreds of rounds.'}
        ]
    },
    'BRN-EXT-GEI-001': {
        'finishes': ['Desert Dirt Color (DDC) Anodized', 'Luna Black Factory Finish', '40mm Green Custom Finish'],
        'origin': 'North Wales, Pennsylvania (USA) - Geissele Automatics Vault',
        'itar': 'Yes (Category I(a) USML Match Carbine Regulated)',
        'ffl': 'Required (Class 1 FFL / SOT Firearms Transfer)',
        'warranty': 'Geissele Automatics Lifetime Structural & Precision Warranty',
        'manual_title': 'Geissele Super Duty Mod1 Armorer Maintenance Manual',
        'manual_meta': '76 Pages • Geissele Engineering Laboratory • 16.5 MB',
        'ballistic_title': '5.56x45mm NATO 77gr OTM Precision Bore Ballistics',
        'ballistic_meta': 'Sub-MOA Velocity & Terminal Energy Table • 4.9 MB',
        'qa': [
            {'q': 'What makes the Geissele Nanoweapon coating on the REBCG superior to standard chrome or phosphate?', 'a': 'Nanoweapon is a Geissele proprietary solid lubricant coating developed specifically for high-stress aerospace applications. It has a surface hardness greater than diamond, creating a self-lubricating, zero-wear carrier that sheds carbon with a dry cloth.'},
            {'q': 'What is the pull weight and break definition of the factory-installed SSA-E X with Lightning Bow?', 'a': 'The SSA-E X combines the ultra-light, crisp break of the Geissele Super Semi-Automatic Enhanced trigger (3.5 lbs total: 2.3 lb 1st stage, 1.2 lb 2nd stage) with the ergonomic hybrid curved/flat Lightning Bow trigger blade.'},
            {'q': 'How does the Geissele center-aligning anti-rotation tab on the SMR MK16 rail work?', 'a': 'The Super Modular Rail (SMR) MK16 features precisely machined alignment tabs that mate directly with a matching slot in the Geissele Super Duty upper receiver. This guarantees zero axial rotation or shifting of front laser aiming devices.'}
        ]
    }
}

for sku, cdata in product_finishes_and_compliance.items():
    try:
        p = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        continue
    s_dict = {}
    if p.specifications:
        try:
            s_dict = json.loads(p.specifications)
        except Exception:
            pass
    s_dict['_dynamic_finishes'] = cdata['finishes']
    s_dict['_origin'] = cdata['origin']
    s_dict['_itar'] = cdata['itar']
    s_dict['_ffl'] = cdata['ffl']
    s_dict['_warranty'] = cdata['warranty']
    s_dict['_manual_title'] = cdata['manual_title']
    s_dict['_manual_meta'] = cdata['manual_meta']
    s_dict['_ballistic_title'] = cdata['ballistic_title']
    s_dict['_ballistic_meta'] = cdata['ballistic_meta']
    s_dict['_qa'] = cdata['qa']
    
    p.specifications = json.dumps(s_dict)
    p.save()
    print(f"Updated compliance and dynamic Q&A data for {p.name}")

# 3. Create real distinct accessory products in the database
acc_cat, _ = Category.objects.get_or_create(name='Tactical Accessories & Optics', slug='accessories')

accessories_list = [
    {
        'name': 'SureFire SOCOM556-RC2 Fast-Attach Suppressor (Black / FDE)',
        'sku': 'SF-SOCOM556-RC2',
        'price': '1199.00',
        'short_desc': 'US Special Operations Command contract suppressor featuring patented fast-attach locking collar and zero first-round flash signature.',
        'rich_desc': '<div class="p-3 bg-light rounded-3 border"><strong class="d-block text-dark font-outfit mb-1">SOCOM Contract Proven</strong><p class="small text-secondary mb-0">Engineered specifically for 5.56 NATO combat rifles, the SureFire SOCOM556-RC2 delivers superior sound reduction, minimal backpressure, and extreme durability under full-auto fire.</p></div>',
        'img': 'springfield-armory-saint-victor-v2-5-56-nato-semi-_5_handguard.jpg'
    },
    {
        'name': 'Trijicon ACOG 4x32 Dual-Illuminated Combat Riflescope (TA31F)',
        'sku': 'TRJ-ACOG-TA31F',
        'price': '1380.00',
        'short_desc': 'Battle-proven 4x32 fixed magnification optic with fiber optic and tritium dual illumination, featuring red chevron BDC reticle for 5.56 NATO.',
        'rich_desc': '<div class="p-3 bg-light rounded-3 border"><strong class="d-block text-dark font-outfit mb-1">Dual-Illuminated Tritium & Fiber Optic</strong><p class="small text-secondary mb-0">The Trijicon ACOG TA31F combines legendary durability with Bindon Aiming Concept (BAC) both-eyes-open target acquisition. Forged 7075-T6 aluminum housing.</p></div>',
        'img': 'colt-m4a1-carbine-socom-5-56x45-nato-semi-auto-rif_4_receiver.jpg'
    },
    {
        'name': 'Magpul PMAG 30 AR/M4 GEN M3 Window 5.56 NATO (3-Pack Bundle)',
        'sku': 'MAG-PMAG30-M3-3PK',
        'price': '47.85',
        'short_desc': 'Next-generation impact and crush resistant polymer magazines with MagLevel transparent windows and over-travel insertion stops.',
        'rich_desc': '<div class="p-3 bg-light rounded-3 border"><strong class="d-block text-dark font-outfit mb-1">GEN M3 Polymer Construction</strong><p class="small text-secondary mb-0">The PMAG 30 AR/M4 GEN M3 Window is a 30-round 5.56x45 NATO polymer magazine for AR15/M4 compatible weapons featuring anti-tilt follower and stainless steel spring.</p></div>',
        'img': 'geissele-automatics-llc-super-duty-mod1-5-56x45-na_1_stock.jpg'
    },
    {
        'name': 'Armor Defense Level IV Standalone Ceramic Composite Body Armor Plate (Pair)',
        'sku': 'ARM-LVL4-CERAMIC-PR',
        'price': '480.00',
        'short_desc': 'NIJ 0101.06 Certified Level IV multi-hit ceramic composite armor plates capable of stopping .30-06 AP M2 armor-piercing rounds.',
        'rich_desc': '<div class="p-3 bg-light rounded-3 border"><strong class="d-block text-dark font-outfit mb-1">NIJ Level IV Multi-Hit Protection</strong><p class="small text-secondary mb-0">Manufactured with monolithic silicon carbide composite backed by high-density UHMWPE, providing maximum ballistic protection in a lightweight 10x12 Shooters Cut.</p></div>',
        'img': 'daniel-defense-dd5-v4-7-62x51-nato-semi-auto-rifle_3_receiver.jpg'
    }
]

for acc in accessories_list:
    p_acc, created = Product.objects.get_or_create(
        sku=acc['sku'],
        defaults={
            'name': acc['name'],
            'slug': acc['sku'].lower().replace('/', '-'),
            'price': decimal.Decimal(acc['price']),
            'short_description': acc['short_desc'],
            'rich_description': acc['rich_desc'],
            'category': acc_cat,
            'is_active': True,
            'stock_quantity': 50
        }
    )
    if not created:
        p_acc.name = acc['name']
        p_acc.price = decimal.Decimal(acc['price'])
        p_acc.short_description = acc['short_desc']
        p_acc.rich_description = acc['rich_desc']
        p_acc.category = acc_cat
        p_acc.is_active = True
        p_acc.save()
        
    p_acc.images.all().delete()
    ProductImage.objects.create(
        product=p_acc,
        image=f"catalog/products/gallery/{acc['img']}",
        is_primary=True,
        sort_order=1
    )
    print(f"Verified accessory record: {p_acc.name} ({p_acc.sku})")

print("All variants, dynamic specifications, and accessories created successfully!")
