from django.urls import path

from .views import (
    create_activity, list_activity, update_activity
)

urlpatterns = [
    path('list', list_activity, name='activity_list'),
    path('create/<int:city>', create_activity, name='activity_create'),
    path('update/<int:id>', update_activity, name='update_activity')
]
