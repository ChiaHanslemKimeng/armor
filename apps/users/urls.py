from django.urls import path
from django.shortcuts import redirect
from .views import login_view, register_view, logout_view, dashboard_view, two_factor_setup_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='user_dashboard'),
    path('2fa/', two_factor_setup_view, name='two_factor_setup'),
    path('profile/', lambda r: redirect('/users/2fa/'), name='user_profile'),
]
