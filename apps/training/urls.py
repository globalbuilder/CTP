# apps/training/urls.py

from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Student URLs
    path('browse_entities/', views.browse_training_entities, name='browse_entities'),
    path('request_training/<int:entity_id>/', views.request_training, name='request_training'),
    path('request_letter/', views.request_letter, name='request_letter'),

    path('my_requests/', views.view_my_requests, name='view_my_requests'),
    path('training_details/', views.training_details, name='training_details'),
    path('download_letter/<int:pk>/', views.download_letter, name='download_letter'),

    # Head URLs
    path('training_requests_overview/', views.training_requests_overview, name='training_requests_overview'),
    path('process_training_request/<int:pk>/', views.process_training_request, name='process_training_request'),
    path('letter_requests_overview/', views.letter_requests_overview, name='letter_requests_overview'),
    path('process_letter_request/<int:pk>/', views.process_letter_request, name='process_letter_request'),

    # Training Entity Management URLs
    path('manage_training_entities/', views.manage_training_entities, name='manage_training_entities'),
    path('add_training_entity/', views.add_training_entity, name='add_training_entity'),
    path('edit_training_entity/<int:pk>/', views.edit_training_entity, name='edit_training_entity'),
    path('delete_training_entity/<int:pk>/', views.delete_training_entity, name='delete_training_entity'),
]
