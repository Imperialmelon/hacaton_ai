from rest_framework import permissions
from .redis import session_storage
from .models import User

from rest_framework import authentication
from rest_framework import exceptions

from django.contrib.auth.models import AnonymousUser
class Auth_by_Session(authentication.BaseAuthentication):
    def authenticate(self, request):
        session_id = request.COOKIES.get('session_id')
        print(session_id)
        if session_id is None:
            raise exceptions.AuthenticationFailed('Authentication failed')
        try:
            user_name = session_storage.get(session_id).decode('utf-8')
            print(user_name)
        except:
            raise exceptions.AuthenticationFailed('The user is not authorized')
        user = User.objects.get(username=user_name)
        return user, None

