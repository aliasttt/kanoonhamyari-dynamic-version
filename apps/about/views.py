from django.shortcuts import render
from apps.core.models import Goal, HeroSlide


def about(request):
    """صفحه درباره ما"""
    goals = Goal.objects.filter(is_active=True)
    hero_slides = HeroSlide.objects.filter(is_active=True)
    
    context = {
        'goals': goals,
        'hero_slides': hero_slides,
    }
    
    return render(request, 'about/about.html', context)

