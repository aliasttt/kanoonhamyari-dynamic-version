from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, ServiceCategory, Service, Testimonial, Goal, HeroSlide


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone_1', 'is_active', 'updated_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        # فقط یک رکورد تنظیمات داشته باشیم
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'icon')
        }),
        ('محتوای', {
            'fields': ('short_description', 'description')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'order', 'created_at']
    list_editable = ['rating', 'is_active', 'order']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'content']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title']


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title']

