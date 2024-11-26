# apps/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('student_register/', views.student_register, name='student_register'),
    path('supervisor_register/', views.supervisor_register, name='supervisor_register'),
    path('manage_students/', views.manage_students, name='manage_students'),
    path('manage_supervisors/', views.manage_supervisors, name='manage_supervisors'),
    path('assign_supervisors/', views.assign_supervisors, name='assign_supervisors'),
    path('view_assigned_students/', views.view_assigned_students, name='view_assigned_students'),

    path('manage_students/<int:student_id>/', views.view_student, name='view_student'),
    path('manage_students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('manage_students/<int:student_id>/delete/', views.delete_student, name='delete_student'),

    path('manage_supervisors/<int:supervisor_id>/', views.view_supervisor, name='view_supervisor'),
    path('manage_supervisors/<int:supervisor_id>/edit/', views.edit_supervisor, name='edit_supervisor'),
    path('manage_supervisors/<int:supervisor_id>/delete/', views.delete_supervisor, name='delete_supervisor'),
]
