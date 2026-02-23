# Medi_Clinics/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def homepage_view(request):
    """Landing page for non-authenticated visitors."""
    return render(request, 'medi_clinics/home.html')

@login_required
def dashboard_redirect(request):
    """Redirect authenticated users to their respective dashboards."""
    if request.user.profile.user_type == 'owner':
        return redirect('clinic_owners:dashboard')
    elif request.user.profile.user_type == 'staff':
        return redirect('staff:dashboard')
    else:
        return redirect('admin:index')