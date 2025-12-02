from django.urls import path
from . import views

app_name = 'decoration'

urlpatterns = [
    path('', views.decoration_list, name='list'),
    path('<str:slug>/', views.decoration_detail, name='detail'),
    path('<str:slug>/inquiry/', views.decoration_inquiry, name='inquiry'),
]

