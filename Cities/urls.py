from xml.etree.ElementInclude import include
from django.urls import path
from .views import PairList


urlpatterns = [
    path('pairs', PairList.as_view(), name="city_pair")
]