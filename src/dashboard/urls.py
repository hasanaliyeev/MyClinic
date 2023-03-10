from django.contrib import admin
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='home'),

    path('appointments/', views.appointments, name='appointments'),
    path('appointments/make-appointment/<int:pk>/', views.make_appointment, name='make_appointment'),

    path('doctors/', views.doctors, name='doctors'),
    path('doctors/add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctors/<slug:slug>/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctors/<slug:slug>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<slug:slug>/delete/', views.doctor_delete, name='delete_doctor'),
    path('doctors/<slug:slug>/edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),

    path('doctors/<slug:slug>/add-education/', views.add_doctor_education, name='add_doctor_education'),
    path('doctors/delete-education/<int:pk>/', views.delete_doctor_education, name='delete_doctor_education'),
    path('doctors/edit-education/<int:pk>/', views.edit_doctor_education, name='edit_doctor_education'),

    path('doctors/<slug:slug>/add-experience/', views.add_doctor_experience, name='add_doctor_experience'),
    path('doctors/delete-experience/<int:pk>/', views.delete_doctor_experience, name='delete_doctor_experience'),
    path('doctors/edit-experience/<int:pk>/', views.edit_doctor_experience, name='edit_doctor_experience'),

    path('doctors/<slug:slug>/schedules/', views.schedules, name='schedules'),
    path('doctors/<slug:slug>/schedule-detail/', views.get_schedule_day, name='get_schedule_day'),
    path('doctors/<slug:slug>/schedules/<int:year>/<int:month>/<int:day>/', views.schedule_list,
         name='day_schedule_list'),
    path('doctors/<slug:slug>/schedules/<int:year>/<int:month>/<int:day>/add-schedule/', views.add_schedule,
         name='add_schedule'),
    path('doctors/schedule-delete/<int:pk>/', views.delete_schedule, name='delete_schedule'),
    path('doctors/edit-schedule/<int:pk>/', views.edit_schedule, name='edit_schedule'),

    path('doctors/<slug:slug>/appointments/', views.doctor_appointments, name='doctor_appointments'),

    path('specialities/', views.specialities, name='specialities'),
    path('add-speciality/', views.add_speciality, name='add_speciality'),
    path('delete-speciality/<int:pk>/', views.delete_speciality, name='delete_speciality'),
    path('edit-speciality/<int:pk>/', views.edit_speciality, name='edit_speciality'),


]
