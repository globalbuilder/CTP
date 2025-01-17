# apps/training/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from datetime import date, timedelta

from accounts.decorators import student_required, training_unit_head_required
from accounts.models import User
from .models import (
    TrainingRequest,
    LetterRequest,
    TrainingDetail,
    TrainingEntity
)
from .forms import (
    UnifiedTrainingRequestForm,
    LetterRequestForm,
    TrainingEntityForm
)


@login_required
@student_required
def browse_training_entities(request):
    student_profile = request.user.student_profile
    queryset = TrainingEntity.objects.filter(
        is_available=True,
        available_slots__gt=0
    )
    if student_profile.gender == 'male':
        queryset = queryset.filter(gender__in=['male', 'both'])
    elif student_profile.gender == 'female':
        queryset = queryset.filter(gender__in=['female', 'both'])

    if student_profile.department:
        queryset = queryset.filter(departments=student_profile.department)

    queryset = queryset.filter(min_hours__lte=student_profile.hours_completed)

    return render(request, 'training/browse_entities.html', {
        'entities': queryset
    })


@login_required
@student_required
def request_training(request, entity_id):
    """
    Student requests a direct training. 
    New check: If student has any non-rejected letter or direct request, forbid.
    Also if student already has a training_entity in profile, forbid.
    """
    student_profile = request.user.student_profile

    if student_profile.training_entity is not None:
        messages.error(request, 'لا يمكنك تقديم طلب جديد لأن لديك جهة تدريب حالياً.')
        return redirect('training:view_my_requests')

    existing_direct_requests = TrainingRequest.objects.filter(
        student=request.user
    ).exclude(status='rejected')  

    existing_letter_requests = LetterRequest.objects.filter(
        student=request.user
    ).exclude(status='rejected')

    if existing_direct_requests.exists() or existing_letter_requests.exists():
        messages.error(
            request,
            'لا يمكنك تقديم طلب تدريب الآن، لديك طلب آخر قيد المعالجة أو معتمد.'
        )
        return redirect('training:view_my_requests')

    entity = get_object_or_404(TrainingEntity, pk=entity_id, is_available=True, available_slots__gt=0)

    if student_profile.gender == 'male' and entity.gender not in ['male', 'both']:
        messages.error(request, 'لا يمكنك طلب تدريب في هذه الجهة.')
        return redirect('training:browse_entities')
    if student_profile.gender == 'female' and entity.gender not in ['female', 'both']:
        messages.error(request, 'لا يمكنك طلب تدريب في هذه الجهة.')
        return redirect('training:browse_entities')
    if student_profile.department and not entity.departments.filter(pk=student_profile.department.pk).exists():
        messages.error(request, 'لا يمكنك طلب تدريب في هذه الجهة (القسم غير متطابق).')
        return redirect('training:browse_entities')
    if student_profile.hours_completed < entity.min_hours:
        messages.error(request, 'لا يمكنك طلب تدريب في هذه الجهة (الساعات المكتسبة غير كافية).')
        return redirect('training:browse_entities')

    if request.method == 'POST':
        form = UnifiedTrainingRequestForm(request.POST, request.FILES, student=student_profile, single_entity=entity)
        if form.is_valid():
            motivation_letter = form.cleaned_data.get('motivation_letter', "")
            additional_documents = form.cleaned_data.get('additional_documents', None)

            TrainingRequest.objects.create(
                student=request.user,
                training_entity=entity,
                motivation_letter=motivation_letter,
                additional_documents=additional_documents
            )
            messages.success(request, 'تم تقديم طلب التدريب بنجاح.')
            return redirect('training:view_my_requests')
    else:
        form = UnifiedTrainingRequestForm(student=student_profile, single_entity=entity)

    return render(request, 'training/request_training.html', {
        'form': form,
        'entity': entity
    })


