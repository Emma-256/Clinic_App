from django import forms
from .models import (
    Day, Department, Clinic,
    District, County, Subcounty, Parish, Village
)

class ClinicForm(forms.ModelForm):
    # Location hierarchy fields
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'District'})
    )
    county = forms.ModelChoiceField(
        queryset=County.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'County'})
    )
    sub_county = forms.ModelChoiceField(
        queryset=Subcounty.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Subcounty'})
    )
    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Parish'})
    )
    village = forms.ModelChoiceField(
        queryset=Village.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Village'})
    )

    # Departments
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

    # Days
    operation_days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )

    class Meta:
        model = Clinic
        fields = [
            'name', 'slogan', 'logo',
            'district', 'county', 'sub_county', 'parish', 'village',
            'phone', 'email', 'website', 'emergency_contact',
            'description', 'bank_name', 'bank_account_number', 'bank_branch',
            'latitude', 'longitude', 'established_date',
            'is_main_clinic',
            'licensing_body', 'registration_date', 'registration_number',
            'supervisor_title', 'supervisor', 'licence_expiry_date',
            'operation_status', 'opening_time', 'closing_time',
            'departments', 'operation_days', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clinic name'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slogan'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Description'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank name'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account number'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
            'established_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'licence_expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number'}),
            'supervisor_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supervisor title'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supervisor'}),
            'operation_status': forms.Select(attrs={'class': 'form-select'}),
            'opening_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_main_clinic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

        # Apply Bootstrap classes to all non-checkbox fields
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'form-control')

        if self.instance and self.instance.pk:
            # Edit mode — populate dropdowns from saved instance
            self.fields['county'].queryset = County.objects.filter(district=self.instance.district)
            self.fields['sub_county'].queryset = Subcounty.objects.filter(county=self.instance.county)
            self.fields['parish'].queryset = Parish.objects.filter(subcounty=self.instance.sub_county)
            self.fields['village'].queryset = Village.objects.filter(parish=self.instance.parish)

        elif self.data:
            # Failed POST re-render — repopulate dropdowns from submitted data
            # so validation passes on resubmission
            district_id = self.data.get('district')
            county_id = self.data.get('county')
            subcounty_id = self.data.get('sub_county')
            parish_id = self.data.get('parish')

            if district_id:
                self.fields['county'].queryset = County.objects.filter(district_id=district_id)
            if county_id:
                self.fields['sub_county'].queryset = Subcounty.objects.filter(county_id=county_id)
            if subcounty_id:
                self.fields['parish'].queryset = Parish.objects.filter(subcounty_id=subcounty_id)
            if parish_id:
                self.fields['village'].queryset = Village.objects.filter(parish_id=parish_id)

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        # Guard against a logo field containing only whitespace (corrupt DB value)
        if logo and hasattr(logo, 'name') and not logo.name.strip():
            return None
        return logo

    def clean_supervisor(self):
        supervisor = self.cleaned_data.get('supervisor')
        if supervisor and len(supervisor) < 2:
            raise forms.ValidationError("Supervisor name must be at least 2 characters.")
        return supervisor

    def clean_latitude(self):
        lat = self.cleaned_data.get('latitude')
        if lat is not None and (lat < -90 or lat > 90):
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return lat

    def clean_longitude(self):
        lon = self.cleaned_data.get('longitude')
        if lon is not None and (lon < -180 or lon > 180):
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return lon

    def clean(self):
        cleaned_data = super().clean()
        supervisor = cleaned_data.get('supervisor')
        if supervisor and self.owner:
            qs = Clinic.objects.filter(owner=self.owner, supervisor=supervisor)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('supervisor', 'You already have another clinic with this supervisor. Supervisor must be unique per owner.')
        return cleaned_data