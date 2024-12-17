# apps/evaluations/models.py

from django.db import models
from django.contrib.auth import get_user_model
from training.models import TrainingEntity

User = get_user_model()

SCORE_CHOICES = (
    (10, 'ممتاز'),
    (8, 'جيد جدا'),
    (6, 'جيد'),
    (4, 'مقبول'),
    (2, 'ضعيف'),
)

EVALUATION_TYPE_CHOICES = (
    ('student', 'تقييم الطالب'),
    ('entity', 'تقييم جهة التدريب'),
)

class Evaluation(models.Model):
    evaluator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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
    evaluation_type = models.CharField(
        max_length=10,
        choices=EVALUATION_TYPE_CHOICES,
        verbose_name='نوع التقييم'
    )

    # 10 fixed criteria fields
    c1_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 1')
    c2_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 2')
    c3_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 3')
    c4_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 4')
    c5_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 5')
    c6_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 6')
    c7_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 7')
    c8_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 8')
    c9_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 9')
    c10_score = models.PositiveIntegerField(choices=SCORE_CHOICES, verbose_name='المعيار 10')

    total_score = models.PositiveIntegerField(
        verbose_name='الدرجة الإجمالية',
        blank=True,
        null=True,
    )
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='التعليقات'
    )

    def save(self, *args, **kwargs):
        # Calculate total score
        self.total_score = (
            self.c1_score + self.c2_score + self.c3_score + self.c4_score +
            self.c5_score + self.c6_score + self.c7_score + self.c8_score +
            self.c9_score + self.c10_score
        )
        super().save(*args, **kwargs)

    def __str__(self):
        if self.evaluation_type == 'student':
            return f"تقييم الطالب {self.student.get_full_name()} بواسطة {self.evaluator.get_full_name()}"
        else:
            return f"تقييم جهة التدريب {self.training_entity.name} بواسطة {self.evaluator.get_full_name()}"
