from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('profile-setting/', views.profile_setting, name='profile_setting'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
