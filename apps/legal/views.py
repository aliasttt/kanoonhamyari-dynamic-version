from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import LegalService, LegalCategory, LegalInquiry
from django.views.decorators.cache import cache_page
from .forms import LegalInquiryForm


@cache_page(60 * 10)
def legal_list(request):
    """لیست خدمات حقوقی"""
    services = LegalService.objects.filter(is_active=True, is_published=True)
    categories = LegalCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(LegalCategory, slug=category_slug, is_active=True)
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
    
    return render(request, 'legal/list.html', context)


def legal_detail(request, slug):
    """جزئیات خدمت حقوقی"""
    service = get_object_or_404(LegalService, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    service.views_count += 1
    service.save(update_fields=['views_count'])
    
    # خدمات مرتبط
    related_services = LegalService.objects.filter(
        is_active=True,
        is_published=True,
        category=service.category
    ).exclude(id=service.id)[:4]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'legal/detail.html', context)


def legal_inquiry(request, slug):
    """استعلام خدمت حقوقی"""
    service = get_object_or_404(LegalService, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = LegalInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.legal_service = service
            inquiry.save()
            messages.success(request, 'استعلام شما با موفقیت ثبت شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('legal:detail', slug=slug)
    else:
        form = LegalInquiryForm()
    
    context = {
        'service': service,
        'form': form,
    }
    
    return render(request, 'legal/inquiry.html', context)
