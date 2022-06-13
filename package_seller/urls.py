"""package_seller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from buses.admin import bus_site
from rest_framework.authtoken import views



from django.conf.urls.static import static

urlpatterns = [
    path('authenticate', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('buses/', bus_site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("v1/cities/", include('Cities.urls')),
    path("v1/hotels/", include('hotels.urls')),
    path("v1/activities/", include('activities.urls')),
    path("v1/buses/", include('buses.urls')),
    path("v1/packages/", include('pack_orders.urls')),
    path('agent/', include('uiflow.urls'))
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) + static(settings.STATIC_URL , document_root= settings.STATIC_ROOT)






