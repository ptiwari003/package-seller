from django import views
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication


from hotels.serializers import HotelSerializer
from .models import (
    Hotel,
    HotelCategory,
    ImageResource,
    Room,
    RoomCategory,
    HotelImage,
    MealPlan
)

from Cities.models import City

from django.db import transaction



""" utils """

def _create_and_attach(file, hotel):
  
    _resouce_file = ImageResource()
    _resouce_file.image = file
    
    _resouce_file.save()
    
    _hotel_image = HotelImage()
    
    _hotel_image.hotel = hotel
    _hotel_image.image = _resouce_file
    
    _hotel_image.save()
    
    return _hotel_image
    

""" utils """

@api_view(['POST'])
@transaction.atomic()
@authentication_classes([TokenAuthentication])
def create_hotel(request,  category, city):
    
    try:
        _hotel = Hotel(**request.data)
        _category = HotelCategory.objects.get(pk=category)
        _city = City.objects.get(pk=city)
        
        if not _category:
            return Response({'message':'Category cannot be found'}, 400)
        
        if not _category:
            return Response({'message':'City cannot be found'}, 400)
        
            
        _hotel.category = _category
        _hotel.city = _city
        
        _hotel.save()
        
        return Response({'id':_hotel.pk, 'message':'Hotel Created Successfully'}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'Hotel Cannot be created'}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@transaction.atomic()
@authentication_classes([TokenAuthentication])
def add_room(request, hotel, category):
    
    try:
        _hotel = Hotel.objects.get(pk= hotel)
        _category = RoomCategory.objects.get(pk=category)
        
        if not _hotel:
            return Response({'message':'Hotel cannot be found'}, 400)
        

        if not _category:
            return Response({'message':'Category canot be found'})
        
        
        _room =  Room(**request.data)
        
        _room.category = _category
        
        _room.hotel = _hotel
        
        _room.save()
        
        return Response({'id':_room.pk, 'message':f'Room added to Successfully {_hotel.name} successfully' }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'id':_room.pk, 'message':f'Room Cannot be added' }, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_images(request, hotel):
    
    try:
        _hotel = Hotel.objects.get(pk=hotel)
        _files = request.FILES.getlist('file')
        
        
        
        if not _hotel:
            return Response({'id': None, 'message':f'Hotel cannot be found' }, status=status.HTTP_400_BAD_REQUEST)
            
        
        if not _files or len(_files) < 1:
            return Response({'id': None, 'message':f'Images cannot be added to the hotel' }, status=status.HTTP_400_BAD_REQUEST)
            
        _added = [ _create_and_attach(x, _hotel) for x in _files]
        
        print(_added)
        
        return Response({'message':'Images added successfully'}, 200)
    
        
    except Exception as e:
        print(e)
        return Response({'id': "OK", 'message':f'Internal Error'}, 400)
        
        
        
@api_view(['POST'])
@transaction.atomic()
@authentication_classes([TokenAuthentication])
def add_meal(request, room, hotel):
    
    try:
        _room = Room.objects.get(pk=room)
        _hotel = Hotel.objects.get(pk=hotel)    
        
        
        if not _room:
            return Response ({'message':'Room cannot be found'}, 400)
        
        if not _hotel:
            return Response({'message':'Hotel cannot be found'}, 400)
        
        _meal_plan = MealPlan(**request.data)
        
        _meal_plan.hotel = _hotel
        _meal_plan.room = _room
        
        _meal_plan.save()
        
        
        return Response({'message':'Meal plan added to the Room'}, 200)
    except Exception as e:
        print(e)
        return Response({'message':'Internal Error'}, 400)
    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_hotel_list(request, city, category):
    _hotel_objects = Hotel.objects.filter(
        Q(city__pk = city) & Q(category__id = category)
    ) 
    
    _serializer = HotelSerializer(_hotel_objects, many=True)
           
    return Response( _serializer.data , 200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_hotel_list_in_city(_, city):
    _hotel_objects = Hotel.objects.filter(
        Q(city__name__icontains = city)
    ) 
    
    _serializer = HotelSerializer(_hotel_objects, many=True)
           
    return Response( _serializer.data , 200)





