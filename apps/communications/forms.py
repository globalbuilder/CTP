# apps/communications/forms.py

from django import forms
from .models import Message
from accounts.models import User

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='المستقبل',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'subject': 'الموضوع',
            'body': 'المحتوى',
            'attachment': 'مرفق',
        }
