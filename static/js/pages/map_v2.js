/**
 * Mapbox GL JS Map v2 Implementation
 * Focused on premium aesthetics and clean UI
 */

document.addEventListener('DOMContentLoaded', function () {
    // ========================================
    // 1. INITIALIZATION & STATE
    // ========================================
    const hasMapboxToken = window.MAPBOX_TOKEN && window.MAPBOX_TOKEN !== 'None' && window.MAPBOX_TOKEN !== '';
    
    const PLACEHOLDER_IMG = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22300%22%20height%3D%22200%22%20xmlns%3D%22http%3D%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22300%22%20height%3D%22200%22%20fill%3D%22%23eee%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20font-family%3D%22sans-serif%22%20font-size%3D%2216%22%20fill%3D%22%23aaa%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';

    let state = {
        mapService: localStorage.getItem('gomangatarem_map_service') || (hasMapboxToken ? 'mapbox' : 'leaflet'),
        mapStyle: localStorage.getItem('gomangatarem_map_style') || 'light',
        currentCategory: 'all',
        selectedPlace: null,
        userLocation: null,
        pendingDirections: null, 
        isNearMeMode: false,
        allPlaces: [],
        markers: [],
        currentNavMode: 'driving',
        isNavigating: false,
        bookmarkedIds: {
            attractions: [],
            establishments: []
        },
        currentRouteLayer: null, // Track Leaflet route layer
        selectedCoords: null // Track currently selected alternative/primary coordinates
    };

    const MAP_STYLES = {
        mapbox: {
            light: 'mapbox://styles/mapbox/light-v11',
            dark: 'mapbox://styles/mapbox/dark-v11',
            streets: 'mapbox://styles/mapbox/streets-v12',
            satellite: 'mapbox://styles/mapbox/satellite-streets-v12'
        },
        leaflet: {
            light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            dark: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            streets: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
            satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        }
    };

    // ========================================
    // 2. CORE MAP EVENTS
    // ========================================
    const onMapLoad = () => {
        console.log("🗺️ Map Engine Ready:", isLeafletMode ? "Leaflet" : "Mapbox");
        
        if (!isLeafletMode) {
            add3DBuildings(map);
        }
        initFilters();
        initSearch();
        initNearMe();
        initModal();
        initNavigation();
        initNavPanel();
        initMapServiceSwitcher();
        
        // Fetch bookmarks if logged in
        if (window.USER_AUTH) {
            fetchBookmarks();
        }
        
        if (!isLeafletMode) {
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
        }

        // Re-initialize SheetManager if service switched
        if (window.sheetManager) {
            window.sheetManager.map = map;
        }

        // Initial Fetch
        fetchData();

        // Smooth fly-in
        flyToCoords([120.2986, 15.7889], 15.5);
    };

    let map;
    let isLeafletMode = state.mapService === 'leaflet';

    function initMapInstance() {
        // Clear previous map if exists
        if (map) {
            if (isLeafletMode) {
                map.remove();
            } else {
                map.remove();
            }
            const mapContainer = document.getElementById('map');
            mapContainer.innerHTML = '';
        }

        isLeafletMode = state.mapService === 'leaflet';

        if (!isLeafletMode && hasMapboxToken) {
            mapboxgl.accessToken = window.MAPBOX_TOKEN;
            map = new mapboxgl.Map({
                container: 'map',
                style: MAP_STYLES.mapbox[state.mapStyle] || MAP_STYLES.mapbox.light,
                center: [120.2986, 15.7889], // Mangatarem
                zoom: 14.5,
                pitch: 60,
                bearing: -15,
                antialias: true
            });
            map.on('load', onMapLoad);
        } else {
            if (!hasMapboxToken && state.mapService === 'mapbox') {
                console.warn("⚠️ Mapbox token missing but requested. Forcing Leaflet.");
                state.mapService = 'leaflet';
                isLeafletMode = true;
            }

            // Initialize Leaflet with safety check
            if (typeof L === 'undefined') {
                console.error("❌ Leaflet library (L) is not loaded. Check CSP or network.");
                const mapContainer = document.getElementById('map');
                if (mapContainer) {
                    mapContainer.innerHTML = `
                        <div class="flex flex-col items-center justify-center h-full p-8 text-center bg-gray-50">
                            <div class="w-16 h-16 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center mb-4">
                                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                                </svg>
                            </div>
                            <h3 class="text-lg font-bold text-gray-900 mb-2">Map Engine Blocked</h3>
                            <p class="text-sm text-gray-500 mb-6">Your browser blocked the map library. This is usually due to a cached security policy.</p>
                            <button onclick="location.reload(true)" class="px-6 py-2 bg-[#00ED64] text-gray-900 font-bold rounded-xl shadow-lg">Force Refresh</button>
                        </div>
                    `;
                }
                return;
            }

            map = L.map('map', {
                zoomControl: false 
            }).setView([15.7889, 120.2986], 15);
            
            const tileUrl = MAP_STYLES.leaflet[state.mapStyle] || MAP_STYLES.leaflet.light;
            window.baseLayer = L.tileLayer(tileUrl, {
                attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
            }).addTo(map);
            
            L.control.zoom({ position: 'bottomleft' }).addTo(map);
            
            onMapLoad(); 
        }
    }

    // Initial Map Load
    initMapInstance();

    // ========================================
    // 3. DATA FETCHING & RENDERING
    // ========================================
    function handleUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const selectPlaceId = urlParams.get('select_place');
        const routeToId = urlParams.get('route_to');

        console.log("🔗 [URL Params] select_place:", selectPlaceId, "route_to:", routeToId);

        if (selectPlaceId || routeToId) {
            const targetId = parseInt(selectPlaceId || routeToId);
            if (!isNaN(targetId)) {
                let place = state.allPlaces.find(p => p.id === targetId && p.type === 'attraction');
                if (!place) {
                    place = state.allPlaces.find(p => p.id === targetId);
                }

                if (place) {
                    console.log("🎯 [URL Params] Found target place:", place.name);
                    
                    setTimeout(() => {
                        flyToPlace(place);
                        showModal(place);
                        
                        if (routeToId) {
                            console.log("🛣️ [URL Params] Auto-triggering routing for:", place.name);
                            if (!state.userLocation) {
                                console.log("⏳ [URL Params] User location missing. Setting pending directions.");
                                state.pendingDirections = place;
                                
                                const locateBtn = document.getElementById('search-locate-btn') || document.getElementById('locate-me-btn');
                                if (locateBtn) {
                                    console.log("🖱️ [URL Params] Triggering location fetch via button click");
                                    locateBtn.click();
                                }
                            } else {
                                getRoute(state.userLocation, {
                                    lat: place.latitude || place.lat,
                                    lng: place.longitude || place.lng
                                });
                            }
                        }
                    }, 800);
                } else {
                    console.warn("⚠️ [URL Params] Place not found with ID:", targetId);
                }
            }
        }
    }

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
            
            // Handle URL Parameters (select_place or route_to)
            handleUrlParams();
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
            
            const isBookmarked = (place.type === 'attraction' && state.bookmarkedIds.attractions.includes(place.id)) ||
                                 (place.type === 'establishment' && state.bookmarkedIds.establishments.includes(place.id));
            
            card.innerHTML = `
                <img src="${img}" class="place-img" alt="${place.name}" onerror="this.src='${PLACEHOLDER_IMG}'">
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <h3 class="text-sm font-bold text-gray-900 line-clamp-1 pr-8">${place.name}</h3>
                        ${distLabel}
                    </div>
                    <p class="text-[11px] text-gray-400 font-medium mt-0.5">${place.category || 'Spot'} • ${place.barangay || 'Mangatarem'}</p>
                    <div class="flex items-center gap-1 mt-2">
                        <span class="text-yellow-400 text-xs">★</span>
                        <span class="text-[11px] font-bold text-gray-600">${(place.rating || place.rating_avg || 4.5).toFixed(1)}</span>
                    </div>
                </div>
                <button class="card-bookmark-btn ${isBookmarked ? 'active' : ''}" data-id="${place.id}" data-type="${place.type}">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                </button>
            `;
            
            const bookmarkBtn = card.querySelector('.card-bookmark-btn');
            bookmarkBtn.onclick = (e) => {
                e.stopPropagation();
                handleToggleBookmark(place.id, place.type, bookmarkBtn);
            };
            
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

        el.onclick = (e) => {
            if (e.stopPropagation) e.stopPropagation();
            showModal(place);
            flyToPlace(place);
        };

        if (!isLeafletMode) {
            const marker = new mapboxgl.Marker(el)
                .setLngLat([lng, lat])
                .addTo(map);
            state.markers.push(marker);
        } else {
            const marker = L.marker([lat, lng], {
                icon: L.divIcon({
                    className: '',
                    html: el.outerHTML,
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                })
            }).addTo(map);
            
            // Re-bind click since Leaflet divIcon might clone the element
            marker.on('click', (e) => {
                showModal(place);
                flyToPlace(place);
            });
            
            state.markers.push(marker);
        }
    }

    function showModal(place) {
        console.log("ℹ️ [Modal] Opening modal for:", place.name, place);
        const overlay = document.getElementById('details-modal-overlay');
        const img = document.getElementById('modal-img');
        const title = document.getElementById('modal-title');
        const category = document.getElementById('modal-category');
        const locationText = document.getElementById('modal-location-text');
        const description = document.getElementById('modal-description');
        const viewDetails = document.getElementById('modal-view-details');
        const directionsBtn = document.getElementById('modal-directions');
        const bookmarkBtn = document.getElementById('modal-bookmark');
        const alternativesContainer = document.getElementById('modal-alternatives-container');
        const alternativesSelect = document.getElementById('modal-alternatives-select');

        console.log("ℹ️ [Modal] alternativesContainer:", alternativesContainer, "alternativesSelect:", alternativesSelect);
        console.log("ℹ️ [Modal] place.osm_alternatives:", place.osm_alternatives);

        const isBookmarked = (place.type === 'attraction' && state.bookmarkedIds.attractions.includes(place.id)) ||
                             (place.type === 'establishment' && state.bookmarkedIds.establishments.includes(place.id));
        
        if (bookmarkBtn) {
            bookmarkBtn.classList.toggle('active', isBookmarked);
            bookmarkBtn.onclick = (e) => {
                e.stopPropagation();
                handleToggleBookmark(place.id, place.type, bookmarkBtn);
            };
        }

        img.src = place.image || place.cover_image_url || PLACEHOLDER_IMG;
        title.textContent = place.name;
        category.textContent = place.category || 'Spot';
        locationText.textContent = `${place.barangay || 'Mangatarem'}`;
        
        // Use a default description if none exists
        description.textContent = place.description || 'Explore this beautiful spot in Mangatarem. Known for its cultural significance and natural beauty, it is a must-visit for every traveler.';
        
        viewDetails.href = place.type === 'attraction' ? `/attractions/${place.id}` : `/business/${place.id}`;
        
        // Dynamic coordinates tracker
        let currentTargetCoords = {
            lat: place.latitude || place.lat,
            lng: place.longitude || place.lng,
            name: place.name
        };
        state.selectedCoords = currentTargetCoords;

        // Handle alternatives dropdown
        if (alternativesContainer && alternativesSelect) {
            if (place.osm_alternatives && place.osm_alternatives.length > 0) {
                // Populate options
                alternativesSelect.innerHTML = '';
                
                // Add primary location option
                const primaryOpt = document.createElement('option');
                primaryOpt.value = JSON.stringify({
                    lat: place.latitude || place.lat,
                    lng: place.longitude || place.lng,
                    name: place.name
                });
                primaryOpt.textContent = `Default: ${place.name} (Official Coords)`;
                alternativesSelect.appendChild(primaryOpt);
                
                // Add alternative options
                place.osm_alternatives.forEach((alt, idx) => {
                    const altOpt = document.createElement('option');
                    altOpt.value = JSON.stringify({
                        lat: alt.lat,
                        lng: alt.lon || alt.lng,
                        name: alt.display_name
                    });
                    altOpt.textContent = `Alt ${idx + 1}: ${alt.display_name.split(',')[0]} (${alt.lat.toFixed(4)}, ${(alt.lon || alt.lng).toFixed(4)})`;
                    alternativesSelect.appendChild(altOpt);
                });
                
                // Reset select value to primary
                alternativesSelect.value = primaryOpt.value;
                
                // Show dropdown
                alternativesContainer.classList.remove('hidden');
                
                // When selection changes, update targeted coordinates and pan map
                alternativesSelect.onchange = () => {
                    try {
                        const selectedVal = JSON.parse(alternativesSelect.value);
                        console.log("📍 [Alternatives] Selection changed:", selectedVal);
                        
                        currentTargetCoords = selectedVal;
                        state.selectedCoords = selectedVal;
                        
                        // Fly to the new coordinate
                        flyToCoords([selectedVal.lng, selectedVal.lat], 17, 70);
                        
                        // Dynamically update the bottom sheet stats & routing listener
                        if (state.userLocation) {
                            const dist = calculateDistance(state.userLocation.lat, state.userLocation.lng, selectedVal.lat, selectedVal.lng);
                            const distEl = document.getElementById('stat-distance');
                            const timeEl = document.getElementById('stat-time');
                            if (distEl) distEl.textContent = `${dist.toFixed(1)} KM`;
                            if (timeEl) timeEl.textContent = `${Math.round(dist * 2.5)} Min`;
                        }
                    } catch (err) {
                        console.error("Error updating targeted alternative coordinates:", err);
                    }
                };
            } else {
                alternativesContainer.classList.add('hidden');
            }
        }

        if (directionsBtn) {
            directionsBtn.onclick = () => {
                console.log("🔗 [Modal] Directions clicked. Target coords:", currentTargetCoords, "User location:", state.userLocation);
                if (!state.userLocation) {
                    console.log("⏳ [Modal] Location missing. Setting pending directions for:", currentTargetCoords.name);
                    state.pendingDirections = {
                        ...place,
                        latitude: currentTargetCoords.lat,
                        longitude: currentTargetCoords.lng,
                        name: currentTargetCoords.name
                    };
                    
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
                getRoute(state.userLocation, { lat: currentTargetCoords.lat, lng: currentTargetCoords.lng });
            };
        }

        overlay.classList.add('active');
    }

    async function fetchBookmarks() {
        try {
            const res = await fetch('/user/favorites/ids');
            const data = await res.json();
            if (data.success) {
                state.bookmarkedIds = {
                    attractions: data.attractions || [],
                    establishments: data.establishments || []
                };
                applyFilters(); // Re-render to show bookmark state
            }
        } catch (error) {
            console.error('Error fetching bookmarks:', error);
        }
    }

    async function handleToggleBookmark(id, type, btnElement) {
        if (!window.USER_AUTH) {
            Swal.fire({
                title: 'Login Required',
                text: 'You need to be logged in to bookmark places.',
                icon: 'info',
                showCancelButton: true,
                confirmButtonText: 'Log In',
                confirmButtonColor: '#00ED64',
                cancelButtonColor: '#9CA3AF'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/auth/login?next=' + encodeURIComponent(window.location.pathname);
                }
            });
            return;
        }

        const isAdding = !btnElement.classList.contains('active');
        
        // Optimistic UI update
        btnElement.classList.toggle('active');
        
        // Update all instances of this bookmark button (modal and sidebar)
        const allBtns = document.querySelectorAll(`[data-id="${id}"][data-type="${type}"]`);
        allBtns.forEach(btn => btn.classList.toggle('active', isAdding));
        if (document.getElementById('modal-bookmark')) {
            // Check if current modal matches this ID
            if (state.selectedPlace && state.selectedPlace.id === id && state.selectedPlace.type === type) {
                document.getElementById('modal-bookmark').classList.toggle('active', isAdding);
            }
        }

        // Update state
        const listName = type === 'attraction' ? 'attractions' : 'establishments';
        if (isAdding) {
            if (!state.bookmarkedIds[listName].includes(id)) {
                state.bookmarkedIds[listName].push(id);
            }
        } else {
            state.bookmarkedIds[listName] = state.bookmarkedIds[listName].filter(bid => bid !== id);
        }

        try {
            const res = await fetch('/user/favorites/toggle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Need to ensure getCsrfToken exists or use standard way
                },
                body: JSON.stringify({
                    target_type: type,
                    target_id: id
                })
            });
            const data = await res.json();
            if (!data.success) {
                throw new Error(data.error || 'Failed to toggle bookmark');
            }
            
            // Success - show subtle toast
            const action = isAdding ? 'Added to' : 'Removed from';
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true
            });
            Toast.fire({
                icon: 'success',
                title: `${action} bookmarks`
            });

        } catch (error) {
            console.error('Bookmark toggle error:', error);
            // Revert on error
            btnElement.classList.toggle('active');
            allBtns.forEach(btn => btn.classList.toggle('active', !isAdding));
            if (isAdding) {
                state.bookmarkedIds[listName] = state.bookmarkedIds[listName].filter(bid => bid !== id);
            } else {
                state.bookmarkedIds[listName].push(id);
            }
            Swal.fire('Error', 'Could not update bookmark. Please try again.', 'error');
        }
    }

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.content || '';
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
        state.markers.forEach(m => {
            if (!isLeafletMode) {
                m.remove();
            } else {
                map.removeLayer(m);
            }
        });
        state.markers = [];
    }

    function flyToPlace(place) {
        state.selectedPlace = place;
        const lat = place.latitude || place.lat;
        const lng = place.longitude || place.lng;
        
        flyToCoords([lng, lat], 17, 70);

        updateStats(place);
    }

    function flyToCoords(coords, zoom, pitch = 0) {
        if (!isLeafletMode) {
            map.flyTo({
                center: coords,
                zoom: zoom,
                pitch: pitch,
                duration: 1500,
                essential: true
            });
        } else {
            map.flyTo([coords[1], coords[0]], zoom, {
                animate: true,
                duration: 1.5
            });
        }
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
                
                // Show route on map instead of Google Maps using selectedCoords override if available
                const destination = state.selectedCoords || { 
                    lat: state.selectedPlace.latitude || state.selectedPlace.lat, 
                    lng: state.selectedPlace.longitude || state.selectedPlace.lng 
                };
                getRoute(state.userLocation, destination);
            };
        }
    }

    async function getRoute(origin, destination, mode = 'driving') {
        console.log("🛣️ [Routing] Calculating route:", { origin, destination, mode });
        
        if (isLeafletMode) {
            try {
                state.currentNavMode = mode;
                state.isNavigating = true;

                const profile = mode === 'driving' ? 'driving' : mode === 'walking' ? 'walking' : 'cycling';
                // Using OSRM Public Demo Server
                const url = `https://router.project-osrm.org/route/v1/${profile}/${origin.lng},${origin.lat};${destination.lng},${destination.lat}?overview=full&geometries=geojson&steps=true`;
                console.log("🌐 [Routing] Fetching from OSRM:", url);

                const response = await fetch(url);
                const json = await response.json();

                if (json.code !== 'Ok' || !json.routes || json.routes.length === 0) {
                    Swal.fire('Route Not Found', 'No route found for this destination.', 'warning');
                    return;
                }

                const data = json.routes[0];
                const routeCoords = data.geometry.coordinates; // OSRM GeoJSON is [lng, lat]
                
                // Remove existing route
                if (state.currentRouteLayer) {
                    map.removeLayer(state.currentRouteLayer);
                }

                // Convert [lng, lat] to [lat, lng] for Leaflet
                const leafletCoords = routeCoords.map(coord => [coord[1], coord[0]]);
                
                state.currentRouteLayer = L.polyline(leafletCoords, {
                    color: '#00ED64',
                    weight: 6,
                    opacity: 0.8,
                    lineJoin: 'round'
                }).addTo(map);

                // Zoom to fit
                map.fitBounds(state.currentRouteLayer.getBounds(), {
                    padding: [50, 50]
                });

                // Update Side Panel
                updateNavigationUI(data);
                return;
            } catch (error) {
                console.error('OSRM Routing error:', error);
                Swal.fire('Error', 'Could not calculate route via OSRM.', 'error');
                return;
            }
        }

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
            updateNavigationUI(data);

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
                
                // Clear Mapbox Route
                if (!isLeafletMode) {
                    if (map.getLayer('route')) map.removeLayer('route');
                    if (map.getSource('route')) map.removeSource('route');
                } 
                
                // Clear Leaflet Route
                if (state.currentRouteLayer) {
                    map.removeLayer(state.currentRouteLayer);
                    state.currentRouteLayer = null;
                }
                
                state.isNavigating = false;
            };
        }

        modeBtns.forEach(btn => {
            btn.onclick = () => {
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.currentNavMode = btn.dataset.mode;
                
                if (state.userLocation && state.selectedPlace) {
                    const destination = state.selectedCoords || {
                        lat: state.selectedPlace.latitude || state.selectedPlace.lat,
                        lng: state.selectedPlace.longitude || state.selectedPlace.lng
                    };
                    getRoute(state.userLocation, destination, state.currentNavMode);
                }
            };
        });
    }

    // Helper to share UI update logic between engines - Moved to outer scope for accessibility
    function updateNavigationUI(data) {
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
                    if (step.maneuver.type && step.maneuver.type.includes('turn')) {
                        icon = (step.maneuver.modifier && step.maneuver.modifier.includes('right')) ? '→' : '←';
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

        // Update stats in bottom sheet
        const distEl = document.getElementById('stat-distance');
        const timeEl = document.getElementById('stat-time');
        if (distEl && timeEl) {
            distEl.textContent = `${(data.distance / 1000).toFixed(1)} KM`;
            timeEl.textContent = `${Math.round(data.duration / 60)} Min`;
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

    function initMapServiceSwitcher() {
        const btn = document.getElementById('map-service-btn');
        const menu = document.getElementById('map-service-menu');
        const serviceOptions = document.querySelectorAll('.service-option');
        const styleOptions = document.querySelectorAll('.style-option');

        if (!btn || !menu) return;

        // Set initial active states
        serviceOptions.forEach(opt => {
            opt.classList.toggle('active', opt.dataset.service === state.mapService);
        });
        styleOptions.forEach(opt => {
            opt.classList.toggle('active', opt.dataset.style === state.mapStyle);
        });

        btn.onclick = (e) => {
            e.stopPropagation();
            menu.classList.toggle('active');
        };

        serviceOptions.forEach(opt => {
            opt.onclick = () => {
                const newService = opt.dataset.service;
                if (newService === state.mapService) return;

                serviceOptions.forEach(o => o.classList.remove('active'));
                opt.classList.add('active');
                
                menu.classList.remove('active');
                switchMapService(newService);
            };
        });

        styleOptions.forEach(opt => {
            opt.onclick = () => {
                const newStyle = opt.dataset.style;
                if (newStyle === state.mapStyle) return;

                styleOptions.forEach(o => o.classList.remove('active'));
                opt.classList.add('active');
                
                switchMapStyle(newStyle);
            };
        });

        // Close menu on click outside
        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && e.target !== btn && !btn.contains(e.target)) {
                menu.classList.remove('active');
            }
        });
    }

    function switchMapStyle(newStyle) {
        console.log(`🎨 Switching map style to: ${newStyle}`);
        state.mapStyle = newStyle;
        localStorage.setItem('gomangatarem_map_style', newStyle);

        if (!isLeafletMode) {
            // Mapbox style switch
            const styleUrl = MAP_STYLES.mapbox[newStyle];
            if (styleUrl) {
                map.setStyle(styleUrl);
                // We need to re-add things like 3D buildings and custom layers when style changes
                map.once('style.load', () => {
                    add3DBuildings(map);
                    // If directions was active, we might need to re-add the route source/layer
                    if (state.isNavigating && state.userLocation && state.selectedPlace) {
                        getRoute(state.userLocation, {
                            lat: state.selectedPlace.latitude || state.selectedPlace.lat,
                            lng: state.selectedPlace.longitude || state.selectedPlace.lng
                        }, state.currentNavMode);
                    }
                });
            }
        } else {
            // Leaflet style switch
            const tileUrl = MAP_STYLES.leaflet[newStyle];
            if (tileUrl && window.baseLayer) {
                map.removeLayer(window.baseLayer);
                window.baseLayer = L.tileLayer(tileUrl, {
                    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
                }).addTo(map);
            }
        }
    }

    function switchMapService(newService) {
        console.log(`🔄 Switching map service to: ${newService}`);
        
        // Save to state and persistence
        state.mapService = newService;
        localStorage.setItem('gomangatarem_map_service', newService);

        // Optional: Show loading state
        Swal.fire({
            title: 'Updating Map...',
            text: 'Switching map engines.',
            allowOutsideClick: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading()
            },
            timer: 1000
        });

        // Re-init map
        setTimeout(() => {
            initMapInstance();
        }, 300);
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
                        if (!isLeafletMode) {
                            window.userMarker.setLngLat([coords.lng, coords.lat]);
                        } else {
                            window.userMarker.setLatLng([coords.lat, coords.lng]);
                        }
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
                        
                        if (!isLeafletMode) {
                            window.userMarker = new mapboxgl.Marker(userEl)
                                .setLngLat([coords.lng, coords.lat])
                                .addTo(map);
                        } else {
                            window.userMarker = L.marker([coords.lat, coords.lng], {
                                icon: L.divIcon({
                                    className: '',
                                    html: userEl.outerHTML,
                                    iconSize: [20, 20],
                                    iconAnchor: [10, 10]
                                })
                            }).addTo(map);
                        }
                    }

                    applyFilters();
                    
                    flyToCoords([coords.lng, coords.lat], 15, 45);

                    // Start watching position for "navigation" feel
                    if (!window.positionWatcher) {
                        window.positionWatcher = navigator.geolocation.watchPosition(
                            (p) => {
                                console.log("🔄 [Geolocation] Position updated:", p.coords.latitude, p.coords.longitude);
                                state.userLocation = { lat: p.coords.latitude, lng: p.coords.longitude };
                                if (window.userMarker) {
                                    if (!isLeafletMode) {
                                        window.userMarker.setLngLat([p.coords.longitude, p.coords.latitude]);
                                    } else {
                                        window.userMarker.setLatLng([p.coords.latitude, p.coords.longitude]);
                                    }
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
            const mapCanvas = !isLeafletMode ? this.map.getCanvasContainer() : this.map.getContainer();
            
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
            if (!isLeafletMode) {
                const handlers = ['dragPan', 'scrollZoom', 'boxZoom', 'keyboard', 'doubleClickZoom', 'touchZoomRotate', 'touchPitch'];
                handlers.forEach(h => {
                    if (this.map[h]) this.map[h].disable();
                });
            } else {
                this.map.dragging.disable();
                this.map.touchZoom.disable();
                this.map.doubleClickZoom.disable();
                this.map.scrollWheelZoom.disable();
                this.map.boxZoom.disable();
                this.map.keyboard.disable();
            }
        }

        enableMapInteractions() {
            if (!this.map || this.isDragging) return;
            if (!isLeafletMode) {
                const handlers = ['dragPan', 'scrollZoom', 'boxZoom', 'keyboard', 'doubleClickZoom', 'touchZoomRotate', 'touchPitch'];
                handlers.forEach(h => {
                    if (this.map[h]) this.map[h].enable();
                });
            } else {
                this.map.dragging.enable();
                this.map.touchZoom.enable();
                this.map.doubleClickZoom.enable();
                this.map.scrollWheelZoom.enable();
                this.map.boxZoom.enable();
                this.map.keyboard.enable();
            }
        }

        onDragStart(e) {
            this.isDragging = true;
            this.hasMoved = false;
            this.startY = e.touches[0].clientY;
            
            this.disableMapInteractions();
            const mapCanvas = !isLeafletMode ? this.map.getCanvasContainer() : this.map.getContainer();
            mapCanvas.style.pointerEvents = 'none';
            
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
            const mapCanvas = !isLeafletMode ? this.map.getCanvasContainer() : this.map.getContainer();
            mapCanvas.style.pointerEvents = 'auto';
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
        if (!map || isLeafletMode) return;
        if (map.getLayer('3d-buildings')) return;

        const style = map.getStyle();
        if (!style || !style.layers) return;

        const labelLayer = style.layers.find(
            (layer) => layer.type === 'symbol' && layer.layout && layer.layout['text-field']
        );
        const labelLayerId = labelLayer ? labelLayer.id : undefined;

        try {
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
        } catch (e) {
            console.warn("⚠️ Could not add 3D buildings to this style:", e);
        }
    }
});
