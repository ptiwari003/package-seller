from django import views
from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CityPair
from .serializers import (Pair, PairSerializer, PairListSerialzier)

class PairList(APIView):
    
    def get(self, _, format=None):
        _pair_datasource = [ Pair(p.pk, p.source.name, p.destination.name, p.source.pk, p.destination.pk) for p in CityPair.objects.all() ]

        _pairs = PairListSerialzier(_pair_datasource, many=True)
        
        return Response(_pairs.data, status=status.HTTP_200_OK)
     
     
    
    def post(self, request, format=None):
        
        _serailizer = PairSerializer(data= request.data)
        
        if _serailizer.is_valid():
            _serailizer.save()
            return Response(_serailizer.data, status= status.HTTP_201_CREATED)
    
        return Response(_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
