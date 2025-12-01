from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, EventCategory, EventRegistration
from django.views.decorators.cache import cache_page
from .forms import EventRegistrationForm


@cache_page(60 * 10)
def event_list(request):
    """لیست رویدادها"""
    events = Event.objects.filter(is_active=True, is_published=True)
    categories = EventCategory.objects.filter(is_active=True)
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(EventCategory, slug=category_slug, is_active=True)
        events = events.filter(category=category)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        events = events.filter(title__icontains=search_query)
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_slug,
    }
    
    return render(request, 'events/list.html', context)


def event_detail(request, slug):
    """جزئیات رویداد"""
    event = get_object_or_404(Event, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    event.views_count += 1
    event.save(update_fields=['views_count'])
    
    # رویدادهای مرتبط
    related_events = Event.objects.filter(
        is_active=True, 
        is_published=True,
        category=event.category
    ).exclude(id=event.id)[:4]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    
    return render(request, 'events/detail.html', context)


def event_register(request, slug):
    """ثبت‌نام در رویداد"""
    event = get_object_or_404(Event, slug=slug, is_active=True, is_published=True)
    
    if not event.is_registration_open():
        messages.error(request, 'مهلت ثبت‌نام این رویداد به پایان رسیده است.')
        return redirect('events:detail', slug=slug)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد. در صورت نیاز با شما تماس خواهیم گرفت.')
            return redirect('events:detail', slug=slug)
    else:
        form = EventRegistrationForm()
    
    context = {
        'event': event,
        'form': form,
    }
    
    return render(request, 'events/register.html', context)


def event_yalda_detail(request):
    """صفحه جزئیات نمونه برای جشن شب یلدا (استاتیک برای نمایش طرح)"""
    context = {
        'title': 'جشن شب یلدا',
        'price': 300,
        'date_str': '30 آذر',
        'time_str': '20:00',
        'location': 'استانبول، ترکیه',
    }
    return render(request, 'events/yalda_detail.html', context)
