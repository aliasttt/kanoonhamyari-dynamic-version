from django.contrib import admin
from .models import PropertyType, Property, PropertyImage, PropertyInquiry


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'status', 'location', 'price', 'area', 'is_featured', 'is_active', 'is_published', 'views_count', 'created_at']
    list_filter = ['property_type', 'status', 'is_featured', 'is_active', 'is_published', 'has_parking', 'has_elevator', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'location', 'address']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('property_type', 'title', 'slug', 'image', 'short_description', 'description')
        }),
        ('اطلاعات ملک', {
            'fields': ('status', 'price', 'area', 'rooms', 'bathrooms', 'location', 'address', 'google_maps_url')
        }),
        ('ویژگی‌ها', {
            'fields': ('has_parking', 'has_elevator', 'has_balcony', 'has_garden', 'is_furnished')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'property', 'phone', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'property', 'created_at']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'phone', 'email', 'property__title']
    readonly_fields = ['created_at']

