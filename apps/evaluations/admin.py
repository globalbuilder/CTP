# apps/evaluations/admin.py

from django.contrib import admin
from .models import Evaluation, EvaluationTemplate, EvaluationCriteria, EvaluationItem

class EvaluationItemInline(admin.TabularInline):
    model = EvaluationItem
    extra = 1
    verbose_name = 'عنصر التقييم'
    verbose_name_plural = 'عناصر التقييم'

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluator', 'training_entity', 'evaluation_date', 'total_score')
    list_filter = ('training_entity',)
    search_fields = ('student__username', 'evaluator__username')
    inlines = [EvaluationItemInline]
    verbose_name = 'التقييم'
    verbose_name_plural = 'التقييمات'

@admin.register(EvaluationTemplate)
class EvaluationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('criteria',)
    verbose_name = 'نموذج التقييم'
    verbose_name_plural = 'نماذج التقييم'

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('description', 'max_score')
    search_fields = ('description',)
    verbose_name = 'معيار التقييم'
    verbose_name_plural = 'معايير التقييم'
