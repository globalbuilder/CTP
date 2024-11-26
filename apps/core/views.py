# apps/core/views.py

from django.shortcuts import render
from accounts.models import User
from training.models import TrainingRequest, LetterRequest, TrainingEntity

def home(request):
    if request.user.is_authenticated:
        user = request.user
        context = {}
        if user.user_type == 'head':
            context['total_students'] = User.objects.filter(user_type='student').count()
            context['pending_training_requests'] = TrainingRequest.objects.filter(status='pending').count()
            context['pending_letter_requests'] = LetterRequest.objects.filter(status='pending').count()
            context['total_entities'] = TrainingEntity.objects.count()
            template_name = 'core/home_training_unit_head.html'
        elif user.user_type == 'student':
            # Add any context variables needed for students
            template_name = 'core/home_student.html'
        elif user.user_type == 'supervisor':
            # Add any context variables needed for supervisors
            template_name = 'core/home_supervisor.html'
        else:
            # Fallback template
            template_name = 'core/home.html'
        return render(request, template_name, context)
    else:
        return render(request, 'core/home.html')
