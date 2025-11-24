from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignupForm, LoginForm
from apps.courses.models import Enrollment


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('accounts:dashboard')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'ورود با موفقیت انجام شد.')
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('core:index')


@login_required
def dashboard_view(request):
    certificates = Enrollment.objects.filter(user=request.user, passed=True).select_related('course')
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course').order_by('-created_at')
    return render(request, 'accounts/dashboard.html', {
        'certificates': certificates,
        'enrollments': enrollments,
    })


