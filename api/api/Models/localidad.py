from django.db import models
from ..Models.client import Client
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Localidad(models.Model):
    # date = models.DateTimeField(max_length=11, blank=False, unique=True, primary_key=True) #models.DateTimeField(auto_now_add=True)
    Latitude = models.DecimalField(max_digits=100, decimal_places=15, null=True)
    Longitude = models.DecimalField(max_digits=100, decimal_places=2, null=True)
    Client = models.ManyToOneRel(Client,on_delete=models.CASCADE)
    
    

    class Meta:
        ordering = ['date']

