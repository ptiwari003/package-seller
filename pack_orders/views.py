from dataclasses import fields
from email import message
from functools import reduce
from multiprocessing import context
from pyexpat import model
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from django.template.loader import get_template
from django.views.generic import View
from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from json import dumps
from rest_framework.decorators import api_view, authentication_classes , permission_classes


NONE = '----'

from xhtml2pdf import pisa

from operator import contains, itemgetter

from json import loads, dumps


from .models import OrderDetail, PackageDetail

from .data import test_data

class Planner :
    
    def __init__(self, data) -> None:
        self.data = data
        
    def get_formated(self):
        _calculated = self.__calculate__()
        return _calculated

    def __format_days__(self, data):
        return [ {**x, 'day': x.get('day')+1 } for x in data]
    
    
    def _get_activity_price_(self, activities):
        return reduce( lambda x, y: x + y , [ (float(x[0]) + float(x[1])) for x in  [ (x.get('price'), x.get('tax', 0)) for x in activities ]])
    
    
    
    def _calculate_hotel_cost (self, hotel):
        _total = 0
        _meal_pricing = 0
        
        if hotel is not None:
            for room in hotel.get('rooms'):
                _price = float(room.get('cost_price', 0))
                _tax = float(room.get('tax', 0))
                
                _room_price_ = _price + ( _price * (_tax / 100))
                
                for meal in room.get('meals', []):
                    _m_price = float(meal.get('pricing'))
                    _ttl_price_ = _room_price_ + _m_price
                    _meal_pricing += _m_price
                    
                    _total += _ttl_price_
                    
        
        return _total
    
    def _add_record_(self,  day ,activities, hotel, bus):
        return dict(day=day, activities=activities, hotel=hotel, bus=bus)
    
    
    def _calculate_bus_price(self, bus):
        if bus is not None:
            _price = float(bus.get('pricing', 0))
            _tax = float(bus.get('tax', 0))
            
            return _price + (_price * (_tax / 100))
        
        return 0
    
    
    
    def __calculate__(self):
        
        _totals = []
        _package_cost_ = 0
        
        for x in self.__format_days__(self.data):
            
            day = x.get('day')
            
            if day ==1 :
               _activities = self._get_activity_price_(x.get('activities'))
               _bus = self._calculate_bus_price(x.get('bus', None))
               _totals.append(self._add_record_(day, _activities, NONE,_bus))
               
            elif day == len(self.data):
                _activities = self._get_activity_price_(x.get('destinationActivities', []))
                _bus = self._calculate_bus_price(x.get('returns', None))
                _totals.append(self._add_record_(day, _activities, NONE, _bus))
                
            else:
                _activities = self._get_activity_price_(x.get('destinationActivities', []))
                _hotel = self._calculate_hotel_cost(x.get('hotel', None))
                _totals.append(self._add_record_(day, _activities, _hotel, NONE))
                 
        
        for _record_ in _totals:
            if _record_.get('activities') is not None:
                _package_cost_ += float(_record_.get('activities', 0))
            
            if _record_.get('bus') is not NONE:
                _package_cost_ += float(_record_.get('bus', 0))
            
            if _record_.get('hotel') is not NONE:
                _package_cost_ += float(_record_.get('hotel', 0))
                
                
        return  {
            'data':self.__format_days__(self.data),
            'pricing_summary':_totals,
            'package_costing': _package_cost_
        }
    

    
    

class PdfView(APIView):
    
    authentication_classes = ()
    permission_classes = ()
    
    def post(self, request, *args, **kwargs):
        _data = Planner(request.data.get('plans'))
        
        if request.data.get('planningFor') is None:
            return Response(dict(message='Plannig for is Required'))
        
        if request.data.get('tripName') is None:
            return Response(dict(message='Plannig for is Required'))
        
        
        context = {
            'Name':request.data.get('customer', 0),
            'tripName':request.data.get('tripName'),
            'planningFor':request.data.get('planningFor'),
            'data': _data.get_formated(),
            
        }
        
        return Response(context, 200)        
        #return render(request, 'packages/finalize.html', context)
    
    
    def get(self, request, *args, **kwargs):
        
        _data = Planner(test_data.get('plans'))
        
        context = {
            'Name':test_data.get('customer', 0),
            'tripName':test_data.get('tripName'),
            'planningFor':test_data.get('planingFor'),
            'data': _data.get_formated(),
            'dataLength':len(test_data.get('plans'))
        }
        
        return render(request, 'packages/finalize.html', context)
    
    
class CalculateTAkeRate(APIView):
    
    def post(self, request, *args, **kwargs):
        
        _data = request.data
        
        _Package_price = _data.get('costing', 0)
        
        if not _Package_price > 0 :
            return Response(dict(message='Package cost cannot be zero'), 400)
        _markup = _data.get('markup', 1)

        if not _markup > 0:
            return Response(dict(message='Markup Percentage cannot be zero'), 400)
        
        _margin = float(_Package_price) * (float(_markup) / 100)
        
        _order_base = float(_Package_price) + float(_margin)
        
        take_rate = round(float(_margin/_order_base) * 100, 2)
        
        
        context = dict(margin= f"₹ { _margin}", totalCost= f"₹ {_order_base}" , takeRate= f"{take_rate} %", packageCost=f"₹ {_Package_price}",)
        
        return Response(context, 200)
        
            
            
            
