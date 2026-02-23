# clinic_owners/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib import messages
from .forms import OwnerRegistrationForm
from clinics.models import Clinic



# clinic_owners/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, CustomPasswordChangeForm, ProfileUpdateForm

@login_required
def profile_view(request):
    if request.user.profile.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    context = {
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'clinic_owners/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('clinic_owners:dashboard')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'clinic_owners/register.html', {'form': form})

@login_required
def update_user_view(request):
    if request.user.profile.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            messages.success(request, 'Login credentials updated successfully.')
            return redirect('clinic_owners:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'clinic_owners/update_user_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

@login_required
def update_profile_view(request):
    if request.user.profile.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('clinic_owners:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'clinic_owners/update_profile.html', {'profile_form': profile_form})


@login_required
def delete_profile_view(request):
    if request.user.profile.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        request.user.profile.delete()
        messages.success(request, 'Profile deleted successfully.')
        return redirect('home')

    return render(request, 'clinic_owners/delete_profile.html')

@login_required
def dashboard_view(request):
    if request.user.profile.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Clinics owned by this user
    clinics = Clinic.objects.filter(owner=request.user).prefetch_related('departments', 'operation_days')

    # For each clinic, add placeholder counts (these will be replaced by real data later)
    for clinic in clinics:
        clinic.staff_count = 0          # placeholder
        clinic.today_appointments = 0   # placeholder
        clinic.inventory_count = 0      # placeholder

    context = {
        'clinics': clinics,
        'register_clinic_url': reverse('clinics:clinic_create'),
    }
    return render(request, 'clinic_owners/dashboard.html', context)



class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'clinic_owners/login.html'
