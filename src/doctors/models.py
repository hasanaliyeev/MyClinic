from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import datetime, date
from django.utils.text import slugify

from other import utils


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


GENDER_SELECT = (
    ('Male', 'Male'),
    ('Female', 'Female'))


class Doctor(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='doctors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='doctors/', default='doctors/default.jpg')
    bio = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, default='-')
    skill = models.TextField()
    state = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if not self.middle_name else f'{self.first_name} {self.last_name} {self.middle_name}'

    def clean(self):
        if not utils.phone_validator(self.phone):
            raise ValidationError('Wrong phone number')

    def save(self, *args, **kwargs):
        self.slug = slugify(utils.slug_generator(self.first_name)) + '-' + slugify(self.last_name) + '-' + slugify(
            self.middle_name)
        self.clean()
        super().save(*args, **kwargs)


class Education(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    starting_date = models.DateField()
    complete_date = models.DateField()
    degree = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.institution} {self.subject}'


class Experience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=100)
    job_position = models.CharField(max_length=50)
    address = models.TextField()
    period_from = models.DateField()
    period_to = models.DateField()

    def __str__(self):
        return f'{self.company_name} - {self.job_position}'


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_from = models.TimeField()
    finish_by = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.doctor} - {self.date} - from {self.start_from} to {self.finish_by}'

    def clean(self):
        if self.start_from > self.finish_by:
            raise ValidationError('Input wrong time')
        qs = Schedule.objects.filter(doctor=self.doctor, date=self.date, start_from=self.start_from,
                                     finish_by=self.finish_by).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Input same date')
        current_date = date.today()
        if self.date < current_date:
            raise ValidationError('Current date error')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.OneToOneField(Schedule, on_delete=models.PROTECT, related_name='appointment')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.doctor} - {self.schedule}'


class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='doctors/specialities/', default='doctors/default.jpg')

    def __str__(self):
        return self.name
