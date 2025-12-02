from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='list'),
    path('subscribe/', views.newsletter_subscribe, name='subscribe'),
    path('unsubscribe/<uuid:token>/', views.newsletter_unsubscribe, name='unsubscribe'),
    path('preview/<int:campaign_id>/', views.newsletter_preview, name='preview'),
    path('send/<int:campaign_id>/', views.send_newsletter, name='send'),
    path('track/open/<int:campaign_id>/<int:subscriber_id>/', views.track_email_open, name='track_open'),
    path('track/click/<int:campaign_id>/<int:subscriber_id>/', views.track_email_click, name='track_click'),
    path('<str:slug>/', views.blog_detail, name='detail'),
    path('<str:slug>/comment/', views.blog_comment, name='comment'),
]

