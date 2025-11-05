from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogImage, BlogComment


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'is_active', 'is_published', 'views_count', 'published_at', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'is_published', 'published_at', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'author']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [BlogImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'title', 'slug', 'image', 'short_description', 'content', 'author')
        }),
        ('تنظیمات', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'published_at', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'post', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'content', 'post__title']
    readonly_fields = ['created_at']

