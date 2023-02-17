from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<slug:slug>/booking/', views.booking, name='booking'),
    path('<slug:slug>/profile/', views.profile, name='profile'),
    path('<slug:slug>/make-appointment/<int:pk>/', views.make_appointment, name='make_appointment'),
]