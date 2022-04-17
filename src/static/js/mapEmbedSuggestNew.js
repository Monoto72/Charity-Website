function initAutocomplete() {
    const inputField = document.querySelector('#suggestion-address');
    const nameField = document.querySelector('#suggestion-name');
    const geolocationField = document.querySelector('#suggestion-geolocation');

    let map = new google.maps.Map(document.getElementById('map'), {
      center: {
        lat: 50.816946,
        lng: -1.089735
      },
      zoom: 10,
      disableDefaultUI: true
    });
  
    const autocomplete = new google.maps.places.Autocomplete(inputField);
    let blip = new google.maps.Marker({
      map: map
    });
  
    autocomplete.bindTo('bounds', map);
    autocomplete.setFields(
      ['address_components', 'geometry', 'name']);
  
    autocomplete.addListener('place_changed', () => {
      let place = autocomplete.getPlace();
      if (!place.geometry) {
        return console.log("Returned place contains no geometry");
      }
      let bounds = new google.maps.LatLngBounds();
      blip.setPosition(place.geometry.location);

      nameField.value = place.name;
      let locationClean = String(place.geometry.location).split(",")
      geolocationField.value = `${locationClean[0].slice(1)},${locationClean[1].slice(1, -1)}`;
  
      if (place.geometry.viewport) {
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
      map.fitBounds(bounds);
    });
  }
  document.addEventListener("DOMContentLoaded", (event) => {
    initAutocomplete();
  });