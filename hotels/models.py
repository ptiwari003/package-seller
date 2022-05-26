from pyexpat import model
from statistics import mode
from django.db import models

from Cities.models import City



# Create your models here.
class HotelCategory(models.Model):
    name = models.CharField(max_length=56)
    
    class Meta:
        verbose_name_plural = 'Hotel Categories'
    
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class RoomCategory(models.Model):
    name = models.CharField(max_length=56)

    class Meta:
        verbose_name_plural = 'Room Categories'
    

    def __str__(self) -> str:
        return f"{self.name}"
    
    

class ImageResource(models.Model):
    image = models.ImageField(
        upload_to= "images"
    )
    
    
    def __str__(self) -> str:
        return self.image.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField(default=0)
    address = models.CharField(max_length=255, default="* Mandatory")
    budget = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    
    category = models.ForeignKey(HotelCategory, related_name="hotel_category", on_delete=models.PROTECT)
    
    city = models.ForeignKey(City, related_name="hotel_in_city", on_delete= models.PROTECT)
    
    
    def __str__(self) -> str:
        return self.name
    
    

class Room(models.Model):
    category = models.ForeignKey(RoomCategory, related_name="room_category", on_delete=models.PROTECT)
    hotel = models.ForeignKey(Hotel, related_name="hotel_room_key", on_delete=models.PROTECT)
    base_price = models.IntegerField()
    selling_price = models.IntegerField()
    cost_price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.FloatField(default=5.0) 
    

    
    def __str__(self) -> str:
        return f"{self.pk} <= {self.hotel.name}"
    
class MealPlan(models.Model):
    
    name = models.CharField(max_length=56)
    description = models.TextField()
    pricing = models.IntegerField(default=0)
    configurable = models.BooleanField(default=True)
    room = models.ForeignKey(Room, related_name="room_meal_plan", on_delete= models.PROTECT)
    hotel = models.ForeignKey(Hotel, related_name="meal_hotel", on_delete=models.PROTECT)
    
    
    def __str__(self) -> str:
        return f"{self.name} [Room Id:{self.room.pk}] => {self.hotel.name}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="hotel_image", on_delete=models.PROTECT)
    image = models.ForeignKey(ImageResource, related_name="hotel_image", on_delete=models.PROTECT)
    
    
    