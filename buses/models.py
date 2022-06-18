from django.db import models
from Cities.models import (
    City,
    CityPair
)
from hotels.models import Hotel
# Create your models here.

from hotels.models import ImageResource


class BusType(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    
    def __str__(self) -> str:
        return f"{self.name}"
    



class Bus(models.Model):
    
    boarding_point = models.TextField()
    dropping_point = models.TextField()
    operator_name = models.CharField(max_length=255, default="")
    pricing = models.IntegerField()
    tax = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
    type = models.ForeignKey(BusType, on_delete=models.PROTECT)        
    pair = models.ForeignKey(CityPair, related_name="bus_city_pair", on_delete=models.PROTECT,null=True)


    def __str__(self):
        return f"{self.type.name} #{self.pk}"
    

class BusImage(models.Model):
    
    bus = models.ForeignKey(Bus, related_name="pivot_bus", on_delete=models.PROTECT)
    image = models.ForeignKey(ImageResource, related_name="pivot_image", on_delete=models.PROTECT)


# class Bus(models.Model):
    
#     boarding_point = models.TextField()
#     dropping_point = models.TextField()
#     operator_name = models.CharField(max_length=255, default="")
#     pricing = models.IntegerField()
#     tax = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
#     type = models.ForeignKey(BusType, on_delete=models.PROTECT)        
#     source = models.ForeignKey(City, related_name="bus_city", on_delete=models.PROTECT)


#     def __str__(self):
#         return f"{self.type.name} #{self.pk}"
    

# class BusImage(models.Model):
    
#     bus = models.ForeignKey(Bus, related_name="pivot_bus", on_delete=models.PROTECT)
#     image = models.ForeignKey(ImageResource, related_name="pivot_image", on_delete=models.PROTECT)




