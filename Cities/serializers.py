from unicodedata import name
from .models import City, CityPair
from rest_framework import serializers

class Pair:
    
    def __init__(self, id, source, destination, source_id ,destination_id) -> None:
        self.id = id
        self.source = source
        self.destination = destination
        self.destination_id= destination_id
        self.source_id= source_id


class PairListSerialzier(serializers.Serializer):
    id = serializers.IntegerField()
    source = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length = 255)
    destination_id = serializers.IntegerField()
    source_id = serializers.IntegerField()
    
    

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
        
    
           