from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from math import ceil

from .models import Course, CourseVideo, Enrollment, QuizQuestion, QuizOption, QuizAttempt
from .forms import InitialForm, QuizForm


def list_view(request):
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'courses/list.html', {'courses': courses})


@login_required
def detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    videos = list(course.videos.all()[:6])
    questions = course.questions.all()

    initial_form = None
    if enrollment.initial_form_data:
        initial_form_submitted = True
    else:
        initial_form_submitted = False
        if request.method == 'POST' and request.POST.get('action') == 'initial_form':
            initial_form = InitialForm(request.POST)
            if initial_form.is_valid():
                enrollment.initial_form_data = initial_form.cleaned_data
                enrollment.current_step = 1
                enrollment.save(update_fields=['initial_form_data', 'current_step'])
                messages.success(request, 'فرم اولیه با موفقیت ثبت شد.')
                return redirect(course.get_absolute_url())
        else:
            initial_form = InitialForm()

    return render(request, 'courses/detail.html', {
        'course': course,
        'enrollment': enrollment,
        'videos': videos,
        'initial_form': initial_form,
        'initial_form_submitted': initial_form_submitted,
        'questions': questions,
    })


@login_required
def quiz_submit_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    questions = list(course.questions.all())
    if not questions:
        raise Http404("سوالی تعریف نشده است.")

    if not enrollment.can_attempt_quiz():
        messages.error(request, 'حداکثر سه تلاش مجاز است یا قبلاً قبول شده‌اید.')
        return redirect(course.get_absolute_url())

    if request.method != 'POST':
        return HttpResponseForbidden('Method not allowed')

    # Evaluate answers
    total = len(questions)
    correct = 0
    for q in questions:
        chosen = request.POST.get(f'question_{q.id}')
        if not chosen:
            continue
        try:
            option = QuizOption.objects.get(id=int(chosen), question=q)
            if option.is_correct:
                correct += 1
        except (QuizOption.DoesNotExist, ValueError):
            pass

    passed = correct >= ceil(total / 2)

    # Save attempt and update enrollment
    attempt = QuizAttempt.objects.create(
        enrollment=enrollment,
        score=correct,
        total=total,
        passed=passed,
    )
    enrollment.attempts_used += 1
    if passed:
        enrollment.passed = True
        if not enrollment.certificate_code:
            enrollment.certificate_code = f"CERT-{enrollment.id:06d}"
    enrollment.save(update_fields=['attempts_used', 'passed', 'certificate_code'])

    if passed:
        messages.success(request, f'تبریک! با امتیاز {correct} از {total} قبول شدید.')
    else:
        remaining = max(0, 3 - enrollment.attempts_used)
        if remaining:
            messages.warning(request, f'نمره شما {correct} از {total} بود. {remaining} تلاش دیگر دارید.')
        else:
            messages.error(request, f'نمره شما {correct} از {total} بود. تلاش‌ها به پایان رسید.')

    return redirect(course.get_absolute_url() + "#quiz")


@login_required
def certificate_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if not enrollment.passed:
        return HttpResponseForbidden('گواهینامه در دسترس نیست.')
    return render(request, 'courses/certificate.html', {
        'course': course,
        'enrollment': enrollment,
    })










