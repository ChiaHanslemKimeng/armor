import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/armor_project/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add jazzmin to INSTALLED_APPS if not present
if "'jazzmin'," not in content and '"jazzmin",' not in content:
    content = re.sub(
        r"INSTALLED_APPS = \[",
        "INSTALLED_APPS = [\n    'jazzmin',",
        content,
        count=1
    )

jazzmin_config = """
# Jazzmin Admin Theme Settings
JAZZMIN_SETTINGS = {
    "site_title": "Glocks And Armor Admin",
    "site_header": "Glocks And Armor",
    "site_brand": "Glocks And Armor",
    "site_logo": "images/glocks_and_armor_logo.png",
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to Glocks And Armor Command Center",
    "copyright": "Glocks And Armor",
    "search_model": ["auth.User", "catalog.Product", "orders.Order"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Storefront", "url": "/", "new_window": True},
        {"name": "Orders", "url": "admin:orders_order_changelist"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "catalog.Product": "fas fa-crosshairs",
        "catalog.Category": "fas fa-list",
        "catalog.Brand": "fas fa-industry",
        "orders.Order": "fas fa-shopping-cart",
        "reviews.Review": "fas fa-star",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
"""

if "JAZZMIN_SETTINGS" not in content:
    with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/armor_project/settings.py', 'w', encoding='utf-8') as f:
        f.write(content + "\n" + jazzmin_config)
    print("Jazzmin configured successfully.")
else:
    print("Jazzmin configuration already exists.")
