from django.db import models
#from ..models.Cultivo.model import Cultivo
from .user import User


class Client(models.Model):
    create_date  = models.DateTimeField(max_length=11, blank=True, unique=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(max_length=11, blank=True, auto_now_add=True) #models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    class Meta:
        ordering = ['id']
        
        
