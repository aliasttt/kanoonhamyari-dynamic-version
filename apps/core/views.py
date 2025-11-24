from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Service, Testimonial, Goal, HeroSlide


@cache_page(60 * 10)  # cache homepage for 10 minutes
def index(request):
    """صفحه اصلی"""
    services = Service.objects.filter(is_active=True, is_featured=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    goals = Goal.objects.filter(is_active=True)
    hero_slides = HeroSlide.objects.filter(is_active=True)
    
    context = {
        'services': services,
        'testimonials': testimonials,
        'goals': goals,
        'hero_slides': hero_slides,
    }
    
    return render(request, 'core/index.html', context)

