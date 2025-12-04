from django.urls import path
from . import views

app_name = 'legal'

urlpatterns = [
    path('', views.legal_list, name='list'),
    path('<str:slug>/', views.legal_detail, name='detail'),
    path('<str:slug>/inquiry/', views.legal_inquiry, name='inquiry'),
]




