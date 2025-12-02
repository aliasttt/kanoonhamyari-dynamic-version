from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from .models import (
    BlogPost, BlogCategory, BlogComment,
    NewsletterSection, NewsletterSubscriber, NewsletterCampaign,
    NewsletterAnalytics, Tag
)
from .forms import BlogCommentForm, NewsletterSubscribeForm


def blog_list(request):
    """لیست پست‌های وبلاگ با بخش‌های داینامیک خبرنامه"""
    # دریافت بخش‌های فعال خبرنامه به ترتیب order
    sections = NewsletterSection.objects.filter(is_active=True).order_by('order')
    
    # دریافت پست‌های منتشر شده
    posts = BlogPost.objects.filter(
        is_active=True,
        is_published=True
    ).filter(
        Q(published_at__lte=timezone.now()) | Q(published_at__isnull=True)
    )
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug, is_active=True)
        posts = posts.filter(category=category)
    
    # فیلتر بر اساس تگ
    tag_slug = request.GET.get('tag')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(subtitle__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # ساخت دیکشنری برای هر بخش
    sections_data = {}
    for section in sections:
        section_posts = posts.filter(newsletter_section=section)
        if section.section_type == 'featured':
            section_posts = section_posts.filter(is_featured=True)
        section_posts = section_posts[:section.max_items]
        sections_data[section] = section_posts
    
    # پست‌های اخیر (برای بخش Latest)
    latest_posts = posts.order_by('-published_at', '-created_at')[:6]
    
    # پست‌های ویژه
    featured_posts = posts.filter(is_featured=True)[:6]
    
    categories = BlogCategory.objects.filter(is_active=True)
    tags = Tag.objects.all()
    
    context = {
        'sections': sections_data,
        'latest_posts': latest_posts,
        'featured_posts': featured_posts,
        'all_posts': posts.order_by('-published_at', '-created_at'),
        'categories': categories,
        'tags': tags,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'search_query': search_query,
    }
    
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    """جزئیات پست یا نمونه نمایشی"""
    try:
        post = BlogPost.objects.get(slug=slug, is_active=True, is_published=True)
    except BlogPost.DoesNotExist:
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


@require_POST
def newsletter_subscribe(request):
    """اشتراک در خبرنامه"""
    form = NewsletterSubscribeForm(request.POST)
    if form.is_valid():
        # بررسی وجود ایمیل غیرفعال
        email = form.cleaned_data['email']
        existing = NewsletterSubscriber.objects.filter(email=email).first()
        
        if existing:
            if existing.is_active:
                messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            else:
                # فعال کردن مجدد
                existing.is_active = True
                existing.name = form.cleaned_data.get('name', existing.name)
                existing.unsubscribed_at = None
                existing.save()
                if form.cleaned_data.get('tags'):
                    existing.tags.set(form.cleaned_data['tags'])
                messages.success(request, 'اشتراک شما فعال شد.')
        else:
            subscriber = form.save()
            messages.success(request, 'اشتراک شما با موفقیت ثبت شد.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'اشتراک شما با موفقیت ثبت شد.'})
        
        return redirect('blog:list')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'errors': form.errors})
    
    messages.error(request, 'خطا در ثبت اشتراک. لطفاً دوباره تلاش کنید.')
    return redirect('blog:list')


def newsletter_unsubscribe(request, token):
    """لغو اشتراک خبرنامه"""
    try:
        subscriber = NewsletterSubscriber.objects.get(unsubscribe_token=token)
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        messages.success(request, 'اشتراک شما با موفقیت لغو شد.')
    except NewsletterSubscriber.DoesNotExist:
        messages.error(request, 'لینک نامعتبر است.')
    
    return render(request, 'blog/unsubscribe.html')


def newsletter_preview(request, campaign_id):
    """پیش‌نمایش خبرنامه برای ادمین"""
    campaign = get_object_or_404(NewsletterCampaign, id=campaign_id)
    
    # تولید HTML خبرنامه
    html_content = generate_newsletter_html(campaign, request)
    
    context = {
        'campaign': campaign,
        'html_content': html_content,
    }
    
    return render(request, 'blog/newsletter_preview.html', context)


def generate_newsletter_html(campaign, request=None):
    """تولید HTML خبرنامه از کمپین"""
    from django.contrib.sites.models import Site
    
    sections = campaign.sections.all()
    posts = campaign.posts.all()
    tags = campaign.tags.all()
    
    # اگر پست‌های خاصی انتخاب نشده، از بخش‌ها استفاده کن
    if not posts.exists():
        for section in sections:
            section_posts = BlogPost.objects.filter(
                newsletter_section=section,
                is_active=True,
                is_published=True
            ).filter(
                Q(published_at__lte=timezone.now()) | Q(published_at__isnull=True)
            )[:section.max_items]
            posts = posts | section_posts
    
    # اگر تگ انتخاب شده، فیلتر کن
    if tags.exists():
        posts = posts.filter(tags__in=tags).distinct()
    
    # دریافت host
    if request:
        host = request.get_host()
        scheme = request.scheme
    else:
        site = Site.objects.get_current()
        host = site.domain
        scheme = 'https'
    
    context = {
        'campaign': campaign,
        'sections': sections,
        'posts': posts.order_by('-published_at', '-created_at'),
        'request': type('obj', (), {'get_host': lambda: host, 'scheme': scheme})(),
    }
    
    html_content = render_to_string('blog/newsletter_email.html', context)
    campaign.html_content = html_content
    campaign.save(update_fields=['html_content'])
    
    return html_content


