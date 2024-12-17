# apps/evaluations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EvaluationForm
from .models import Evaluation
from accounts.decorators import supervisor_required, training_unit_head_required
from accounts.models import User
from training.models import TrainingDetail

@login_required
@supervisor_required
def evaluate_students(request):
    students = User.objects.filter(student_profile__supervisor=request.user)
    return render(request, 'evaluations/evaluate_students.html', {'students': students})

@login_required
@supervisor_required
def submit_evaluation(request, student_id):
    student = get_object_or_404(User, id=student_id, user_type='student')
    training_detail = get_object_or_404(TrainingDetail, student=student)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, evaluation_type='student')
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.student = student
            evaluation.training_entity = training_detail.training_entity
            evaluation.evaluation_type = 'student'
            evaluation.save()
            messages.success(request, f'تم تقديم التقييم للطالب {student.get_full_name()}.')
            return redirect('evaluations:evaluate_students')
    else:
        form = EvaluationForm(evaluation_type='student')

    # Create a list of fields in Python rather than in the template
    fields = [
        form['c1_score'],
        form['c2_score'],
        form['c3_score'],
        form['c4_score'],
        form['c5_score'],
        form['c6_score'],
        form['c7_score'],
        form['c8_score'],
        form['c9_score'],
        form['c10_score'],
    ]

    return render(request, 'evaluations/submit_evaluation.html', {
        'form': form,
        'fields': fields,
        'student': student,
    })

@login_required
def view_evaluations(request):
    user = request.user
    if user.user_type == 'student':
        evaluations = Evaluation.objects.filter(student=user)
    elif user.user_type == 'supervisor':
        evaluations = Evaluation.objects.filter(evaluator=user, evaluation_type='student')
    elif user.user_type == 'head':
        evaluations = Evaluation.objects.all()
    else:
        evaluations = []
    return render(request, 'evaluations/view_evaluations.html', {'evaluations': evaluations})

@login_required
@training_unit_head_required
def view_training_entity_evaluations(request):
    evaluations = Evaluation.objects.filter(evaluation_type='entity')
    return render(request, 'evaluations/view_training_entity_evaluations.html', {'evaluations': evaluations})

@login_required
def submit_entity_evaluation(request):
    if request.user.user_type != 'student':
        messages.error(request, 'هذه الصفحة غير متاحة.')
        return redirect('core:home')

    try:
        training_detail = TrainingDetail.objects.get(student=request.user)
    except TrainingDetail.DoesNotExist:
        messages.error(request, 'لا يمكنك تقييم جهة التدريب قبل اعتماد التدريب.')
        return redirect('core:home')

    if request.method == 'POST':
        form = EvaluationForm(request.POST, evaluation_type='entity')
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.student = request.user
            evaluation.training_entity = training_detail.training_entity
            evaluation.evaluation_type = 'entity'
            evaluation.save()
            messages.success(request, 'تم تقديم تقييم جهة التدريب بنجاح.')
            return redirect('evaluations:view_evaluations')
    else:
        form = EvaluationForm(evaluation_type='entity')

    # Create a fields list
    fields = [
        form['c1_score'],
        form['c2_score'],
        form['c3_score'],
        form['c4_score'],
        form['c5_score'],
        form['c6_score'],
        form['c7_score'],
        form['c8_score'],
        form['c9_score'],
        form['c10_score'],
    ]

    return render(request, 'evaluations/submit_entity_evaluation.html', {
        'form': form,
        'fields': fields,
        'training_entity': training_detail.training_entity,
    })
