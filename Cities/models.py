from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=120)
    
        

class City(models.Model):

        
    name = models.TextField(null=False, blank=False, max_length=100)
    is_active= models.BooleanField()

    class Meta:
        verbose_name_plural = "city"
        
    def __str__(self) -> str:
        return f"{self.name}"


class CityPair(models.Model):
    
    source = models.ForeignKey(City, on_delete=models.PROTECT, related_name="source_id")
    destination = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_id")
    
    class Meta:
        verbose_name_plural = "City Pairs"
        unique_together = ['source', 'destination'] 
    
    def __str__(self) -> str:
        return f"{self.source.name} - {self.destination.name}"
    
