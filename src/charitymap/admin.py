from django.contrib import admin
from .models import Location, SuggestedLocation, VotedLocations
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
          'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }


@admin.register(SuggestedLocation)
class SuggestedLocation(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
          'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }


admin.site.register(VotedLocations)