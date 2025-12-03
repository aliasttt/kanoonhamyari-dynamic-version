from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'پروفایل'
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'gender', 'birth_date', 'mobile')
        }),
        ('اطلاعات آدرس', {
            'fields': ('country', 'city', 'district', 'full_address', 'postal_code', 'landline')
        }),
        ('اطلاعات شغلی', {
            'fields': ('current_job', 'field_of_activity', 'company_name', 'job_position', 
                      'years_of_experience', 'website', 'linkedin', 'instagram')
        }),
        ('اطلاعات تحصیلی', {
            'fields': ('education_level', 'field_of_study', 'university', 'graduation_year')
        }),
        ('ترجیحات', {
            'fields': ('favorite_categories', 'preferred_content_type', 'preferred_message_hours', 
                      'followed_topics', 'how_did_you_hear')
        }),
        ('سایر', {
            'fields': ('terms_accepted', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)



