from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='آدرس')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def __str__(self):
        return f"پروفایل {self.user.username}"





