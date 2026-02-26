import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDDS.settings')
django.setup()

from bdds_dashboard.models import Nlogines_creations

print("Nlogines_creations data:")
data = Nlogines_creations.objects.all()
if not data:
    print("No registrations found.")
else:
    for i in data:
        user_name = i.user.username if i.user else "None"
        station = i.post.p_post if i.post else "None"
        print(f"User: {user_name} | Station: {station}")
