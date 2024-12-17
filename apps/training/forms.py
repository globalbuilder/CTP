# apps/training/forms.py

from django import forms
from .models import TrainingEntity

REQUEST_TYPE_CHOICES = (
    ('direct', 'طلب تدريب مباشر'),
    ('letter', 'طلب خطاب تدريب'),
)

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
        
class UnifiedTrainingRequestForm(forms.Form):
    request_type = forms.ChoiceField(choices=REQUEST_TYPE_CHOICES, widget=forms.RadioSelect, label='نوع الطلب')
    motivation_letter = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='رسالة الدافع', required=False)
    additional_documents = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}), label='المستندات الإضافية', required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ البدء', required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ الانتهاء', required=False)

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        single_entity = kwargs.pop('single_entity', None)
        super().__init__(*args, **kwargs)
        # We already have the entity from the URL, so no need to filter here.
        # The student and single_entity parameters are just for future validation if needed.
        # If we needed to do additional checks, we could do them here.
