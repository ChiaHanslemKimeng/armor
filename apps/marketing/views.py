from django.http import HttpResponse
from .models import NewsletterSubscriber


def subscribe_newsletter_view(request):
    """HTMX endpoint to subscribe email and return a success badge."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            return HttpResponse('''
            <div class="alert alert-success py-2 px-3 small rounded-pill border-0 bg-success bg-opacity-10 text-success d-flex align-items-center gap-2 mb-0">
                <i class="bi bi-check-circle-fill"></i> Subscribed to VIP Enterprise Alerts!
            </div>
            ''')
    return HttpResponse("Invalid email", status=400)
