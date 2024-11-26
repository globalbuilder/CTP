# apps/reports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReportUploadForm
from .models import Report, ReportArchive
from accounts.decorators import student_required, supervisor_required, training_unit_head_required
from accounts.models import User

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
            return redirect('reports:view_reports')
    else:
        form = ReportUploadForm()
    return render(request, 'reports/upload_report.html', {'form': form})

@login_required
def view_reports(request):
    if request.user.user_type == 'student':
        reports = Report.objects.filter(student=request.user)
    elif request.user.user_type == 'supervisor':
        students = User.objects.filter(student_profile__supervisor=request.user)
        reports = Report.objects.filter(student__in=students)
    elif request.user.user_type == 'head':
        reports = Report.objects.all()
    else:
        reports = []
    return render(request, 'reports/view_reports.html', {'reports': reports})

@login_required
@training_unit_head_required
def view_archive(request):
    archived_reports = ReportArchive.objects.all()
    return render(request, 'reports/view_archive.html', {'archived_reports': archived_reports})
