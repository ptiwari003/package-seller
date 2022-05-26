from cgitb import html
from functools import reduce
from multiprocessing import context
from unittest import result
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render

from django.template.loader import get_template
from django.views.generic import View
from requests import delete
from rest_framework.views import APIView
from xhtml2pdf import pisa

from operator import contains, itemgetter

from json import loads, dumps


from .models import PackageDetail

from .data import test_data, name, email, phone, tripName




def _define_dict(key, value):
    _d = dict()
    _d[key] = value
    
    return _d



def render_to_pdf(template, context_dict={}):
    
    _template = get_template(template)
    _html = _template.render(context_dict)
    
    result = BytesIO()
    
    _pdf = pisa.pisaDocument(BytesIO(_html.encode("utf-8")), result)
    
    if not _pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    
    return None



class GenerateOrder:
    
    def __init__(self, payload, markup) -> None:
        self._items = payload
        self.markup = markup
        
        
    def _map_meals_(self,room):
        return {
            **room,
            **_define_dict('meals', list(filter( lambda x: x.get('selected') == True,  room.get('meals') )) )
        }
        
        
    def _calculate_rooms_price(self, rooms):
        
        __calc_room_price = lambda price, discount, tax : (price +  price *( tax/100)) - discount

        _room_price = [ [x.get('cost_price'), x.get('tax', 12.00 ), x.get('discount')] for x in rooms] 
        
        _meal_price_ =  [ reduce( lambda x, y : x+y , list(map(lambda x: x.get('pricing'),  x)) ) for x in [list(filter( lambda mx: mx.get('selected') == True  , x.get('meals'))) for x in rooms] ]
        
        
        _ttl_price =  reduce( 
                   lambda x, y: x+y , 
                map(lambda x: __calc_room_price(x[0]+x[1][0], x[1][2], x[1][1])   ,zip(_meal_price_, _room_price)),
                0
            )
            
        return _ttl_price
    
    
    def _parse_bus_payload_(self, bus):
        
        _tax = float(bus.get('tax'))
        _pricing = float(bus.get('pricing'))
        
        return {
            'summary': bus,
            'total': _pricing + (_pricing * (_tax/ 100) )
        }
    
        
    
    def _calculate_pricing_independent_(self, item):
        
        _hotel = item.get('hotel')
        
        _rooms_ = list(filter( lambda x: x.get('selected') == True  ,_hotel.get('rooms')))
        
        
        conext =  {
            **_define_dict('dayIndex', item.get('day')),
            **_define_dict('source', item.get('source')),
            **_define_dict('destination', item.get('destination')),
            **_define_dict('activities', list(filter(lambda x: x.get('selected') == True ,item.get('activities')))),
            **_define_dict('destination_activities', list(filter(lambda x: x.get('selected') == True ,item.get('destinationActivities')))),
            **_define_dict('hotel', {
                **item.get('hotel'),
                'rooms':_rooms_
                }),
            **_define_dict('bus', self._parse_bus_payload_(item.get('bus')) )
        }
        
        
        return conext
    
    def _format_payload_acc_(self, plans):
        
        return list(
            map(
             self._map_activity_, plans   
            )
        )
    


    def _map_activity_(self, _plan):
        
        
        
        _calc_tax = lambda price, _tax_per : price + (price * (_tax_per / 100 ))
        
        _mapped_activity_ = [ {**x, 'costPrice': x.get('price'), 'basePrice': _calc_tax( float(x.get('price')),float( x.get('tax')))  } for x in _plan.get('activities') ]
        
        _activities_ = {
            'summary': _mapped_activity_,
            'total': reduce(lambda acc, next : acc + next , list(map( lambda x: x.get('basePrice'),_mapped_activity_ )) , 0 )        
        }
        
        
         
        return ({
            'dayIndex':_plan.get('dayIndex'),
            'activities' :_activities_,
            'bus':_plan.get('bus'),
            'source':_plan.get('source'),
            'destination':_plan.get('destination'),
            'hotel':_plan.get('hotel')
        })
    
    
    
    def _calculate_hotel_pricing_(self, item):
        _rooms = item.get('hotel').get('rooms')
        
        _calc_room_price = lambda price, tax: (price * (tax/100)) + price
        
        _room_total_ =  map(lambda x: ({
            '#room_price':_calc_room_price(float(x.get('cost_price')), float(x.get('tax'))) - float(x.get('discount')),
            '#meal_price': list(map( lambda y: y.get('pricing') ,x.get('meals')))    
        }) , _rooms) 
        
        
        _room_ttl_ = map( lambda x: float(x.get('#room_price'))+ float(reduce( lambda x, y: x+y , x.get('#meal_price') )) , _room_total_)    
        
        _bus = item.get('bus').get('total')
        _activities = item.get('activities').get('total')
        
                
        return (
            reduce(lambda x,y : x+y  ,_room_ttl_ , 0)
          + _bus
          + _activities
        )
        
    
    def _calculate_plan_pricing_(self, payload):
        
        _new_payload_ = list(map(self._calculate_hotel_pricing_, payload))
        
        return reduce( lambda x, y: x+y  ,_new_payload_, 0)
        
    
    
    def _calculate_pricing_complete_(self, items, _markup):
        _items_ = [self._calculate_pricing_independent_(x) for x in items]
        _payload_  = self._format_payload_acc_(_items_)
        
        _ttl =  self._calculate_plan_pricing_(_payload_)
        
        _ttl_package_cost = float("{:.2f}".format(_ttl))
        
        _margin = _ttl *(float(_markup) /100)
        
        _package_price_ = _ttl + _margin
        _extras_ = {
            'markup':f"{_markup}%",
            'ttl_costing': _ttl,
            'margin': _margin,
            'package_price': _package_price_,
            'take_rate': (_margin / _package_price_) * 100
        }
        
        return [_payload_, _ttl_package_cost, _extras_]
    
    
    def format(self):
        return self._calculate_pricing_complete_(self._items, self.markup)
    


