from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class LegalCategory(models.Model):
    """دسته‌بندی خدمات حقوقی"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی خدمات حقوقی'
        verbose_name_plural = 'دسته‌بندی‌های خدمات حقوقی'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class LegalService(models.Model):
    """خدمات حقوقی"""
    category = models.ForeignKey(LegalCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='legal/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('LegalImage', blank=True, related_name='legal_galleries', verbose_name='گالری تصاویر')
    
    # اطلاعات خدمت
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='قیمت')
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name='مدت زمان')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='مکان')
    
    # ویژگی‌های خاص
    is_24_7 = models.BooleanField(default=False, verbose_name='پشتیبانی 24/7')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='امتیاز')
    
    # تنظیمات
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'خدمت حقوقی'
        verbose_name_plural = 'خدمات حقوقی'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('legal:detail', kwargs={'slug': self.slug})


class LegalImage(models.Model):
    """تصاویر گالری خدمت حقوقی"""
    legal_service = models.ForeignKey(LegalService, on_delete=models.CASCADE, related_name='images', verbose_name='خدمت')
    image = models.ImageField(upload_to='legal/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر خدمت حقوقی'
        verbose_name_plural = 'تصاویر خدمت حقوقی'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.legal_service.title} - تصویر {self.order}"


class LegalInquiry(models.Model):
    """استعلام خدمت حقوقی"""
    legal_service = models.ForeignKey(LegalService, on_delete=models.CASCADE, related_name='inquiries', verbose_name='خدمت')
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    message = models.TextField(blank=True, null=True, verbose_name='پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_replied = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'استعلام خدمت حقوقی'
        verbose_name_plural = 'استعلام‌های خدمت حقوقی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.legal_service.title}"
