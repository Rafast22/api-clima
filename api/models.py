from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(models.Model):
    username  = models.CharField(max_length=100, blank=False, default='', unique=True) #models.DateTimeField(auto_now_add=True)
    password  = models.CharField(max_length=100, blank=False, default='')
    email  = models.TextField(max_length=100, blank=False, null=False, unique=True)
    first_name  = models.CharField(max_length=100, blank=False, default='') 
    last_name  = models.CharField(max_length=100, blank=False, default='') #models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    is_superuser  = models.BooleanField(default=False) # models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined =  models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['date_joined']