class PdfView(APIView):
    def post(self, request, *args, **kwargs):
        
        _customer_name = request.data.get('Name')
        _email = request.data.get('email')
        _contact = request.data.get('contact')
        _tripName = request.data.get('tripName')
        _markup = request.data.get('markup')
        _tripDetails = loads(request.data.get('tripdetails'))
        
        _plans = _tripDetails.get('plans')
        
        _details = GenerateOrder(_plans, _markup)
        
        _summary, _pricing, extras  = _details.format()
        
        context = {
            **_define_dict('Name', _customer_name),
            **_define_dict('Email', _email),
            **_define_dict('Contact', _contact),
            **_define_dict('TripName', _tripName),
            **_define_dict('Markup', _markup),
            **_define_dict('summary', _summary),
           **_define_dict('pricing', _pricing),
           **_define_dict('extras', extras),
        }
        
        _customer = {
            **_define_dict('Name', _customer_name),
            **_define_dict('Email', _email),
            **_define_dict('Contact', _contact),
            
        }
        
        __package_detail_ = dumps({
            'customer': _customer,
            'summary':_summary,
            'pricing': _pricing,
            'extras': extras
        })
        
        
        _package = PackageDetail(name= _tripName, details = __package_detail_, state ='CREATED')
        
        _package.save()
        
        
        
        
        
        _template = render( request ,'packages/index.html', context)
        return HttpResponse(_template)
    
    def get(self, request, *args, **kwargs):
        _tripDetails = test_data
        _plans = _tripDetails['plans']    
        
        _markup = 15
        
        
        
        _order_details_ = GenerateOrder(_plans, _markup)
        
        _fmt_ =  _order_details_.format()
        
        
        print(_fmt_)
        
        _template = render(request, 'packages/index.html')
        return HttpResponse(_template)
    
        
        
