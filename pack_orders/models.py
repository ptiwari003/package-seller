from statistics import mode
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class PackageDetail(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    state = models.CharField(max_length=255)
    created_by = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.name
    
    
class OrderDetail(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=55)
    
    pricing_details = models.TextField()
    markup_details = models.TextField()
    order_details = models.TextField()
    trip_details = models.TextField(default= "")
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT)
