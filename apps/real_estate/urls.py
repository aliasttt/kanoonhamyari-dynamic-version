from django.urls import path
from . import views

app_name = 'real_estate'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('<slug:slug>/', views.property_detail, name='detail'),
    path('<slug:slug>/inquiry/', views.property_inquiry, name='inquiry'),
]

