from django.shortcuts import render, get_object_or_404
from apps.core.models import Service, ServiceCategory
from django.views.decorators.cache import cache_page


@cache_page(60 * 10)
def service_list(request):
    """لیست خدمات"""
    services = Service.objects.filter(is_active=True)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = ServiceCategory.objects.get(slug=category_slug, is_active=True)
            services = services.filter(category=category)
        except ServiceCategory.DoesNotExist:
            # اگر دسته‌بندی وجود نداشت، همه خدمات را نشان بده
            pass
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        services = services.filter(title__icontains=search_query)
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    """جزئیات خدمت"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # خدمات مرتبط
    related_services = Service.objects.filter(
        is_active=True,
        category=service.category
    ).exclude(id=service.id)[:4]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'services/detail.html', context)


# صفحات جداگانه برای هر دسته‌بندی
def advertising_page(request):
    """صفحه تبلیغات"""
    return render(request, 'services/advertising.html')


def education_page(request):
    """صفحه تحصیلی"""
    from .models import University
    
    universities = University.objects.filter(is_active=True).order_by('order', '-created_at')
    
    context = {
        'universities': universities,
    }
    return render(request, 'services/education.html', context)


def university_detail(request, slug):
    """جزئیات دانشگاه"""
    from .models import University
    
    university = get_object_or_404(University, slug=slug, is_active=True)
    
    # دانشگاه‌های مرتبط
    related_universities = University.objects.filter(
        is_active=True,
        university_type=university.university_type
    ).exclude(id=university.id)[:4]
    
    context = {
        'university': university,
        'related_universities': related_universities,
    }
    
    return render(request, 'services/university_detail.html', context)


def business_page(request):
    """صفحه بیزینس"""
    return render(request, 'services/business.html')


def decoration_page(request):
    """صفحه دکوراسیون"""
    return render(request, 'services/decoration.html')


def legal_page(request):
    """صفحه حقوقی"""
    return render(request, 'services/legal.html')

