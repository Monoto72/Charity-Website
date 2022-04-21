from turtle import distance
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import Http404
from jinja2 import Undefined
from charitymap.models import Location, SuggestedLocation, VotedLocations
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
import requests
import math
import json
import random

def index(request):
    """The landing page, this allows users, and non authenticated users to see the locations avaliable, whilst also allowing them to navigated to other areas.

    Args:
        request (object): Returns metadata

    Raises:
        Http404: If the database does not exist it will provide a 404 response

    Returns:
        route: Generates the home page with the populated entries
    """
    logged_in = False
    if request.user.is_authenticated:
        logged_in = True

    data = []
    url = "Home"
    try:
        locations = Location.objects.all()
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
    except Location.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'home.html', { 'data': data, "page_url":url, "is_auth": logged_in })


def test(request):  # new
    try:
        locations = Location.objects.all()
    except Location.DoesNotExist:
        raise Http404('Database does not exist')
    return render(request, 'test.html', { 'data': locations })


def register_req(request):
    """Allows users to register themselves, allowing them to suggest new locations, and ensure the future proofing, by inputting their locations.

    Args:
        request (object): Returns metadatar

    Returns:
        route: Generates the Register Page
        route2: Redirects to the home-page IF logged in
    """
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
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CreateUserForm()
    return render (request, 'register.html', {"register_form": form, "page_url": url })


