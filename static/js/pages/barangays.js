/**
 * Barangays Directory Interactions
 * Handles view toggling (grid/map), filtering, and map initialization
 */
document.addEventListener('DOMContentLoaded', function () {
    const gridViewBtn = document.getElementById('gridViewBtn');
    const mapViewBtn = document.getElementById('mapViewBtn');
    const gridView = document.getElementById('gridView');
    const mapView = document.getElementById('mapView');
    const searchInput = document.getElementById('barangaySearch');
    const categoryFilter = document.getElementById('categoryFilter');
    const barangayCards = document.querySelectorAll('.barangay-card-refined');

    // Intersection Observer for Scroll Reveals
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });

    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
    }

    let mapInitialized = false;
    let map;

    // View Toggling
    function switchView(view) {
        if (view === 'grid') {
            gridView.classList.remove('hidden');
            mapView.classList.add('hidden');
            gridViewBtn.classList.add('active');
            gridViewBtn.classList.remove('inactive');
            mapViewBtn.classList.remove('active');
            mapViewBtn.classList.add('inactive');
        } else {
            gridView.classList.add('hidden');
            mapView.classList.remove('hidden');
            mapViewBtn.classList.add('active');
            mapViewBtn.classList.remove('inactive');
            gridViewBtn.classList.remove('active');
            gridViewBtn.classList.add('inactive');

            if (!mapInitialized) {
                initMap();
                mapInitialized = true;
            } else {
                setTimeout(() => map.invalidateSize(), 100);
            }
        }
    }

    if (gridViewBtn) gridViewBtn.addEventListener('click', () => switchView('grid'));
    if (mapViewBtn) mapViewBtn.addEventListener('click', () => switchView('map'));

    // Map Initialization
    function initMap() {
        const escapeHTML = (str) => {
            if (!str) return '';
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        };

        map = L.map('barangayMap').setView([15.7888, 120.2990], 11);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        const dataStore = document.getElementById('barangays-data-store');
        if (dataStore && dataStore.dataset.barangays) {
            const barangaysData = JSON.parse(dataStore.dataset.barangays);

            barangaysData.forEach(b => {
                if (b.lat && b.lng) {
                    const marker = L.marker([b.lat, b.lng]).addTo(map);
                    const safeName = escapeHTML(b.name);
                    const safeImageUrl = b.image_url ? b.image_url.replace(/"/g, '&quot;') : null;
                    const encodedName = encodeURIComponent(b.name);

                    const popupContent = `
                        <div class="text-center">
                            <div class="h-32 overflow-hidden mb-0">
                                ${safeImageUrl ? `<img src="${safeImageUrl}" class="w-full h-full object-cover" alt="${safeName}">` : '<div class="w-full h-full bg-heritage-green/5 flex items-center justify-center">RECORD</div>'}
                            </div>
                            <div class="p-4 bg-heritage-cream">
                                <h3 class="font-bold text-lg text-heritage-green mb-1">${safeName}</h3>
                                <div class="text-[10px] uppercase tracking-widest text-heritage-gold mb-3">${parseInt(b.attraction_count) || 0} Attractions</div>
                                <a href="/barangay/${encodedName}" class="btn-heritage !py-2 !px-4 !text-[10px] !gap-2">
                                    Open Profile
                                </a>
                            </div>
                        </div>
                    `;

                    marker.bindPopup(popupContent, {
                        maxWidth: 250,
                        className: 'heritage-popup'
                    });
                }
            });
        }
    }

    // Search and Filter Logic
    function filterBarangays() {
        const searchTerm = searchInput.value.toLowerCase();
        const category = categoryFilter.value.toLowerCase();

        barangayCards.forEach(card => {
            const nameEl = card.querySelector('h3');
            const name = nameEl ? nameEl.textContent.toLowerCase() : '';
            const tagEl = card.querySelector('.barangay-tag-badge');
            const tags = tagEl ? [tagEl.textContent.trim().toLowerCase()] : [];

            const matchesSearch = name.includes(searchTerm);
            const matchesCategory = category === 'all' || tags.some(t => t.includes(category));

            if (matchesSearch && matchesCategory) {
                card.style.display = '';
                if (card.classList.contains('reveal')) {
                    card.classList.add('active');
                }
            } else {
                card.style.display = 'none';
            }
        });
    }

    if (searchInput) searchInput.addEventListener('input', filterBarangays);
    if (categoryFilter) categoryFilter.addEventListener('change', filterBarangays);
});
