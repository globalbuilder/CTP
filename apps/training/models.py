# apps/training/models.py

from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Department

User = get_user_model()

class TrainingEntity(models.Model):
    GENDER_CHOICES = (
        ('male', 'ذكر'),
        ('female', 'أنثى'),
        ('both', 'الكل'),
    )

    SEMESTER_CHOICES = (
        ('first', 'الفصل الأول'),
        ('second', 'الفصل الثاني'),
        ('summer', 'الفصل الصيفي'),
    )

    name = models.CharField(max_length=200, verbose_name='اسم جهة التدريب')
    description = models.TextField(blank=True, null=True, verbose_name='وصف الجهة')
    address = models.CharField(max_length=300, verbose_name='العنوان')
    contact_person = models.CharField(max_length=100, verbose_name='الشخص المسؤول')
    contact_email = models.EmailField(verbose_name='البريد الإلكتروني للتواصل')
    contact_phone = models.CharField(max_length=20, verbose_name='رقم الهاتف للتواصل')
    website = models.URLField(blank=True, null=True, verbose_name='الموقع الإلكتروني')
    available_positions = models.TextField(blank=True, null=True, verbose_name='الوظائف المتاحة')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='both', verbose_name='الجنس')
    min_hours = models.PositiveIntegerField(default=0, verbose_name='الحد الأدنى من الساعات')
    departments = models.ManyToManyField(Department, verbose_name='الأقسام')
    available_slots = models.PositiveIntegerField(default=1, verbose_name='عدد الطلاب المتاح')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, verbose_name='الفصل الدراسي')
    is_available = models.BooleanField(default=False, verbose_name='متاح للطلاب')

    def __str__(self):
        return self.name

class TrainingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'معلق'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        verbose_name='الطالب'
    )
    training_entity = models.ForeignKey(
        TrainingEntity,
        on_delete=models.CASCADE,
        verbose_name='جهة التدريب'
    )
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    motivation_letter = models.TextField(verbose_name='رسالة الدافع')
    additional_documents = models.FileField(upload_to='training_requests/', null=True, blank=True, verbose_name='المستندات الإضافية')

    def __str__(self):
        return f"طلب تدريب (مباشر) من {self.student.get_full_name()} إلى {self.training_entity.name}"

class LetterRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'معلق'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'student'},
        verbose_name='الطالب'
    )
    training_entity = models.ForeignKey(
        TrainingEntity,
        on_delete=models.CASCADE,
        verbose_name='جهة التدريب'
    )
    start_date = models.DateField(verbose_name='تاريخ البدء')
    end_date = models.DateField(verbose_name='تاريخ الانتهاء')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    letter_file = models.FileField(upload_to='letters/', null=True, blank=True, verbose_name='ملف الخطاب')

    def __str__(self):
        return f"طلب خطاب من {self.student.get_full_name()} إلى {self.training_entity.name}"

class TrainingDetail(models.Model):
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='student_training_details',
                                limit_choices_to={'user_type': 'student'},
                                verbose_name='الطالب')
    training_entity = models.ForeignKey(TrainingEntity, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='جهة التدريب')
    supervisor = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='supervised_training_details',
                                   limit_choices_to={'user_type': 'supervisor'},
                                   verbose_name='المشرف الأكاديمي')
    start_date = models.DateField(verbose_name='تاريخ البدء')
    end_date = models.DateField(verbose_name='تاريخ الانتهاء')
    tasks_assigned = models.TextField(blank=True, null=True, verbose_name='المهام الموكلة')
    skills_learned = models.TextField(blank=True, null=True, verbose_name='المهارات المكتسبة')

    def __str__(self):
        return f"تفاصيل التدريب للطالب {self.student.get_full_name()}"

    class Meta:
        verbose_name = 'تفاصيل التدريب'
        verbose_name_plural = 'تفاصيل التدريبات'