def send_newsletter(request, campaign_id):
    """ارسال خبرنامه به اشتراک‌کنندگان"""
    from django.contrib.sites.models import Site
    
    campaign = get_object_or_404(NewsletterCampaign, id=campaign_id)
    
    if campaign.is_sent:
        messages.error(request, 'این خبرنامه قبلاً ارسال شده است.')
        return redirect('admin:blog_newslettercampaign_changelist')
    
    # دریافت host و scheme
    if request:
        host = request.get_host()
        scheme = request.scheme
    else:
        site = Site.objects.get_current()
        host = site.domain
        scheme = 'https'
    
    base_url = f"{scheme}://{host}"
    
    # تولید HTML
    html_content = generate_newsletter_html(campaign, request)
    
    # دریافت اشتراک‌کنندگان فعال
    subscribers = NewsletterSubscriber.objects.filter(is_active=True)
    
    # اگر تگ انتخاب شده، فقط به اشتراک‌کنندگان با آن تگ ارسال کن
    if campaign.tags.exists():
        subscribers = subscribers.filter(
            Q(tags__in=campaign.tags.all()) | Q(tags__isnull=True)
        ).distinct()
    
    sent_count = 0
    for subscriber in subscribers:
        try:
            # ایجاد لینک unsubscribe
            unsubscribe_url = f"{base_url}{reverse('blog:unsubscribe', kwargs={'token': str(subscriber.unsubscribe_token)})}"
            
            # ایجاد لینک‌های tracking
            open_tracking_url = f"{base_url}{reverse('blog:track_open', kwargs={'campaign_id': campaign.id, 'subscriber_id': subscriber.id})}"
            
            # جایگزینی لینک‌ها در HTML
            personalized_html = html_content.replace('{{unsubscribe_url}}', unsubscribe_url)
            # اضافه کردن tracking pixel
            tracking_pixel = f'<img src="{open_tracking_url}" width="1" height="1" style="display:none;" />'
            personalized_html = personalized_html.replace('</body>', f'{tracking_pixel}</body>')
            
            # جایگزینی لینک‌های پست‌ها با لینک‌های tracking
            for post in campaign.posts.all():
                post_url = f"{base_url}{post.get_absolute_url()}"
                click_tracking_url = f"{base_url}{reverse('blog:track_click', kwargs={'campaign_id': campaign.id, 'subscriber_id': subscriber.id})}?url={post_url}"
                personalized_html = personalized_html.replace(post_url, click_tracking_url)
            
            # ارسال ایمیل
            email = EmailMultiAlternatives(
                subject=campaign.subject,
                body='لطفاً این ایمیل را در مرورگر خود باز کنید.',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                to=[subscriber.email]
            )
            email.attach_alternative(personalized_html, 'text/html')
            email.send()
            
            # ثبت آمار
            analytics, created = NewsletterAnalytics.objects.get_or_create(
                campaign=campaign,
                subscriber=subscriber
            )
            
            sent_count += 1
        except Exception as e:
            print(f"Error sending to {subscriber.email}: {e}")
    
    campaign.sent_count = sent_count
    campaign.is_sent = True
    campaign.sent_at = timezone.now()
    campaign.save()
    
    messages.success(request, f'خبرنامه با موفقیت به {sent_count} نفر ارسال شد.')
    return redirect('admin:blog_newslettercampaign_changelist')


@csrf_exempt
def track_email_open(request, campaign_id, subscriber_id):
    """ردیابی باز شدن ایمیل"""
    try:
        campaign = NewsletterCampaign.objects.get(id=campaign_id)
        subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)
        
        analytics, created = NewsletterAnalytics.objects.get_or_create(
            campaign=campaign,
            subscriber=subscriber
        )
        
        if not analytics.is_opened:
            analytics.is_opened = True
            analytics.opened_at = timezone.now()
            analytics.save()
            
            campaign.opened_count = NewsletterAnalytics.objects.filter(
                campaign=campaign, is_opened=True
            ).count()
            campaign.save(update_fields=['opened_count'])
    except:
        pass
    
    # بازگرداندن تصویر 1x1 شفاف برای ردیابی
    from django.http import HttpResponse
    from django.core.files.base import ContentFile
    import base64
    
    pixel = base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
    return HttpResponse(pixel, content_type='image/gif')


@csrf_exempt
def track_email_click(request, campaign_id, subscriber_id):
    """ردیابی کلیک روی لینک"""
    url = request.GET.get('url', '')
    
    try:
        campaign = NewsletterCampaign.objects.get(id=campaign_id)
        subscriber = NewsletterSubscriber.objects.get(id=subscriber_id)
        
        analytics, created = NewsletterAnalytics.objects.get_or_create(
            campaign=campaign,
            subscriber=subscriber
        )
        
        if not analytics.is_clicked:
            analytics.is_clicked = True
            analytics.clicked_url = url
            analytics.clicked_at = timezone.now()
            analytics.save()
            
            campaign.clicked_count = NewsletterAnalytics.objects.filter(
                campaign=campaign, is_clicked=True
            ).count()
            campaign.save(update_fields=['clicked_count'])
    except:
        pass
    
    return redirect(url)
