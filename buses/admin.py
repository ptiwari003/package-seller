from unittest import suite
from django.contrib import admin

# Register your models here.

from .models import (
    BusImage,
    BusType,
    Bus,
)




admin.site.register(BusImage)
admin.site.register(BusType)
admin.site.register(Bus)






class BusAdmin(admin.AdminSite):
    
    site_header = "BusAdmin"
    


class BusModelAdmin(admin.ModelAdmin):
    pass


    

bus_site = BusAdmin(name="bus_admin")


bus_site.register(Bus)