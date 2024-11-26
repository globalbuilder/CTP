# apps/reports/admin.py

from django.contrib import admin
from .models import Report, ReportArchive

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'report_type', 'upload_date')
    list_filter = ('report_type',)
    search_fields = ('student__username',)
    verbose_name = 'تقرير'
    verbose_name_plural = 'التقارير'

@admin.register(ReportArchive)
class ReportArchiveAdmin(admin.ModelAdmin):
    list_display = ('report', 'archived_date', 'reason_for_archival')
    search_fields = ('report__student__username',)
    verbose_name = 'تقرير مؤرشف'
    verbose_name_plural = 'تقارير الأرشيف'
