# apps/accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    LoginForm, StudentRegistrationForm, StudentProfileForm,
    SupervisorRegistrationForm, SupervisorProfileForm,
    TrainingUnitHeadProfileForm, EditProfileForm
)
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, StudentProfile, SupervisorProfile, TrainingUnitHeadProfile, Department
from .decorators import student_required, supervisor_required, training_unit_head_required
from django.contrib.auth.decorators import user_passes_test

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home')

@login_required
def profile_view(request):
    user = request.user
    if user.user_type == 'student':
        profile = user.student_profile
        form_class = StudentProfileForm
    elif user.user_type == 'supervisor':
        profile = user.supervisor_profile
        form_class = SupervisorProfileForm
    elif user.user_type == 'head':
        profile = user.head_profile
        form_class = TrainingUnitHeadProfileForm
    else:
        profile = None
        form_class = None

    if request.method == 'POST':
        if 'edit_profile' in request.POST:
            edit_form = EditProfileForm(request.POST, instance=user)
            profile_form = form_class(request.POST, instance=profile)
            if edit_form.is_valid() and profile_form.is_valid():
                edit_form.save()
                profile_form.save()
                messages.success(request, 'تم تحديث الملف الشخصي بنجاح.')
                return redirect('accounts:profile')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'تم تغيير كلمة المرور بنجاح.')
                return redirect('accounts:profile')
    else:
        edit_form = EditProfileForm(instance=user)
        profile_form = form_class(instance=profile)
        password_form = PasswordChangeForm(user=user)

    context = {
        'edit_form': edit_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'accounts/profile.html', context)

def student_register(request):
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'student'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'تم تسجيل الطالب بنجاح.')
            return redirect('core:home')
    else:
        user_form = StudentRegistrationForm()
        profile_form = StudentProfileForm()
    return render(request, 'accounts/student_register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def supervisor_register(request):
    if request.method == 'POST':
        user_form = SupervisorRegistrationForm(request.POST)
        profile_form = SupervisorProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'supervisor'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'تم تسجيل المشرف بنجاح.')
            return redirect('core:home')
    else:
        user_form = SupervisorRegistrationForm()
        profile_form = SupervisorProfileForm()
    return render(request, 'accounts/supervisor_register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
@training_unit_head_required
def manage_students(request):
    students = StudentProfile.objects.all()
    return render(request, 'accounts/manage_students.html', {'students': students})

@login_required
@training_unit_head_required
def manage_supervisors(request):
    supervisors = SupervisorProfile.objects.all()
    return render(request, 'accounts/manage_supervisors.html', {'supervisors': supervisors})

@login_required
@training_unit_head_required
def assign_supervisors(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('supervisor_') and value:
                student_id = key.split('_')[1]
                supervisor_user_id = value
                student = get_object_or_404(StudentProfile, id=student_id)
                supervisor_user = get_object_or_404(User, id=supervisor_user_id, user_type='supervisor')
                student.supervisor = supervisor_user
                student.save()
                messages.success(request, f'تم تعيين المشرف {supervisor_user.get_full_name()} للطالب {student.user.get_full_name()} بنجاح.')
        return redirect('accounts:assign_supervisors')
    else:
        students = StudentProfile.objects.filter(supervisor__isnull=True)
        supervisors = User.objects.filter(user_type='supervisor')  # Ensuring these are User instances
    return render(request, 'accounts/assign_supervisors.html', {'students': students, 'supervisors': supervisors})
    
@login_required
@supervisor_required
def view_assigned_students(request):
    supervisor = request.user
    students = StudentProfile.objects.filter(supervisor=supervisor)
    return render(request, 'accounts/view_assigned_students.html', {'students': students})

def is_training_unit_head(user):
    return user.user_type == 'head'

@user_passes_test(is_training_unit_head)
def view_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, 'accounts/view_student.html', {'student': student})

@user_passes_test(is_training_unit_head)
def edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل بيانات الطالب بنجاح.')
            return redirect('accounts:manage_students')
    else:
        form = StudentProfileForm(instance=student)
    return render(request, 'accounts/edit_student.html', {'form': form, 'student': student})

@user_passes_test(is_training_unit_head)
def delete_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'تم حذف الطالب بنجاح.')
        return redirect('accounts:manage_students')
    return render(request, 'accounts/delete_student.html', {'student': student})

@user_passes_test(is_training_unit_head)
def view_supervisor(request, supervisor_id):
    supervisor = get_object_or_404(SupervisorProfile, id=supervisor_id)
    return render(request, 'accounts/view_supervisor.html', {'supervisor': supervisor})

@user_passes_test(is_training_unit_head)
def edit_supervisor(request, supervisor_id):
    supervisor = get_object_or_404(SupervisorProfile, id=supervisor_id)
    if request.method == 'POST':
        form = SupervisorProfileForm(request.POST, instance=supervisor)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل بيانات المشرف بنجاح.')
            return redirect('accounts:manage_supervisors')
    else:
        form = SupervisorProfileForm(instance=supervisor)
    return render(request, 'accounts/edit_supervisor.html', {'form': form, 'supervisor': supervisor})

@user_passes_test(is_training_unit_head)
def delete_supervisor(request, supervisor_id):
    supervisor = get_object_or_404(SupervisorProfile, id=supervisor_id)
    if request.method == 'POST':
        user = supervisor.user
        supervisor.delete()
        user.delete()
        messages.success(request, 'تم حذف المشرف بنجاح.')
        return redirect('accounts:manage_supervisors')
    return render(request, 'accounts/delete_supervisor.html', {'supervisor': supervisor})
