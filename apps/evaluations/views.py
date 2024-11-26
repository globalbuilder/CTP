# apps/evaluations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EvaluationForm, EvaluationItemFormSet
from .models import Evaluation, EvaluationTemplate, EvaluationCriteria, EvaluationItem
from accounts.decorators import supervisor_required, training_unit_head_required
from accounts.models import User

@login_required
@supervisor_required
def evaluate_students(request):
    students = User.objects.filter(student_profile__supervisor=request.user)
    return render(request, 'evaluations/evaluate_students.html', {'students': students})

@login_required
@supervisor_required
def submit_evaluation(request, student_id):
    student = get_object_or_404(User, id=student_id, user_type='student')
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        formset = EvaluationItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.student = student
            evaluation.save()
            formset.instance = evaluation
            formset.save()
            total_score = sum([item.score for item in evaluation.items.all()])
            evaluation.total_score = total_score
            evaluation.save()
            messages.success(request, f'تم تقديم التقييم للطالب {student.get_full_name()}.')
            return redirect('evaluations:evaluate_students')
    else:
        form = EvaluationForm()
        formset = EvaluationItemFormSet()
    return render(request, 'evaluations/submit_evaluation.html', {
        'form': form,
        'formset': formset,
        'student': student,
    })

@login_required
def view_evaluations(request):
    if request.user.user_type == 'student':
        evaluations = request.user.evaluations.all()
    elif request.user.user_type == 'supervisor':
        evaluations = Evaluation.objects.filter(evaluator=request.user)
    elif request.user.user_type == 'head':
        evaluations = Evaluation.objects.all()
    else:
        evaluations = []
    return render(request, 'evaluations/view_evaluations.html', {'evaluations': evaluations})

@login_required
@training_unit_head_required
def view_training_entity_evaluations(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'evaluations/view_training_entity_evaluations.html', {'evaluations': evaluations})
