// Heritage detail mini-map initialization
(function() {
    'use strict';

    function initHeritageMap() {
        const mapContainer = document.getElementById('heritage-mini-map');
        if (!mapContainer || typeof L === 'undefined') return;

        const lat = parseFloat(mapContainer.dataset.lat);
        const lng = parseFloat(mapContainer.dataset.lng);

        if (isNaN(lat) || isNaN(lng)) return;

        const map = L.map('heritage-mini-map', {
            center: [lat, lng],
            zoom: 15,
            zoomControl: false,
            attributionControl: false
        });

        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

        const icon = L.divIcon({
            className: 'custom-div-icon',
            html: "<div style='background-color:#10b981; width:12px; height:12px; border-radius:50%; border:2px solid white; box-shadow:0 0 10px rgba(0,0,0,0.3)'></div>",
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });

        L.marker([lat, lng], { icon: icon }).addTo(map);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeritageMap);
    } else {
        initHeritageMap();
    }
})();
