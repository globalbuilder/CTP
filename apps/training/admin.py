# apps/training/admin.py

from django.contrib import admin
from .models import TrainingRequest, LetterRequest, TrainingDetail, TrainingEntity

@admin.register(TrainingEntity)
class TrainingEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available', 'available_slots', 'semester')
    list_filter = ('is_available', 'semester', 'gender')
    search_fields = ('name',)
    filter_horizontal = ('departments',)

@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'training_entity', 'request_date', 'status')
    list_filter = ('status', 'training_entity')
    search_fields = ('student__username', 'training_entity__name')

@admin.register(LetterRequest)
class LetterRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'entity_name', 'request_date', 'status')
    list_filter = ('status',)
    search_fields = ('student__username', 'entity_name')

@admin.register(TrainingDetail)
class TrainingDetailAdmin(admin.ModelAdmin):
    list_display = ('student', 'training_entity', 'supervisor', 'start_date', 'end_date')
    list_filter = ('training_entity',)
    search_fields = ('student__username', 'supervisor__username')
