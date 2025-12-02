from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone
import secrets


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    short_description = models.TextField(blank=True, null=True, verbose_name='توضیحات کوتاه')
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    quiz_time_limit = models.PositiveIntegerField(default=30, verbose_name='زمان آزمون (دقیقه)')
    passing_score = models.PositiveIntegerField(default=50, verbose_name='حداقل نمره قبولی (درصد)')
    max_attempts = models.PositiveIntegerField(default=3, verbose_name='حداکثر تعداد تلاش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره‌ها'
        ordering = ['-created_at']

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
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='ترتیب')
    video_url = models.URLField(blank=True, null=True, verbose_name='آدرس ویدیو')
    video_file = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name='فایل ویدیو')
    duration = models.CharField(max_length=20, blank=True, null=True, verbose_name='مدت زمان')
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
    attempts_used = models.PositiveIntegerField(default=0, verbose_name='تعداد تلاش‌های مصرف شده')
    passed = models.BooleanField(default=False, verbose_name='قبول شده')
    certificate_code = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name='کد مدرک')
    can_retake = models.BooleanField(default=True, verbose_name='می‌تواند دوباره امتحان دهد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'ثبت‌نام دوره'
        verbose_name_plural = 'ثبت‌نام‌های دوره'
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def can_attempt_quiz(self):
        """بررسی اینکه آیا کاربر می‌تواند امتحان بدهد"""
        if self.passed:
            return False
        if self.attempts_used >= self.course.max_attempts:
            return self.can_retake
        return True

    def generate_certificate_code(self):
        """تولید کد یکتا برای سرتیفیکیت"""
        if not self.certificate_code:
            self.certificate_code = f"CERT-{secrets.token_hex(8).upper()}"
            self.save(update_fields=['certificate_code'])
        return self.certificate_code


class QuizQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', verbose_name='دوره')
    text = models.TextField(verbose_name='صورت سوال')
    order = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='ترتیب')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')

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
    order = models.PositiveIntegerField(default=1, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه‌ها'
        ordering = ['order']

    def __str__(self):
        return f"گزینه {self.order} برای سوال {self.question.id}"


class QuizAttempt(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attempts', verbose_name='ثبت‌نام')
    answers = models.JSONField(default=dict, verbose_name='پاسخ‌ها')
    score = models.PositiveIntegerField(default=0, verbose_name='امتیاز')
    total = models.PositiveIntegerField(default=0, verbose_name='کل سوالات')
    percentage = models.FloatField(default=0.0, verbose_name='درصد')
    passed = models.BooleanField(default=False, verbose_name='قبول شده')
    time_taken = models.PositiveIntegerField(default=0, verbose_name='زمان صرف شده (ثانیه)')
    completed = models.BooleanField(default=False, verbose_name='تکمیل شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'تلاش آزمون'
        verbose_name_plural = 'تلاش‌های آزمون'
        ordering = ['-created_at']

    def __str__(self):
        return f"Attempt {self.id} - {self.enrollment.user.username} - {self.score}/{self.total}"

    def calculate_score(self, questions):
        """محاسبه نمره بر اساس سوالات و پاسخ‌ها"""
        total = len(questions)
        correct = 0
        
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in self.answers:
                try:
                    option_id = int(self.answers[answer_key])
                    option = QuizOption.objects.get(id=option_id, question=question)
                    if option.is_correct:
                        correct += 1
                except (QuizOption.DoesNotExist, ValueError, TypeError):
                    pass
        
        self.score = correct
        self.total = total
        self.percentage = (correct / total * 100) if total > 0 else 0
        self.passed = self.percentage >= self.enrollment.course.passing_score
        self.save(update_fields=['score', 'total', 'percentage', 'passed'])


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate', verbose_name='ثبت‌نام')
    certificate_code = models.CharField(max_length=32, unique=True, verbose_name='کد مدرک')
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ صدور')
    
    class Meta:
        verbose_name = 'گواهینامه'
        verbose_name_plural = 'گواهینامه‌ها'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"Certificate - {self.enrollment.user.username} - {self.enrollment.course.title}"
