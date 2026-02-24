from django.db import models
from django.core.validators import RegexValidator
from clinic_owners.models import CustomUser


TECHNICAL_ROLES = [
    ("physician", "Physician/Doctor"),
    ("specialist", "Specialist"),
    ("nurse", "Nurse"),
    ("nurse_practitioner", "Nurse Practitioner"),
    ("physician_assistant", "Physician Assistant"),
    ("medical_assistant", "Medical Assistant"),
    ("pharmacist", "Pharmacist"),
    ("lab_technician", "Lab Technician"),
    ("radiology_technician", "Radiology Technician"),
    ("dietitian", "Dietitian/Nutritionist"),
    ("social_worker", "Social Worker/Counselor"),
]

SUPPORT_ROLES = [
    ("clinic_manager", "Clinic Manager/Administrator"),
    ("receptionist", "Receptionist/Front Desk"),
    ("billing_specialist", "Billing & Insurance Specialist"),
    ("records_clerk", "Medical Records Clerk"),
    ("it_support", "IT Support Staff"),
    ("maintenance", "Cleaning & Maintenance Staff"),
]

ALL_ROLES = TECHNICAL_ROLES + SUPPORT_ROLES

EMPLOYMENT_TYPE_CHOICES = [
    ("technical", "Technical"),
    ("support", "Support"),
]

ACCOUNT_STATUS_CHOICES = [
    ("active", "Active"),
    ("inactive", "Inactive"),
]

DUTY_STATUS_CHOICES = [
    ("on_duty", "On Duty"),
    ("on_leave", "On Leave"),
    ("off_duty", "Off Duty"),
]


class StaffProfile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+256\d{9}$',
        message="Phone number must be in the format: '+256XXXXXXXXX' (total 13 characters)."
    )
    nok_phone_regex = RegexValidator(
        regex=r'^\+256\d{9}$',
        message="Phone number must be in the format: '+256XXXXXXXXX' (total 13 characters)."
    )

    # --- Core link fields ---
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='staff_members',
        limit_choices_to={'profile__user_type': 'owner'}
    )

    # --- Personal info ---
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='staff_profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=20, unique=True)

    # --- Employment info ---
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES)
    role = models.CharField(max_length=30, choices=ALL_ROLES)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)

    # --- Next of kin ---
    next_of_kin = models.CharField(max_length=100)
    nok_relationship = models.CharField(max_length=50)
    nok_phone = models.CharField(validators=[nok_phone_regex], max_length=17)

    # --- Compensation ---
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- Status ---
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')
    duty_status = models.CharField(max_length=10, choices=DUTY_STATUS_CHOICES, default='on_duty')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()}) - {self.owner.username}"