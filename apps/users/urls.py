from django.urls import path
from django.shortcuts import redirect
from .views import login_view, register_view, logout_view, dashboard_view, two_factor_setup_view, edit_profile_view, save_push_subscription, get_vapid_public_key

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='user_dashboard'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('2fa/', two_factor_setup_view, name='two_factor_setup'),
    path('profile/', lambda r: redirect('/users/edit-profile/'), name='user_profile'),
    path('save_push_subscription/', save_push_subscription, name='save_push_subscription'),
    path('vapid_public_key/', get_vapid_public_key, name='vapid_public_key'),
]
