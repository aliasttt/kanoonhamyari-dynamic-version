from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse
import uuid


class BlogCategory(models.Model):
    """دسته‌بندی پست‌های وبلاگ"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی پست'
        verbose_name_plural = 'دسته‌بندی پست‌ها'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """تگ‌های پست‌های وبلاگ برای فیلتر کردن"""
    name = models.CharField(max_length=100, unique=True, verbose_name='نام تگ')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    color = models.CharField(max_length=7, default='#ff6b35', verbose_name='رنگ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class NewsletterSection(models.Model):
    """بخش‌های خبرنامه (Featured News, Latest Articles, Promotions, Tips)"""
    SECTION_TYPES = [
        ('featured', 'اخبار ویژه'),
        ('latest', 'آخرین مقالات'),
        ('promotions', 'پیشنهادات ویژه'),
        ('tips', 'نکات و راهنما'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='نام بخش')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='latest', verbose_name='نوع بخش')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    max_items = models.IntegerField(default=6, verbose_name='حداکثر تعداد آیتم‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'بخش خبرنامه'
        verbose_name_plural = 'بخش‌های خبرنامه'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """پست‌های وبلاگ"""
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='دسته‌بندی')
    newsletter_section = models.ForeignKey('NewsletterSection', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='بخش خبرنامه')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name='زیرعنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    content = RichTextField(verbose_name='محتوای کامل')
    image = models.ImageField(upload_to='blog/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('BlogImage', blank=True, related_name='post_galleries', verbose_name='گالری تصاویر')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name='تگ‌ها')
    
    author = models.CharField(max_length=200, default='مدیر سایت', verbose_name='نویسنده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name='زمان برنامه‌ریزی شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'پست وبلاگ'
        verbose_name_plural = 'پست‌های وبلاگ'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


class BlogImage(models.Model):
    """تصاویر گالری پست"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image = models.ImageField(upload_to='blog/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر پست'
        verbose_name_plural = 'تصاویر پست'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.post.title} - تصویر {self.order}"


class BlogComment(models.Model):
    """نظرات پست‌های وبلاگ"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    content = models.TextField(verbose_name='نظر')
    is_approved = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.post.title}"


class NewsletterSubscriber(models.Model):
    """اشتراک‌کنندگان خبرنامه"""
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='نام')
    tags = models.ManyToManyField('Tag', blank=True, related_name='subscribers', verbose_name='تگ‌های مورد علاقه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='توکن لغو اشتراک')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اشتراک')
    unsubscribed_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ لغو اشتراک')
    
    class Meta:
        verbose_name = 'اشتراک‌کننده خبرنامه'
        verbose_name_plural = 'اشتراک‌کنندگان خبرنامه'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    def get_unsubscribe_url(self):
        return reverse('blog:unsubscribe', kwargs={'token': str(self.unsubscribe_token)})


class NewsletterCampaign(models.Model):
    """کمپین‌های خبرنامه"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    subject = models.CharField(max_length=300, verbose_name='موضوع ایمیل')
    sections = models.ManyToManyField('NewsletterSection', related_name='campaigns', verbose_name='بخش‌ها')
    posts = models.ManyToManyField('BlogPost', blank=True, related_name='campaigns', verbose_name='پست‌ها')
    tags = models.ManyToManyField('Tag', blank=True, related_name='campaigns', verbose_name='تگ‌ها')
    
    html_content = models.TextField(blank=True, null=True, verbose_name='محتوای HTML')
    sent_count = models.IntegerField(default=0, verbose_name='تعداد ارسال شده')
    opened_count = models.IntegerField(default=0, verbose_name='تعداد باز شده')
    clicked_count = models.IntegerField(default=0, verbose_name='تعداد کلیک شده')
    
    is_sent = models.BooleanField(default=False, verbose_name='ارسال شده')
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name='زمان برنامه‌ریزی شده')
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name='زمان ارسال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'کمپین خبرنامه'
        verbose_name_plural = 'کمپین‌های خبرنامه'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class NewsletterAnalytics(models.Model):
    """تحلیل و آمار خبرنامه"""
    campaign = models.ForeignKey('NewsletterCampaign', on_delete=models.CASCADE, related_name='analytics', verbose_name='کمپین')
    subscriber = models.ForeignKey('NewsletterSubscriber', on_delete=models.CASCADE, related_name='analytics', verbose_name='اشتراک‌کننده')
    
    is_opened = models.BooleanField(default=False, verbose_name='باز شده')
    opened_at = models.DateTimeField(blank=True, null=True, verbose_name='زمان باز شدن')
    
    is_clicked = models.BooleanField(default=False, verbose_name='کلیک شده')
    clicked_url = models.URLField(blank=True, null=True, verbose_name='لینک کلیک شده')
    clicked_at = models.DateTimeField(blank=True, null=True, verbose_name='زمان کلیک')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'آمار خبرنامه'
        verbose_name_plural = 'آمار خبرنامه'
        ordering = ['-created_at']
        unique_together = ['campaign', 'subscriber']
    
    def __str__(self):
        return f"{self.campaign.title} - {self.subscriber.email}"

