# clinics/migrations/0002_seed_departments_days.py
from django.db import migrations

def seed_departments_and_days(apps, schema_editor):
    Department = apps.get_model('clinics', 'Department')
    Day = apps.get_model('clinics', 'Day')

    # Hospital departments
    departments = [
        "Reception", "Outpatient", "Inpatient", "Emergency", "Pharmacy",
        "Laboratory", "Radiology", "Surgery", "Maternity", "Pediatrics",
        "Internal Medicine", "Dental", "ENT", "Physiotherapy",
        "Nutrition", "Counseling"
    ]
    for dept in departments:
        Department.objects.get_or_create(name=dept)

    # Days of the week
    days = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]
    for order, name in days:
        Day.objects.get_or_create(order=order, name=name)

def unseed_departments_and_days(apps, schema_editor):
    Department = apps.get_model('clinics', 'Department')
    Day = apps.get_model('clinics', 'Day')
    Department.objects.all().delete()
    Day.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0001_initial'),  # adjust to your actual initial migration
    ]

    operations = [
        migrations.RunPython(seed_departments_and_days, unseed_departments_and_days),
    ]
