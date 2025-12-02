from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import DecorationService, DecorationCategory, DecorationInquiry
from django.views.decorators.cache import cache_page
from .forms import DecorationInquiryForm


@cache_page(60 * 10)
def decoration_list(request):
    """لیست خدمات دکوراسیون"""
    services = DecorationService.objects.filter(is_active=True, is_published=True)
    categories = DecorationCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(DecorationCategory, slug=category_slug, is_active=True)
        services = services.filter(category=category)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        services = services.filter(title__icontains=search_query)
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'decoration/list.html', context)


def decoration_detail(request, slug):
    """جزئیات خدمت دکوراسیون"""
    service = get_object_or_404(DecorationService, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    service.views_count += 1
    service.save(update_fields=['views_count'])
    
    # خدمات مرتبط
    related_services = DecorationService.objects.filter(
        is_active=True,
        is_published=True,
        category=service.category
    ).exclude(id=service.id)[:4]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'decoration/detail.html', context)


def decoration_inquiry(request, slug):
    """استعلام خدمت دکوراسیون"""
    service = get_object_or_404(DecorationService, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = DecorationInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.decoration_service = service
            inquiry.save()
            messages.success(request, 'استعلام شما با موفقیت ثبت شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('decoration:detail', slug=slug)
    else:
        form = DecorationInquiryForm()
    
    context = {
        'service': service,
        'form': form,
    }
    
    return render(request, 'decoration/inquiry.html', context)
