from django.contrib import admin
from .models import Course, CourseVideo, Enrollment, QuizQuestion, QuizOption, QuizAttempt


class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 1
    fields = ('title', 'order', 'video_url', 'video_file', 'must_watch_full')
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseVideoInline]
    search_fields = ('title',)
    list_filter = ('is_active',)


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2
    fields = ('text', 'is_correct')


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'order', 'text')
    inlines = [QuizOptionInline]
    ordering = ('course', 'order')
    list_filter = ('course',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'attempts_used', 'passed', 'created_at')
    list_filter = ('passed', 'course')
    search_fields = ('user__username', 'user__email')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'score', 'total', 'passed', 'created_at')
    list_filter = ('passed',)





