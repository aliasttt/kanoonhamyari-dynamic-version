from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, PropertyType, PropertyInquiry
from django.views.decorators.cache import cache_page
from .forms import PropertyInquiryForm


@cache_page(60 * 10)
def property_list(request):
    """لیست املاک"""
    properties = Property.objects.filter(is_active=True, is_published=True)
    types = PropertyType.objects.filter(is_active=True)
    
    # فیلتر بر اساس نوع
    type_slug = request.GET.get('type')
    if type_slug:
        property_type = get_object_or_404(PropertyType, slug=type_slug, is_active=True)
        properties = properties.filter(property_type=property_type)
    
    # فیلتر بر اساس وضعیت
    status = request.GET.get('status')
    if status:
        properties = properties.filter(status=status)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        properties = properties.filter(title__icontains=search_query)
    
    context = {
        'properties': properties,
        'types': types,
        'selected_type': type_slug,
        'selected_status': status,
    }
    
    return render(request, 'real_estate/list.html', context)


def property_detail(request, slug):
    """جزئیات ملک"""
    property = get_object_or_404(Property, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    property.views_count += 1
    property.save(update_fields=['views_count'])
    
    # املاک مرتبط
    related_properties = Property.objects.filter(
        is_active=True,
        is_published=True,
        property_type=property.property_type
    ).exclude(id=property.id)[:4]
    
    context = {
        'property': property,
        'related_properties': related_properties,
    }
    
    return render(request, 'real_estate/detail.html', context)


def property_inquiry(request, slug):
    """استعلام ملک"""
    property = get_object_or_404(Property, slug=slug, is_active=True, is_published=True)
    
    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = property
            inquiry.save()
            messages.success(request, 'استعلام شما با موفقیت ثبت شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('real_estate:detail', slug=slug)
    else:
        form = PropertyInquiryForm()
    
    context = {
        'property': property,
        'form': form,
    }
    
    return render(request, 'real_estate/inquiry.html', context)

