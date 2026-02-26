import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BDDS.settings")
django.setup()

from bdds_dashboard.models import Form_data

def check_records():
    print("Checking Form_data records...")
    records = Form_data.objects.all()
    for r in records:
        print(f"ID: {r.id}")
        print(f"  Serial: {r.fserial}")
        print(f"  User: {r.user.id if r.user else 'None'} ({r.user.username if r.user else ''})")
        print(f"  Bomb ID: {r.d_bomb}")
        print(f"  Date: {r.fdate}")
        print(f"  Location: {r.flocation}")
        print(f"  Incident: {r.fincident.i_incident if r.fincident else 'None'}")
        print("-" * 20)

if __name__ == "__main__":
    check_records()
