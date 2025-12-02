from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class BusinessCategory(models.Model):
    """دسته‌بندی خدمات بیزینسی"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی خدمات بیزینسی'
        verbose_name_plural = 'دسته‌بندی خدمات بیزینسی'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BusinessService(models.Model):
    """خدمات بیزینسی"""
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='services', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='business/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('BusinessImage', blank=True, related_name='business_galleries', verbose_name='گالری تصاویر')
    
    # اطلاعات خدمت
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='قیمت')
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name='مدت زمان')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='مکان')
    
    # تنظیمات
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'خدمت بیزینسی'
        verbose_name_plural = 'خدمات بیزینسی'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('business:detail', kwargs={'slug': self.slug})


class BusinessImage(models.Model):
    """تصاویر گالری خدمت بیزینسی"""
    business_service = models.ForeignKey(BusinessService, on_delete=models.CASCADE, related_name='images', verbose_name='خدمت')
    image = models.ImageField(upload_to='business/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر خدمت بیزینسی'
        verbose_name_plural = 'تصاویر خدمت بیزینسی'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.business_service.title} - تصویر {self.order}"


class BusinessInquiry(models.Model):
    """استعلام خدمت بیزینسی"""
    business_service = models.ForeignKey(BusinessService, on_delete=models.CASCADE, related_name='inquiries', verbose_name='خدمت')
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    message = models.TextField(blank=True, null=True, verbose_name='پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_replied = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'استعلام خدمت بیزینسی'
        verbose_name_plural = 'استعلام‌های خدمت بیزینسی'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.business_service.title}"
