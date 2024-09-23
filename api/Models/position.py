from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Position(models.Model):
    create_date  = models.DateTimeField(max_length=11, blank=False, unique=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    client = models.ForeignKey("client")
    

    class Meta:
        ordering = ['id']
