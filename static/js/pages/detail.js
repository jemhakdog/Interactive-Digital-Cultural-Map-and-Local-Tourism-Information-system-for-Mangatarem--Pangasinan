/**
 * Detail Page Map Initialization
 * Handles the mini map display for specific locations
 */
document.addEventListener('DOMContentLoaded', function () {
    const mapElement = document.getElementById('mini-map');
    if (!mapElement) return;

    const lat = parseFloat(mapElement.dataset.lat);
    const lng = parseFloat(mapElement.dataset.lng);

    if (isNaN(lat) || isNaN(lng)) return;

    const map = L.map('mini-map', {
        center: [lat, lng],
        zoom: 15,
        zoomControl: false,
        dragging: !L.Browser.mobile,
        touchZoom: L.Browser.mobile,
        scrollWheelZoom: false
    });

    // Add Premium Dark/Emerald Tile Layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Custom Marker
    const customIcon = L.divIcon({
        className: 'custom-div-icon',
        html: `<div class="w-8 h-8 bg-emerald-500 rounded-full border-4 border-white shadow-xl flex items-center justify-center">
                    <div class="w-2 h-2 bg-white rounded-full animate-ping"></div>
                   </div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    L.marker([lat, lng], { icon: customIcon }).addTo(map);

    // Add subtle interaction
    map.on('click', function () {
        window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank');
    });
});
