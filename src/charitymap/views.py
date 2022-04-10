from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import Http404
from charitymap.models import Locations
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def index(request):
    logged_in = False
    if request.user.is_authenticated:
        logged_in = True

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
    return render(request, 'home.html', { 'data': data, "page_url":url, "is_auth": logged_in })


def test(request):  # new
    try:
        locations = Locations.objects.all()
    except Locations.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'test.html', { 'data': locations })


def register_req(request):
    if request.user.is_authenticated:
        return redirect("/")

    url = "Register"
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            redirect("/")
            return messages.success(request, "Registration successful." )
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CreateUserForm()
    return render (request, 'register.html', {"register_form": form, "page_url": url })


def login_req(request):
    if request.user.is_authenticated:
        return redirect("/")

    url = "Login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You successfully logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", { "login_form": form, "page_url": url})


def logout_req(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
        # Could add a see you next time
    else:
        return redirect("/")


def suggest_location(request):
    logged_in = False
    if request.user.is_authenticated:
        logged_in = True
    else:
        return redirect("/")

    url = "Suggest Location"
    return render(request, "suggest.html", { "page_url": url, "is_auth": logged_in })


def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"