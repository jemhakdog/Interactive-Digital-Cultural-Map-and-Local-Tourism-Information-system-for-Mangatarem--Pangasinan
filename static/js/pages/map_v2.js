/**
 * Mapbox GL JS Map v2 Implementation
 * Focused on premium aesthetics and clean UI
 */

document.addEventListener('DOMContentLoaded', function () {
    // ========================================
    // 1. INITIALIZATION & STATE
    // ========================================
    mapboxgl.accessToken = window.MAPBOX_TOKEN;
    
    const PLACEHOLDER_IMG = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22300%22%20height%3D%22200%22%20xmlns%3D%22http%3D%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22300%22%20height%3D%22200%22%20fill%3D%22%23eee%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20font-family%3D%22sans-serif%22%20font-size%3D%2216%22%20fill%3D%22%23aaa%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';

    let state = {
        currentCategory: 'all',
        selectedPlace: null,
        userLocation: null,
        pendingDirections: null, // To store destination if waiting for location
        isNearMeMode: false,
        allPlaces: [],
        markers: [],
        currentNavMode: 'driving',
        isNavigating: false
    };

    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v11',
        center: [120.2986, 15.7889], // Mangatarem
        zoom: 14.5,
        pitch: 60,
        bearing: -15,
        antialias: true
    });

    // ========================================
    // 2. CORE MAP EVENTS
    // ========================================
    map.on('load', () => {
        add3DBuildings(map);
        initFilters();
        initSearch();
        initNearMe();
        initModal();
        initNavigation();
        initNavPanel();
        
        // Add native Geolocate Control for real-time tracking
        map.addControl(new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            trackUserLocation: true,
            showUserHeading: true
        }), 'bottom-left');

        // Add standard navigation controls
        map.addControl(new mapboxgl.NavigationControl(), 'bottom-left');

        // Initial Fetch
        fetchData();

        // Smooth fly-in
        map.flyTo({
            center: [120.2986, 15.7889],
            zoom: 15.5,
            duration: 3000,
            essential: true
        });
    });

    // ========================================
    // 3. DATA FETCHING & RENDERING
    // ========================================
    async function fetchData() {
        const placesList = document.getElementById('places-list');
        const resultsCount = document.getElementById('results-count');
        
        // Clear UI
        clearMarkers();
        placesList.innerHTML = '<div class="text-center py-12 text-gray-400 text-sm">Searching for gems...</div>';
        resultsCount.textContent = '0 spots';

        try {
            // Fetch both attractions and establishments with correct endpoints
            const [attrRes, estRes] = await Promise.all([
                fetch('/api/attractions?per_page=100'),
                fetch('/business/api?per_page=100')
            ]);

            const attrData = await attrRes.json();
            const estData = await estRes.json();

            // Merge and process data with consistent field mapping
            state.allPlaces = [
                ...(attrData.attractions || []).map(a => ({ 
                    ...a, 
                    type: 'attraction',
                    category: a.category,
                    image: a.image_url 
                })),
                ...(estData.establishments || []).map(e => ({ 
                    ...e, 
                    type: 'establishment', 
                    category: e.type,
                    image: e.cover_image_url
                }))
            ];

            console.log('Fetched places:', state.allPlaces.length);
            applyFilters();
        } catch (error) {
            console.error('Fetch error:', error);
            placesList.innerHTML = '<div class="text-center py-12 text-red-400 text-sm">Oops! Something went wrong while loading data.</div>';
        }
    }

    function applyFilters() {
        let filtered = state.allPlaces;

        // 1. Category Filter
        if (state.currentCategory !== 'all') {
            filtered = filtered.filter(p => p.category.toLowerCase() === state.currentCategory.toLowerCase());
        }

        // 2. Search Filter
        if (state.searchTerm) {
            const term = state.searchTerm.toLowerCase();
            filtered = filtered.filter(p => 
                p.name.toLowerCase().includes(term) || 
                (p.description && p.description.toLowerCase().includes(term)) ||
                (p.barangay && p.barangay.toLowerCase().includes(term))
            );
        }

        // 3. Near Me Sort (if applicable)
        if (state.isNearMeMode && state.userLocation) {
            filtered.forEach(p => {
                p.dist = calculateDistance(
                    state.userLocation.lat, 
                    state.userLocation.lng, 
                    p.latitude || p.lat, 
                    p.longitude || p.lng
                );
            });
            filtered.sort((a, b) => a.dist - b.dist);
        }

        renderUI(filtered);
    }

    function renderUI(places) {
        const placesList = document.getElementById('places-list');
        const resultsCount = document.getElementById('results-count');
        const sectionTitle = document.getElementById('section-title');
        
        clearMarkers();
        placesList.innerHTML = '';
        resultsCount.textContent = `${places.length} spots`;
        sectionTitle.textContent = state.isNearMeMode ? 'Places Near You' : 'Recommended for You';

        if (places.length === 0) {
            placesList.innerHTML = '<div class="text-center py-12 text-gray-400 text-sm">No spots found matching your filter.</div>';
            return;
        }

        places.forEach(place => {
            // 1. Add Marker to Map
            addMarker(place);

            // 2. Add to List
            const card = document.createElement('div');
            card.className = 'place-card-v2';
            const img = place.image || place.cover_image_url || PLACEHOLDER_IMG;
            const distLabel = place.dist ? `<span class="text-[10px] text-[#008F3C] font-bold">${place.dist.toFixed(2)} km away</span>` : '';
            
            card.innerHTML = `
                <img src="${img}" class="place-img" alt="${place.name}" onerror="this.src='${PLACEHOLDER_IMG}'">
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <h3 class="text-sm font-bold text-gray-900 line-clamp-1">${place.name}</h3>
                        ${distLabel}
                    </div>
                    <p class="text-[11px] text-gray-400 font-medium mt-0.5">${place.category || 'Spot'} • ${place.barangay || 'Mangatarem'}</p>
                    <div class="flex items-center gap-1 mt-2">
                        <span class="text-yellow-400 text-xs">★</span>
                        <span class="text-[11px] font-bold text-gray-600">${(place.rating || place.rating_avg || 4.5).toFixed(1)}</span>
                    </div>
                </div>
            `;
            
            card.onclick = () => {
                flyToPlace(place);
                showModal(place);
            };
            placesList.appendChild(card);
        });
    }

    // ========================================
    // 4. UTILS & HELPERS
    // ========================================
    function addMarker(place) {
        const lat = place.latitude || place.lat;
        const lng = place.longitude || place.lng;
        
        if (!lat || !lng) return;

        const el = document.createElement('div');
        el.className = 'marker-v2';
        el.style.width = '24px';
        el.style.height = '24px';
        el.style.backgroundColor = '#00ED64';
        el.style.borderRadius = '50%';
        el.style.border = '3px solid white';
        el.style.boxShadow = '0 4px 12px rgba(0, 237, 100, 0.3)';
        el.style.cursor = 'pointer';

        const marker = new mapboxgl.Marker(el)
            .setLngLat([lng, lat])
            .addTo(map);

        el.onclick = (e) => {
            e.stopPropagation();
            showModal(place);
            flyToPlace(place);
        };

        state.markers.push(marker);
    }

    function showModal(place) {
        const overlay = document.getElementById('details-modal-overlay');
        const img = document.getElementById('modal-img');
        const title = document.getElementById('modal-title');
        const category = document.getElementById('modal-category');
        const locationText = document.getElementById('modal-location-text');
        const description = document.getElementById('modal-description');
        const viewDetails = document.getElementById('modal-view-details');
        const directionsBtn = document.getElementById('modal-directions');

        img.src = place.image || place.cover_image_url || PLACEHOLDER_IMG;
        title.textContent = place.name;
        category.textContent = place.category || 'Spot';
        locationText.textContent = `${place.barangay || 'Mangatarem'}`;
        
        // Use a default description if none exists
        description.textContent = place.description || 'Explore this beautiful spot in Mangatarem. Known for its cultural significance and natural beauty, it is a must-visit for every traveler.';
        
        viewDetails.href = place.type === 'attraction' ? `/attractions/${place.id}` : `/business/${place.id}`;
        
        if (directionsBtn) {
            directionsBtn.onclick = () => {
                console.log("🔗 [Modal] Directions clicked. User location:", state.userLocation);
                if (!state.userLocation) {
                    console.log("⏳ [Modal] Location missing. Setting pending directions for:", place.name);
                    state.pendingDirections = place;
                    
                    // Try to find the search locate button which we know exists
                    const locateBtn = document.getElementById('search-locate-btn') || document.getElementById('locate-me-btn');
                    console.log("🔍 [Modal] Searching for locate button:", locateBtn ? "Found" : "NOT Found");
                    if (locateBtn) {
                        console.log("🖱️ [Modal] Triggering click on locate button");
                        locateBtn.click();
                    }
                    Swal.fire({
                        title: 'Locating...',
                        text: 'Please wait a moment.',
                        allowOutsideClick: true,
                        showConfirmButton: false,
                        didOpen: () => {
                            Swal.showLoading()
                        }
                    });
                    return;
                }
                overlay.classList.remove('active');
                getRoute(state.userLocation, { lat: place.latitude || place.lat, lng: place.longitude || place.lng });
            };
        }

        overlay.classList.add('active');
    }

    function initModal() {
        const overlay = document.getElementById('details-modal-overlay');
        const closeBtn = document.getElementById('modal-close');
        
        if (!overlay || !closeBtn) return;

        closeBtn.onclick = () => overlay.classList.remove('active');
        overlay.onclick = (e) => {
            if (e.target === overlay) overlay.classList.remove('active');
        };

        // Close on Escape
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') overlay.classList.remove('active');
        });
    }

    function clearMarkers() {
        state.markers.forEach(m => m.remove());
        state.markers = [];
    }

    function flyToPlace(place) {
        state.selectedPlace = place;
        const lat = place.latitude || place.lat;
        const lng = place.longitude || place.lng;
        
        map.flyTo({
            center: [lng, lat],
            zoom: 17,
            pitch: 70,
            duration: 1500,
            essential: true
        });

        updateStats(place);
    }

    function updateStats(place) {
        const statsEl = document.getElementById('place-stats');
        const distEl = document.getElementById('stat-distance');
        const timeEl = document.getElementById('stat-time');
        
        if (!statsEl || !distEl || !timeEl) return;
        
        statsEl.classList.remove('hidden');

        if (state.userLocation) {
            const dist = calculateDistance(
                state.userLocation.lat, state.userLocation.lng,
                place.latitude || place.lat, place.longitude || place.lng
            );
            distEl.textContent = `${dist.toFixed(1)} KM`;
            timeEl.textContent = `${Math.round(dist * 2.5)} Min`;
        } else {
            distEl.textContent = '-- KM';
            timeEl.textContent = '-- Min';
        }
    }

    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function initNavigation() {
        const startNavBtn = document.getElementById('start-navigation');
        if (startNavBtn) {
            startNavBtn.onclick = () => {
                if (!state.userLocation) {
                    const nearMeBtn = document.getElementById('locate-me-btn');
                    if (nearMeBtn) {
                        nearMeBtn.click();
                        Swal.fire({
                            title: 'Locating...',
                            text: 'Please wait a moment.',
                            allowOutsideClick: true,
                            showConfirmButton: false,
                            didOpen: () => {
                                Swal.showLoading()
                            }
                        });
                    } else {
                        Swal.fire('Error', 'Please enable location services.', 'error');
                    }
                    return;
                }
                
                if (!state.selectedPlace) {
                    Swal.fire('Selection Required', 'Please select a place first.', 'info');
                    return;
                }
                
                // Show route on map instead of Google Maps
                getRoute(state.userLocation, { 
                    lat: state.selectedPlace.latitude || state.selectedPlace.lat, 
                    lng: state.selectedPlace.longitude || state.selectedPlace.lng 
                });
            };
        }
    }

    async function getRoute(origin, destination, mode = 'driving') {
        console.log("🛣️ [Routing] Calculating route:", { origin, destination, mode });
        
        if (!origin || !destination || isNaN(origin.lat) || isNaN(origin.lng) || isNaN(destination.lat) || isNaN(destination.lng)) {
            console.error("❌ [Routing] Invalid coordinates provided:", { origin, destination });
            throw new Error("Invalid coordinates for routing");
        }

        try {
            state.currentNavMode = mode;
            state.isNavigating = true;
            
            const profile = mode === 'driving' ? 'driving' : mode === 'walking' ? 'walking' : 'cycling';
            const url = `https://api.mapbox.com/directions/v5/mapbox/${profile}/${origin.lng},${origin.lat};${destination.lng},${destination.lat}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`;
            console.log("🌐 [Routing] Fetching from Mapbox:", url.split('access_token=')[0] + 'access_token=...');
            
            const query = await fetch(url, { method: 'GET' });
            const json = await query.json();
            if (!json.routes || json.routes.length === 0) {
                Swal.fire('Route Not Found', 'No route found for this destination.', 'warning');
                return;
            }

            const data = json.routes[0];
            const route = data.geometry.coordinates;
            console.log("🗺️ [Routing] Route data received. Points:", route.length);
            
            if (!route || route.length === 0) {
                throw new Error("Route geometry is empty");
            }
            
            // Show Panel
            const navPanel = document.getElementById('nav-panel');
            if (navPanel) {
                navPanel.classList.remove('hidden');
                document.getElementById('nav-dest-input').value = state.selectedPlace?.name || 'Destination';
                document.getElementById('route-summary').textContent = `${(data.distance / 1000).toFixed(1)} km • ${Math.round(data.duration / 60)} min`;
                
                // Populate Instructions
                const instructionsEl = document.getElementById('nav-instructions');
                if (instructionsEl) {
                    instructionsEl.innerHTML = data.legs[0].steps.map(step => {
                        let icon = '●';
                        if (step.maneuver.type.includes('turn')) {
                            icon = step.maneuver.modifier.includes('right') ? '→' : '←';
                        }
                        return `
                            <div class="instruction-step">
                                <div class="w-6 h-6 flex items-center justify-center bg-[#00ED64]/10 rounded-lg shrink-0 text-[#00ED64] text-[10px] font-bold">
                                    ${icon}
                                </div>
                                <div>
                                    <p class="text-[11px] text-gray-800 font-bold leading-tight">${step.maneuver.instruction}</p>
                                    <p class="text-[9px] text-gray-400 mt-0.5">${(step.distance / 1000).toFixed(2)} km</p>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }

            const geojson = {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: route
                }
            };

            // Remove existing route if any
            if (map.getLayer('route')) map.removeLayer('route');
            if (map.getSource('route')) map.removeSource('route');

            map.addSource('route', {
                type: 'geojson',
                data: geojson
            });

            map.addLayer({
                id: 'route',
                type: 'line',
                source: 'route',
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                paint: {
                    'line-color': '#00ED64',
                    'line-width': 6,
                    'line-opacity': 0.8
                }
            });

            // Zoom to fit the route
            const bounds = new mapboxgl.LngLatBounds();
            route.forEach(coord => bounds.extend(coord));
            map.fitBounds(bounds, {
                padding: { top: 100, bottom: 100, left: 400, right: 100 },
                duration: 2000
            });

            // Update stats in bottom sheet too
            const distEl = document.getElementById('stat-distance');
            const timeEl = document.getElementById('stat-time');
            if (distEl && timeEl) {
                distEl.textContent = `${(data.distance / 1000).toFixed(1)} KM`;
                timeEl.textContent = `${Math.round(data.duration / 60)} Min`;
            }

        } catch (error) {
            console.error('Routing error:', error);
            Swal.fire('Error', 'Could not calculate route. Please try again.', 'error');
        }
    }

    function initNavPanel() {
        const navPanel = document.getElementById('nav-panel');
        if (!navPanel) return;

        const closeBtn = document.getElementById('close-nav');
        const modeBtns = document.querySelectorAll('.nav-mode-btn');

        if (closeBtn) {
            closeBtn.onclick = () => {
                navPanel.classList.add('hidden');
                if (map.getLayer('route')) map.removeLayer('route');
                if (map.getSource('route')) map.removeSource('route');
                state.isNavigating = false;
            };
        }

        modeBtns.forEach(btn => {
            btn.onclick = () => {
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.currentNavMode = btn.dataset.mode;
                
                if (state.userLocation && state.selectedPlace) {
                    getRoute(state.userLocation, {
                        lat: state.selectedPlace.latitude || state.selectedPlace.lat,
                        lng: state.selectedPlace.longitude || state.selectedPlace.lng
                    }, state.currentNavMode);
                }
            };
        });
    }

    function calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    // ========================================
    // 5. EVENT HANDLERS
    // ========================================
    function initFilters() {
        const chips = document.querySelectorAll('.category-chip');
        chips.forEach(chip => {
            chip.onclick = () => {
                chips.forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                state.currentCategory = chip.dataset.category;
                applyFilters();
            };
        });
    }

    function initSearch() {
        const searchInput = document.getElementById('route-search');
        if (!searchInput) return;

        searchInput.oninput = (e) => {
            state.searchTerm = e.target.value;
            applyFilters();
        };

        // Expand sheet when searching
        searchInput.onfocus = () => {
            if (window.sheetManager) window.sheetManager.snapTo('full');
        };
    }

    function initNearMe() {
        const locateMeBtn = document.getElementById('locate-me-btn');
        const searchLocateBtn = document.getElementById('search-locate-btn');
        
        const handleLocation = () => {
            console.log("🚀 [NearMe] handleLocation triggered");
            if (!navigator.geolocation) {
                Swal.fire('Not Supported', 'Geolocation is not supported by your browser.', 'error');
                return;
            }

            console.log("📍 [Geolocation] Requesting current position...");
            const btns = [locateMeBtn, searchLocateBtn].filter(Boolean);
            btns.forEach(btn => btn.classList.add('animate-pulse'));
            
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    console.log("✅ [Geolocation] Position found:", pos.coords.latitude, pos.coords.longitude);
                    Swal.close();
                    const coords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
                    state.userLocation = coords;
                    state.isNearMeMode = true;
                    
                    btns.forEach(btn => {
                        btn.classList.remove('animate-pulse');
                        btn.style.color = '#00ED64';
                        if (btn.id === 'locate-me-btn') {
                            btn.style.backgroundColor = '#1F1D2B';
                        }
                    });
                    
                    // Handle pending directions from modal
                    if (state.pendingDirections) {
                        const dest = state.pendingDirections;
                        console.log("🎯 [Geolocation] Auto-triggering route for:", dest.name);
                        
                        // Close modal and start route
                        const overlay = document.getElementById('details-modal-overlay');
                        if (overlay) overlay.classList.remove('active');
                        
                        getRoute(state.userLocation, { 
                            lat: dest.latitude || dest.lat, 
                            lng: dest.longitude || dest.lng 
                        });
                        
                        state.pendingDirections = null;
                    }
                    
                    // Update or create user marker
                    if (window.userMarker) {
                        window.userMarker.setLngLat([coords.lng, coords.lat]);
                    } else {
                        const userEl = document.createElement('div');
                        userEl.className = 'user-marker';
                        userEl.innerHTML = `
                            <div class="relative flex items-center justify-center">
                                <div class="absolute w-8 h-8 bg-[#00ED64]/30 rounded-full animate-ping"></div>
                                <div class="relative w-5 h-5 bg-[#00ED64] rounded-full border-2 border-white shadow-lg flex items-center justify-center">
                                    <div class="w-2 h-2 bg-white rounded-full"></div>
                                </div>
                            </div>
                        `;
                        window.userMarker = new mapboxgl.Marker(userEl)
                            .setLngLat([coords.lng, coords.lat])
                            .addTo(map);
                    }

                    applyFilters();
                    
                    map.flyTo({
                        center: [coords.lng, coords.lat],
                        zoom: 15,
                        pitch: 45,
                        duration: 2000
                    });

                    // Start watching position for "navigation" feel
                    if (!window.positionWatcher) {
                        window.positionWatcher = navigator.geolocation.watchPosition(
                            (p) => {
                                console.log("🔄 [Geolocation] Position updated:", p.coords.latitude, p.coords.longitude);
                                state.userLocation = { lat: p.coords.latitude, lng: p.coords.longitude };
                                if (window.userMarker) {
                                    window.userMarker.setLngLat([p.coords.longitude, p.coords.latitude]);
                                }
                                // Update stats if a place is selected
                                if (state.selectedPlace) {
                                    updateStats(state.selectedPlace);
                                }
                            },
                            (err) => console.error('Watch error:', err),
                            { enableHighAccuracy: true }
                        );
                    }
                },
                (err) => {
                    console.error("❌ [Geolocation] Error:", err.code, err.message);
                    let errorMsg = 'Could not get your location.';
                    if (err.code === 1) errorMsg = 'Permission denied. Please allow location access.';
                    if (err.code === 2) errorMsg = 'Position unavailable. Check your GPS/network.';
                    if (err.code === 3) errorMsg = 'Location request timed out. Please try again.';

                    btns.forEach(btn => btn.classList.remove('animate-pulse'));
                    Swal.fire('Location Error', errorMsg, 'error');
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
            );
        };

        if (locateMeBtn) locateMeBtn.onclick = handleLocation;
        if (searchLocateBtn) searchLocateBtn.onclick = handleLocation;
        
        // Also bind to any element with .locate-trigger class
        document.querySelectorAll('.locate-trigger').forEach(el => {
            el.onclick = handleLocation;
        });
    }

    // ========================================
    // 6. BOTTOM SHEET & INTERACTION
    // ========================================
    
    /**
     * SheetManager handles the bottom sheet's drag and snapping behavior
     * It also prevents map interference more aggressively
     */
    class SheetManager {
        constructor(sheet, handle, map) {
            this.sheet = sheet;
            this.handle = handle;
            this.map = map;
            
            this.isDragging = false;
            this.startY = 0;
            this.startTranslateY = 0;
            this.currentTranslateY = 0;
            
            this.init();
        }

        init() {
            // 1. Map Interference Prevention
            const uiSelectors = ['.floating-header', '.floating-filters', '.mapboxgl-ctrl-group'];
            const mapCanvas = this.map.getCanvasContainer();
            
            // For static UI elements (filters, header), we can use a simple locker
            const lockMap = (e) => {
                // Don't stop propagation if we're clicking a button, link, or filter chip
                if (e.target.closest('button') || e.target.closest('a') || e.target.closest('.category-chip')) {
                    return;
                }
                
                e.stopPropagation();
                this.disableMapInteractions();
            };

            uiSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    ['mousedown', 'touchstart', 'pointerdown'].forEach(type => {
                        el.addEventListener(type, lockMap, { capture: true, passive: true });
                    });
                    ['mouseup', 'touchend', 'pointerup', 'mouseleave'].forEach(type => {
                        el.addEventListener(type, () => this.enableMapInteractions(), { capture: true, passive: true });
                    });
                });
            });

            // 2. Bottom Sheet Specific Logic
            // We DON'T use stopPropagation in capture phase for the sheet, 
            // so our own listeners below can catch the events.
            this.sheet.addEventListener('touchstart', (e) => {
                // If touching the sheet, always disable map
                this.disableMapInteractions();
                mapCanvas.style.pointerEvents = 'none';
            }, { passive: true });

            this.handle.addEventListener('touchstart', (e) => {
                e.stopPropagation(); // Stop from reaching map, but NOT capture phase
                this.onDragStart(e);
            }, { passive: false });
            
            const resultsSection = document.getElementById('results-section');
            resultsSection.addEventListener('touchstart', (e) => {
                if (resultsSection.scrollTop <= 0) {
                    this.onDragStart(e);
                }
            }, { passive: false });

            window.addEventListener('touchmove', (e) => this.onDragMove(e), { passive: false });
            window.addEventListener('touchend', (e) => this.onDragEnd(e));

            // Default state initialization
            this.snapTo('peek');
        }

        disableMapInteractions() {
            if (!this.map) return;
            const handlers = ['dragPan', 'scrollZoom', 'boxZoom', 'keyboard', 'doubleClickZoom', 'touchZoomRotate', 'touchPitch'];
            handlers.forEach(h => {
                if (this.map[h]) this.map[h].disable();
            });
        }

        enableMapInteractions() {
            if (!this.map || this.isDragging) return;
            const handlers = ['dragPan', 'scrollZoom', 'boxZoom', 'keyboard', 'doubleClickZoom', 'touchZoomRotate', 'touchPitch'];
            handlers.forEach(h => {
                if (this.map[h]) this.map[h].enable();
            });
        }

        onDragStart(e) {
            this.isDragging = true;
            this.hasMoved = false;
            this.startY = e.touches[0].clientY;
            
            this.disableMapInteractions();
            this.map.getCanvasContainer().style.pointerEvents = 'none';
            
            e.stopPropagation();

            const style = window.getComputedStyle(this.sheet);
            const transform = style.transform;
            
            if (transform && transform !== 'none') {
                const matrix = new DOMMatrixReadOnly(transform);
                this.startTranslateY = matrix.m42 || matrix.f || 0;
            } else {
                this.startTranslateY = 0;
            }
            
            this.sheet.style.transition = 'none'; 
        }

        onDragMove(e) {
            if (!this.isDragging) return;
            
            const currentY = e.touches[0].clientY;
            const deltaY = currentY - this.startY;
            
            if (Math.abs(deltaY) > 5) this.hasMoved = true;
            
            let newTranslateY = this.startTranslateY + deltaY;
            const peekY = window.innerHeight - 100; // Match 100px peek
            const fullY = 0;
            
            // Resistance
            if (newTranslateY < fullY) newTranslateY = newTranslateY * 0.2; 
            if (newTranslateY > peekY) newTranslateY = peekY + (newTranslateY - peekY) * 0.2;

            this.currentTranslateY = newTranslateY;
            this.sheet.style.transform = `translateY(${newTranslateY}px)`;
            
            if (e.cancelable) {
                e.preventDefault();
                e.stopPropagation();
            }
        }

        onDragEnd(e) {
            if (!this.isDragging) return;
            this.isDragging = false;
            
            // Re-enable map
            this.map.getCanvasContainer().style.pointerEvents = 'auto';
            this.enableMapInteractions();

            this.sheet.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
            
            // If it was a quick tap/click without much movement
            if (!this.hasMoved) {
                if (this.sheet.classList.contains('is-peek')) {
                    this.snapTo('mid');
                } else {
                    this.snapTo('peek');
                }
            } else {
                const peekY = window.innerHeight - 100;
                const midY = window.innerHeight * 0.5;
                
                if (this.currentTranslateY > midY + (peekY - midY) / 2) {
                    this.snapTo('peek');
                } else if (this.currentTranslateY < midY / 2) {
                    this.snapTo('full');
                } else {
                    this.snapTo('mid');
                }
            }
        }

        snapTo(state) {
            this.sheet.classList.remove('is-peek', 'is-mid', 'is-full');
            this.sheet.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
            
            if (state === 'peek') {
                this.sheet.classList.add('is-peek');
                this.sheet.style.transform = `translateY(calc(100% - 100px))`;
            } else if (state === 'full') {
                this.sheet.classList.add('is-full');
                this.sheet.style.transform = 'translateY(0)';
            } else if (state === 'mid') {
                this.sheet.classList.add('is-mid');
                const midY = window.innerHeight * 0.5;
                this.sheet.style.transform = `translateY(${midY}px)`;
            }
        }
    }

    // Initialize Sheet Manager
    const sheet = document.getElementById('bottom-sheet');
    const handle = document.getElementById('sheet-handle');
    if (sheet && handle) {
        window.sheetManager = new SheetManager(sheet, handle, map);
    }

    /**
     * Adds 3D buildings with a clean white/gray look
     */
    function add3DBuildings(map) {
        const layers = map.getStyle().layers;
        const labelLayerId = layers.find(
            (layer) => layer.type === 'symbol' && layer.layout['text-field']
        ).id;

        map.addLayer(
            {
                'id': '3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 15,
                'paint': {
                    'fill-extrusion-color': '#ffffff', 
                    'fill-extrusion-height': ['get', 'height'],
                    'fill-extrusion-base': ['get', 'min_height'],
                    'fill-extrusion-opacity': 0.8
                }
            },
            labelLayerId
        );
    }
});
