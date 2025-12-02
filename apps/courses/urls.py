from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<str:slug>/', views.detail_view, name='detail'),
    path('<str:slug>/quiz/question/<int:question_id>/answer/', views.quiz_answer_view, name='quiz_answer'),
    path('<str:slug>/quiz/submit/', views.quiz_submit_view, name='quiz_submit'),
    path('<str:slug>/certificate/', views.certificate_view, name='certificate'),
]










