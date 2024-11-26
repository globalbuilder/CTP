# apps/training/urls.py

from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Student URLs
    path('submit_training_request/', views.submit_training_request, name='submit_training_request'),
    path('submit_letter_request/', views.submit_letter_request, name='submit_letter_request'),
    path('my_requests/', views.view_my_requests, name='view_my_requests'),
    path('training_details/', views.training_details, name='training_details'),
    path('download_letter/<int:pk>/', views.download_letter, name='download_letter'),

    # Training Unit Head URLs
    path('application_requests/', views.application_requests, name='application_requests'),
    path('process_training_request/<int:pk>/', views.process_training_request, name='process_training_request'),
    path('letter_requests/', views.letter_requests, name='letter_requests'),
    path('process_letter_request/<int:pk>/', views.process_letter_request, name='process_letter_request'),

    # Training Entity Management URLs
    path('manage_training_entities/', views.manage_training_entities, name='manage_training_entities'),
    path('add_training_entity/', views.add_training_entity, name='add_training_entity'),
    path('edit_training_entity/<int:pk>/', views.edit_training_entity, name='edit_training_entity'),
    path('delete_training_entity/<int:pk>/', views.delete_training_entity, name='delete_training_entity'),
]
