from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class SiteSettings(models.Model):
    """تنظیمات کلی سایت"""
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_description = models.TextField(verbose_name='توضیحات سایت')
    site_logo = models.ImageField(upload_to='site/', verbose_name='لوگو')
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='فاویکون')
    
    # اطلاعات تماس
    address = models.TextField(verbose_name='آدرس')
    phone_1 = models.CharField(max_length=20, verbose_name='تلفن ۱')
    phone_2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن ۲')
    phone_3 = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن ۳')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='واتساپ')
    
    # شبکه‌های اجتماعی
    instagram = models.URLField(blank=True, null=True, verbose_name='اینستاگرام')
    telegram = models.URLField(blank=True, null=True, verbose_name='تلگرام')
    youtube = models.URLField(blank=True, null=True, verbose_name='یوتیوب')
    facebook = models.URLField(blank=True, null=True, verbose_name='فیس بوک')
    
    # تنظیمات SEO
    meta_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='عنوان متا')
    meta_description = models.TextField(blank=True, null=True, verbose_name='توضیحات متا')
    meta_keywords = models.CharField(max_length=500, blank=True, null=True, verbose_name='کلمات کلیدی')
    
    # Google Maps
    google_maps_url = models.URLField(blank=True, null=True, verbose_name='لینک نقشه گوگل')
    
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # فقط یک رکورد تنظیمات داشته باشیم
        if not self.pk:
            SiteSettings.objects.all().delete()
        super().save(*args, **kwargs)


class ServiceCategory(models.Model):
    """دسته‌بندی خدمات"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی خدمات'
        verbose_name_plural = 'دسته‌بندی خدمات'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Service(models.Model):
    """خدمات"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='services/', verbose_name='تصویر')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})


class Testimonial(models.Model):
    """نظرات و توصیه‌نامه‌ها"""
    name = models.CharField(max_length=200, verbose_name='نام')
    role = models.CharField(max_length=200, blank=True, null=True, verbose_name='سمت/شغل')
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name='تصویر')
    content = models.TextField(verbose_name='متن نظر')
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name='امتیاز')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'نظر و توصیه'
        verbose_name_plural = 'نظرات و توصیه‌ها'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.name


class Goal(models.Model):
    """اهداف کانون"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='goals/', verbose_name='تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'هدف'
        verbose_name_plural = 'اهداف'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    """اسلایدهای صفحه اصلی"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    subtitle = models.TextField(blank=True, null=True, verbose_name='زیرعنوان')
    image = models.ImageField(upload_to='hero/', verbose_name='تصویر')
    link = models.URLField(blank=True, null=True, verbose_name='لینک')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'اسلاید صفحه اصلی'
        verbose_name_plural = 'اسلایدهای صفحه اصلی'
        ordering = ['order']
    
    def __str__(self):
        return self.title

