# apps/reports/urls.py

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('upload/', views.upload_report, name='upload_report'),
    path('my_reports/', views.view_my_reports, name='view_my_reports'),
    path('students_reports/', views.view_students_reports, name='view_students_reports'),
    path('process/<int:pk>/', views.process_report, name='process_report'),
    path('download/<int:pk>/', views.download_report, name='download_report'),
]
