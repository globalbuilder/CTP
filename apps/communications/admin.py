# apps/communications/admin.py

from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'sent_date', 'read')
    list_filter = ('read',)
    search_fields = ('subject', 'sender__username', 'recipient__username')
    verbose_name = 'رسالة'
    verbose_name_plural = 'الرسائل'
