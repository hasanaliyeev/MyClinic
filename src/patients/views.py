from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from doctors.models import Appointment
from .forms import PatientForm
from .models import Patient


def dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    context = {'action': 'dashboard'}
    appointments = Appointment.objects.filter(user=request.user)
    context['appointments'] = appointments
    return render(request, 'patients/dashboard.html', context)


def profile_setting(request):
    context = {}
    patient = get_object_or_404(Patient, user=request.user)
    context['action'] = 'profile_setting'
    if not request.user.is_authenticated:
        if request.user != patient.user:
            return redirect('patients:profile_setting', slug=request.user.patient.slug)
    else:
        return redirect('siteauth:handle_login')

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('patients:profile_setting')
        context['form'] = form
        return render(request, 'patients/profile-settings.html', context)
    else:
        form = PatientForm(instance=patient)
        context['form'] = form
    return render(request, 'patients/profile-settings.html', context)
