# apps/communications/urls.py

from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
]
