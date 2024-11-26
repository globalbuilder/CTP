# apps/training/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TrainingRequestForm, LetterRequestForm, TrainingDetailForm, TrainingEntityForm
from .models import TrainingRequest, LetterRequest, TrainingDetail, TrainingEntity
from accounts.decorators import student_required, training_unit_head_required
from accounts.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
from xhtml2pdf import pisa
from io import BytesIO

@login_required
@student_required
def submit_training_request(request):
    student_profile = request.user.student_profile
    if request.method == 'POST':
        form = TrainingRequestForm(request.POST, request.FILES, student=student_profile)
        if form.is_valid():
            training_request = form.save(commit=False)
            training_request.student = request.user
            training_request.save()
            messages.success(request, 'تم تقديم طلب التدريب بنجاح.')
            return redirect('training:view_my_requests')
    else:
        form = TrainingRequestForm(student=student_profile)
    return render(request, 'training/submit_training_request.html', {'form': form})

@login_required
@student_required
def submit_letter_request(request):
    if request.method == 'POST':
        form = LetterRequestForm(request.POST)
        if form.is_valid():
            letter_request = form.save(commit=False)
            letter_request.student = request.user
            letter_request.save()
            messages.success(request, 'تم تقديم طلب الخطاب بنجاح.')
            return redirect('training:view_my_requests')
    else:
        form = LetterRequestForm()
    return render(request, 'training/submit_letter_request.html', {'form': form})

@login_required
@student_required
def view_my_requests(request):
    training_requests = TrainingRequest.objects.filter(student=request.user)
    letter_requests = LetterRequest.objects.filter(student=request.user)
    return render(request, 'training/view_my_requests.html', {
        'training_requests': training_requests,
        'letter_requests': letter_requests,
    })

@login_required
@student_required
def training_details(request):
    try:
        training_detail = TrainingDetail.objects.get(student=request.user)
    except TrainingDetail.DoesNotExist:
        training_detail = None
    return render(request, 'training/training_details.html', {'training_detail': training_detail})

@login_required
def download_letter(request, pk):
    letter_request = get_object_or_404(LetterRequest, pk=pk, student=request.user, status='approved')
    if not letter_request.letter_file:
        messages.error(request, 'الخطاب غير متوفر.')
        return redirect('training:view_my_requests')
    response = HttpResponse(letter_request.letter_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="letter_{letter_request.student.username}.pdf"'
    return response

@login_required
@training_unit_head_required
def application_requests(request):
    pending_requests = TrainingRequest.objects.filter(status='pending')
    return render(request, 'training/application_requests.html', {'pending_requests': pending_requests})

@login_required
@training_unit_head_required
def process_training_request(request, pk):
    training_request = get_object_or_404(TrainingRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            training_request.status = 'approved'
            training_request.save()
            # Decrement available slots
            training_entity = training_request.training_entity
            training_entity.available_slots -= 1
            training_entity.save()
            # Create TrainingDetail
            TrainingDetail.objects.create(
                student=training_request.student,
                training_entity=training_entity,
                supervisor=training_request.student.student_profile.supervisor,
                start_date=None,
                end_date=None,
            )
            messages.success(request, f'تم اعتماد طلب التدريب من الطالب {training_request.student.get_full_name()}.')
        elif action == 'reject':
            training_request.status = 'rejected'
            training_request.save()
            messages.warning(request, f'تم رفض طلب التدريب من الطالب {training_request.student.get_full_name()}.')
        return redirect('training:application_requests')
    return render(request, 'training/process_training_request.html', {'training_request': training_request})

@login_required
@training_unit_head_required
def letter_requests(request):
    pending_letters = LetterRequest.objects.filter(status='pending')
    return render(request, 'training/letter_requests.html', {'pending_letters': pending_letters})

@login_required
@training_unit_head_required
def process_letter_request(request, pk):
    letter_request = get_object_or_404(LetterRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # Generate the letter PDF using xhtml2pdf
            context = {
                'letter_request': letter_request,
            }
            html_string = render_to_string('training/letter_template.html', context)
            # Create a file-like buffer to receive PDF data.
            result = BytesIO()
            # Create the PDF object, and write it to the buffer.
            pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
            if not pdf.err:
                # Save the PDF to the model
                letter_request.status = 'approved'
                letter_filename = f'letter_{letter_request.id}.pdf'
                letter_request.letter_file.save(letter_filename, result)
                letter_request.save()
                messages.success(request, 'تم اعتماد طلب الخطاب وإرسال الخطاب إلى الطالب.')
                return redirect('training:letter_requests')
            else:
                messages.error(request, 'حدث خطأ أثناء إنشاء ملف PDF.')
                return redirect('training:letter_requests')
        elif action == 'reject':
            letter_request.status = 'rejected'
            letter_request.save()
            messages.warning(request, 'تم رفض طلب الخطاب.')
            return redirect('training:letter_requests')
    return render(request, 'training/process_letter_request.html', {'letter_request': letter_request})

@login_required
@training_unit_head_required
def manage_training_entities(request):
    entities = TrainingEntity.objects.all()
    return render(request, 'training/manage_training_entities.html', {'entities': entities})

@login_required
@training_unit_head_required
def add_training_entity(request):
    if request.method == 'POST':
        form = TrainingEntityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة جهة تدريب جديدة.')
            return redirect('training:manage_training_entities')
    else:
        form = TrainingEntityForm()
    return render(request, 'training/add_training_entity.html', {'form': form})

@login_required
@training_unit_head_required
def edit_training_entity(request, pk):
    entity = get_object_or_404(TrainingEntity, pk=pk)
    if request.method == 'POST':
        form = TrainingEntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث جهة التدريب.')
            return redirect('training:manage_training_entities')
    else:
        form = TrainingEntityForm(instance=entity)
    return render(request, 'training/edit_training_entity.html', {'form': form})

@login_required
@training_unit_head_required
def delete_training_entity(request, pk):
    entity = get_object_or_404(TrainingEntity, pk=pk)
    if request.method == 'POST':
        entity.delete()
        messages.success(request, 'تم حذف جهة التدريب.')
        return redirect('training:manage_training_entities')
    return render(request, 'training/delete_training_entity.html', {'entity': entity})
