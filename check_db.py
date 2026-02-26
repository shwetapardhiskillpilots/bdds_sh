import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDDS.settings')
django.setup()

from django.db import connection
print(f"Connected to database: {connection.settings_dict['NAME']} on {connection.settings_dict['HOST']}")

from bdds_dashboard.models import Form_data

print(f"Total entries in Form_data: {Form_data.objects.count()}")
print("Checking last 5 submissions:")
data = Form_data.objects.all().order_by('-id')[:5]
if not data:
    print("No data found.")
else:
    for i in data:
        user_name = i.user.username if i.user else "None"
        print(f"ID: {i.id} | Serial: {i.fserial} | FIR: {i.fir} | User: {user_name} | Date: {i.fdate}")
