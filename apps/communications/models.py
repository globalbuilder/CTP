# apps/communications/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE,
        verbose_name='المرسل'
    )
    recipient = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE,
        verbose_name='المستقبل'
    )
    subject = models.CharField(
        max_length=200,
        verbose_name='الموضوع'
    )
    body = models.TextField(
        verbose_name='المحتوى'
    )
    sent_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإرسال'
    )
    read = models.BooleanField(
        default=False,
        verbose_name='تم القراءة'
    )
    attachment = models.FileField(
        upload_to='messages/',
        null=True,
        blank=True,
        verbose_name='مرفق'
    )

    def __str__(self):
        return f"رسالة من {self.sender.get_full_name()} إلى {self.recipient.get_full_name()}"
