from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Cultivo(models.Model):
    
    class Cycle(models.IntegerChoices):
        EARLY = 1
        SEMI_PRECOCIUS = 2
        MEDIUM = 3
        LATE = 4

    
    id = models.IntegerField(blank=False, unique=True, primary_key=True, auto_created=True)
    create_date  = models.DateTimeField(max_length=11, blank=False, unique=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(max_length=11, blank=False, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    name = models.TextField(max_length=32, blank=False, unique=True)
    variety = models.TextField(max_length=32, blank=True)
    cycle_duration = models.IntegerField(null=True)
    client_id = models.IntegerField()
    

    class Meta:
        ordering = ['id']
