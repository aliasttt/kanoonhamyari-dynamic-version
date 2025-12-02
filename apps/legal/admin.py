from django.contrib import admin
from .models import LegalCategory, LegalService, LegalImage, LegalInquiry


class LegalImageInline(admin.TabularInline):
    model = LegalImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(LegalCategory)
class LegalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(LegalService)
class LegalServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_24_7', 'rating', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_24_7', 'is_featured', 'is_active', 'is_published', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published', 'is_24_7']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [LegalImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات خدمت', {
            'fields': ('price', 'duration', 'location', 'is_24_7', 'rating')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LegalInquiry)
class LegalInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'legal_service', 'phone', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'legal_service', 'created_at']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'phone', 'email', 'legal_service__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات استعلام', {
            'fields': ('legal_service', 'name', 'phone', 'email', 'message', 'is_read', 'is_replied')
        }),
        ('تاریخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
