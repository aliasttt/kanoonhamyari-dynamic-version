from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='list'),
    path('advertising/', views.advertising_page, name='advertising'),
    path('education/', views.education_page, name='education'),
    path('education/university/<slug:slug>/', views.university_detail, name='university_detail'),
    path('business/', views.business_page, name='business'),
    path('decoration/', views.decoration_page, name='decoration'),
    path('legal/', views.legal_page, name='legal'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]

