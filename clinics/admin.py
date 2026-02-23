from django.contrib import admin
from .models import Day, Department, Clinic, District, County, Parish, Village, Subcounty

# Register your models here.
admin.site.register(Clinic)
admin.site.register(Day)
admin.site.register(Department)
admin.site.register(District)
admin.site.register(County)
admin.site.register(Subcounty)
admin.site.register(Parish)
admin.site.register(Village)

