from csv import list_dialects
from django.contrib import admin


# Register your models here.

from .models import (
    HotelCategory,
    RoomCategory,
    Hotel,
    HotelImage,
    ImageResource,
    MealPlan,
)





admin.site.register(HotelCategory)
admin.site.register(RoomCategory)

admin.site.register(Hotel)

admin.site.register(HotelImage)


admin.site.register(MealPlan)


@admin.register(ImageResource)
class ResourceAdmin(admin.ModelAdmin):
    
    def image_tag(self, obj):
        from django.utils.html import format_html
        return format_html(f'<img src="{obj.image.url}"  width="200" height="200" />')
    
    image_tag.short_description = 'Image'
    
    list_display = ['image_tag',]
    
