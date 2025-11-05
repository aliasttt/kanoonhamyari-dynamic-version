from django.shortcuts import render, get_object_or_404, redirect
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
    """جزئیات پست"""
    post = get_object_or_404(BlogPost, slug=slug, is_active=True, is_published=True)
    
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

