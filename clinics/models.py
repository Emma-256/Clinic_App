from django.db import models
from clinic_owners.models import CustomUser
from django.core.validators import RegexValidator
from .utils import logo_upload_to


class Department(models.Model):
    """Clinic department (e.g., Lab, Reception)"""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Day(models.Model):
    """Day of the week with explicit ordering"""
    name = models.CharField(max_length=10, unique=True)
    order = models.PositiveSmallIntegerField(unique=True, help_text="1=Monday, 7=Sunday")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class County(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="counties")

    class Meta:
        unique_together = ('name', 'district')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.district.name})"


class Subcounty(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="subcounties")

    class Meta:
        unique_together = ('name', 'county')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.county.name})"


class Parish(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    subcounty = models.ForeignKey(Subcounty, on_delete=models.CASCADE, related_name="parishes")

    class Meta:
        unique_together = ('name', 'subcounty')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.subcounty.name})"


class Village(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name="villages")

    class Meta:
        unique_together = ('name', 'parish')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.parish.name})"


class Clinic(models.Model):
    LICENSING_BODIES = [
        ('UMDPC', 'Uganda Medical and Dental Practitioners Council (UMDPC)'),
        ('AHPC', 'Allied Health Professionals Council (AHPC)'),
        ('UNMC', 'Uganda Nurses and Midwives Council (UNMC)'),
        ('Pharmacy', 'Pharmacy Council of Uganda'),
        ('Others', 'Others'),
    ]
    SUPERVISOR_TITLES = [
        ('MD', 'MD'),
        ('MCO', 'MCO'),
        ('EN', 'EN'),
        ('RN', 'RN'),
        ('BSN', 'BSN'),
        ('Others', 'Others'),
    ]
    OPERATION_STATUS_CHOICES = [
        ('operating', 'Operating'),
        ('not_operating', 'Not Operating'),
    ]

    # Owner
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='clinics')

    # Basic Information
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slogan = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to=logo_upload_to, blank=True, null=True)

    # Location (normalized)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='clinics')
    county = models.ForeignKey(County, on_delete=models.PROTECT, related_name='clinics')
    sub_county = models.ForeignKey(Subcounty, on_delete=models.PROTECT, related_name='clinics')
    parish = models.ForeignKey(Parish, on_delete=models.PROTECT, related_name='clinics')
    village = models.ForeignKey(Village, on_delete=models.PROTECT, related_name='clinics')

    # Contact
    phone_regex = RegexValidator(
        regex=r'^\+256\d{9}$',
        message="Phone number must be entered in the format: '+256XXXXXXXXX' (total 13 characters)."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, db_index=True)
    email = models.EmailField(blank=True, null=True, help_text="Clinic contact email")
    website = models.URLField(blank=True, null=True, help_text="Clinic website URL")
    emergency_contact = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_regex],
        help_text="Emergency contact number"
    )

    # Description & Bank
    description = models.TextField(blank=True, help_text="About the clinic")
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)

    # Geographic coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Dates
    established_date = models.DateField(blank=True, null=True, help_text="Date clinic was established")
    registration_date = models.DateField()
    licence_expiry_date = models.DateField()

    # Licensing & Supervisor
    licensing_body = models.CharField(max_length=50, choices=LICENSING_BODIES)
    registration_number = models.CharField(max_length=100, unique=True, db_index=True)
    supervisor_title = models.CharField(max_length=64, choices=SUPERVISOR_TITLES)
    supervisor = models.CharField(max_length=200)

    # Flags
    is_main_clinic = models.BooleanField(default=False, help_text="Mark if this is the primary clinic",)
    
    # Operations
    operation_status = models.CharField(max_length=20, choices=OPERATION_STATUS_CHOICES, default='operating', db_index=True)
    operation_days = models.ManyToManyField(Day, related_name='clinics')
    # Flexible operation hours (instead of fixed choices)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    # Departments
    departments = models.ManyToManyField(Department, related_name='clinics')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Soft delete flag")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['owner', 'supervisor'], name='unique_supervisor_per_owner')
        ]
