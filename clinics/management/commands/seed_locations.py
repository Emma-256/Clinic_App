import csv
from django.core.management.base import BaseCommand
from clinics.models import District, County, Subcounty, Parish, Village

class Command(BaseCommand):
    help = "Bulk import Uganda location hierarchy from CSV"

    def handle(self, *args, **kwargs):
        with open('uganda_locations.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                district, _ = District.objects.get_or_create(name=row['district'])
                county, _ = County.objects.get_or_create(name=row['county'], district=district)
                subcounty, _ = Subcounty.objects.get_or_create(name=row['subcounty'], county=county)
                parish, _ = Parish.objects.get_or_create(name=row['parish'], subcounty=subcounty)
                Village.objects.get_or_create(name=row['village'], parish=parish)

        self.stdout.write(self.style.SUCCESS("✅ Bulk seeded Uganda locations"))