@login_required
@student_required
def request_letter(request):
    """
    Student requests a letter-based training.
    New check: If student has any non-rejected direct or letter request, forbid.
    Also if student has a training_entity assigned, forbid.
    """
    student_profile = request.user.student_profile

    if student_profile.training_entity is not None:
        messages.error(request, 'لا يمكنك تقديم طلب خطاب لأن لديك جهة تدريب حالياً.')
        return redirect('training:view_my_requests')

    existing_direct_requests = TrainingRequest.objects.filter(
        student=request.user
    ).exclude(status='rejected')

    existing_letter_requests = LetterRequest.objects.filter(
        student=request.user
    ).exclude(status='rejected')

    if existing_direct_requests.exists() or existing_letter_requests.exists():
        messages.error(
            request,
            'لا يمكنك تقديم طلب خطاب الآن، لديك طلب آخر قيد المعالجة أو معتمد.'
        )
        return redirect('training:view_my_requests')

    if request.method == 'POST':
        form = LetterRequestForm(request.POST)
        if form.is_valid():
            letter_req = form.save(commit=False)
            letter_req.student = request.user
            letter_req.save()
            messages.success(request, 'تم تقديم طلب الخطاب بنجاح.')
            return redirect('training:view_my_requests')
    else:
        form = LetterRequestForm()

    return render(request, 'training/request_letter.html', {
        'form': form
    })


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
    training_detail = TrainingDetail.objects.filter(student=request.user).order_by('-start_date').first()
    return render(request, 'training/training_details.html', {
        'training_detail': training_detail
    })


@login_required
def download_letter(request, pk):
    letter_request = get_object_or_404(LetterRequest, pk=pk, student=request.user, status='approved')
    if not letter_request.letter_file:
        messages.error(request, 'الخطاب غير متوفر.')
        return redirect('training:view_my_requests')

    file_path = letter_request.letter_file.path
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="letter_{letter_request.student.username}.pdf"'
        return response


@login_required
@training_unit_head_required
def training_requests_overview(request):
    direct_requests = TrainingRequest.objects.filter(status='pending')
    return render(request, 'training/training_requests_overview.html', {
        'direct_requests': direct_requests,
    })


@login_required
@training_unit_head_required
def letter_requests_overview(request):
    letter_requests = LetterRequest.objects.filter(status='pending')
    return render(request, 'training/letter_requests_overview.html', {
        'letter_requests': letter_requests,
    })


@login_required
@training_unit_head_required
def process_training_request(request, pk):
    training_request = get_object_or_404(TrainingRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            training_request.status = 'approved'
            training_request.save()
            entity = training_request.training_entity

            student_profile = training_request.student.student_profile
            student_profile.training_entity = entity
            student_profile.save()

            entity.available_slots = max(entity.available_slots - 1, 0)
            entity.save()

            start_date = date.today()
            end_date = start_date + timedelta(days=60)
            TrainingDetail.objects.create(
                student=training_request.student,
                training_entity=entity,
                supervisor=student_profile.supervisor,
                start_date=start_date,
                end_date=end_date
            )

            messages.success(
                request,
                f'تم اعتماد طلب التدريب للطالب {training_request.student.get_full_name()}.'
            )
        elif action == 'reject':
            training_request.status = 'rejected'
            training_request.save()
            messages.warning(
                request,
                f'تم رفض طلب التدريب من الطالب {training_request.student.get_full_name()}.'
            )
        return redirect('training:training_requests_overview')

    return render(request, 'training/process_training_request.html', {
        'training_request': training_request
    })


@login_required
@training_unit_head_required
def process_letter_request(request, pk):
    letter_request = get_object_or_404(LetterRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            context = {'letter_request': letter_request}
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(render_to_string('training/letter_template.html', context).encode("UTF-8")), result)
            if not pdf.err:
                letter_request.status = 'approved'
                letter_filename = f'letter_{letter_request.id}.pdf'
                letter_request.letter_file.save(letter_filename, result)
                letter_request.save()

                messages.success(request, 'تم اعتماد طلب الخطاب وإرسال الخطاب إلى الطالب.')
                return redirect('training:letter_requests_overview')
            else:
                messages.error(request, 'حدث خطأ أثناء إنشاء ملف PDF.')
                return redirect('training:letter_requests_overview')
        elif action == 'reject':
            letter_request.status = 'rejected'
            letter_request.save()
            messages.warning(request, 'تم رفض طلب الخطاب.')
            return redirect('training:letter_requests_overview')

    return render(request, 'training/process_letter_request.html', {
        'letter_request': letter_request
    })


@login_required
@training_unit_head_required
def manage_training_entities(request):
    entities = TrainingEntity.objects.all()
    return render(request, 'training/manage_training_entities.html', {
        'entities': entities
    })


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
