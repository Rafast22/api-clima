from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User, Group, Permission
from  django.utils import timezone
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
     
    # username  = models.CharField(max_length=100, blank=False, default='', unique=True) #models.DateTimeField(auto_now_add=True)
    # password  = models.CharField(max_length=100, blank=False, default='')
    # email  = models.TextField(max_length=100, blank=False, null=False, unique=True)
    # first_name  = models.CharField(max_length=100, blank=False, default='') 
    # last_name  = models.CharField(max_length=100, blank=False, default='') #models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=False, default="user")
    # date_joined =  models.DateTimeField(auto_now_add=True)
    last_login =  models.DateTimeField( auto_now=True)
    
    groups = models.ManyToManyField( Group, related_name='custom_user_set' )

    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    class Meta:
        ordering = ['date_joined']

