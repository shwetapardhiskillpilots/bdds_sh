import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDDS.settings')
django.setup()

from django.apps import apps

print("Model Counts:")
for model in apps.get_models():
    try:
        count = model.objects.count()
        if count > 0:
            print(f"{model.__name__}: {count}")
    except Exception as e:
        print(f"Error checking {model.__name__}: {e}")
