from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from clinics.models import Clinic
from .forms import InventoryItemForm
from .models import InventoryItem


@login_required
def inventory_add_view(request, clinic_pk):
    clinic = get_object_or_404(Clinic, pk=clinic_pk, owner=request.user)

    if request.method == "POST":
        form = InventoryItemForm(request.POST, clinic=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{form.instance.brand_name}' added to inventory.")
            return redirect(reverse("clinics:clinic_dashboard", args=[clinic_pk]))
    else:
        form = InventoryItemForm(clinic=clinic)

    context = {
        "form":             form,
        "clinic":           clinic,
        "title":            "Add Inventory Item",
        "use_sidebar":      True,
        "sb_dashboard_url": reverse("clinics:clinic_dashboard", args=[clinic_pk]),
        "sb_inventory_url": f"/clinics/{clinic_pk}/inventory/add/",
        "sb_add_item_url":  f"/clinics/{clinic_pk}/inventory/add/",
        "sb_profile_url":   reverse("clinics:clinic_detail",    args=[clinic_pk]),
        "sb_staff_url":     "#",
        "sb_reports_url":   "#",
    }
    return render(request, "inventory/inventory_form.html", context)


@login_required
def inventory_edit_view(request, clinic_pk, item_pk):
    clinic = get_object_or_404(Clinic, pk=clinic_pk, owner=request.user)
    item   = get_object_or_404(InventoryItem, pk=item_pk, clinic=clinic)

    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item, clinic=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{item.brand_name}' updated successfully.")
            return redirect(reverse("clinics:clinic_dashboard", args=[clinic_pk]))
    else:
        form = InventoryItemForm(instance=item, clinic=clinic)

    context = {
        "form":             form,
        "clinic":           clinic,
        "title":            f"Edit — {item.brand_name}",
        "use_sidebar":      True,
        "sb_dashboard_url": reverse("clinics:clinic_dashboard", args=[clinic_pk]),
        "sb_inventory_url": f"/clinics/{clinic_pk}/inventory/add/",
        "sb_add_item_url":  f"/clinics/{clinic_pk}/inventory/add/",
        "sb_profile_url":   reverse("clinics:clinic_detail",    args=[clinic_pk]),
        "sb_staff_url":     "#",
        "sb_reports_url":   "#",
    }
    return render(request, "inventory/inventory_form.html", context)