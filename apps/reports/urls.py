# apps/reports/urls.py

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('upload/', views.upload_report, name='upload_report'),
    path('view/', views.view_reports, name='view_reports'),
    path('archive/', views.view_archive, name='view_archive'),
]
