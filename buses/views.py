import imp
import pstats
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from hotels.models import ImageResource
from Cities.models import CityPair
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes


from urllib.parse import parse_qs

from .serializers import (
    BusSerializer, TypeSerializer
)


from django.db.models import Q


from .models import (BusType, BusImage, Bus)

""" utils """
@transaction.atomic()
def _create_and_attach(image, bus):
    _resource_file = ImageResource()
    _resource_file.image = image
    
    _resource_file.save()
    
    _bus_image = BusImage()
    
    _bus_image.bus = bus
    _bus_image.image = _resource_file
    
    _bus_image.save()
    
    return _bus_image



def _get_first_item(dictionary, key):
    return dictionary[key][0]


""" utils """

@api_view(['GET'])
@transaction.atomic()
@authentication_classes([TokenAuthentication])
def get_bus_type(request):
    _data = BusType.objects.all()
    _serializer = TypeSerializer(_data, many=True)
    
    return Response(_serializer.data, 200) 



# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @transaction.atomic()
# def create_bus(request):
#     _serializer = BusSerializer(data= {**request.data})
#     if _serializer.is_valid():
#         _serializer.save()
        
#         return Response(_serializer.data, 200)
    
#     return Response(_serializer.errors, 400)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@transaction.atomic()
def create_bus(request):
    print(request.data.get('pair'))
    __pair__ = CityPair.objects.get(pk=request.data.get('pair'))
    __type_ = BusType.objects.get(pk=request.data.get('type'))
    _bus_ =  Bus(**{**request.data, 'pair':__pair__, 'type':__type_})
    
    _bus_.save()
    _data = BusSerializer(_bus_)
    print("BUS ADDING DATA")
    print(_data.data)
    return Response({'message':'Bus created'})


@api_view(['POST'])
@transaction.atomic()
@authentication_classes([TokenAuthentication])
def add_images(request, busId):
    
    try:
        _bus = Bus.objects.get(pk=busId)
        _files = request.FILES.getlist('file')
        
        
        
        if not _bus:
            return Response({'id': None, 'message':f'Bus cannot be found' }, status=status.HTTP_400_BAD_REQUEST)
            
        
        if not _files or len(_files) < 1:
            return Response({'id': None, 'message':f'Images cannot be added to the Bus' }, status=status.HTTP_400_BAD_REQUEST)
            
        _added = [ _create_and_attach(x, _bus) for x in _files]
        
        print(_added)
        
        return Response({'message':'Images added successfully'}, 200)
    
        
    except Exception as e:
        print(e)
        return Response({'id': "OK", 'message':f'Internal Error'}, 400)
        
        
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_bus_type(request):
    _serializer = TypeSerializer(data={**request.data})
    
    if _serializer.is_valid():
        _serializer.save()
        
        return Response(_serializer.data, 200)
    
    return Response(_serializer.errors, 400)


@api_view(['GET'])
@transaction.atomic()
def get_bus_type_citywise(request,city):
    _data = Bus.objects.all().filter(pair=city)
    _serializer = BusSerializer(_data, many=True)
    return Response(_serializer.data, 200) 



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_buses(request):
    _query = parse_qs(request.GET.urlencode())
    
    _query_dict = _query
    
    print(_query_dict)
    
    if('city' in _query_dict.keys()) and ('type' in _query_dict.keys()):
        _city = _get_first_item(_query_dict, 'city')
        _type = _get_first_item(_query_dict, 'type')
        
        print((_city, _type))
        
        _bus_objects = Bus.objects.filter(
            Q(pair__source__name = _city) & Q(type__pk = _type)
        )
        
        _serailizer = BusSerializer(_bus_objects, many=True)
        
        return Response(_serailizer.data, 200)    
    
    return Response({'message':'NOP'})


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# def get_buses(request):
#     _query = parse_qs(request.GET.urlencode())
    
#     _query_dict = _query
    
#     print(_query_dict)
    
#     if('city' in _query_dict.keys()) and ('type' in _query_dict.keys()):
#         _city = _get_first_item(_query_dict, 'city')
#         _type = _get_first_item(_query_dict, 'type')
        
#         print((_city, _type))
        
#         _bus_objects = Bus.objects.filter(
#             Q(source__name__icontains = _city) & Q(type__pk = _type)
#         )
        
#         _serailizer = BusSerializer(_bus_objects, many=True)
        
#         return Response(_serailizer.data, 200)    
    
#     return Response({'message':'NOP'})




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_hotels():
    pass

 