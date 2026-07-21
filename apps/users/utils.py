import json
from pywebpush import webpush, WebPushException
from django.conf import settings
from .models import PushSubscription

def send_web_push(title, body, url="/admin/"):
    """
    Sends a Web Push Notification to all subscribed admin users.
    """
    admin_subscriptions = PushSubscription.objects.filter(user__is_staff=True)
    
    payload = json.dumps({
        "title": title,
        "body": body,
        "url": url,
        "icon": "/static/images/glocks_and_armor_logo.png",
        "badge": "/static/images/glocks_and_armor_logo.png",
        "vibrate": [200, 100, 200, 100, 200, 100, 200],
        "requireInteraction": True
    })

    if not settings.VAPID_PRIVATE_KEY or not settings.VAPID_PUBLIC_KEY:
        print("Web push aborted: VAPID keys not configured in settings.")
        return

    for sub in admin_subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                },
                data=payload,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_ADMIN_EMAIL,
                }
            )
        except WebPushException as ex:
            print(f"Web push failed for {sub.user.email}: {ex}")
            # If the subscription is expired or revoked (404 or 410), delete it
            if ex.response and ex.response.status_code in [404, 410]:
                sub.delete()
        except Exception as e:
            print(f"Unexpected error sending push to {sub.user.email}: {e}")
