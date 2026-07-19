import os

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/apps/catalog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for email
if 'from django.core.mail import EmailMultiAlternatives' not in content:
    content = content.replace('from django.db.models import Q, Count', 'from django.db.models import Q, Count\nfrom django.core.mail import EmailMultiAlternatives\nfrom django.template.loader import render_to_string\nfrom django.utils.html import strip_tags\nfrom django.contrib import messages')

new_contact_view = """def contact_view(request):
    \"\"\"Contact Our Armory Support - Phone, Email, & FFL Transfer Department.\"\"\"
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        department = request.POST.get('department', 'General Support')
        message = request.POST.get('message', '')
        
        if name and email and message:
            # Send Email
            subject = f"New Contact Request from {name} - {department}"
            html_message = render_to_string('emails/contact_notification.html', {
                'name': name,
                'email': email,
                'department': department,
                'message': message,
            })
            plain_message = strip_tags(html_message)
            
            try:
                msg = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    'support@glocksandarmor.com',
                    ['support@glocksandarmor.com'] # Sends to store owner
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send()
                messages.success(request, "Your message has been sent successfully. Our team will contact you shortly.")
            except Exception as e:
                messages.error(request, "There was an error sending your message. Please try again later.")
        else:
            messages.error(request, "Please fill in all required fields.")
            
    return render(request, 'catalog/contact.html')"""

import re
content = re.sub(r'def contact_view\(request\):\n\s*\"\"\"Contact Our Armory Support - Phone, Email, & FFL Transfer Department\.\"\"\"\n\s*return render\(request, \'catalog/contact.html\'\)', new_contact_view, content, count=1)

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/apps/catalog/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated contact_view successfully.")
