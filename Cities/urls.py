from xml.etree.ElementInclude import include
from django.urls import path
from .views import PairList


urlpatterns = [
    # path('list', CityList.as_view(), name="city_List"),
    path('pairs', PairList.as_view(), name="city_pair")
]