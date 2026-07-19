import pyotp
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from apps.core.models import UUIDModel, TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, UUIDModel, TimeStampedModel):
    ROLES = [
        ('superadmin', 'System Superadmin'),
        ('brand_partner', 'Brand Partner'),
        ('store_manager', 'Store Manager'),
        ('customer', 'Customer'),
    ]

    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLES, default='customer')
    
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # TOTP 2FA Security
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=64, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def generate_2fa_secret(self):
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
            self.save(update_fields=['two_factor_secret'])
        return self.two_factor_secret

    def get_totp_uri(self):
        secret = self.generate_2fa_secret()
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=self.email,
            issuer_name="Glocks And Armor"
        )

    def verify_totp(self, code):
        if not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(str(code).strip())


class Address(UUIDModel, TimeStampedModel):
    ADDRESS_TYPES = [('shipping', 'Shipping Address'), ('billing', 'Billing Address')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES, default='shipping')
    full_name = models.CharField(max_length=200)
    street_line1 = models.CharField(max_length=255)
    street_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    phone = models.CharField(max_length=30)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.street_line1}, {self.city}"


class SavedPaymentMethod(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    provider = models.CharField(max_length=50, default='Stripe')  # Stripe, PayPal
    card_brand = models.CharField(max_length=50)  # Visa, Mastercard, AMEX
    last_four = models.CharField(max_length=4)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    token_id = models.CharField(max_length=255, help_text='Tokenized payment gateway reference')
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.card_brand} **** {self.last_four} (exp {self.exp_month}/{self.exp_year})"
