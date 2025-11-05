from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class BlogCategory(models.Model):
    """دسته‌بندی پست‌های وبلاگ"""
    name = models.CharField(max_length=200, verbose_name='نام دسته')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='آیکون')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی پست'
        verbose_name_plural = 'دسته‌بندی پست‌ها'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """پست‌های وبلاگ"""
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='اسلاگ')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    content = RichTextField(verbose_name='محتوای کامل')
    image = models.ImageField(upload_to='blog/', verbose_name='تصویر اصلی')
    gallery = models.ManyToManyField('BlogImage', blank=True, related_name='post_galleries', verbose_name='گالری تصاویر')
    
    author = models.CharField(max_length=200, default='مدیر سایت', verbose_name='نویسنده')
    views_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    
    class Meta:
        verbose_name = 'پست وبلاگ'
        verbose_name_plural = 'پست‌های وبلاگ'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


class BlogImage(models.Model):
    """تصاویر گالری پست"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image = models.ImageField(upload_to='blog/gallery/', verbose_name='تصویر')
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='توضیح تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'تصویر پست'
        verbose_name_plural = 'تصاویر پست'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.post.title} - تصویر {self.order}"


class BlogComment(models.Model):
    """نظرات پست‌های وبلاگ"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    content = models.TextField(verbose_name='نظر')
    is_approved = models.BooleanField(default=False, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.post.title}"

