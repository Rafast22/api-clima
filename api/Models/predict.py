from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Predict(models.Model):
    date  = models.CharField(max_length=11, blank=False, unique=True) #models.DateTimeField(auto_now_add=True)
    PRECTOTCORR  = models.DecimalField(max_digits=10, decimal_places=2, null=True)
   
    

    class Meta:
        ordering = ['date']

