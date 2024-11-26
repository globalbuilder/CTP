# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم القسم')

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'طالب'),
        ('supervisor', 'مشرف'),
        ('head', 'رئيس وحدة التدريب'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        verbose_name='نوع المستخدم'
    )

    def __str__(self):
        return self.get_full_name()

class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='المستخدم'
    )
    student_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='الرقم الجامعي'
    )
    national_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الهوية'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='الجنس'
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name='رقم الجوال'
    )
    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='المعدل'
    )
    hours_completed = models.PositiveIntegerField(
        default=0,
        verbose_name='الساعات المكتسبة'
    )
    major = models.CharField(
        max_length=100,
        verbose_name='التخصص'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='القسم'
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'supervisor'},
        related_name='supervised_students',
        verbose_name='المشرف الأكاديمي'
    )
    training_entity = models.ForeignKey(
        'training.TrainingEntity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='جهة التدريب'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class SupervisorProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supervisor_profile',
        verbose_name='المستخدم'
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='الرقم التعريفي'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='الجنس'
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name='رقم الجوال'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='القسم'
    )
    specialization = models.CharField(
        max_length=100,
        verbose_name='التخصص'
    )
    status = models.CharField(
        max_length=50,
        verbose_name='الحالة'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class TrainingUnitHeadProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='head_profile',
        verbose_name='المستخدم'
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='رقم الموظف'
    )
    office_number = models.CharField(
        max_length=20,
        verbose_name='رقم المكتب'
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name='رقم الاتصال'
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
