from django.urls import path
from . import views

app_name = 'siteauth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.handle_login, name='handle_login'),
    path('logout/', views.handle_logout, name='handle_logout'),
]
