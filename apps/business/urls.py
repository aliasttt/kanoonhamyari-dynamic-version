from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    path('', views.business_list, name='list'),
    path('<slug:slug>/', views.business_detail, name='detail'),
    path('<slug:slug>/inquiry/', views.business_inquiry, name='inquiry'),
]




