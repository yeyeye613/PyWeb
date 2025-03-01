from django.urls import path
from . import views

urlpatterns = [
    path('ai/', views.test, name='test'),
    path('ai/stream_chat/', views.stream_chat, name='stream_chat')
]
