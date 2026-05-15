// Establishment detail map initialization
(function() {
    'use strict';

    function initEstablishmentMap() {
        const mapContainer = document.getElementById('establishment-map');
        if (!mapContainer || typeof mapboxgl === 'undefined') return;

        const longitude = parseFloat(mapContainer.dataset.lng);
        const latitude = parseFloat(mapContainer.dataset.lat);
        const accessToken = mapContainer.dataset.accessToken;
        const hasToken = accessToken && accessToken !== 'None' && accessToken !== '';

        if (mapContainer && longitude && latitude && !isNaN(longitude) && !isNaN(latitude)) {
            if (hasToken && typeof mapboxgl !== 'undefined') {
                mapboxgl.accessToken = accessToken;
                
                const map = new mapboxgl.Map({
                    container: 'establishment-map',
                    style: 'mapbox://styles/mapbox/dark-v11',
                    center: [longitude, latitude],
                    zoom: 15,
                    interactive: false
                });

                new mapboxgl.Marker({ color: '#10b981' })
                    .setLngLat([longitude, latitude])
                    .addTo(map);
            } else if (typeof L !== 'undefined') {
                // Leaflet Fallback
                console.warn("⚠️ Mapbox token missing or library unavailable. Using Leaflet fallback for establishment map.");
                const map = L.map('establishment-map', {
                    zoomControl: false,
                    interactive: false
                }).setView([latitude, longitude], 15);

                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; CARTO'
                }).addTo(map);

                const icon = L.divIcon({
                    className: 'custom-div-icon',
                    html: "<div style='background-color:#10b981; width:12px; height:12px; border-radius:50%; border:2px solid white; box-shadow:0 0 10px rgba(0,0,0,0.3)'></div>",
                    iconSize: [12, 12],
                    iconAnchor: [6, 6]
                });

                L.marker([latitude, longitude], { icon: icon }).addTo(map);
            }
        } else if (mapContainer) {
            // Hide map container if no valid coordinates
            const parent = mapContainer.parentElement;
            if (parent) parent.style.display = 'none';
            console.warn('Invalid coordinates for establishment map:', { longitude, latitude });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEstablishmentMap);
    } else {
        initEstablishmentMap();
    }
})();
