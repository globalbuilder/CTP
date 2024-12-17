# apps/evaluations/admin.py

from django.contrib import admin
from .models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluator', 'training_entity', 'evaluation_type', 'evaluation_date', 'total_score')
    list_filter = ('training_entity','evaluation_type')
    search_fields = ('student__username', 'evaluator__username')
    verbose_name = 'التقييم'
    verbose_name_plural = 'التقييمات'