def login_req(request):
    """Log-in system to ensure suggested locations don't get abuse... well, allows for better abuse control.

    Args:
        request (object): Returns metadata

    Returns:
        route: Generates the Login Page
        route2: Redirects to the home-page IF logged in
    """
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
    """Log-out functionality

    Ensuring a users account doesn't get abused when `AFK`

    Args:
        request (object): Returns metadata

    Returns:
        route: Redirects to the homepage after logging out
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
        # Could add a see you next time
    else:
        return redirect("/")


def suggest_location(request):
    """This generates the page `Suggested Locations`, on this page the view processes all the data and sends the information to the front end, allowing for the modals to be populates, and the general data to the page.
    On top of that, this handles the voting system and the user creation system, which will determine new routes/ areas, allowing for future proofing.

    Args:
        request (object): Returns metadata

    Raises:
        Http404: If the database does not exist it will provide a 404 response

    Returns:
        route: Generates the suggestion page with the populated entries
    """
    logged_in = False
    
    suggested_data = []

    if request.user.is_authenticated:
        logged_in = True
    else:
        return redirect("/register")

    url = "Suggest"

    try:
        suggested_locations = SuggestedLocation.objects.all()
        for x in suggested_locations:
            if not x.name == "Deleted":
                coords = str(x.geolocation).split(",")
                suggested_location = VotedLocations.objects.filter(suggestion=x).filter(user=request.user.id)
                if not suggested_location.exists():
                    json = {
                        "name": x.name,
                        "address": x.address,
                        "type": x.type,
                        "votes": int(x.votes),
                        "geolocation": {
                            "longitude": float(coords[0]),
                            "latitude": float(coords[1])
                        }
                    }
                    suggested_data.append(json)
            
    except Location.DoesNotExist:
        raise Http404('Database does not exist')
    
    if request.method == "POST":
        location = request.POST.get("location")
        location_arr = str(location).split(",")
        if "accepted_suggestion" in request.POST:
            vote_handler(suggested_locations, location_arr, True, request.user)
            return redirect("/suggest")
        elif "denied_suggestion" in request.POST:
            vote_handler(suggested_locations, location_arr, False, request.user)
            return redirect("/suggest")

    return render(request, "suggest.html", { "page_url": url, "is_auth": logged_in, "map_data": suggested_data })



def vote_handler(data, location, boolean, user):
    """Takes the data from the modal, once 10 votes are accumulated, it populates the main Locations model with the suggested location.

    Args:
        data (object): Every suggested Location in the SuggestedLocation database
        location (list): Location taken from the selected modal on front end
        boolean (boolean): iteration for the Voting addition and subtraction

    Returns:
        route: Redirects to the current page
    """
    for index, x in enumerate(data):
        db_location = str(x.geolocation).split(",")
        if db_location == location:
            iteration = x.votes+1 if boolean else x.votes-1
            if x.votes in range(10):
                if x.votes == 0:
                    if boolean:
                        SuggestedLocation.objects.filter(pk=index+1).update(votes=x.votes+1)
                elif x.votes == 9:
                    if boolean:
                        Location.objects.create(name = x.name, address = x.address, geolocation = x.geolocation, type = x.type)
                        SuggestedLocation.objects.filter(pk=index+1).update(name="Deleted")
                    elif not boolean:
                        SuggestedLocation.objects.filter(pk=index+1).update(votes=x.votes-1)
                else:
                    SuggestedLocation.objects.filter(pk=index+1).update(votes=iteration)
                VotedLocations.objects.create(user=user, suggestion=x)
    return redirect("/suggest")


def suggest_new_location(request):
    logged_in = False

    if request.user.is_authenticated:
        logged_in = True
    else:
        return redirect("/")

    url = "New Location"
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        location = request.POST.get("location")
        type = request.POST.get("type")
        
        if "accepted_suggestion" in request.POST:
            try:
                suggested_locations = SuggestedLocation.objects.filter(address=address)
                if suggested_locations.exists():
                    messages.error(request,"Location already exist!")
                    return redirect("/suggest/new")
                else:
                    SuggestedLocation.objects.create(name=name, address=address, geolocation=location, type=type)
                    return redirect("/suggest/")
            except SuggestedLocation.DoesNotExist:
                raise Http404('Database does not exist')
    return render(request, "suggest-new.html", { "page_url": url, "is_auth": logged_in })


def donate(request):
    logged_in = False
    url = "Donate"
    
    types = ["shop", "bin"]
    
    if request.user.is_authenticated:
        logged_in = True

    if request.method == "POST":
        location = request.POST.get("location").split(",")
        type = request.POST.get("type")
        transport_type = request.POST.get("transport-type")
   
        if "user_location" in request.POST:
            if type == "both":
                type = random.choice(types)
            return redirect(f"/donate/user-loc={location[0]},{location[1]}&type={type}&travel-type={transport_type}")

    return render(request, "donate.html", { "page_url": url, "is_auth": logged_in })


def donate_route(request, lat, lng, type, transport):
    logged_in = False
    url = "Route"
    
    if request.user.is_authenticated:
        logged_in = True

    user_gpt = { "longitude": float(lat), "latitude": float(lng) }
    
    geopts = []
    
    payload = {}
    headers = {}
    
    try:
        locations = Location.objects.all() # Filter to come soon for Bin and Shop
        for x in locations:
            location = str(x.geolocation).split(",")
            geopt = { "longitude": float(location[0]), "latitude": float(location[1]) }
            geopts.append(geopt)
    except Location.DoesNotExist:
        raise Http404('Database does not exist')
    
    dist_from_user = []
    
    for x in geopts:
        dist = distance_meters(x["longitude"], user_gpt["longitude"], x["latitude"], user_gpt["latitude"])
        dist_data = {
            "dist": dist,
            "geolocation": {
                "longitude": x["longitude"],
                "latitude": x["latitude"]
            }
        }
        dist_from_user.append(dist_data)

    clos_dist = min(dist_from_user["dist"] for dist_from_user in dist_from_user)
    clos_dist_geolocation = [x["geolocation"] for x in dist_from_user if x["dist"] == clos_dist]

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={user_gpt['longitude']},{user_gpt['latitude']}&destination={clos_dist_geolocation[0]['longitude']},{clos_dist_geolocation[0]['latitude']}&mode={transport}&key=AIzaSyAZ9-IagGyXsTI1nd5gvuUM3_bz3yFLm9A"
    
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    
    """ Road API snap to location back-end stuffs (Uneeded and impractical for this APP)
    payload2 = {}
    headers2 = {}
    
    poly_point_str = ""
    
    for index, x in enumerate(json_object["routes"][0]["legs"][0]["steps"]):
        if index == 0:
            poly_point_str = f"{x['start_location']['lat']},{x['start_location']['lng']}"
        else:
            poly_point_str += f"|{x['end_location']['lat']},{x['end_location']['lng']}"
            
    url = f"https://roads.googleapis.com/v1/snapToRoads?path={poly_point_str}&key=AIzaSyAZ9-IagGyXsTI1nd5gvuUM3_bz3yFLm9A"
    
    response2 = requests.request("GET", url, headers=headers2, data=payload2)
    data = json.loads(response2.text)
    """

    return render(request, "donate-route.html", { "page_url": url, "is_auth": logged_in, "map_data": json_object })

def distance_meters(db_lat, user_lat, db_long, user_long):
    x = degrees_to_radius(db_long - user_long) * math.cos(degrees_to_radius((db_lat + user_lat) / 2))
    y = degrees_to_radius(db_lat - user_lat)
    distance = 6371000 * math.sqrt(x*x + y*y)
    
    return distance

def degrees_to_radius(degrees):
    pi = math.pi
    return degrees * (pi/180)


def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"