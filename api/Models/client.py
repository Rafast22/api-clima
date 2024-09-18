from django.db import models
from ..Models.cultivo import Cultivo
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Client(models.Model):
    id = models.IntegerField(blank=False, unique=True, primary_key=True, auto_created=True)
    create_date  = models.DateTimeField(max_length=11, blank=True, unique=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(max_length=11, blank=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
