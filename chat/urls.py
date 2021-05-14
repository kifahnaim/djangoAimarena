from django.urls import path
from . import views


urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('chat2/', views.chat, name='chat2'),
    path('chat_sender/', views.chat_sender, name='chat_sender'),
    path('fetch/', views.fetch, name='fetch'),
    path('room/', views.room, name='room'),
    path('selectRoom/', views.selectRoom, name='selectRoom')

]
