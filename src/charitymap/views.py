from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import Http404
from charitymap.models import Locations
from .forms import CreateUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def index(request):
    data = []
    url = "Home Page"
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
    return render(request, 'home.html', { 'data': data, "page_url":url })


def test(request):  # new
    try:
        locations = Locations.objects.all()
    except Locations.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'test.html', { 'data': locations })


def register(request):
    url = "Register"
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CreateUserForm()
    return render (request, 'register.html', {"register_form": form, "page_url": url })


def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"