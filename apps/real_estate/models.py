from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class PropertyType(models.Model):
    """نوع ملک"""
    name = models.CharField(max_length=200, verbose_name='نام نوع')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'نوع ملک'
        verbose_name_plural = 'انواع ملک'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Property(models.Model):
    """املاک"""
    PROPERTY_STATUS_CHOICES = [
        ('for_sale', 'برای فروش'),
        ('for_rent', 'برای اجاره'),
        ('sold', 'فروخته شده'),
        ('rented', 'اجاره داده شده'),
    ]
    
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name='نوع ملک')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='properties/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('PropertyImage', blank=True, related_name='property_galleries', verbose_name='گالری تصاویر')
    
    # اطلاعات ملک
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS_CHOICES, default='for_sale', verbose_name='وضعیت')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='قیمت')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مساحت (متر مربع)')
    rooms = models.IntegerField(blank=True, null=True, verbose_name='تعداد اتاق')
    bathrooms = models.IntegerField(blank=True, null=True, verbose_name='تعداد سرویس بهداشتی')
    location = models.CharField(max_length=200, verbose_name='مکان')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس کامل')
    google_maps_url = models.URLField(blank=True, null=True, verbose_name='لینک نقشه گوگل')
    
    # ویژگی‌ها
    has_parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    has_elevator = models.BooleanField(default=False, verbose_name='آسانسور')
    has_balcony = models.BooleanField(default=False, verbose_name='بالکن')
    has_garden = models.BooleanField(default=False, verbose_name='باغ/باغچه')
    is_furnished = models.BooleanField(default=False, verbose_name='مبله')
    
    # تنظیمات
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'ملک'
        verbose_name_plural = 'املاک'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('real_estate:detail', kwargs={'slug': self.slug})


class PropertyImage(models.Model):
    """تصاویر گالری ملک"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name='ملک')
    image = models.ImageField(upload_to='properties/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر ملک'
        verbose_name_plural = 'تصاویر ملک'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.property.title} - تصویر {self.order}"


class PropertyInquiry(models.Model):
    """استعلام ملک"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries', verbose_name='ملک')
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    message = models.TextField(blank=True, null=True, verbose_name='پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_replied = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'استعلام ملک'
        verbose_name_plural = 'استعلام‌های ملک'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.property.title}"

