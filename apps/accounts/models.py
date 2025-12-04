from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """پروفایل کاربر با اطلاعات تکمیلی"""
    
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
        ('O', 'سایر'),
    ]
    
    EDUCATION_CHOICES = [
        ('diploma', 'دیپلم'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکترا'),
        ('other', 'سایر'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('articles', 'مقالات'),
        ('videos', 'ویدیوها'),
        ('courses', 'دوره‌ها'),
        ('events', 'رویدادها'),
        ('all', 'همه'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    
    # اطلاعات شخصی
    first_name = models.CharField(max_length=100, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='نام خانوادگی')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='جنسیت')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='شماره موبایل')
    
    # اطلاعات آدرس
    country = models.CharField(max_length=100, blank=True, verbose_name='کشور')
    city = models.CharField(max_length=100, blank=True, verbose_name='شهر')
    district = models.CharField(max_length=100, blank=True, verbose_name='منطقه/محله')
    full_address = models.TextField(blank=True, verbose_name='آدرس کامل')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='کد پستی')
    landline = models.CharField(max_length=20, blank=True, verbose_name='شماره تلفن ثابت')
    
    # اطلاعات شغلی
    current_job = models.CharField(max_length=200, blank=True, verbose_name='شغل فعلی')
    field_of_activity = models.CharField(max_length=200, blank=True, verbose_name='زمینه فعالیت')
    company_name = models.CharField(max_length=200, blank=True, verbose_name='نام شرکت')
    job_position = models.CharField(max_length=200, blank=True, verbose_name='سمت شغلی')
    years_of_experience = models.IntegerField(null=True, blank=True, verbose_name='سال‌های تجربه')
    website = models.URLField(blank=True, verbose_name='وب‌سایت شخصی یا کاری')
    linkedin = models.URLField(blank=True, verbose_name='لینکدین')
    instagram = models.CharField(max_length=200, blank=True, verbose_name='اینستاگرام / شبکه‌های اجتماعی')
    
    # اطلاعات تحصیلی
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True, verbose_name='آخرین مدرک تحصیلی')
    field_of_study = models.CharField(max_length=200, blank=True, verbose_name='رشته')
    university = models.CharField(max_length=200, blank=True, verbose_name='دانشگاه / موسسه')
    graduation_year = models.IntegerField(null=True, blank=True, verbose_name='سال فارغ‌التحصیلی')
    
    # ترجیحات
    favorite_categories = models.CharField(max_length=500, blank=True, verbose_name='دسته‌بندی‌های مورد علاقه')
    preferred_content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, blank=True, verbose_name='نوع محتوای مورد علاقه')
    preferred_message_hours = models.CharField(max_length=100, blank=True, verbose_name='ساعات ترجیحی دریافت پیام‌ها')
    followed_topics = models.TextField(blank=True, verbose_name='انتخاب موضوعاتی که دنبال می‌کند')
    how_did_you_hear = models.CharField(max_length=200, blank=True, verbose_name='نحوه آشنایی با سایت')
    
    # قبول قوانین
    terms_accepted = models.BooleanField(default=False, verbose_name='قبول قوانین و حریم خصوصی')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'
    
    def __str__(self):
        return f'{self.user.username} - Profile'
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ایجاد پروفایل خودکار هنگام ایجاد کاربر"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ذخیره پروفایل هنگام ذخیره کاربر"""
    if hasattr(instance, 'profile'):
        instance.profile.save()




