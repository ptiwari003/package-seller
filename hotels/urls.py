from unicodedata import name
from django.urls import path
from .views import HOtelCrudView, RoomCategoryCrudView,ResourcesView
from .hotels import create_hotel, add_room , add_images, add_meal, get_hotel_list, get_hotel_list_in_city, HotelListView


urlpatterns = [
    path('hotel_list/<int:city>', HotelListView.as_view(), name="hotel_list"),
    path('hotel_categories', HOtelCrudView.as_view(), name="hotel_crud_view"),
    path('room_categories', RoomCategoryCrudView.as_view(), name='room_crud_view'),
    path('resources', ResourcesView.as_view(), name='resources'),
    path('add_hotel/<int:category>/city/<int:city>', create_hotel, name='add_hotel'),
    path('add_room/<int:hotel>/roomType/<int:category>', add_room, name='add_room'),
    path('add_images/<int:hotel>', add_images, name='add_room'),
    path('add_meal/<int:room>/hotel/<int:hotel>', add_meal, name='add_meal'),
    path('fetch/hotels/<str:city>', get_hotel_list_in_city, name='hotel_list_city'),
    path('list/hotels/<int:city>/category/<int:category>', get_hotel_list, name='hotel_list')
]