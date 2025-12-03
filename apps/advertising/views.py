from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Advertisement, AdvertisingCategory, AdvertisementInquiry
from django.views.decorators.cache import cache_page
from .forms import AdvertisementInquiryForm


@cache_page(60 * 10)
def advertisement_list(request):
    """لیست تبلیغات"""
    advertisements = Advertisement.objects.filter(is_active=True, is_published=True)
    categories = AdvertisingCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(AdvertisingCategory, slug=category_slug, is_active=True)
        advertisements = advertisements.filter(category=category)
    
    # جستجو پیشرفته در چند فیلد
    search_query = request.GET.get('search')
    if search_query:
        from django.db.models import Q
        advertisements = advertisements.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'advertisements': advertisements,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query if 'search_query' in locals() else '',
    }
    
    return render(request, 'advertising/list.html', context)


def advertisement_detail(request, slug):
    """جزئیات تبلیغ"""
    advertisement = get_object_or_404(Advertisement, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    advertisement.views_count += 1
    advertisement.save(update_fields=['views_count'])
    
    # تبلیغات مرتبط
    related_advertisements = Advertisement.objects.filter(
        is_active=True,
        is_published=True,
        category=advertisement.category
    ).exclude(id=advertisement.id)[:4]
    
    context = {
        'advertisement': advertisement,
        'related_advertisements': related_advertisements,
    }
    
    return render(request, 'advertising/detail.html', context)


def advertisement_inquiry(request, slug):
    """استعلام تبلیغ"""
    advertisement = get_object_or_404(Advertisement, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = AdvertisementInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.advertisement = advertisement
            inquiry.save()
            messages.success(request, 'استعلام شما با موفقیت ثبت شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('advertising:detail', slug=slug)
    else:
        form = AdvertisementInquiryForm()
    
    context = {
        'advertisement': advertisement,
        'form': form,
    }
    
    return render(request, 'advertising/inquiry.html', context)
