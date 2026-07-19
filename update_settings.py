
with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/armor_project/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

email_settings = """

# Email Configuration
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = 'Glocks And Armor <support@glocksandarmor.com>'
SERVER_EMAIL = 'support@glocksandarmor.com'
"""

if 'EMAIL_BACKEND' not in content:
    with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/armor_project/settings.py', 'a', encoding='utf-8') as f:
        f.write(email_settings)
    print("Added email settings to settings.py")
else:
    print("Email settings already exist.")
