from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone


class EventCategory(models.Model):
    """دسته‌بندی رویدادها"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی رویداد'
        verbose_name_plural = 'دسته‌بندی رویدادها'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Event(models.Model):
    """رویدادها"""
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='events', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='events/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('EventImage', blank=True, related_name='event_galleries', verbose_name='گالری تصاویر')
    
    # اطلاعات رویداد
    event_date = models.DateTimeField(verbose_name='تاریخ و زمان رویداد')
    location = models.CharField(max_length=200, verbose_name='مکان')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس کامل')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='قیمت')
    capacity = models.IntegerField(blank=True, null=True, verbose_name='ظرفیت')
    registration_deadline = models.DateTimeField(blank=True, null=True, verbose_name='مهلت ثبت‌نام')
    
    # تنظیمات
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'رویداد'
        verbose_name_plural = 'رویدادها'
        ordering = ['-event_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})
    
    def is_upcoming(self):
        """بررسی اینکه رویداد آینده است یا نه"""
        return self.event_date > timezone.now()
    
    def is_registration_open(self):
        """بررسی اینکه ثبت‌نام باز است یا نه"""
        if self.registration_deadline:
            return self.registration_deadline > timezone.now()
        return self.is_upcoming()


class EventImage(models.Model):
    """تصاویر گالری رویداد"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', verbose_name='رویداد')
    image = models.ImageField(upload_to='events/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر رویداد'
        verbose_name_plural = 'تصاویر رویداد'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.event.title} - تصویر {self.order}"


class EventRegistration(models.Model):
    """ثبت‌نام در رویداد"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name='رویداد')
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    message = models.TextField(blank=True, null=True, verbose_name='پیام')
    number_of_people = models.IntegerField(default=1, verbose_name='تعداد نفرات')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت‌نام')
    
    class Meta:
        verbose_name = 'ثبت‌نام رویداد'
        verbose_name_plural = 'ثبت‌نام‌های رویداد'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"

