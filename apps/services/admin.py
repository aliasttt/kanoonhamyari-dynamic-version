from django.contrib import admin
from django.utils.html import format_html
from .models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'university_type', 'price', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['university_type', 'is_featured', 'is_active', 'created_at']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'short_description', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'image', 'short_description', 'description')
        }),
        ('قیمت', {
            'fields': ('price', 'price_note')
        }),
        ('اطلاعات کلی', {
            'fields': ('location', 'university_type', 'language', 'ranking')
        }),
        ('اطلاعات جزئی', {
            'fields': ('programs', 'admission_requirements', 'scholarship_info')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
