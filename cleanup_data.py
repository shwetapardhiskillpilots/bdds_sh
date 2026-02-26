import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BDDS.settings")
django.setup()

from bdds_dashboard.models import Form_data, images, s_report, sk_report, death_person, injured_person, exploded

def clear_data():
    print("Starting database cleanup...")
    
    # Due to models.CASCADE, deleting Form_data should delete all related records.
    # However, to be absolutely sure and clear everything even if orphans exist:
    
    models_to_clear = [
        images,
        s_report,
        sk_report,
        death_person,
        injured_person,
        exploded,
        Form_data
    ]
    
    for model in models_to_clear:
        count = model.objects.count()
        print(f"Deleting {count} records from {model.__name__}...")
        model.objects.all().delete()
    
    print("Cleanup complete!")

if __name__ == "__main__":
    clear_data()
