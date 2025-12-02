from django.shortcuts import render, get_object_or_404
from apps.core.models import Service, ServiceCategory
from django.views.decorators.cache import cache_page
from django.utils.safestring import mark_safe
import re


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
    from apps.advertising.models import Advertisement, AdvertisingCategory
    
    advertisements = Advertisement.objects.filter(is_active=True, is_published=True)
    categories = AdvertisingCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = AdvertisingCategory.objects.get(slug=category_slug, is_active=True)
            advertisements = advertisements.filter(category=category)
        except AdvertisingCategory.DoesNotExist:
            pass
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        advertisements = advertisements.filter(title__icontains=search_query)
    
    context = {
        'advertisements': advertisements,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'advertising/list.html', context)


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

    # محتوای ارسالی از ادمین ممکن است شامل فوترهای قالب‌های قدیمی باشد.
    # این تابع، تمام بلاک‌های فوتر را از HTML حذف می‌کند.
    def sanitize_html_remove_footer(html: str) -> str:
        if not html:
            return ''
        cleaned = html
        # 1) حذف هر <footer>...</footer>
        cleaned = re.sub(r'(?is)<footer[\s\S]*?</footer>', '', cleaned)
        # 2) حذف هر دیو/سکشن/نَو با id یا کلاس حاوی کلمه footer یا kh-footer
        cleaned = re.sub(
            r'(?is)<(div|section|nav|header)[^>]*?(?:id|class)\s*=\s*["\'][^"\']*(?:kh-)?footer[^"\']*["\'][^>]*>[\s\S]*?</\1>',
            '',
            cleaned
        )
        # 3) حذف بلاک‌های خاص kh-footer__top و kh-footer__bottom اگر باقی مانده باشند
        cleaned = re.sub(
            r'(?is)<div[^>]*class[^>]*=["\'][^"\']*kh-footer__(?:top|bottom)[^"\']*["\'][^>]*>[\s\S]*?</div>',
            '',
            cleaned
        )
        # 4) پاکسازی‌های تکراری برای پوشش تودرتویی‌های احتمالی
        for _ in range(2):
            cleaned = re.sub(r'(?is)<footer[\s\S]*?</footer>', '', cleaned)
            cleaned = re.sub(
                r'(?is)<(div|section|nav|header)[^>]*?(?:id|class)\s*=\s*["\'][^"\']*(?:kh-)?footer[^"\']*["\'][^>]*>[\s\S]*?</\1>',
                '',
                cleaned
            )
        return cleaned

    description_html = mark_safe(sanitize_html_remove_footer(university.description or ''))
    programs_html = mark_safe(sanitize_html_remove_footer(university.programs or ''))
    admission_requirements_html = mark_safe(sanitize_html_remove_footer(university.admission_requirements or ''))
    scholarship_info_html = mark_safe(sanitize_html_remove_footer(university.scholarship_info or ''))
    
    # دانشگاه‌های مرتبط
    related_universities = University.objects.filter(
        is_active=True,
        university_type=university.university_type
    ).exclude(id=university.id)[:4]
    
    context = {
        'university': university,
        'related_universities': related_universities,
        'description_html': description_html,
        'programs_html': programs_html,
        'admission_requirements_html': admission_requirements_html,
        'scholarship_info_html': scholarship_info_html,
    }
    
    return render(request, 'services/university_detail.html', context)


def business_page(request):
    """صفحه بیزینس"""
    from apps.business.models import BusinessService, BusinessCategory
    
    services = BusinessService.objects.filter(is_active=True, is_published=True)
    categories = BusinessCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = BusinessCategory.objects.get(slug=category_slug, is_active=True)
            services = services.filter(category=category)
        except BusinessCategory.DoesNotExist:
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
    
    return render(request, 'business/list.html', context)


def decoration_page(request):
    """صفحه دکوراسیون"""
    from apps.decoration.models import DecorationService, DecorationCategory
    
    services = DecorationService.objects.filter(is_active=True, is_published=True)
    categories = DecorationCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = DecorationCategory.objects.get(slug=category_slug, is_active=True)
            services = services.filter(category=category)
        except DecorationCategory.DoesNotExist:
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
    
    return render(request, 'decoration/list.html', context)


def legal_page(request):
    """صفحه حقوقی"""
    from apps.legal.models import LegalService, LegalCategory
    
    services = LegalService.objects.filter(is_active=True, is_published=True)
    categories = LegalCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = LegalCategory.objects.get(slug=category_slug, is_active=True)
            services = services.filter(category=category)
        except LegalCategory.DoesNotExist:
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
    
    return render(request, 'legal/list.html', context)

