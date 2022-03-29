let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(-33.91722, 151.23064),
        zoom: 16,
    });

    const icons = {
        store: {
            icon: "static/images/store_front_icon.png",
        },
        bin: {
            icon: "static/images/charity_bin_icon.png",
        }
    };
    const features = [{
            position: new google.maps.LatLng(-33.91721, 151.2263),
            type: "store",
        },
        {
            position: new google.maps.LatLng(-33.91539, 151.2282),
            type: "bin",
        },
    ];

    // Create markers.
    for (let i = 0; i < features.length; i++) {
        const marker = new google.maps.Marker({
            position: features[i].position,
            icon: icons[features[i].type].icon,
            map: map,
        });
    }
}