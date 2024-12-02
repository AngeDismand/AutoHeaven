from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.core.serializers.json import DjangoJSONEncoder
import json

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.session.modified:
            if 'last_activity' in request.session:
                last_activity_str = request.session['last_activity']
                last_activity = timezone.datetime.strptime(last_activity_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                session_timeout = settings.SESSION_COOKIE_AGE
                if timezone.now() - last_activity > timezone.timedelta(seconds=session_timeout):
                    logout(request)
                    return redirect('login') 

        request.session['last_activity'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        response = self.get_response(request)
        return response
