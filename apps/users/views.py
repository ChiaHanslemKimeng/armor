import qrcode
import io
import base64
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import User, Address


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.two_factor_enabled:
                request.session['pre_2fa_user_id'] = str(user.id)
                return redirect('two_factor_verify')
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid enterprise credentials. Please check your email and password.")
    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this enterprise email already exists.")
        else:
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('user_dashboard')
    return render(request, 'users/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def dashboard_view(request):
    addresses = request.user.addresses.all()
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'addresses': addresses,
        'orders': orders,
    })


@login_required
def two_factor_setup_view(request):
    uri = request.user.get_totp_uri()
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    if request.method == 'POST':
        code = request.POST.get('totp_code')
        if request.user.verify_totp(code):
            request.user.two_factor_enabled = True
            request.user.save()
            messages.success(request, "Two-Factor Authentication (TOTP) enabled successfully!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid authentication token code. Please try again.")

    return render(request, 'users/2fa_setup.html', {'qr_image_b64': qr_b64})
