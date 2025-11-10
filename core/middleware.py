from django.utils import timezone
from django.contrib.auth.models import User

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Update last activity timestamp for authenticated users
        if request.user.is_authenticated:
            profile = request.user.profile
            profile.last_activity = timezone.now()
            profile.save(update_fields=['last_activity'])
        
        return response
