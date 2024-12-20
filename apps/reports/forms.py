# apps/reports/forms.py

from django import forms
from .models import Report

class ReportUploadForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'file']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'report_type': 'نوع التقرير',
            'file': 'الملف',
        }
