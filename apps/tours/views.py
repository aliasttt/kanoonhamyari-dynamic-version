from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Tour, TourCategory, TourRegistration
from django.views.decorators.cache import cache_page
from .forms import TourRegistrationForm


@cache_page(60 * 10)
def tour_list(request):
    """لیست تورها"""
    tours = Tour.objects.filter(is_active=True, is_published=True).select_related('category').order_by('-created_at')
    categories = TourCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(TourCategory, slug=category_slug, is_active=True)
        tours = tours.filter(category=category)
    
    # جستجو پیشرفته در چند فیلد
    search_query = request.GET.get('search')
    if search_query:
        from django.db.models import Q
        tours = tours.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'tours': tours,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query if 'search_query' in locals() else '',
    }
    
    return render(request, 'tours/list.html', context)


def tour_detail(request, slug):
    """جزئیات تور"""
    tour = get_object_or_404(Tour, slug=slug, is_active=True, is_published=True)
    
    # افزایش تعداد بازدید
    tour.views_count += 1
    tour.save(update_fields=['views_count'])
    
    # تورهای مرتبط
    related_tours = Tour.objects.filter(
        is_active=True, 
        is_published=True,
        category=tour.category
    ).select_related('category').exclude(id=tour.id).order_by('-created_at')[:4]
    
    context = {
        'tour': tour,
        'related_tours': related_tours,
    }
    
    return render(request, 'tours/detail.html', context)


def tour_register(request, slug):
    """ثبت‌نام در تور"""
    tour = get_object_or_404(Tour, slug=slug, is_active=True, is_published=True)
    
    if not tour.is_registration_open():
        messages.error(request, 'مهلت ثبت‌نام این تور به پایان رسیده است.')
        return redirect('tours:detail', slug=slug)
    
    if request.method == 'POST':
        form = TourRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.tour = tour
            registration.save()
            messages.success(request, 'ثبت‌نام شما با موفقیت انجام شد. در صورت نیاز با شما تماس خواهیم گرفت.')
            return redirect('tours:detail', slug=slug)
    else:
        form = TourRegistrationForm()
    
    context = {
        'tour': tour,
        'form': form,
    }
    
    return render(request, 'tours/register.html', context)

