let map;

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

    const mapOptions = {
        center: new google.maps.LatLng(50.816946, -1.089735),
        zoom: 12,
        styles: mapStyles,
        mapTypeControl: false,
        disableDefaultUI: true,
        zoomControl: true,
    }

    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    const locations = [{
            position: new google.maps.LatLng(-33.91721, 151.2263),
            type: "store",
        },
        {
            position: new google.maps.LatLng(-33.91539, 151.2282),
            type: "bin",
        },
    ];

    markerHandler(locations, map)
    // Create markers.
}

const markerHandler = (markers, map) => {

    const icons = {
        store: "static/images/store_front_icon.png",
        bin: "static/images/charity_bin_icon.png"
    };

    markers.forEach((marker, index) => {
        new google.maps.Marker({
            position: marker.position,
            icon: icons[marker.type],
            map: map,
        });
    })
}