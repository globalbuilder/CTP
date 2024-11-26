from datetime import datetime
from communications.models import Message

def current_year(request):
    return {'current_year': datetime.now().year}

def unread_messages_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
