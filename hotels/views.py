from json import dumps
from django.shortcuts import render
from rest_framework import views
# Create your views here.
from .models import HotelCategory, RoomCategory, ImageResource
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from .serializers import HotelCategorySerializer, RoomCategorySerializer

from rest_framework import serializers

class HOtelCrudView(views.APIView):
    
    authentication_classes = (TokenAuthentication,)
    
    def get(self, _, format=None):
        
        _hotel_categories = HotelCategory.objects.all()
        _serializer = HotelCategorySerializer(_hotel_categories, many=True)
        
        return  Response(_serializer.data, status=200)
        
    def post(self, request, format=None):
        
        _data = request.data
        
        _serializer = HotelCategorySerializer(data=_data)
        
        if _serializer.is_valid():
            
            _serializer.save()
            
            return Response(_serializer.data, status=200)
        
        return Response(_serializer.errors, 400)
    


class RoomCategoryCrudView(views.APIView):
    
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, _request, format=None):
        _room_categories = RoomCategory.objects.all()
        _serializer = RoomCategorySerializer(_room_categories, many=True)
        
        return Response(_serializer.data, 200)
    
    
    def post(delf, request, format=None):
        _data = request.data
        
        _serializer = RoomCategorySerializer(data=_data)
        
        if _serializer.is_valid():
            
            _serializer.save()
            
            return Response(_serializer.data, status=200)
        
        return Response(_serializer.errors, 400)
    
    


class ResourcesView(views.APIView):
    
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, format=None):
        return Response([], 200)
    
    
    def post(self, request, format=None):
        _file = request.FILES['file']
        _im = ImageResource()
        _im.image = _file
        
        _im.save()
        
            
        return Response({'name': _im.image.name, 'url': _im.image.url,  'id': _im.pk}, 200)
    
    
    
class UserProfileView(views.APIView):
    
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, format=None):
        _user_data_ = request.user
        
        return Response({'username': _user_data_.username})
        
        

