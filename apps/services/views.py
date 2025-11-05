from django.shortcuts import render, get_object_or_404
from apps.core.models import Service, ServiceCategory


def service_list(request):
    """لیست خدمات"""
    services = Service.objects.filter(is_active=True)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(ServiceCategory, slug=category_slug, is_active=True)
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

