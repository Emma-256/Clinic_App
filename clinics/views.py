from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets

from .models import Clinic, District, County, Subcounty, Parish, Village
from .forms import ClinicForm
from .serializers import (
    DistrictSerializer, CountySerializer,
    SubcountySerializer, ParishSerializer, VillageSerializer
)

@login_required
def clinic_create(request, pk):
    """Create a new clinic for the logged-in owner"""
    pk=pk
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'owner':
        raise PermissionDenied("Only owners can register clinics.")

    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES, owner=request.user)
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.owner = request.user
            clinic.save()
            form.save_m2m()
            messages.success(request, 'Clinic created successfully.')
            return redirect('clinics:clinic_detail', pk=clinic.pk)
    else:
        form = ClinicForm(owner=request.user)

    return render(request, 'clinics/clinic_form.html', {'form': form, 'title': 'Register Clinic'})


@login_required
def clinic_edit(request, pk):
    """Edit an existing clinic"""
    clinic = get_object_or_404(
        Clinic.objects.select_related('owner', 'district', 'county', 'sub_county', 'parish', 'village'),
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES, instance=clinic, owner=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clinic updated successfully.')
            return redirect('clinics:clinic_detail', pk=clinic.pk)
    else:
        form = ClinicForm(instance=clinic, owner=request.user)
        context = {
                    'form': form, 
                    'title': 'Edit Clinic',
                    'clinic': clinic,
                    'clinics_dashboard': reverse('clinics:dashboard', kwargs={'pk': clinic.pk})}
    return render(request, 'clinics/clinic_form.html',context)


@login_required
def clinic_delete(request, pk):
    """Soft delete a clinic"""
    clinic = get_object_or_404(Clinic, pk=pk, owner=request.user)

    if request.method == 'POST':
        clinic.is_active = False
        clinic.save()
        messages.success(request, 'Clinic deactivated successfully.')
        return redirect('clinic_owners:dashboard')

    return render(request, 'clinics/clinic_confirm_delete.html', {'clinic': clinic})


@login_required
def clinic_detail(request, pk):
    """Detailed view of a single clinic"""
    clinic = get_object_or_404(
        Clinic.objects.select_related(
            'owner', 'district', 'county', 'sub_county', 'parish', 'village'
        ).prefetch_related('departments', 'operation_days'),
        pk=pk,
        owner=request.user,
        is_active=True
    )
    context = {
    'clinic': clinic,
    'clinics_dashboard': reverse('clinics:dashboard', kwargs={'pk': clinic.pk})
        }
    return render(request, 'clinics/clinic_detail.html',context )

@login_required
def clinic_dashboard_view(request, pk):
    """Dashboard for a specific clinic – owner only."""
    clinic = get_object_or_404(Clinic, pk=pk, owner=request.user)

    # Dummy data for other sections
    dummy_staff = [
        {'name': 'Dr. John Doe', 'role': 'Doctor', 'status': 'Active'},
        {'name': 'Nurse Jane Smith', 'role': 'Nurse', 'status': 'On Leave'},
        {'name': 'Receptionist Amy', 'role': 'Receptionist', 'status': 'Active'},
    ]
    dummy_inventory = [
        {'item': 'Paracetamol', 'quantity': 150, 'expiry': '2025-12-31'},
        {'item': 'Syringes', 'quantity': 500, 'expiry': '2026-06-30'},
    ]
    dummy_reports = [
        {'name': 'Monthly Revenue', 'date': 'Feb 2025', 'url': '#'},
        {'name': 'Patient Visits', 'date': 'Feb 2025', 'url': '#'},
    ]

    context = {
        'clinic': clinic,
        'dummy_staff': dummy_staff,
        'dummy_inventory': dummy_inventory,
        'dummy_reports': dummy_reports,
    }
    return render(request, 'clinics/clinic_dashboard.html', context)


























# ========== API ViewSets ==========

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all().order_by('name')
    serializer_class = DistrictSerializer


class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CountySerializer

    def get_queryset(self):
        district_id = self.request.GET.get('district')
        if district_id:
            return County.objects.filter(district_id=district_id)
        return County.objects.none()


class SubcountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubcountySerializer

    def get_queryset(self):
        county_id = self.request.GET.get('county')
        if county_id:
            return Subcounty.objects.filter(county_id=county_id)
        return Subcounty.objects.none()


class ParishViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParishSerializer

    def get_queryset(self):
        subcounty_id = self.request.GET.get('subcounty')
        if subcounty_id:
            return Parish.objects.filter(subcounty_id=subcounty_id)
        return Parish.objects.none()


class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VillageSerializer

    def get_queryset(self):
        parish_id = self.request.GET.get('parish')
        if parish_id:
            return Village.objects.filter(parish_id=parish_id)
        return Village.objects.none()