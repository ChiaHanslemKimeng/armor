from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address, SavedPaymentMethod


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class SavedPaymentMethodInline(admin.TabularInline):
    model = SavedPaymentMethod
    extra = 0
    readonly_fields = ('provider', 'card_brand', 'last_four', 'exp_month', 'exp_year', 'token_id')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_verified', 'two_factor_enabled')
    list_filter = ('role', 'is_active', 'is_verified', 'two_factor_enabled', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    inlines = [AddressInline, SavedPaymentMethodInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('two_factor_enabled', 'two_factor_secret')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role', 'first_name', 'last_name'),
        }),
    )

