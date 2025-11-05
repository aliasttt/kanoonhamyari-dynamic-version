from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone


class TourCategory(models.Model):
    """دسته‌بندی تورها"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی تور'
        verbose_name_plural = 'دسته‌بندی تورها'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tour(models.Model):
    """تورها"""
    category = models.ForeignKey(TourCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='tours/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('TourImage', blank=True, related_name='tour_galleries', verbose_name='گالری تصاویر')
    
    # اطلاعات تور
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name='مدت زمان')
    location = models.CharField(max_length=200, verbose_name='مقصد')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    capacity = models.IntegerField(blank=True, null=True, verbose_name='ظرفیت')
    registration_deadline = models.DateTimeField(blank=True, null=True, verbose_name='مهلت ثبت‌نام')
    
    # امکانات
    includes = RichTextField(blank=True, null=True, verbose_name='شامل')
    excludes = RichTextField(blank=True, null=True, verbose_name='شامل نمی‌شود')
    itinerary = RichTextField(blank=True, null=True, verbose_name='برنامه سفر')
    
    # تنظیمات
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'تور'
        verbose_name_plural = 'تورها'
        ordering = ['-start_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tours:detail', kwargs={'slug': self.slug})
    
    def is_upcoming(self):
        """بررسی اینکه تور آینده است یا نه"""
        return self.start_date > timezone.now()
    
    def is_registration_open(self):
        """بررسی اینکه ثبت‌نام باز است یا نه"""
        if self.registration_deadline:
            return self.registration_deadline > timezone.now()
        return self.is_upcoming()


class TourImage(models.Model):
    """تصاویر گالری تور"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images', verbose_name='تور')
    image = models.ImageField(upload_to='tours/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر تور'
        verbose_name_plural = 'تصاویر تور'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.tour.title} - تصویر {self.order}"


class TourRegistration(models.Model):
    """ثبت‌نام در تور"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='registrations', verbose_name='تور')
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    message = models.TextField(blank=True, null=True, verbose_name='پیام')
    number_of_people = models.IntegerField(default=1, verbose_name='تعداد نفرات')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت‌نام')
    
    class Meta:
        verbose_name = 'ثبت‌نام تور'
        verbose_name_plural = 'ثبت‌نام‌های تور'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.tour.title}"

