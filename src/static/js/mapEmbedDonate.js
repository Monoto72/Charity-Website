function initAutocomplete() {
    const inputField = document.querySelector('#suggestion-address');
    const geolocationField = document.querySelectorAll('#suggestion-geolocation');
  
    const autocomplete = new google.maps.places.Autocomplete(inputField);
    autocomplete.setFields(
      ['address_components', 'geometry', 'name']);
  
    autocomplete.addListener('place_changed', () => {
      let place = autocomplete.getPlace();
      if (!place.geometry) {
        return console.log("Returned place contains no geometry");
      }

      let locationClean = String(place.geometry.location).split(",")
      geolocationField.forEach(element => {
        element.value = `${locationClean[0].slice(1)},${locationClean[1].slice(1, -1)}`
      })
    });
  }
  document.addEventListener("DOMContentLoaded", (event) => {
    initAutocomplete();
  });