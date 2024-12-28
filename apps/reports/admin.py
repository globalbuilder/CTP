# apps/reports/admin.py

from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'report_type', 'upload_date', 'status')  # Fields to display in the admin list view
    list_filter = ('report_type', 'status', 'upload_date')  # Filters for the sidebar
    search_fields = ('student__username', 'student__first_name', 'student__last_name')  # Search bar for students
    list_per_page = 20  # Pagination for large datasets

