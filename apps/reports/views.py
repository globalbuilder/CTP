# apps/reports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Report
from .forms import ReportUploadForm
from accounts.decorators import student_required, supervisor_required
from django.http import HttpResponse
import os

@login_required
@student_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.student = request.user
            report.save()
            messages.success(request, 'تم رفع التقرير بنجاح.')
            return redirect('reports:view_my_reports')
    else:
        form = ReportUploadForm()
    return render(request, 'reports/upload_report.html', {'form': form})

@login_required
@student_required
def view_my_reports(request):
    # Student views their reports and sees status
    reports = Report.objects.filter(student=request.user)
    return render(request, 'reports/view_my_reports.html', {'reports': reports})

@login_required
@supervisor_required
def view_students_reports(request):
    # Supervisor views reports of their assigned students
    students = request.user.supervisor_profile.supervised_students.all()
    reports = Report.objects.filter(student__in=students)
    return render(request, 'reports/view_students_reports.html', {'reports': reports})

@login_required
@supervisor_required
def process_report(request, pk):
    # Supervisor accepts or rejects the report
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            report.status = 'accepted'
            report.save()
            messages.success(request, 'تم قبول التقرير.')
        elif action == 'reject':
            report.status = 'rejected'
            report.save()
            messages.warning(request, 'تم رفض التقرير.')
        return redirect('reports:view_students_reports')
    return render(request, 'reports/process_report.html', {'report': report})

@login_required
@supervisor_required
def download_report(request, pk):
    # Supervisor downloads the student’s report
    report = get_object_or_404(Report, pk=pk)
    file_path = report.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    messages.error(request, 'الملف غير موجود.')
    return redirect('reports:view_students_reports')
