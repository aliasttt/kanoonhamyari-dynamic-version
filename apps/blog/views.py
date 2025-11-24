from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from .models import BlogPost, BlogCategory, BlogComment
from .forms import BlogCommentForm


def blog_list(request):
    """لیست پست‌های وبلاگ"""
    posts = BlogPost.objects.filter(is_active=True, is_published=True)
    categories = BlogCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug, is_active=True)
        posts = posts.filter(category=category)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    
    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    """جزئیات پست یا نمونه نمایشی"""
    try:
        post = BlogPost.objects.get(slug=slug, is_active=True, is_published=True)
    except BlogPost.DoesNotExist:
        # نمایش نمونه ثابت وقتی هنوز داده واقعی نداریم
        if slug.startswith('sample'):
            sample = {
                'title': 'نمونه مطلب وبلاگ',
                'author': 'تحریریه',
                'published_at': None,
                'views_count': 123,
                'category': type('obj', (), {'name': 'نمونه'})(),
                'image_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&q=70&auto=format&fit=crop',
                'content': """
                <p>این یک مطلب نمونه است تا نمایش صفحه جزئیات وبلاگ را ببینید. بعداً این محتوا با مطالب واقعی جایگزین خواهد شد.</p>
                <p>طراحی صفحه ثابت است و فقط عنوان، تصویر و متن هر پست تغییر می‌کند.</p>
                <ul>
                    <li>طراحی حرفه‌ای و خوانا</li>
                    <li>سازگار با موبایل</li>
                    <li>رنگ‌بندی سفید–نارنجی</li>
                </ul>
                """
            }
            return render(request, 'blog/sample_detail.html', {'sample': sample})
        raise Http404

    # افزایش تعداد بازدید
    post.views_count += 1
    post.save(update_fields=['views_count'])

    # پست‌های مرتبط
    related_posts = BlogPost.objects.filter(
        is_active=True,
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:4]

    # نظرات تایید شده
    comments = post.comments.filter(is_approved=True)

    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }

    return render(request, 'blog/detail.html', context)


def blog_comment(request, slug):
    """ثبت نظر برای پست"""
    post = get_object_or_404(BlogPost, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود.')
            return redirect('blog:detail', slug=slug)
    else:
        form = BlogCommentForm()
    
    context = {
        'post': post,
        'form': form,
    }
    
    return render(request, 'blog/comment.html', context)

