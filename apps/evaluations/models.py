# apps/evaluations/models.py

from django.db import models
from django.contrib.auth import get_user_model
from training.models import TrainingEntity

User = get_user_model()

class EvaluationCriteria(models.Model):
    description = models.CharField(
        max_length=255,
        verbose_name='الوصف'
    )
    max_score = models.PositiveIntegerField(
        default=10,
        verbose_name='الحد الأقصى للدرجة'
    )

    def __str__(self):
        return self.description

class EvaluationTemplate(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='اسم النموذج'
    )
    description = models.TextField(
        verbose_name='وصف النموذج'
    )
    criteria = models.ManyToManyField(
        EvaluationCriteria,
        verbose_name='المعايير'
    )

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    evaluator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type__in': ['supervisor', 'head']},
        verbose_name='المقيم'
    )
    student = models.ForeignKey(
        User,
        related_name='evaluations',
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        verbose_name='الطالب'
    )
    training_entity = models.ForeignKey(
        TrainingEntity,
        on_delete=models.CASCADE,
        verbose_name='وحدة التدريب'
    )
    evaluation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التقييم'
    )
    template = models.ForeignKey(
        EvaluationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='نموذج التقييم'
    )
    total_score = models.PositiveIntegerField(
        verbose_name='الدرجة الإجمالية'
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='التعليقات'
    )

    def __str__(self):
        return f"تقييم {self.student.get_full_name()} بواسطة {self.evaluator.get_full_name()}"

class EvaluationItem(models.Model):
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='التقييم'
    )
    criteria = models.ForeignKey(
        EvaluationCriteria,
        on_delete=models.CASCADE,
        verbose_name='المعيار'
    )
    score = models.PositiveIntegerField(
        verbose_name='الدرجة'
    )

    def __str__(self):
        return f"{self.criteria.description} - درجة: {self.score}"
