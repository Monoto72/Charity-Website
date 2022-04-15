const mapData = JSON.parse(document.getElementById(`mapEmbedSuggest`).textContent);
const charityNodeList = document.querySelector('#charity-suggestions').querySelectorAll('.suggestion');
let map;
let blip;

let modalData = {}

charityNodeList.forEach(element => {
    element.addEventListener('click', (event) => {
        modalData = mapData[event.path[0].id-1];
        map.setCenter({
            lat: modalData.geolocation.longitude,
            lng: modalData.geolocation.latitude
        })

        if (blip) blip.setMap(null);
        blip = new google.maps.Marker({
            position: new google.maps.LatLng(modalData.geolocation.longitude, modalData.geolocation.latitude),
            title: modalData.name,
            map: map,
        });
    });
})

function initMap(long = 50.816946, lat = -1.089735) {

    const mapOptions = {
        center: new google.maps.LatLng(long, lat),
        zoom: 12,
        mapTypeControl: true,
        disableDefaultUI: true,
        zoomControl: true,
    }

    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}