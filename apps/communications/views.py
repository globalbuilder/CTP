# apps/communications/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MessageForm
from .models import Message
from accounts.models import User

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'تم إرسال الرسالة بنجاح.')
            return redirect('communications:inbox')
    else:
        form = MessageForm()
    return render(request, 'communications/send_message.html', {'form': form})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user)
    return render(request, 'communications/inbox.html', {'messages': messages_received})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    if not message.read:
        message.read = True
        message.save()
    return render(request, 'communications/message_detail.html', {'message': message})
