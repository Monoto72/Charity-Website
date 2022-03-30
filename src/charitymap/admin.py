from django.contrib import admin
from .models import Locations
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
          'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }