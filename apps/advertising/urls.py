from django.urls import path
from . import views

app_name = 'advertising'

urlpatterns = [
    path('', views.advertisement_list, name='list'),
    path('<slug:slug>/', views.advertisement_detail, name='detail'),
    path('<slug:slug>/inquiry/', views.advertisement_inquiry, name='inquiry'),
]

