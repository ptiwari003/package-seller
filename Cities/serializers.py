from unicodedata import name
from .models import City, CityPair
from rest_framework import serializers

class Pair:
    
    def __init__(self, id, source, destination) -> None:
        self.source = source
        self.destination = destination
        self.id = id
        


class PairListSerialzier(serializers.Serializer):
    
    source = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length = 255)
    id = serializers.IntegerField()
    
    

class PairSerializer(serializers.Serializer):
    
    source = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length = 255)



    def create(self, validated_data):
        _source, _  = City.objects.get_or_create(name=validated_data.get('source'), is_active=True)
        _destination, __  = City.objects.get_or_create(name=validated_data.get('destination'), is_active=True)
        
        return CityPair.objects.create(source= _source, destination= _destination)
    

    
    
class CitySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = City
        fields = '__all__'
        
    
           