import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from doctors.models import Doctor, Schedule, Appointment


def doctor_list(request):
    doctors = Doctor.objects.all()
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'action': 'doctors'}
    return render(request, 'doctors/doctors.html', context)


def booking(request, slug):
    context = {}
    doctor = get_object_or_404(Doctor, slug=slug)
    schedule_obj = create_schedule_calendar(doctor)
    print(schedule_obj)
    context['schedule_obj'] = schedule_obj
    context['doctor'] = doctor

    if request.method == 'POST':
        schedule_pk = int(request.POST.get('schedule'))
        schedule = get_object_or_404(Schedule, pk=schedule_pk)
        appointment = Appointment(doctor=doctor, user=request.user, schedule=schedule)
        appointment.save()
    return render(request, 'doctors/booking.html', context)


def make_appointment(request, slug, pk):
    doctor = get_object_or_404(Doctor, slug=slug)
    schedule = get_object_or_404(Schedule, pk=pk)
    appointment = Appointment(doctor=doctor, user=request.user, schedule=schedule)
    appointment.save()
    return redirect('doctors:booking', slug=slug)


def create_schedule_calendar(doctor, start=None):
    start_date = datetime.date.today()
    date_list = [start_date + datetime.timedelta(days=d) for d in range(0, 7)]
    schedule_obj = list()
    for date in date_list:
        date_obj = {}
        schedules = Schedule.objects.filter(doctor=doctor, date=date)
        schedule_list = list()
        if schedules:
            for schedule in schedules:
                schedule_list.append(schedule)
                date_obj[date] = schedule_list
            schedule_obj.append(date_obj)
        else:
            date_obj[date] = list()
            schedule_obj.append(date_obj)

    return schedule_obj


def profile(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    context = {'doctor': doctor}
    return render(request, 'doctors/profile.html', context)
