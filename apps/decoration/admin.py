from django.contrib import admin
from .models import DecorationCategory, DecorationService, DecorationImage, DecorationInquiry


class DecorationImageInline(admin.TabularInline):
    model = DecorationImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(DecorationCategory)
class DecorationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(DecorationService)
class DecorationServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'is_published', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [DecorationImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات خدمت', {
            'fields': ('price', 'duration', 'location')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DecorationInquiry)
class DecorationInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'decoration_service', 'phone', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'decoration_service', 'created_at']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'phone', 'email', 'decoration_service__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات استعلام', {
            'fields': ('decoration_service', 'name', 'phone', 'email', 'message', 'is_read', 'is_replied')
        }),
        ('تاریخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
