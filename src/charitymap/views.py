from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from charitymap.models import Locations

# Create your views here.

def index(request):
    data = []
    try:
        locations = Locations.objects.all()
        for x in locations:
            location = str(x.geolocation).split(",")
            json = {
                "name": x.name,
                "address": x.address,
                "type": int(x.type),
                "geolocation": {
                    "longitude": float(location[0]),
                    "latitude": float(location[1])
                }
            }
            data.append(json)
    except Locations.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'home.html', { 'data': data })


def test(request):  # new
    try:
        locations = Locations.objects.all()
    except Locations.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'test.html', { 'data': locations })


def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"