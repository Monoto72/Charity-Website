let element = document.querySelector('#map');
let map;

initMap = () => {
    map = new google.maps.Map(element, {
        center: { 
            lat: 50.808, 
            lng: -1.072 
        },
        zoom: 10,
    });
}