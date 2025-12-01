from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class University(models.Model):
    """دانشگاه‌ها"""
    name = models.CharField(max_length=200, verbose_name='نام دانشگاه')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات کامل')
    image = models.ImageField(upload_to='universities/', blank=True, null=True, verbose_name='تصویر')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='قیمت (لیر ترکیه)')
    price_note = models.CharField(max_length=200, blank=True, null=True, verbose_name='یادداشت قیمت')
    
    # اطلاعات کلی
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='موقعیت')
    university_type = models.CharField(
        max_length=50,
        choices=[
            ('public', 'دولتی'),
            ('private', 'خصوصی'),
        ],
        default='public',
        verbose_name='نوع دانشگاه'
    )
    language = models.CharField(max_length=100, blank=True, null=True, verbose_name='زبان تدریس')
    ranking = models.CharField(max_length=100, blank=True, null=True, verbose_name='رتبه')
    
    # اطلاعات جزئی
    programs = RichTextField(blank=True, null=True, verbose_name='رشته‌های تحصیلی')
    admission_requirements = RichTextField(blank=True, null=True, verbose_name='شرایط پذیرش')
    scholarship_info = RichTextField(blank=True, null=True, verbose_name='اطلاعات بورسیه')
    
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'دانشگاه'
        verbose_name_plural = 'دانشگاه‌ها'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('services:university_detail', kwargs={'slug': self.slug})

