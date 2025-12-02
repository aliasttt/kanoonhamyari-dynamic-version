from django.contrib import admin
from .models import AdvertisingCategory, Advertisement, AdvertisementImage, AdvertisementInquiry


class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(AdvertisingCategory)
class AdvertisingCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'is_published', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [AdvertisementImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات تبلیغ', {
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


@admin.register(AdvertisementInquiry)
class AdvertisementInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'advertisement', 'phone', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'advertisement', 'created_at']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'phone', 'email', 'advertisement__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات استعلام', {
            'fields': ('advertisement', 'name', 'phone', 'email', 'message', 'is_read', 'is_replied')
        }),
        ('تاریخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
