import os

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/apps/orders/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for email
if 'from django.core.mail import EmailMultiAlternatives' not in content:
    content = content.replace('from decimal import Decimal', 'from decimal import Decimal\nfrom django.core.mail import EmailMultiAlternatives\nfrom django.template.loader import render_to_string\nfrom django.utils.html import strip_tags')

# Email sending logic
email_logic = """        pm_display = pm_display_map.get(payment_method, payment_method.replace('_', ' ').title())
        
        # Send Order Confirmation Email
        try:
            subject = f"Order Confirmation #{order.order_number} - Glocks And Armor"
            html_message = render_to_string('emails/order_confirmation.html', {
                'order': order,
                'request': request
            })
            plain_message = strip_tags(html_message)
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                'support@glocksandarmor.com',
                [email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        except Exception as e:
            pass # Silent fail for email in dev if not configured

        messages.success"""

content = content.replace("        pm_display = pm_display_map.get(payment_method, payment_method.replace('_', ' ').title())\n        messages.success", email_logic)

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/apps/orders/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated checkout_view successfully.")
