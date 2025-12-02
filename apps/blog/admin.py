from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    BlogCategory, BlogPost, BlogImage, BlogComment,
    Tag, NewsletterSection, NewsletterSubscriber,
    NewsletterCampaign, NewsletterAnalytics
)


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px;">{}</span>',
            obj.color, obj.color
        )
    color_preview.short_description = 'رنگ'


@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section_type', 'order', 'is_active', 'max_items', 'created_at']
    list_editable = ['order', 'is_active', 'max_items']
    list_filter = ['section_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'newsletter_section', 'author', 'is_featured', 'is_active', 'is_published', 'views_count', 'published_at', 'scheduled_at', 'created_at']
    list_filter = ['category', 'newsletter_section', 'tags', 'is_featured', 'is_active', 'is_published', 'published_at', 'created_at']
    list_editable = ['is_featured', 'is_active', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'subtitle', 'content', 'author']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
    inlines = [BlogImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('category', 'newsletter_section', 'title', 'subtitle', 'slug', 'image', 'short_description', 'content', 'author', 'tags')
        }),
        ('تنظیمات انتشار', {
            'fields': ('order', 'is_featured', 'is_active', 'is_published', 'published_at', 'scheduled_at', 'views_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # اگر scheduled_at تنظیم شده و published_at خالی است، منتشر نشود
        if obj.scheduled_at and not obj.published_at:
            if obj.scheduled_at <= timezone.now():
                obj.published_at = timezone.now()
                obj.is_published = True
        elif not obj.published_at and obj.is_published:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'post', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'content', 'post__title']
    readonly_fields = ['created_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'tags', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email', 'name']
    filter_horizontal = ['tags']
    readonly_fields = ['unsubscribe_token', 'subscribed_at', 'unsubscribed_at']
    
    fieldsets = (
        ('اطلاعات اشتراک‌کننده', {
            'fields': ('email', 'name', 'tags', 'is_active')
        }),
        ('اطلاعات فنی', {
            'fields': ('unsubscribe_token', 'subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )


class NewsletterCampaignPostInline(admin.TabularInline):
    model = NewsletterCampaign.posts.through
    extra = 1
    verbose_name = 'پست'
    verbose_name_plural = 'پست‌ها'


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'is_sent', 'sent_count', 'opened_count', 'clicked_count', 'sent_at', 'created_at', 'preview_link', 'send_link']
    list_filter = ['is_sent', 'scheduled_at', 'sent_at', 'created_at']
    search_fields = ['title', 'subject']
    readonly_fields = ['sent_count', 'opened_count', 'clicked_count', 'sent_at', 'created_at', 'html_content']
    filter_horizontal = ['sections', 'tags']
    inlines = [NewsletterCampaignPostInline]
    
    fieldsets = (
        ('اطلاعات کمپین', {
            'fields': ('title', 'subject', 'sections', 'tags')
        }),
        ('آمار', {
            'fields': ('sent_count', 'opened_count', 'clicked_count', 'is_sent', 'sent_at'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('scheduled_at',)
        }),
        ('محتوای HTML', {
            'fields': ('html_content',),
            'classes': ('collapse',)
        }),
        ('تاریخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_sent:
            return self.readonly_fields + ('title', 'subject', 'sections', 'tags', 'scheduled_at')
        return self.readonly_fields
    
    def preview_link(self, obj):
        if obj.id:
            return format_html(
                '<a href="/blog/preview/{}/" target="_blank" style="background: #4CAF50; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none;">پیش‌نمایش</a>',
                obj.id
            )
        return '-'
    preview_link.short_description = 'پیش‌نمایش'
    
    def send_link(self, obj):
        if obj.id and not obj.is_sent:
            return format_html(
                '<a href="/blog/send/{}/" style="background: #ff6b35; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none;" onclick="return confirm(\'آیا مطمئن هستید که می‌خواهید این خبرنامه را ارسال کنید؟\');">ارسال</a>',
                obj.id
            )
        return '-'
    send_link.short_description = 'ارسال'


@admin.register(NewsletterAnalytics)
class NewsletterAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'subscriber', 'is_opened', 'is_clicked', 'clicked_url', 'opened_at', 'clicked_at']
    list_filter = ['is_opened', 'is_clicked', 'campaign', 'created_at']
    search_fields = ['campaign__title', 'subscriber__email', 'clicked_url']
    readonly_fields = ['campaign', 'subscriber', 'is_opened', 'opened_at', 'is_clicked', 'clicked_url', 'clicked_at', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
