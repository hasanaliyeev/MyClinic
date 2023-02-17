import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from doctors.models import Department, Doctor, Education, Experience, Schedule, Speciality
from .forms import DepartmentForm, DoctorForm, DoctorEducationForm, DoctorExperienceForm, ScheduleForm, SpecialityForm


def func():
    return lambda u: u.is_staff


def index(request):
    return render(request, 'dashboard/index.html')


def department_create(request):
    context = {}
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            obj = form.instance
            messages.success(request, f'{obj.name} created')
            return redirect('dashboard:department_detail', pk=obj.pk)
        return render(request, 'dashboard/departments/create.html', context)
    else:
        form = DepartmentForm()
        context['form'] = form
    return render(request, 'dashboard/departments/create.html', context)


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    context = {'department': department}
    return render(request, 'dashboard/departments/detail.html', context)


def departments(request):
    objects = Department.objects.all()
    paginator = Paginator(objects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'dashboard/departments/department-list.html', context)


def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    context = {}
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, f'{department.name} updated')
            return redirect('dashboard:department_detail', pk=pk)
        return render(request, 'dashboard/departments/update.html', context)
    else:
        form = DepartmentForm(instance=department)
        context['form'] = form
    return render(request, 'dashboard/departments/update.html', context)


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    try:
        department.delete()
        messages.success(request, f'{department.name} deleted')
    except Exception as err:
        messages.error(request, err)
        return redirect('dashboard:department_detail', pk=pk)
    return redirect('dashboard:department_list')


def add_doctor(request):
    context = {}
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        context['form'] = form
        if form.is_valid():
            form.save()
            obj = form.instance
            return redirect('dashboard:doctor_profile', slug=obj.slug)
        return render(request, 'dashboard/doctors/add-doctor.html', context)
    else:
        form = DoctorForm()
        context['form'] = form
    return render(request, 'dashboard/doctors/add-doctor.html', context)


