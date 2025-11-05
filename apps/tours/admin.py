from django.contrib import admin
from .models import TourCategory, Tour, TourImage, TourRegistration


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'start_date', 'location', 'price', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'is_published', 'start_date', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [TourImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات تور', {
            'fields': ('start_date', 'end_date', 'duration', 'location', 'price', 'capacity', 'registration_deadline')
        }),
        ('جزئیات تور', {
            'fields': ('includes', 'excludes', 'itinerary')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TourRegistration)
class TourRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'tour', 'phone', 'number_of_people', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'tour', 'created_at']
    list_editable = ['is_confirmed']
    search_fields = ['name', 'phone', 'email', 'tour__title']
    readonly_fields = ['created_at']

