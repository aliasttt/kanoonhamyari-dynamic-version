from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<slug:slug>/', views.detail_view, name='detail'),
    path('<slug:slug>/quiz/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('<slug:slug>/certificate/', views.certificate_view, name='certificate'),
]





