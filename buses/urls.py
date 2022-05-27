from unicodedata import name
from django.urls import path
from .views import (
    add_images,
    get_bus_type,
    create_bus,
    create_bus_type,
    get_buses
)

urlpatterns = [
    path('list/<int:city>', get_bus_type_citywise, name="hotel_crud_view"),
    path('types', get_bus_type, name="hotel_crud_view"),
    path('bus/types', create_bus_type, name="create_bus_type"),
    path('add_bus', create_bus, name='add_bus'),
    path('get', get_buses, name='get_bus'),
    path('add_images/<int:busId>', add_images, name='add_images_bus'),
]