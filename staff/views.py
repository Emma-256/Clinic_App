from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StaffRegistrationForm


@login_required
def register_staff(request):
    # Only clinic owners can register staff
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'owner':
        messages.error(request, "You are not authorized to register staff.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, request.FILES, owner=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member registered successfully.")
            return redirect('staff:staff_list')
    else:
        form = StaffRegistrationForm(owner=request.user)

    return render(request, 'staff/staff_form.html', {'form': form})