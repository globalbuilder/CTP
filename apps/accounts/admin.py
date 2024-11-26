# apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, SupervisorProfile, TrainingUnitHeadProfile, Department

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('user_type',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'national_id', 'major', 'gpa', 'department', 'supervisor')
    search_fields = ('user__username', 'student_id', 'national_id', 'major')
    list_filter = ('major', 'department')
    verbose_name = 'ملف الطالب'
    verbose_name_plural = 'ملفات الطلاب'

@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'specialization', 'status')
    search_fields = ('user__username', 'employee_id', 'specialization')
    list_filter = ('department',)
    verbose_name = 'ملف المشرف'
    verbose_name_plural = 'ملفات المشرفين'

@admin.register(TrainingUnitHeadProfile)
class TrainingUnitHeadProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'office_number')
    search_fields = ('user__username', 'employee_id')
    verbose_name = 'ملف رئيس وحدة التدريب'
    verbose_name_plural = 'ملفات رؤساء وحدات التدريب'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = 'قسم'
    verbose_name_plural = 'الأقسام'
