# apps/reports/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('weekly', 'تقرير أسبوعي'),
        ('final', 'تقرير نهائي'),
    )

    STATUS_CHOICES = (
        ('pending', 'قيد المراجعة'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
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
    file = models.FileField(
        upload_to='reports/',
        verbose_name='الملف'
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الرفع'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة التقرير'
    )

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.get_report_type_display()} ({self.get_status_display()})"