def doctor_profile(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    context = {'doctor': doctor}
    education_form = DoctorEducationForm()
    context['form'] = education_form
    context['active_page'] = 'doctor_dashboard'
    upcoming_apts = doctor.appointments.order_by('schedule__start_from').filter(schedule__date=datetime.date.today())
    context['upc_apts'] = upcoming_apts
    return render(request, 'dashboard/doctors/profile.html', context)


def doctors(request):
    doctors_list = Doctor.objects.all()
    paginator = Paginator(doctors_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'dashboard/doctors/doctors.html', context)


def doctor_update(request, slug):
    context = {}
    doctor = get_object_or_404(Doctor, slug=slug)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        context['form'] = form
        if form.is_valid():
            form.save()
            obj = form.instance
            return redirect('dashboard:doctor_detail', slug=obj.slug)
        return render(request, 'dashboard/doctors/update.html', context)
    else:
        form = DoctorForm(instance=doctor)
        context['form'] = form
    return render(request, 'dashboard/doctors/update.html', context)


def doctor_delete(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    doctor.delete()
    messages.success(request, f'{doctor.first_name} {doctor.last_name} {doctor.middle_name} deleted')
    return redirect('dashboard:doctors')


def edit_doctor_profile(request, slug):
    context = {}
    doctor = get_object_or_404(Doctor, slug=slug)
    educations = Education.objects.filter(doctor=doctor)
    experiences = Experience.objects.filter(doctor=doctor)
    context['doctor'] = doctor
    context['educations'] = educations
    context['experiences'] = experiences

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('dashboard:edit_doctor_profile', slug=doctor.slug)
        return render(request, 'dashboard/doctors/edit-profile.html', context)
    else:
        form = DoctorForm(instance=doctor)
        context['form'] = form
    return render(request, 'dashboard/doctors/edit-profile.html', context)


def add_doctor_education(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    if request.method == 'POST':
        data = request.POST
        institution = data.get('institution')
        subject = data.get('subject')
        starting_date = data.get('starting_date')
        complete_date = data.get('complete_date')
        degree = data.get('degree')
        grade = data.get('grade')
        education = Education(institution=institution, subject=subject, starting_date=starting_date,
                              complete_date=complete_date, degree=degree, grade=grade, doctor=doctor)
        education.save()
        messages.success(request, 'Education added')
        return redirect('dashboard:edit_doctor_profile', slug=slug)
    return redirect('dashboard:edit_doctor_profile', slug=slug)


def edit_doctor_education(request, pk):
    context = {}
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = DoctorEducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('dashboard:edit_doctor_profile', slug=education.doctor.slug)
        context['form'] = form
        return render(request, 'dashboard/doctors/edit-education.html', context)
    else:
        form = DoctorEducationForm(instance=education)
        context['form'] = form
    return render(request, 'dashboard/doctors/edit-education.html', context)


def delete_doctor_education(request, pk):
    education = get_object_or_404(Education, pk=pk)
    doctor = education.doctor
    education.delete()
    return redirect('dashboard:edit_doctor_profile', slug=doctor.slug)


def add_doctor_experience(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    if request.method == 'POST':
        data = request.POST
        company_name = data.get('company_name')
        job_position = data.get('job_position')
        address = data.get('address')
        period_from = data.get('period_from')
        period_to = data.get('period_to')
        experience = Experience(doctor=doctor, company_name=company_name, job_position=job_position, address=address,
                                period_from=period_from, period_to=period_to)
        experience.save()
        messages.success(request, 'Experience added')
        return redirect('dashboard:edit_doctor_profile', slug=slug)
    return redirect('dashboard:edit_doctor_profile', slug=slug)


def edit_doctor_experience(request, pk):
    context = {}
    experience = get_object_or_404(Experience, pk=pk)
    context['doctor'] = experience.doctor
    if request.method == 'POST':
        form = DoctorExperienceForm(request.POST, instance=experience)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('dashboard:edit_doctor_profile', slug=experience.doctor.slug)
        return render(request, 'dashboard/doctors/edit-experience.html', context)
    else:
        form = DoctorExperienceForm(instance=experience)
        context['form'] = form
    return render(request, 'dashboard/doctors/edit-experience.html', context)


def delete_doctor_experience(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    doctor = experience.doctor
    experience.delete()
    messages.success(request, 'Experience deleted')
    return redirect('dashboard:edit_doctor_profile', slug=doctor.slug)


def doctor_schedules(request, slug):
    context = {}
    active_page = 'schedule'
    doctor = get_object_or_404(Doctor, slug=slug)
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=30)
    schedules = Schedule.objects.filter(doctor=doctor, date__range=[start_date, end_date]).order_by('date',
                                                                                                    'start_from')
    context['doctor'] = doctor
    context['active_page'] = active_page
    context['schedules'] = schedules
    return render(request, 'dashboard/doctors/schedules.html', context)


def search_schedule_day(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    if request.method == 'POST':
        str_date = request.POST.get('date')
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        return redirect('dashboard:day_schedule_list', slug=doctor.slug, year=date.year, month=date.month, day=date.day)
    return render(request, 'dashboard/doctors/schedule-list.html')


def schedule_list(request, slug, year, month, day):
    doctor = get_object_or_404(Doctor, slug=slug)
    context = {'doctor': doctor}
    date = datetime.date(year, month, day)
    context['date'] = date
    schedules = Schedule.objects.filter(doctor=doctor, date=date).order_by('start_from')
    context['schedules'] = schedules
    context['active_page'] = 'schedule'
    return render(request, 'dashboard/doctors/schedule-list.html', context)


def add_schedule(request, slug, year, month, day):
    doctor = get_object_or_404(Doctor, slug=slug)
    date = datetime.date(year, month, day)
    if request.method == 'POST':
        data = request.POST
        start_from = data.get('start_from')
        finish_by = data.get('finish_by')
        is_active = data.get('is_active')
        schedule = Schedule(doctor=doctor, date=date, start_from=start_from, finish_by=finish_by, is_active=is_active)
        schedule.save()
        return redirect('dashboard:day_schedule_list', slug=doctor.slug, year=date.year, month=date.month, day=date.day)
    return redirect('dashboard:day_schedule_list', slug=doctor.slug, year=date.year, month=date.month, day=date.day)


def edit_schedule(request, pk):
    action = 'edit'
    schedule = get_object_or_404(Schedule, pk=pk)
    doctor = schedule.doctor
    date = schedule.date
    schedules = Schedule.objects.filter(doctor=doctor, date=date)
    context = {'doctor': doctor, 'date': date, 'schedules': schedules, 'action': action, 'active_page': 'schedule'}

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('dashboard:day_schedule_list', slug=doctor.slug, year=date.year, month=date.month,
                            day=date.day)
    else:
        form = ScheduleForm(instance=schedule)
        context['form'] = form
    return render(request, 'dashboard/doctors/schedule-list.html', context)


def delete_schedule(request, pk):
    try:
        schedule = get_object_or_404(Schedule, pk=pk)
        doctor = schedule.doctor
        date = schedule.date
        schedule.delete()
        return redirect('dashboard:day_schedule_list', slug=doctor.slug, year=date.year, month=date.month, day=date.day)
    except ValueError:
        pass


def appointments(request, slug):
    context = {}
    doctor = get_object_or_404(Doctor, slug=slug)
    context['doctor'] = doctor
    context['active_page'] = 'appointments_page'
    return render(request, 'dashboard/doctors/appointments.html', context)


def make_appointment(request):
    pass


def specialities(request):
    context = {}
    form = SpecialityForm()
    qs = Speciality.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['active_page'] = 'specialities'
    context['form'] = form
    return render(request, 'dashboard/doctors/specialities.html', context)


def add_speciality(request):
    context = {}
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:specialities')
        messages.error(request, form.error_class.as_text(form.errors))
        return redirect('dashboard:specialities')
    else:
        form = SpecialityForm()
        context['form'] = form
    return render(request, 'dashboard/doctors/specialities.html', context)


def edit_speciality(request, pk):
    context = {}
    speciality = get_object_or_404(Speciality, pk=pk)
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES, instance=speciality)
        if form.is_valid():
            form.save()
            return redirect('dashboard:specialities')
        messages.error(request, form.error_class.as_text(form.errors))
        return redirect('dashboard:specialities')
    else:
        form = SpecialityForm(instance=speciality)
        context['form'] = form
    return render(request, 'dashboard/doctors/specialities.html', context)


def delete_speciality(request, pk):
    speciality = get_object_or_404(Speciality, pk=pk)
    speciality.delete()
    return redirect('dashboard:specialities')
