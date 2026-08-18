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

        const dataScript = document.getElementById('assets-data');
        if (dataScript) {
            try {
                const assets = JSON.parse(dataScript.textContent);
                const markers = [];

                assets.forEach(a => {
                    if (!a.latitude || !a.longitude) return;

                    // Choose icon based on type
                    const iconColor = a.type === 'event' ? '#F59E0B' : '#059669'; // Orange for events, Emerald for attractions
                    const iconEmoji = a.type === 'event' ? '📅' : '🏰';
                    
                    // Escape HTML to prevent XSS
                    const escapeHTML = (str) => {
                        if (!str) return '';
                        return str.replace(/[&<>"']/g, (m) => ({
                            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
                        }[m]));
                    };

                    const safeName = escapeHTML(a.name);
                    const safeCategory = escapeHTML(a.category);
                    
                    const marker = L.marker([a.latitude, a.longitude]).addTo(map);
                    
                    const dateInfo = a.type === 'event' ? `<p class="text-[10px] text-gray-500 font-bold uppercase mt-1">Happening: ${escapeHTML(a.date)}</p>` : '';

                    marker.bindPopup(`
                        <div class="p-2 min-w-[150px]">
                            <div style="width: 100%; height: 96px; overflow: hidden; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                                <img src="${a.image_url || 'https://placehold.co/200x120'}" style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                            <div class="flex items-center gap-1.5 mb-1">
                                <span class="text-sm">${iconEmoji}</span>
                                <h3 class="font-bold text-gray-800 leading-tight">${safeName}</h3>
                            </div>
                            <p class="text-[10px] text-green-600 font-semibold mb-1 uppercase tracking-wider">${safeCategory}</p>
                            ${dateInfo}
                            <div class="mt-2 pt-2 border-t border-gray-100">
                                <a href="${a.url}" class="text-xs text-blue-600 hover:underline font-bold">Details →</a>
                            </div>
                        </div>
                    `, {
                        maxWidth: 250,
                        className: 'custom-popup'
                    });
                    markers.push(marker);
                });

                if (markers.length > 0) {
                    const group = new L.featureGroup(markers);
                    map.fitBounds(group.getBounds().pad(0.2)); // Pad 20% for better framing
                }
            } catch (e) {
                console.error("Error parsing map assets data", e);
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
