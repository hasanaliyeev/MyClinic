from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test, name='test'),
]