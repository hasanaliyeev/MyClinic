from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from patients.models import Patient


def signup(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('pass1')
        confirm_password = data.get('pass2')

        if password != confirm_password:
            messages.error(request, 'Password is not matching')
            return redirect('siteauth:signup')

        try:
            if get_object_or_404(User, username=username):
                messages.error(request, 'Username is taken')
                return redirect('siteauth:signup')
        except Exception as identifier:
            pass

        try:
            if get_object_or_404(User, email=email):
                messages.error(request, 'Email is taken')
                return redirect('siteauth:signup')
        except Exception as identifier:
            pass

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()
        patient = Patient(user=user)
        patient.save()
        return redirect('main:home')
    return render(request, 'siteauth/signup.html')


def handle_login(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    if request.method == 'POST':
        data = request.POST
        username = data.get('user')
        password = data.get('password')

        qs = User.objects.filter(email=username).first()

        if qs:
            my_user = authenticate(username=qs.username, password=password)
        else:
            my_user = authenticate(username=username, password=password)

        if my_user is not None:
            login(request, my_user)
            return redirect('main:test')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('siteauth:handle_login')

    return render(request, 'siteauth/login.html')


def handle_logout(request):
    logout(request)
    return redirect('siteauth:handle_login')
