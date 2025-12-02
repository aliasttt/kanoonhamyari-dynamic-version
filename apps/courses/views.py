from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from math import ceil
import json

from .models import Course, CourseVideo, Enrollment, QuizQuestion, QuizOption, QuizAttempt, Certificate
from .forms import InitialForm


def list_view(request):
    """لیست دوره‌ها - اگر لاگین نبود، به لاگین ریدایرکت می‌شود"""
    if not request.user.is_authenticated:
        messages.info(request, 'لطفاً ابتدا وارد حساب کاربری خود شوید.')
        return redirect(reverse('accounts:login') + '?next=' + reverse('courses:list'))
    
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'courses/list.html', {'courses': courses})


@login_required
def detail_view(request, slug):
    """صفحه جزئیات دوره با تب‌های ویدیو، کوییز و موفقیت"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    
    videos = course.videos.all()
    questions = course.questions.all()
    active_tab = request.GET.get('tab', 'videos')
    
    # بررسی وضعیت کوییز
    can_take_quiz = enrollment.can_attempt_quiz()
    current_attempt = None
    quiz_in_progress = False
    
    # بررسی اینکه آیا کوییز در حال انجام است
    ongoing_attempt = QuizAttempt.objects.filter(
        enrollment=enrollment,
        completed=False
    ).first()
    if ongoing_attempt:
        quiz_in_progress = True
    
    if active_tab == 'quiz' and can_take_quiz:
        # ایجاد یا دریافت تلاش فعلی
        current_attempt = QuizAttempt.objects.filter(
            enrollment=enrollment,
            completed=False
        ).first()
        
        if not current_attempt:
            current_attempt = QuizAttempt.objects.create(
                enrollment=enrollment,
                answers={},
                total=questions.count()
            )
    
    # آخرین تلاش تکمیل شده
    last_completed_attempt = enrollment.attempts.filter(completed=True).first()
    
    # بارگذاری پاسخ‌های ذخیره شده
    saved_answers = {}
    if current_attempt:
        saved_answers = current_attempt.answers or {}
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'videos': videos,
        'questions': questions,
        'active_tab': active_tab,
        'can_take_quiz': can_take_quiz,
        'current_attempt': current_attempt,
        'last_completed_attempt': last_completed_attempt,
        'quiz_time_limit': course.quiz_time_limit * 60,  # تبدیل به ثانیه
        'saved_answers': saved_answers,
        'quiz_in_progress': quiz_in_progress,
    }
    
    return render(request, 'courses/detail.html', context)


@login_required
@require_POST
def quiz_answer_view(request, slug, question_id):
    """ذخیره پاسخ یک سوال"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    question = get_object_or_404(QuizQuestion, id=question_id, course=course)
    
    if not enrollment.can_attempt_quiz():
        return JsonResponse({'error': 'شما نمی‌توانید در این آزمون شرکت کنید.'}, status=403)
    
    # دریافت یا ایجاد تلاش فعلی
    current_attempt = QuizAttempt.objects.filter(
        enrollment=enrollment,
        completed=False
    ).first()
    
    if not current_attempt:
        current_attempt = QuizAttempt.objects.create(
            enrollment=enrollment,
            answers={},
            total=course.questions.count()
        )
    
    # بارگذاری پاسخ‌های قبلی
    saved_answers = current_attempt.answers or {}
    
    # ذخیره پاسخ
    option_id = request.POST.get('option_id')
    if option_id:
        try:
            option = QuizOption.objects.get(id=int(option_id), question=question)
            current_attempt.answers[f'question_{question.id}'] = option_id
            current_attempt.save(update_fields=['answers'])
            return JsonResponse({'success': True, 'message': 'پاسخ ذخیره شد.'})
        except (QuizOption.DoesNotExist, ValueError):
            return JsonResponse({'error': 'گزینه نامعتبر است.'}, status=400)
    
    return JsonResponse({'error': 'پاسخ ارسال نشد.'}, status=400)


@login_required
@require_POST
def quiz_submit_view(request, slug):
    """ارسال نهایی آزمون و محاسبه نمره"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if not enrollment.can_attempt_quiz():
        messages.error(request, 'شما نمی‌توانید در این آزمون شرکت کنید.')
        return redirect('courses:detail', slug=slug)
    
    questions = list(course.questions.all())
    if not questions:
        raise Http404("سوالی تعریف نشده است.")

    # دریافت تلاش فعلی
    current_attempt = QuizAttempt.objects.filter(
        enrollment=enrollment,
        completed=False
    ).first()
    
    if not current_attempt:
        current_attempt = QuizAttempt.objects.create(
            enrollment=enrollment,
            answers={},
            total=len(questions)
        )
    
    # دریافت زمان صرف شده
    time_taken = int(request.POST.get('time_taken', 0))
    current_attempt.time_taken = time_taken
    current_attempt.completed = True
    current_attempt.save(update_fields=['time_taken', 'completed'])
    
    # محاسبه نمره
    current_attempt.calculate_score(questions)
    
    # به‌روزرسانی enrollment
    enrollment.attempts_used += 1
    
    if current_attempt.passed:
        enrollment.passed = True
        enrollment.generate_certificate_code()
        # ایجاد گواهینامه
        Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={'certificate_code': enrollment.certificate_code}
        )
        messages.success(request, f'تبریک! شما با نمره {current_attempt.percentage:.1f}% قبول شدید.')
    else:
        remaining = max(0, course.max_attempts - enrollment.attempts_used)
        if remaining > 0:
            messages.warning(request, f'نمره شما {current_attempt.percentage:.1f}% بود. {remaining} تلاش دیگر دارید.')
        else:
            messages.error(request, f'نمره شما {current_attempt.percentage:.1f}% بود. تلاش‌ها به پایان رسید.')
    
    enrollment.save(update_fields=['attempts_used', 'passed', 'certificate_code'])

    return redirect('courses:detail', slug=slug) + '?tab=success'


@login_required
def certificate_view(request, slug):
    """نمایش گواهینامه"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if not enrollment.passed:
        return HttpResponseForbidden('گواهینامه در دسترس نیست.')
    
    certificate = Certificate.objects.filter(enrollment=enrollment).first()
    
    return render(request, 'courses/certificate.html', {
        'course': course,
        'enrollment': enrollment,
        'certificate': certificate,
    })