class OrderGeneration(APIView):
    
    def isNotNull(self, data):
        print(type(data))
        
        if data is None:
            return False
        
        if(isinstance(data, dict)):
            return len(data.keys()) > 0
        
        if(isinstance(data, list)):
            return len(data) > 0
        
        if(isinstance(data, str)):
            return len(data) > 0
        
        return False  
    
    def post(self, request, *args, **kwargs):
        
        _user = request.user
        
        order_details = request.data.get('plans')
        markup_details = request.data.get('marking')
        pricing_details = request.data.get('costing')
        trip_details = request.data.get('trip')
        name = request.data.get('customer').get('name')
        email = request.data.get('customer').get('email')
        contact = request.data.get('customer').get('contact')
        
        
        validation_list  = [
            self.isNotNull(name),
            self.isNotNull(contact),
            self.isNotNull(email),
            self.isNotNull(order_details),
            self.isNotNull(markup_details),
            self.isNotNull(pricing_details),
            self.isNotNull(trip_details)
        ]
         
        
        if(reduce( lambda x, y : x and y, validation_list)):
            
            _payload = dict(
                name=name,
                contact=contact, 
                email=email, 
                order_details=dumps(order_details), 
                markup_details=dumps(markup_details), 
                pricing_details=dumps(pricing_details), 
                trip_details=dumps(trip_details), 
                created_by=request.user
                )
            _order = OrderDetail.objects.create(**_payload)
            return Response(dict(message=f"Order Generated successfully", ), 200)
            
        return Response(dict(message='Order Cannot be generated at this time try again'), 200)
    



class OrderListSerializer(serializers.ModelSerializer):
    
    tripName = serializers.SerializerMethodField('_get_trip')
    tripDescription = serializers.SerializerMethodField('_get_trip_description')
    pricing = serializers.SerializerMethodField('_get_pricing')
    
    class Meta:
        model = OrderDetail
        fields = ['id', 'name', 'contact', 'tripName' , 'tripDescription', 'pricing']
        
    def _get_trip(self, _object):
        _trip_details = loads(_object.trip_details)
        return _trip_details.get('tripName')
        
    def _get_trip_description(sel, _object):
        _trip_details = loads(_object.trip_details)
        return _trip_details.get('description')
        
    
    def _get_pricing(self, _object):
        _markup = loads(_object.markup_details)
        
        
        return _markup
 
 
class OrderSerializer(serializers.ModelSerializer):
    
    pricing_details = serializers.SerializerMethodField('_pricing_details')
    order_details = serializers.SerializerMethodField('_order_details')
    markup_details = serializers.SerializerMethodField('_markup_details')
    trip_details = serializers.SerializerMethodField('_trip_details')
    
    def _pricing_details(self, obj):
        return loads(obj.pricing_details)
    
    def _order_details(self, obj):
        return loads(obj.order_details)
    
    def _markup_details(self, obj):
        return loads(obj.markup_details)
    
    def _trip_details(self, obj):
        return loads(obj.trip_details)
    
    
    class Meta:
        model=OrderDetail
        fields = '__all__'
        
        
class OrderList(APIView):
    
    def get(self, request, *args, **kwargs):
        _user = request.user
        
        _serializer = OrderListSerializer(OrderDetail.objects.filter(created_by= _user), many=True)        
        return Response(_serializer.data, 200)



def _format_data_(_data):
    
    _order_data_ = Planner(_data.order_details)
    _trip_details_ = _data.trip_details
    from django.contrib.auth.models import User
    _created_by_ = User.objects.get(pk=_data.created_by)
    _details_ = _order_data_.get_formated()
    
    
    
      
    context = {
            'Name':_data.name,
            'tripName': _trip_details_.tripName,
            'tripDescription': _trip_details_.description,
            'planningFor':_trip_details_.planningFor,
            'data': _details_,
            'creator': _created_by_.username,
            'salesPrice':_data.markup_details.totalCost,
            'supportNumber':'9818247900',
            'supportEmail':'support@yolobus.in',
            'tripDetails':_data.trip_details ,
            'dataLength':len(_details_.get('data'))
        }
    
    return context



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])    
def render_pdf(request, id):
    _orderDetail = OrderDetail.objects.get(pk=id)
    
    if(_orderDetail is not None):
        
        from attrdict import AttrDict
        _serializer = OrderSerializer(_orderDetail)
        context = _format_data_(AttrDict(**_serializer.data))
        return render(request, 'packages/finalize.html', context)
        #return render(request, 'packages/order.html', context)
        
        #return Response(context, 200)
    return Response({'message':id}, 200)
