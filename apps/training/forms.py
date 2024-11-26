# apps/training/forms.py

from django import forms
from .models import TrainingRequest, LetterRequest, TrainingDetail, TrainingEntity
from accounts.models import StudentProfile

class TrainingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['training_entity', 'motivation_letter', 'additional_documents']
        widgets = {
            'training_entity': forms.Select(attrs={'class': 'form-control'}),
            'motivation_letter': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_documents': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'training_entity': 'جهة التدريب',
            'motivation_letter': 'رسالة الدافع',
            'additional_documents': 'المستندات الإضافية',
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        queryset = TrainingEntity.objects.filter(is_available=True, available_slots__gt=0)
        if student:
            # Filter by gender
            if student.gender:
                if student.gender == 'male':
                    queryset = queryset.filter(gender__in=['male', 'both'])
                elif student.gender == 'female':
                    queryset = queryset.filter(gender__in=['female', 'both'])
            # Filter by departments
            if student.department:
                queryset = queryset.filter(departments=student.department)
            # Filter by min_hours
            queryset = queryset.filter(min_hours__lte=student.hours_completed)
        self.fields['training_entity'].queryset = queryset

class LetterRequestForm(forms.ModelForm):
    class Meta:
        model = LetterRequest
        fields = ['training_entity', 'start_date', 'end_date']
        widgets = {
            'training_entity': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'training_entity': 'جهة التدريب',
            'start_date': 'تاريخ البدء',
            'end_date': 'تاريخ الانتهاء',
        }

class TrainingDetailForm(forms.ModelForm):
    class Meta:
        model = TrainingDetail
        fields = ['start_date', 'end_date', 'tasks_assigned', 'skills_learned']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tasks_assigned': forms.Textarea(attrs={'class': 'form-control'}),
            'skills_learned': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'start_date': 'تاريخ البدء',
            'end_date': 'تاريخ الانتهاء',
            'tasks_assigned': 'المهام الموكلة',
            'skills_learned': 'المهارات المكتسبة',
        }

class TrainingEntityForm(forms.ModelForm):
    class Meta:
        model = TrainingEntity
        fields = [
            'name', 'description', 'address', 'contact_person',
            'contact_email', 'contact_phone', 'website', 'available_positions',
            'gender', 'min_hours', 'departments', 'available_slots', 'semester', 'is_available'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'available_positions': forms.Textarea(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'min_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'departments': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'available_slots': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'اسم جهة التدريب',
            'description': 'وصف الجهة',
            'address': 'العنوان',
            'contact_person': 'الشخص المسؤول',
            'contact_email': 'البريد الإلكتروني للتواصل',
            'contact_phone': 'رقم الهاتف للتواصل',
            'website': 'الموقع الإلكتروني',
            'available_positions': 'الوظائف المتاحة',
            'gender': 'الجنس',
            'min_hours': 'الحد الأدنى من الساعات',
            'departments': 'الأقسام',
            'available_slots': 'عدد الطلاب المتاح',
            'semester': 'الفصل الدراسي',
            'is_available': 'متاح للطلاب',
        }
