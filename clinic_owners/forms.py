# clinic_owners/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm ,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, UserProfile
import re

class OwnerRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling and placeholders, remove labels/help text
        placeholders = {
            'username': 'Choose a username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'password1': 'Enter password',
            'password2': 'Confirm password',
        }

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

            # Remove labels
            field.label = ''

            # Remove default help text (especially for password fields)
            field.help_text = None

    # --- VALIDATION METHODS ---
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+256\d{9}$', phone):
            raise forms.ValidationError("Phone number must be in the format +256XXXXXXXXX.")
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                user_type='owner',
                phone=self.cleaned_data['phone'],
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling and placeholders
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

        # Remove labels and help text
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].help_text = None
        self.fields['password'].help_text = None

class ProfileUpdateForm(forms.ModelForm):
    # Extra fields from CustomUser
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
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256XXXXXXXXX'}),
            'profile_picture': forms.FileInput(attrs={ 'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill with values from related CustomUser
        if self.instance and hasattr(self.instance, "user"):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

            # Remove labels 
            self.fields['first_name'].label = ''
            self.fields['last_name'].label = ''
            self.fields['email'].label = ''   
            self.fields['profile_picture'].label = ''  
            self.fields['phone'].label = ''  
               

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user  # CustomUser linked via OneToOneField
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = ''
        self.fields['username'].help_text = None
        


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'old_password': 'Current password',
            'new_password1': 'New password',
            'new_password2': 'Confirm new password',
        }
        for field_name, field in self.fields.items():
            # Remove default help texts (so rules only show as errors)
            field.help_text = None
            self.fields['old_password'].label = ''
            self.fields['new_password1'].label = ''
            self.fields['new_password2'].label = ''
            # Add Bootstrap styling + placeholders
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, '')
            })
