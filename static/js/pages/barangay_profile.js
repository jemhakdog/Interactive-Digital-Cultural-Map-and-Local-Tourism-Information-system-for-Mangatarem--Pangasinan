/**
 * Barangay Profile Interactions
 * Handles map initialization and scroll reveal animations
 */
document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('barangay-map');
    if (mapElement && typeof L !== 'undefined') {
        const centerLat = parseFloat(mapElement.dataset.lat) || 15.7888;
        const centerLng = parseFloat(mapElement.dataset.lng) || 120.2990;

        const map = L.map('barangay-map').setView([centerLat, centerLng], 14);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        const dataScript = document.getElementById('attractions-data');
        if (dataScript) {
            try {
                const attractions = JSON.parse(dataScript.textContent);
                const markers = [];

                attractions.forEach(a => {
                    const marker = L.marker([a.lat, a.lng]).addTo(map);
                    marker.bindPopup(`
                        <div class="p-2">
                            <div style="width: 100%; height: 96px; overflow: hidden; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                                <img src="${a.image_url || 'https://placehold.co/200x120'}" style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                            <h3 class="font-bold text-gray-800">${a.name}</h3>
                            <p class="text-xs text-green-600 mb-1 font-semibold">${a.category}</p>
                            <a href="/attraction/${a.id}" class="text-xs text-blue-600 hover:underline">View Destination</a>
                        </div>
                    `, {
                        maxWidth: 250,
                        className: 'custom-popup'
                    });
                    markers.push(marker);
                });

                if (markers.length > 0) {
                    const group = new L.featureGroup(markers);
                    map.fitBounds(group.getBounds().pad(0.1));
                }
            } catch (e) {
                console.error("Error parsing attractions data", e);
            }
        }
    }

    // Reveal animation on scroll
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(el => observer.observe(el));
    }
});
