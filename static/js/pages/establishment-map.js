// Establishment detail map initialization
(function() {
    'use strict';

    function initEstablishmentMap() {
        const mapContainer = document.getElementById('establishment-map');
        if (!mapContainer || typeof mapboxgl === 'undefined') return;

        const longitude = parseFloat(mapContainer.dataset.lng);
        const latitude = parseFloat(mapContainer.dataset.lat);
        const accessToken = mapContainer.dataset.accessToken;

        if (mapContainer && longitude && latitude && !isNaN(longitude) && !isNaN(latitude)) {
            mapboxgl.accessToken = accessToken || '';
            
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
