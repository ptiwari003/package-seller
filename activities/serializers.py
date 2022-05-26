from dataclasses import field
from statistics import mode
from rest_framework import serializers
from Cities.models import City
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):

    base_price = serializers.SerializerMethodField('_get_base_price_')

    class Meta:
        model = Activity
        fields = '__all__'
    

    def _get_base_price_(self, instance):
        return ( (instance.price * instance.tax) /100) + instance.price