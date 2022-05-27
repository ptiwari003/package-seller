from dataclasses import field, fields
from pyexpat import model
from re import L
from statistics import mode
from Cities.serializers import CityModelSerializer,CitySerializer

from .models import HotelCategory, HotelImage, RoomCategory, Hotel, MealPlan, Room
from rest_framework.serializers import ModelSerializer, SerializerMethodField



class HotelCategorySerializer(ModelSerializer):
    class Meta:
        model = HotelCategory
        fields = ['id', 'name']

class HotelSerializer(ModelSerializer):
    city = CityModelSerializer(many=False)
    category = HotelCategorySerializer(many=False)
    class Meta:
        model=Hotel
        fields=['id', 'name','stars','address','budget','is_active','category','city']

        

class RoomCategorySerializer(ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = ['id', 'name']
        

class RoomSerializer(ModelSerializer):
    
    meals = SerializerMethodField('_get_meal_plan')
    category = RoomCategorySerializer()
    
      
    class Meta:
        model = Room
        fields = '__all__'
    
    
    def _get_meal_plan(self, instance):
        
        _meals = MealPlan.objects.filter(room__pk = instance.pk)
        
        _serailizer = MealPlanSerializer(_meals, many=True)
        
        return _serailizer.data
        
    
       


class MealPlanSerializer(ModelSerializer):
    class Meta:
        model = MealPlan
        
        fields = '__all__'



class HotelSerializer(ModelSerializer):
   
   category = HotelCategorySerializer() 
   city     =  CitySerializer()
   rooms    = SerializerMethodField('_get_rooms')
   images   = SerializerMethodField('_get_images_')
   
   
   def _get_rooms(self, instance):
       print(instance)
       _rooms =  Room.objects.filter(hotel__pk = instance.id)
       _serailizer = RoomSerializer(_rooms, many=True)
       return _serailizer.data
       
   
   def _get_images_ (self, instance):
       _images = HotelImage.objects.filter(hotel__pk= instance.pk)
       print(_images)
       _image = _images[0]
       
       return [ _image.image.image.url for _image in _images]
   
   class Meta:
       model = Hotel
       fields = '__all__'
 
 
 
class HotelISerializer(ModelSerializer):
    
    class Meta:
        model = Hotel
        fields = '_all_'