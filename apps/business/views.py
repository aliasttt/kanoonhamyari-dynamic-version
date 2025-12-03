from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BusinessService, BusinessCategory, BusinessInquiry
from django.views.decorators.cache import cache_page
from .forms import BusinessInquiryForm


@cache_page(60 * 10)
def business_list(request):
    """لیست خدمات بیزینسی"""
    services = BusinessService.objects.filter(is_active=True, is_published=True)
    categories = BusinessCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BusinessCategory, slug=category_slug, is_active=True)
        services = services.filter(category=category)
    
    # جستجو پیشرفته در چند فیلد
    search_query = request.GET.get('search')
    if search_query:
        from django.db.models import Q
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query if 'search_query' in locals() else '',
    }
    
    return render(request, 'business/list.html', context)


def business_detail(request, slug):
    """جزئیات خدمت بیزینسی"""
    service = get_object_or_404(BusinessService, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    service.views_count += 1
    service.save(update_fields=['views_count'])
    
    # خدمات مرتبط
    related_services = BusinessService.objects.filter(
        is_active=True,
        is_published=True,
        category=service.category
    ).exclude(id=service.id)[:4]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'business/detail.html', context)


def business_inquiry(request, slug):
    """استعلام خدمت بیزینسی"""
    service = get_object_or_404(BusinessService, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = BusinessInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.business_service = service
            inquiry.save()
            messages.success(request, 'استعلام شما با موفقیت ثبت شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('business:detail', slug=slug)
    else:
        form = BusinessInquiryForm()
    
    context = {
        'service': service,
        'form': form,
    }
    
    return render(request, 'business/inquiry.html', context)
