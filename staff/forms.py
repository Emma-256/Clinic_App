from django import forms
from django.contrib.auth.forms import UserCreationForm
from clinic_owners.models import CustomUser
from .models import (
    StaffProfile, TECHNICAL_ROLES, SUPPORT_ROLES,
    EMPLOYMENT_TYPE_CHOICES, ACCOUNT_STATUS_CHOICES, DUTY_STATUS_CHOICES
)
import re


class StaffRegistrationForm(UserCreationForm):
    # --- Contact ---
    phone = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    # --- Personal ---
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    national_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID number'})
    )

    # --- Employment ---
    employment_type = forms.ChoiceField(
        choices=[('', 'Select employment type')] + EMPLOYMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_employment_type'})
    )
    role = forms.ChoiceField(
        choices=[('', 'Select role')],  # populated dynamically via JS or set in __init__
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_role'})
    )
    registration_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number (technical staff only)'})
    )
    license_expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # --- Next of kin ---
    next_of_kin = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'})
    )
    nok_relationship = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mother, Father, Spouse'})
    )
    nok_phone = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'})
    )

    # --- Compensation ---
    gross_salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gross salary'})
    )
    monthly_allowance = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly allowance (default 0)'})
    )

    # --- Status ---
    account_status = forms.ChoiceField(
        choices=ACCOUNT_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duty_status = forms.ChoiceField(
        choices=DUTY_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

        # Combine all roles for the role dropdown
        self.fields['role'].choices = (
            [('', 'Select role')] + TECHNICAL_ROLES + SUPPORT_ROLES
        )

        placeholders = {
            'username': 'Choose a username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'password1': 'Enter password',
            'password2': 'Confirm password',
        }

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.FileInput, forms.Select)):
                field.widget.attrs['class'] = 'form-control'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
            field.label = ''
            field.help_text = None

    # --- Validation ---
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone number must be in the format +256XXXXXXXXX.")
        if StaffProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean_nok_phone(self):
        phone = self.cleaned_data.get('nok_phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone number must be in the format +256XXXXXXXXX.")
        return phone

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if StaffProfile.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("This National ID is already registered.")
        return national_id

    def clean(self):
        cleaned_data = super().clean()
        employment_type = cleaned_data.get('employment_type')
        registration_number = cleaned_data.get('registration_number')
        license_expiry_date = cleaned_data.get('license_expiry_date')

        if employment_type == 'technical':
            if not registration_number:
                self.add_error('registration_number', "Registration number is required for technical staff.")
            if not license_expiry_date:
                self.add_error('license_expiry_date', "License expiry date is required for technical staff.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            StaffProfile.objects.create(
                user=user,
                owner=self.owner,
                phone=self.cleaned_data['phone'],
                profile_picture=self.cleaned_data.get('profile_picture'),
                date_of_birth=self.cleaned_data['date_of_birth'],
                national_id=self.cleaned_data['national_id'],
                employment_type=self.cleaned_data['employment_type'],
                role=self.cleaned_data['role'],
                registration_number=self.cleaned_data.get('registration_number') or None,
                license_expiry_date=self.cleaned_data.get('license_expiry_date') or None,
                next_of_kin=self.cleaned_data['next_of_kin'],
                nok_relationship=self.cleaned_data['nok_relationship'],
                nok_phone=self.cleaned_data['nok_phone'],
                gross_salary=self.cleaned_data['gross_salary'],
                monthly_allowance=self.cleaned_data.get('monthly_allowance') or 0,
                account_status=self.cleaned_data['account_status'],
                duty_status=self.cleaned_data['duty_status'],
            )
        return user


class StaffProfileUpdateForm(forms.ModelForm):
    # Fields from CustomUser
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = StaffProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_picture',
            'date_of_birth', 'national_id', 'employment_type', 'role',
            'registration_number', 'license_expiry_date',
            'next_of_kin', 'nok_relationship', 'nok_phone',
            'gross_salary', 'monthly_allowance',
            'account_status', 'duty_status',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID number'}),
            'employment_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_employment_type'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number'}),
            'license_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_of_kin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'nok_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mother, Father, Spouse'}),
            'nok_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'}),
            'gross_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'account_status': forms.Select(attrs={'class': 'form-control'}),
            'duty_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

        for field in self.fields.values():
            field.label = ''
            field.help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone number must be in the format +256XXXXXXXXX.")
        if StaffProfile.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean_nok_phone(self):
        phone = self.cleaned_data.get('nok_phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone number must be in the format +256XXXXXXXXX.")
        return phone

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if StaffProfile.objects.filter(national_id=national_id).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This National ID is already registered.")
        return national_id

    def clean(self):
        cleaned_data = super().clean()
        employment_type = cleaned_data.get('employment_type')
        registration_number = cleaned_data.get('registration_number')
        license_expiry_date = cleaned_data.get('license_expiry_date')

        if employment_type == 'technical':
            if not registration_number:
                self.add_error('registration_number', "Registration number is required for technical staff.")
            if not license_expiry_date:
                self.add_error('license_expiry_date', "License expiry date is required for technical staff.")

        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile