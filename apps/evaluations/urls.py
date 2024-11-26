# apps/evaluations/urls.py

from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('submit/<int:student_id>/', views.submit_evaluation, name='submit_evaluation'),
    path('view/', views.view_evaluations, name='view_evaluations'),
    path('evaluate_students/', views.evaluate_students, name='evaluate_students'),
    path('training_entity_evaluations/', views.view_training_entity_evaluations, name='view_training_entity_evaluations'),
]
