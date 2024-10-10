# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User
class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        try:
            # user = request.get("username")
            # if user == None:
                
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None