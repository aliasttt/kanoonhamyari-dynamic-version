from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='list'),
    path('yalda/', views.event_yalda_detail, name='yalda'),
    path('<slug:slug>/', views.event_detail, name='detail'),
    path('<slug:slug>/register/', views.event_register, name='register'),
]

