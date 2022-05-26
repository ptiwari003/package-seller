from django.contrib import admin

# Register your models here.

from .models import (
    Activity,
)


class ActivityAdmin(admin.ModelAdmin):
    pass



admin.site.register(Activity, ActivityAdmin)


