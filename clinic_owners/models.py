# clinic_owners/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # enforce uniqueness

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('owner', 'Clinic Owner'),
        ('staff', 'Staff'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='owner')

    phone_regex = RegexValidator(
        regex=r'^\+256\d{9}$',
        message="Phone number must be entered in the format: '+256XXXXXXXXX' (total 13 characters)."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
