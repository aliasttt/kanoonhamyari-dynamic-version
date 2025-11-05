from django.db import models


class ContactMessage(models.Model):
    """پیام‌های تماس"""
    name = models.CharField(max_length=200, verbose_name='نام')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_replied = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactInfo(models.Model):
    """اطلاعات تماس"""
    title = models.CharField(max_length=200, verbose_name='عنوان')
    address = models.TextField(verbose_name='آدرس')
    phone_1 = models.CharField(max_length=20, verbose_name='تلفن ۱')
    phone_2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن ۲')
    phone_3 = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن ۳')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='واتساپ')
    google_maps_url = models.URLField(blank=True, null=True, verbose_name='لینک نقشه گوگل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'اطلاعات تماس'
        verbose_name_plural = 'اطلاعات تماس'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

