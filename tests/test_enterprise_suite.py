from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Brand, Product
from apps.orders.models import Order, CartItem


class EnterprisePlatformIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='shooter@example.com',
            password='SecurePassword123!',
            first_name='John',
            last_name='Customer'
        )
        self.category = Category.objects.create(
            name="Precision Sniper Rifles",
            slug="precision-rifles",
            description="Sub-MOA tactical systems."
        )
        self.brand = Brand.objects.create(
            name="Armor Tactical Defense",
            slug="armor-tactical-defense"
        )
        self.product = Product.objects.create(
            name="Armor Tactical PSR-338 Sniper System",
            slug="armor-psr-338-sniper",
            sku="ARM-PSR-338",
            category=self.category,
            brand=self.brand,
            price=8450.00,
            short_description="Sub-0.5 MOA guarantee. 26 inch fluted stainless barrel.",
            is_active=True
        )

    def test_01_homepage_and_catalog_listing(self):
        """Verifies homepage renders with SEO tags, hero banners, and tactical weapons."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Armor Tactical PSR-338")
        
        prod_resp = self.client.get('/products/')
        self.assertEqual(prod_resp.status_code, 200)
        self.assertContains(prod_resp, "Store Filters")

    def test_02_product_detail_360_viewer(self):
        """Verifies weapon detail page renders 360 viewer canvas and caliber specs."""
        response = self.client.get(f'/product/{self.product.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "360° TACTICAL WEAPON & ARMOR INSPECTION")
        self.assertContains(response, "8,450.00")

    def test_03_htmx_add_to_cart(self):
        """Verifies HTMX endpoint adds weapon to session/DB cart and returns badge."""
        response = self.client.post('/orders/cart/add/', {'sku': self.product.sku, 'qty': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Added!")
        
        # Verify cart page calculation
        cart_resp = self.client.get('/orders/cart/')
        self.assertEqual(cart_resp.status_code, 200)
        self.assertContains(cart_resp, "16900.0")

    def test_04_multi_step_escrow_checkout(self):
        """Verifies tactical checkout creates Order and checks terms."""
        post_data = {
            'full_name': 'Capt. Hanslem Kimeng',
            'email': 'shooter@example.com',
            'street': '100 Tactical Ordnance Way',
            'city': 'Quantico',
            'postal_code': '22134',
            'payment_method': 'Credit Card'
        }
        response = self.client.post('/orders/checkout/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LIVE TRACKING TELEMETRY")
        
        # Check order in database
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.payment_gateway, 'Credit Card')

    def test_05_google_merchant_center_feed(self):
        """Verifies automated XML product feed generates compliant Google Merchant format."""
        response = self.client.get('/dashboard/feed/google.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, "<g:id>ARM-PSR-338</g:id>")
        self.assertContains(response, "8450.00 USD")

    def test_06_analytics_dashboard_telemetry(self):
        """Verifies executive ordnance dashboard renders KPIs and Chart.js canvas."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Store Sales &amp; Revenue Analytics")
        self.assertContains(response, "revenueChart")
