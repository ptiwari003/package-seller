from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.
from Cities.models import (
    City
)

class Activity(models.Model):
    
    city = models.ForeignKey(City, related_name="city", on_delete=models.PROTECT)
    name = models.CharField(max_length=55)
    description = models.TextField()
    configurable = models.BooleanField(default=True)    
    price = models.IntegerField(default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
     
    class Meta:
        verbose_name_plural = 'activities'
        
        
    def __str__(self) -> str:
        return f"{self.city} <= {self.name}"
    
    
    

