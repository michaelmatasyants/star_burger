from django.contrib import admin

from places.models import Place


@admin.register(Place)
class PlaceAdmmin(admin.ModelAdmin):
    list_display = ['address', 'lon', 'lat', 'update_date']
