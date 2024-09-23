from django.db import models
from .client import Client
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Cultivo(models.Model):
    
    class Cycle(models.IntegerChoices):
        EARLY = 1
        SEMI_PRECOCIUS = 2
        MEDIUM = 3
        LATE = 4

    
    create_date  = models.DateTimeField(max_length=11, blank=False, unique=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(max_length=11, blank=False, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    name = models.TextField(max_length=32, blank=False, unique=True)
    variety = models.TextField(max_length=32, blank=True)
    cycle_duration = models.IntegerField(null=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['id']
