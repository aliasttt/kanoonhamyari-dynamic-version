from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره‌ها'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})


class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', verbose_name='دوره')
    title = models.CharField(max_length=200, verbose_name='عنوان ویدیو')
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='ترتیب')
    video_url = models.URLField(blank=True, null=True, verbose_name='آدرس ویدیو')
    video_file = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name='فایل ویدیو')
    must_watch_full = models.BooleanField(default=True, verbose_name='باید کامل تماشا شود')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیوها'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='کاربر')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='دوره')
    initial_form_data = models.JSONField(blank=True, null=True, verbose_name='اطلاعات فرم اولیه')
    current_step = models.PositiveIntegerField(default=0, verbose_name='گام فعلی')
    attempts_used = models.PositiveIntegerField(default=0, verbose_name='تعداد تلاش‌های مصرف شده')
    passed = models.BooleanField(default=False, verbose_name='قبول شده')
    certificate_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='کد مدرک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'ثبت‌نام دوره'
        verbose_name_plural = 'ثبت‌نام‌های دوره'
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def can_attempt_quiz(self):
        return self.attempts_used < 3 and not self.passed


class QuizQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', verbose_name='دوره')
    text = models.TextField(verbose_name='صورت سوال')
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='ترتیب')

    class Meta:
        verbose_name = 'سوال'
        verbose_name_plural = 'سوالات'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - سوال {self.order}"


class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options', verbose_name='سوال')
    text = models.CharField(max_length=500, verbose_name='گزینه')
    is_correct = models.BooleanField(default=False, verbose_name='گزینه صحیح')

    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه‌ها'

    def __str__(self):
        return f"گزینه برای {self.question_id}"


class QuizAttempt(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attempts', verbose_name='ثبت‌نام')
    score = models.PositiveIntegerField(default=0, verbose_name='امتیاز')
    total = models.PositiveIntegerField(default=0, verbose_name='کل سوالات')
    passed = models.BooleanField(default=False, verbose_name='قبول شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تلاش آزمون'
        verbose_name_plural = 'تلاش‌های آزمون'
        ordering = ['-created_at']

    def __str__(self):
        return f"Attempt {self.id} - {self.enrollment.user.username} - {self.score}/{self.total}"





