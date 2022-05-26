from django.db import models

# Create your models here.

class PackageDetail(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    state = models.CharField(max_length=255)
    created_by = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.name
