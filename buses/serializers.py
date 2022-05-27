from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import BusImage, BusType, Bus
from Cities.serializers import CitySerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusType
        fields = '__all__'
        



class BusSerializer(serializers.ModelSerializer):
    
    type = TypeSerializer()
    base_price = serializers.SerializerMethodField('_get_base_price_')
    images = serializers.SerializerMethodField('_get_images_')    
    
    class Meta:
        model = Bus
        fields = ['id', 'boarding_point', 'dropping_point', 'operator_name', 'pricing', 'type', 'pair', 'tax', 'base_price', 'images']
        
        
    def _get_base_price_(self, instance):
        return  ((instance.pricing * instance.tax) / 100) + instance.pricing
    
    def _get_images_(self, instance):
        _images = BusImage.objects.filter(bus__pk= instance.pk)
        return [_images[0].image.image.url for _image in _images]


# class BusSerializer(serializers.ModelSerializer):
    
#     type = TypeSerializer()
#     base_price = serializers.SerializerMethodField('_get_base_price_')
#     images = serializers.SerializerMethodField('_get_images_')    
    
#     class Meta:
#         model = Bus
#         fields = ['id', 'boarding_point', 'dropping_point', 'operator_name', 'pricing', 'type', 'source', 'tax', 'base_price', 'images']
        
        
#     def _get_base_price_(self, instance):
#         return  ((instance.pricing * instance.tax) / 100) + instance.pricing
    
#     def _get_images_(self, instance):
#         _images = BusImage.objects.filter(bus__pk= instance.pk)
#         return [_images[0].image.image.url for _image in _images]
    