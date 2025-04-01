from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notification_count': unread_notifications}
    return {}
