import json
from re import L
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from activities.models import Activity

from django.db.models import Q

from .serializers import ActivitySerializer

from rest_framework.response import Response

from urllib.parse import parse_qs

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_activity(request, city):
    _serializer = ActivitySerializer(data={**request.data, 'city':city})
    if _serializer.is_valid():
        _serializer.save()
        
        return Response(_serializer.data, 200)

    return Response(_serializer.errors, 400)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def update_activity(request, id):
    _activity = Activity.objects.get(pk=id) or None
    
    if _activity is not None:
        for k, v in request.data.items():
            setattr(_activity, k, v)
        
        _activity.save()
                
        return Response( ActivitySerializer(_activity).data, 200) 
    
    return Response({'message': 'Activity not found'}, 400)
             
    
    





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_activity(request):
    _qs = request.GET.urlencode()
    _dictonary = (parse_qs(_qs))
   
    print(_dictonary)
     
    if 'q' in _dictonary.keys():
        
        _sQ = _dictonary['q'][0]
    
        if 'city' in _dictonary.keys():
            _cQ = _dictonary['city'][0]
            _data = Activity.objects.filter(
                Q(name__contains= _sQ) & Q(city__name__contains = _cQ)
            )
            _serializer=  ActivitySerializer(_data, many=True)
            return Response(_serializer.data, 200)
    
        _data = Activity.objects.filter(Q(name__contains = _sQ))
        _serializer=  ActivitySerializer(_data, many=True)
        return Response(_serializer.data, 200)
    
    _data = Activity.objects.all()
    
    _serializer = ActivitySerializer(_data, many=True)
    
    return Response(_serializer.data, 200)
    


