const mapData = JSON.parse(document.getElementById(`mapEmbedDonate`).textContent);

let map;
let toggle = false;

let marker;

function initMap() {
    const mapStyles = [{
            "featureType": "administrative",
            "elementType": "geometry",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "poi",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "road",
            "elementType": "labels.icon",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "road.arterial",
            "elementType": "labels",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "road.local",
            "stylers": [{
                "visibility": "off"
            }]
        },
        {
            "featureType": "transit",
            "stylers": [{
                "visibility": "off"
            }]
        }
    ];

    const locationBounds = {
        north: mapData.routes[0].bounds.northeast.lat,
        east: mapData.routes[0].bounds.northeast.lng,
        south: mapData.routes[0].bounds.southwest.lat,
        west: mapData.routes[0].bounds.southwest.lng
    }

    const routeCoordinates = mapData.routes[0].legs[0].steps.map((step, index) => {
        let polyPoint;
        if (index === 0) {
            polyPoint = { lat: step.start_location.lat, lng: step.start_location.lng }
            return polyPoint
        }
        polyPoint = { lat: step.end_location.lat, lng: step.end_location.lng }
        return polyPoint
    })

    const routePath = new google.maps.Polyline({
        path: routeCoordinates,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    })

    const mapOptions = {
        center: new google.maps.LatLng(50.816946, -1.089735),
        zoom: 12,
        styles: mapStyles,
        mapTypeControl: false,
        disableDefaultUI: true,
        zoomControl: true,
        restriction: {
            latLngBounds: locationBounds,
            strictBounds: false
        }
    }

    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    routePath.setMap(map);
    [routeCoordinates[0], routeCoordinates[routeCoordinates.length-1]].map((location) => {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(location.lat, location.lng),
            map: map,
        });
        return marker
    })
}