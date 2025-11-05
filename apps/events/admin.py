from django.contrib import admin
from django.utils.html import format_html
from .models import EventCategory, Event, EventImage, EventRegistration


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'location', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'is_published', 'event_date', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [EventImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات رویداد', {
            'fields': ('event_date', 'location', 'address', 'price', 'capacity', 'registration_deadline')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'phone', 'number_of_people', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'event', 'created_at']
    list_editable = ['is_confirmed']
    search_fields = ['name', 'phone', 'email', 'event__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات ثبت‌نام', {
            'fields': ('event', 'name', 'phone', 'email', 'number_of_people', 'message', 'is_confirmed')
        }),
        ('تاریخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

