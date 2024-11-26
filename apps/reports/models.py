# apps/reports/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('weekly', 'أسبوعي'),
        ('final', 'نهائي'),
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        verbose_name='الطالب'
    )
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES,
        verbose_name='نوع التقرير'
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الرفع'
    )
    file = models.FileField(
        upload_to='reports/',
        verbose_name='الملف'
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='التعليقات'
    )

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.get_report_type_display()} تقرير"

class ReportArchive(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        verbose_name='التقرير'
    )
    archived_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الأرشفة'
    )
    reason_for_archival = models.TextField(
        verbose_name='سبب الأرشفة'
    )

    def __str__(self):
        return f"تقرير مؤرشف - {self.report}"
