"""
URL configuration for kanoon_dinamic project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('courses/', include('apps.courses.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('events/', include('apps.events.urls')),
    path('tours/', include('apps.tours.urls')),
    path('services/', include('apps.services.urls')),
    path('blog/', include('apps.blog.urls')),
    path('contact/', include('apps.contact.urls')),
    path('real-estate/', include('apps.real_estate.urls')),
    path('about/', include('apps.about.urls')),
    path('advertising/', include('apps.advertising.urls')),
    path('business/', include('apps.business.urls')),
    path('decoration/', include('apps.decoration.urls')),
    path('legal/', include('apps.legal.urls')),
]
 
