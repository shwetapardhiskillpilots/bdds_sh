import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDDS.settings')
try:
    django.setup()
    from django.contrib.auth.models import User
    print(f"User count: {User.objects.count()}")
except Exception as e:
    print(f"Error: {e}")
