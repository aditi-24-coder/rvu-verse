from .models import Notification, Message

def unread_notifications_count(request):
    """Return a dictionary with unread notifications count."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}

def unread_messages_count(request):
    """Return a dictionary with unread messages count."""
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
