from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from apps.courses.models import Enrollment, Course


def signup_view(request):
    """صفحه عضویت"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد.')
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """صفحه ورود"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    next_url = request.GET.get('next', 'accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


@login_required
def dashboard_view(request):
    """پنل کاربر"""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    certificates = []
    
    for enrollment in enrollments:
        if enrollment.passed and enrollment.certificate_code:
            certificates.append({
                'course': enrollment.course,
                'certificate_code': enrollment.certificate_code,
            })
    
    context = {
        'enrollments': enrollments,
        'certificates': certificates,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def logout_view(request):
    """خروج از حساب"""
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('core:index')

