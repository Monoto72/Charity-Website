let map;
let toggle = false;

const mapData = JSON.parse(document.getElementById(`mapData`).textContent);

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

    mapData.forEach(marker => {

        infoContent =
            `<div id="content">
                <div id="siteNotice">
                </div>
                <h1 class="text-xl text-center"><b>${marker.name}</b></h1>
                <div id="bodyContent">
                    <p class="text-center">${marker.address}<p>
                </div>
            </div>`;

        const infoWindow = new google.maps.InfoWindow({
            content: infoContent
        });

        const blip = new google.maps.Marker({
            position: new google.maps.LatLng(marker.geolocation.longitude, marker.geolocation.latitude),
            label: marker.type == 1 ? 'S' : 'B',
            title: marker.name,
            map: map,
        });

        blip.addListener("click", () => {
            if (!toggle) {
                infoWindow.open({
                    anchor: blip,
                    map,
                    shouldFocus: false
                })
                toggle = !toggle
            } else {
                infoWindow.close()
                toggle = !toggle
            }
        });
    })

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const latLng = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };

            map.setCenter(latLng);
        });
    }
}