# apps/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, SupervisorProfile, TrainingUnitHeadProfile, Department

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, label='الاسم الأول')
    last_name = forms.CharField(max_length=30, label='اسم العائلة')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class StudentProfileForm(forms.ModelForm):
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='supervisor'),
        required=False,
        label='المشرف الأكاديمي',
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Supervisor"
    )

    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'national_id', 'gender', 'contact_number', 'gpa',
            'hours_completed', 'major', 'department', 'supervisor', 'training_entity'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'hours_completed': forms.NumberInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'training_entity': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student_id': 'الرقم الجامعي',
            'national_id': 'رقم الهوية',
            'gender': 'الجنس',
            'contact_number': 'رقم الجوال',
            'gpa': 'المعدل',
            'hours_completed': 'الساعات المكتسبة',
            'major': 'التخصص',
            'department': 'القسم',
            'training_entity': 'جهة التدريب',
            'supervisor': 'المشرف الأكاديمي'
        }

        
class SupervisorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, label='الاسم الأول')
    last_name = forms.CharField(max_length=30, label='اسم العائلة')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class SupervisorProfileForm(forms.ModelForm):
    class Meta:
        model = SupervisorProfile
        fields = [
            'employee_id', 'gender', 'contact_number', 'department',
            'specialization', 'status'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'employee_id': 'الرقم التعريفي',
            'gender': 'الجنس',
            'contact_number': 'رقم الجوال',
            'department': 'القسم',
            'specialization': 'التخصص',
            'status': 'الحالة',
        }

class TrainingUnitHeadProfileForm(forms.ModelForm):
    class Meta:
        model = TrainingUnitHeadProfile
        fields = ['employee_id', 'office_number', 'contact_number']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'office_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'employee_id': 'رقم الموظف',
            'office_number': 'رقم المكتب',
            'contact_number': 'رقم الاتصال',
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'email': 'البريد الإلكتروني',
        }
