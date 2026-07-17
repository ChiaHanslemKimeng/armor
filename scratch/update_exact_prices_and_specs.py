import os
import sys
import django
import json

sys.path.insert(0, r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import Product

# Exact primary prices as listed in Brownells schema data and exact specifications
data_updates = {
    'BRN-EXT-GEI-001': {
        'price': '2099.99',
        'short_description': 'Geissele Automatics Super Duty Mod1 5.56x45mm NATO 16" Cold-Hammer-Forged Barrel Rifle with SSA-E X Trigger and SMR MK16 M-LOK Rail.',
        'description': 'The Geissele Super Duty Mod 1 5.56x45mm NATO rifle represents the pinnacle of modern AR-15 manufacturing. Featuring a 16" cold-hammer-forged, chrome-lined barrel with a 1:7 twist, Geissele Reliability Enhanced Bolt Carrier Group (REBCG), and the legendary two-stage SSA-E X Lightning Bow trigger, this platform delivers unmatched reliability and sub-MOA precision under extreme field conditions.',
        'rich_description': '''
<div class="row g-4 my-2">
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Reliability Enhanced BCG (REBCG)</strong>
            <p class="small text-secondary mb-0">Machined from 8620 steel with clean room Nanoweapon coating for zero-friction operation and extreme carbon resistance.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>SSA-E X Match Trigger</strong>
            <p class="small text-secondary mb-0">Two-stage precision match trigger with Lightning Bow profile, delivering an ultra-crisp 3.5 lb total pull weight.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>SMR MK16 M-LOK Handguard</strong>
            <p class="small text-secondary mb-0">Precision machined 15" handguard with center aligning anti-rotation tabs and Geissele proprietary barrel nut.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Cold-Hammer-Forged Barrel</strong>
            <p class="small text-secondary mb-0">16" CHF chrome-lined 5.56 NATO barrel with Geissele Sparkle Night hider and mid-length gas tube.</p>
        </div>
    </div>
</div>
''',
        'specifications': json.dumps({
            'Caliber / Chambering': '5.56x45mm NATO (.223 Rem)',
            'Action Type': 'Direct Impingement Semi-Automatic (Mid-Length Gas System)',
            'Barrel Length & Profile': '16.0" Cold-Hammer-Forged, Chrome-Lined, 1:7" Twist Rate',
            'Muzzle Device & Threads': 'Geissele Sparkle Night Flash Hider (1/2x28 TPI)',
            'Trigger Mechanism': 'Geissele SSA-E X Two-Stage Match Trigger with Lightning Bow (3.5 lbs)',
            'Handguard System': '15.0" Super Modular Rail (SMR) MK16 with M-LOK Slots & Anti-Rotation Tabs',
            'Bolt Carrier Group': 'Geissele Reliability Enhanced BCG (REBCG) with Nanoweapon Coating',
            'Stock & Grip': 'B5 Systems Enhanced Sopmod Stock & B5 Type 23 P-Grip',
            'Weight & Length': '6.45 lbs Overall Weight | 33.5" - 36.75" Overall Length',
            'Factory Accuracy': 'Certified Sub-MOA Match Precision Guarantee'
        })
    },
    'BRN-EXT-SIG-002': {
        'price': '3999.99',
        'short_description': 'Sig Sauer MCX Spear 7.62x51mm NATO (.308 Win) 16" Barrel Tactical Rifle with Dual Non-Reciprocating Charging Handles and SLX Suppressor-Ready Muzzle.',
        'description': 'The SIG SAUER MCX Spear is the civilian evolution of the U.S. Army Next Generation Squad Weapon (NGSW) XM7 rifle. Engineered to harness incredible pressures while maintaining ultra-low recoil and rapid suppressor integration, the MCX Spear features dual charging handles (AR-style and left-side non-reciprocating), fully ambidextrous fire controls, a 2-position adjustable gas piston system, and a folding magpul SL-M stock.',
        'rich_description': '''
<div class="row g-4 my-2">
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Dual Charging Handle System</strong>
            <p class="small text-secondary mb-0">Features both traditional rear AR-style charging handle and a left-side non-reciprocating folding handle for rapid cycling while prone.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>2-Position Adjustable Gas Piston</strong>
            <p class="small text-secondary mb-0">Short-stroke gas piston system with toolless adjustment for seamless suppressed and unsuppressed tactical operation.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Monolithic Upper & Handguard</strong>
            <p class="small text-secondary mb-0">Free-floating M-LOK handguard reinforced for heavy optical/laser aiming devices with zero deflection under thermal load.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Ambidextrous Lower Controls</strong>
            <p class="small text-secondary mb-0">Fully ambidextrous bolt catch/release, magazine release, and 60-degree safety selector for instant adaptability.</p>
        </div>
    </div>
</div>
''',
        'specifications': json.dumps({
            'Caliber / Chambering': '7.62x51mm NATO (.308 Winchester)',
            'Action Type': 'Short-Stroke Gas Piston Semi-Automatic (2-Position Adjustable)',
            'Barrel Length & Profile': '16.0" Chrome-Moly Steel, Cold-Hammer-Forged, 1:10" Twist',
            'Muzzle Device & Threads': 'SIG SLX Suppressor-Ready QD Muzzle Brake (5/8x24 TPI)',
            'Trigger Mechanism': 'SIG Matchlite Duo 2-Stage Precision Flat-Blade Trigger (4.0 lbs)',
            'Handguard & Upper': 'Free-Floating Lightweight M-LOK Aluminum Handguard',
            'Charging Controls': 'Dual Ambidextrous Rear & Left-Side Non-Reciprocating Folding Handle',
            'Stock System': 'Push-Button 6-Position Folding / Collapsible Stock Mechanism',
            'Weight & Length': '8.60 lbs Overall Weight | 35.1" - 38.3" Overall Length',
            'MIL-SPEC Compliance': 'U.S. Army NGSW XM7 Civilian Platform Heritage'
        })
    },
    'BRN-EXT-DAN-003': {
        'price': '3007.00',
        'short_description': 'Daniel Defense DD5 V4 7.62x51mm NATO 18" Cold-Hammer-Forged Barrel Precision Semi-Automatic Rifle with User-Adjustable Gas Block.',
        'description': 'The Daniel Defense DD5 V4 7.62x51mm NATO rifle provides precision shooters and tactical operators with an 18" cold-hammer-forged barrel engineered for extreme accuracy and long-range engagement beyond 800 meters. Featuring an innovative 4-bolt connection system that firmly attaches the free-floating rail to the upper receiver without loading the barrel, alongside an adjustable gas block for suppressed shooting.',
        'rich_description': '''
<div class="row g-4 my-2">
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>4-Bolt Monolithic Rail Connection</strong>
            <p class="small text-secondary mb-0">Patented 4-bolt connection system clamps directly to the upper receiver, creating a rigid platform that never puts tension on the barrel.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>User-Adjustable Gas Block</strong>
            <p class="small text-secondary mb-0">Two-position adjustable gas block engineered specifically to optimize carrier velocity when firing suppressed vs unsuppressed.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>DLC Coated Bolt Carrier Group</strong>
            <p class="small text-secondary mb-0">Superfinished Diamond-Like Carbon (DLC) bolt carrier group with dual ejectors for flawless brass ejection and effortless cleaning.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Geissele SSA 2-Stage Trigger</strong>
            <p class="small text-secondary mb-0">Factory upgraded with Geissele Automatics Super Semi-Automatic (SSA) two-stage trigger for precise shot placement at distance.</p>
        </div>
    </div>
</div>
''',
        'specifications': json.dumps({
            'Caliber / Chambering': '7.62x51mm NATO (.308 Winchester)',
            'Action Type': 'Direct Impingement Semi-Automatic with Rifle-Length Gas System',
            'Barrel Length & Profile': '18.0" Cold-Hammer-Forged, Chrome-Lined, S2W Profile, 1:11" Twist',
            'Muzzle Device & Threads': 'Daniel Defense Superior Suppression Device (5/8x24 TPI)',
            'Trigger Mechanism': 'Geissele SSA 2-Stage Match Trigger (4.5 lbs Total Pull)',
            'Handguard System': '15.0" DD5 V4 M-LOK Free-Floating Rail with 4-Bolt Attachment',
            'Bolt Carrier Group': 'DLC-Coated Bolt Carrier Group with Dual Ejectors & Oversized Cam Pin',
            'Lower & Controls': 'Ambidextrous Safety Selector, Magazine Release & Bolt Catch',
            'Weight & Length': '8.60 lbs Overall Weight | 35.3" - 39.0" Overall Length',
            'Factory Accuracy': 'Certified Sub-MOA Long Range Interdiction Standard'
        })
    },
    'BRN-EXT-COL-004': {
        'price': '1536.70',
        'short_description': 'Colt M4A1 Carbine SOCOM 5.56x45mm NATO 16.1" Heavy Profile Barrel Rifle with Knights Armament Quad Rail and Ambidextrous Safety.',
        'description': 'The Colt M4A1 Carbine SOCOM 5.56x45mm NATO rifle is the authentic semi-automatic reproduction of the legendary combat carbine issued to U.S. Special Operations Command (SOCOM). Featuring a true 16.1" heavy SOCOM contour barrel with M203 grenade launcher flats, Knights Armament Company (KAC) M4 Quad Rail adapter system, Matech folding rear backup sight, and roll-marked Colt Defense lower receiver.',
        'rich_description': '''
<div class="row g-4 my-2">
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>True SOCOM Heavy Contour Barrel</strong>
            <p class="small text-secondary mb-0">16.1" heavy combat barrel with M203 flats, chrome-lined bore and chamber, engineered for sustained high-rate fire without thermal degradation.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>KAC M4 Quad Rail Handguard</strong>
            <p class="small text-secondary mb-0">Authentic Knights Armament Company (KAC) drop-in quad rail system with MIL-STD-1913 Picatinny rails and heat-shield rail panels.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Matech Folding BUIS Rear Sight</strong>
            <p class="small text-secondary mb-0">MIL-SPEC Matech elevation-adjustable folding rear iron sight calibrated from 200 to 600 meters for precise iron sight targeting.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>MIL-SPEC Bolt & Ambi Safety</strong>
            <p class="small text-secondary mb-0">MP/HP tested bolt carrier group with properly staked gas key and factory ambidextrous safety selector switch.</p>
        </div>
    </div>
</div>
''',
        'specifications': json.dumps({
            'Caliber / Chambering': '5.56x45mm NATO (.223 Rem)',
            'Action Type': 'Direct Impingement Semi-Automatic (Carbine-Length Gas System)',
            'Barrel Length & Profile': '16.1" True SOCOM Heavy Contour, Chrome-Lined, 1:7" Twist',
            'Muzzle Device & Threads': 'A2 Birdcage Flash Hider (1/2x28 TPI)',
            'Trigger Mechanism': 'Colt MIL-SPEC Single-Stage Combat Trigger (6.5 lbs)',
            'Handguard System': 'Knights Armament Company (KAC) M4 Quad Rail with Ribbed Covers',
            'Sights & Optics Ready': 'Matech Elevation-Adjustable Rear BUIS & F-Marked Front Sight Post',
            'Stock & Receiver': 'Colt 4-Position Collapsible Carbine Stock & Forged 7075-T6 Receivers',
            'Weight & Length': '7.00 lbs Overall Weight | 32.0" - 35.5" Overall Length',
            'Heritage & Standard': 'Authentic U.S. SOCOM Military Issue Specification'
        })
    },
    'BRN-EXT-SPR-005': {
        'price': '1129.00',
        'short_description': 'Springfield Armory SAINT Victor V2 5.56x45mm NATO 16" Barrel Semi-Automatic AR-15 Rifle with Free-Float M-LOK Handguard and Nickel Boron Trigger.',
        'description': 'The Springfield Armory SAINT Victor V2 5.56 NATO AR-15 rifle is purpose-built for defensive agility, competitive shooting, and duty reliability right out of the box. Weighing just 6.6 lbs, the SAINT Victor V2 features a 16" CMV Melonite-coated barrel with a mid-length gas system, an uninterrupted 15" free-float M-LOK aluminum handguard, and a flat-face Nickel Boron coated single-stage match trigger.',
        'rich_description': '''
<div class="row g-4 my-2">
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Flat-Face NiB Match Trigger</strong>
            <p class="small text-secondary mb-0">Single-stage flat-profile trigger coated in self-lubricating Nickel Boron (NiB) for a zero-creep break and lightning-fast resets.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Mid-Length Pinned Gas System</strong>
            <p class="small text-secondary mb-0">Low-profile pinned gas block combined with a mid-length gas tube softens recoil impulse and extends bolt life significantly.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>15" Free-Float M-LOK Handguard</strong>
            <p class="small text-secondary mb-0">Full-length aluminum M-LOK rail featuring SA Accu-Tite tension system inside the receiver receiver to eliminate rattle.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-3 bg-light rounded-3 border h-100">
            <strong class="d-block text-dark font-outfit mb-1"><i class="bi bi-check-circle-fill text-success me-2"></i>Melonite Treated CMV Barrel</strong>
            <p class="small text-secondary mb-0">16" Chrome Moly Vanadium barrel treated inside and out with Melonite for superior corrosion resistance and accuracy.</p>
        </div>
    </div>
</div>
''',
        'specifications': json.dumps({
            'Caliber / Chambering': '5.56x45mm NATO (.223 Rem)',
            'Action Type': 'Direct Impingement Semi-Automatic (Mid-Length Gas System)',
            'Barrel Length & Profile': '16.0" CMV Melonite-Coated Lightweight Profile, 1:8" Twist',
            'Muzzle Device & Threads': 'SA Muzzle Brake / Compensator (1/2x28 TPI)',
            'Trigger Mechanism': 'Nickel Boron (NiB) Coated Flat-Face Single-Stage Match Trigger (4.0 lbs)',
            'Handguard System': '15.0" Aluminum Free-Float with M-LOK Slots & Accu-Tite Tension System',
            'Bolt Carrier Group': 'M16 BCG, Melonite Coated, 9310 Steel Bolt, MPI Tested',
            'Stock & Furniture': 'B5 Systems Bravo Stock, B5 Type 23 P-Grip & B5 Trigger Guard',
            'Weight & Length': '6.60 lbs Overall Weight | 32.25" - 35.5" Overall Length',
            'Factory Warranty': 'Springfield Armory Limited Lifetime Warranty Guarantee'
        })
    }
}

updated_count = 0
for sku, data in data_updates.items():
    try:
        p = Product.objects.get(sku=sku)
        p.price = data['price']
        p.short_description = data['short_description']
        p.description = data['description']
        p.rich_description = data['rich_description']
        p.specifications = data['specifications']
        p.save()
        print(f"Updated {p.name} -> Price: ${p.price}")
        updated_count += 1
    except Product.DoesNotExist:
        print(f"Product with SKU {sku} not found.")

print(f"Successfully updated {updated_count} products.")
