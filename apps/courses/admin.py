from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Course, CourseVideo, Enrollment, QuizQuestion, QuizOption, QuizAttempt, Certificate


class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 1
    fields = ['title', 'order', 'video_url', 'video_file', 'duration', 'must_watch_full']
    ordering = ['order']


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 4
    fields = ['text', 'is_correct', 'order']
    ordering = ['order']


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    fields = ['text', 'order']
    ordering = ['order']
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz_time_limit', 'passing_score', 'max_attempts', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CourseVideoInline, QuizQuestionInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'image', 'short_description', 'description')
        }),
        ('تنظیمات آزمون', {
            'fields': ('quiz_time_limit', 'passing_score', 'max_attempts')
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['course', 'order', 'text_preview', 'options_count', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['text', 'course__title']
    ordering = ['course', 'order']
    inlines = [QuizOptionInline]
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'صورت سوال'
    
    def options_count(self, obj):
        return obj.options.count()
    options_count.short_description = 'تعداد گزینه‌ها'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'attempts_used', 'passed', 'can_retake', 'certificate_code', 'created_at']
    list_filter = ['passed', 'can_retake', 'course', 'created_at']
    list_editable = ['can_retake']
    search_fields = ['user__username', 'course__title', 'certificate_code']
    readonly_fields = ['user', 'course', 'attempts_used', 'passed', 'certificate_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات ثبت‌نام', {
            'fields': ('user', 'course', 'attempts_used', 'passed', 'certificate_code')
        }),
        ('تنظیمات', {
            'fields': ('can_retake', 'created_at', 'updated_at')
        }),
    )
    
    def reset_attempts(self, request, queryset):
        """اکشن برای ریست کردن تلاش‌ها"""
        count = queryset.update(attempts_used=0, can_retake=True)
        self.message_user(request, f'{count} ثبت‌نام ریست شد.')
    reset_attempts.short_description = 'ریست کردن تلاش‌های انتخاب شده'
    
    actions = [reset_attempts]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'score', 'total', 'percentage', 'passed', 'completed', 'time_taken', 'created_at']
    list_filter = ['passed', 'completed', 'enrollment__course', 'created_at']
    search_fields = ['enrollment__user__username', 'enrollment__course__title']
    readonly_fields = ['enrollment', 'answers', 'score', 'total', 'percentage', 'passed', 'time_taken', 'completed', 'created_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'certificate_code', 'issued_at']
    list_filter = ['issued_at', 'enrollment__course']
    search_fields = ['certificate_code', 'enrollment__user__username', 'enrollment__course__title']
    readonly_fields = ['enrollment', 'certificate_code', 'issued_at']
