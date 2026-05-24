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
        visitedIds: {
            attractions: [],
            establishments: []
        },
        arrivedPlaceIds: {
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
            filtered = filtered.filter(p => {
                const cat = p.category.toLowerCase();
                const current = state.currentCategory.toLowerCase();
                if (current === 'restaurant') {
                    return cat === 'restaurant' || cat === 'fastfood';
                }
                return cat === current;
            });
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
        const visitBtn = document.getElementById('modal-visit');
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

        const isVisited = (place.type === 'attraction' && state.visitedIds.attractions.includes(place.id)) ||
                          (place.type === 'establishment' && state.visitedIds.establishments.includes(place.id));
        
        if (visitBtn) {
            visitBtn.dataset.id = place.id;
            visitBtn.dataset.type = place.type;
            visitBtn.classList.toggle('active', isVisited);
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
            }
            
            // Fetch visited IDs
            const vRes = await fetch('/user/visits/ids');
            const vData = await vRes.json();
            if (vData.success) {
                state.visitedIds = {
                    attractions: vData.attractions || [],
                    establishments: vData.establishments || []
                };
            }
            
            applyFilters(); // Re-render to show bookmark/visited state
        } catch (error) {
            console.error('Error fetching bookmarks/visited:', error);
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

        const closeModal = () => {
            overlay.classList.remove('active');
            
            // Clear selected place and hide stats panel when modal is closed
            state.selectedPlace = null;
            state.selectedCoords = null;
            const statsEl = document.getElementById('place-stats');
            if (statsEl) {
                statsEl.classList.add('hidden');
            }
        };

        closeBtn.onclick = closeModal;
        overlay.onclick = (e) => {
            if (e.target === overlay) closeModal();
        };

        // Close on Escape
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
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

    // ========================================
    // GEMINI LIVE API INTERFACE
    // ========================================
    window.geminiPanMap = function(lat, lng, zoom = 16) {
        console.log(`[Gemini] Panning map to ${lat}, ${lng} at zoom ${zoom}`);
        // Map_v2 uses [lng, lat] for flyToCoords regardless of engine because 
        // flyToCoords internally swaps them for Leaflet
        flyToCoords([lng, lat], zoom, 0);
    };

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
                
                // Store the fixed origin and destination for mode switches
                state.navOrigin = { lat: state.userLocation.lat, lng: state.userLocation.lng };
                state.navDestination = destination;
                
                getRoute(state.navOrigin, state.navDestination);

                // Hide the bottom sheet so that the Directions panel is the only thing visible
                if (window.sheetManager) {
                    window.sheetManager.snapTo('hidden');
                }
            };
        }
    }

    async function getRoute(origin, destination, mode = 'driving') {
        console.log("🛣️ [Routing] Calculating route:", { origin, destination, mode });
        
        if (isLeafletMode) {
            try {
                state.currentNavMode = mode;
                state.isNavigating = true;

                const profile = mode === 'driving' ? 'car' : mode === 'walking' ? 'foot' : 'bicycle';
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
                if (state.traveledRouteLayer) {
                    map.removeLayer(state.traveledRouteLayer);
                    state.traveledRouteLayer = null;
                }
                if (state.routeStepsLayer) {
                    map.removeLayer(state.routeStepsLayer);
                    state.routeStepsLayer = null;
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

                // Add step markers for Leaflet
                const stepMarkers = [];
                data.legs[0].steps.forEach((step, index) => {
                    let coords = null;
                    if (step.geometry && step.geometry.coordinates && step.geometry.coordinates.length > 0) {
                        coords = step.geometry.coordinates[0]; // [lng, lat]
                    } else if (step.maneuver && step.maneuver.location) {
                        coords = step.maneuver.location; // [lng, lat]
                    }
                    if (coords) {
                        const circle = L.circleMarker([coords[1], coords[0]], {
                            radius: 8,
                            fillColor: '#ffffff',
                            color: '#0ea5e9',
                            weight: 3,
                            opacity: 1,
                            fillOpacity: 1
                        });
                        circle.on('click', () => {
                            highlightTraveledRoute(index, data);
                            const instructionsEl = document.getElementById('nav-instructions');
                            if (instructionsEl) {
                                const stepEls = instructionsEl.querySelectorAll('.instruction-step');
                                stepEls.forEach(s => s.classList.remove('bg-red-50', 'border-red-200'));
                                if (stepEls[index]) stepEls[index].classList.add('bg-red-50', 'border-red-200');
                                if (stepEls[index]) stepEls[index].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            }
                        });
                        stepMarkers.push(circle);
                    }
                });
                state.routeStepsLayer = L.featureGroup(stepMarkers).addTo(map);

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
            
            if (json.code !== 'Ok' || !json.routes || json.routes.length === 0) {
                const errorMsg = json.message || `No ${mode} route found. It might be too far.`;
                Swal.fire('Route Not Found', errorMsg, 'warning');
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
            if (map.getLayer('route-traveled')) map.removeLayer('route-traveled');
            if (map.getSource('route-traveled')) map.removeSource('route-traveled');

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

            // Add step points for Mapbox
            const stepPoints = data.legs[0].steps.map((step, index) => {
                let coords = null;
                if (step.geometry && step.geometry.coordinates && step.geometry.coordinates.length > 0) {
                    coords = step.geometry.coordinates[0];
                } else if (step.maneuver && step.maneuver.location) {
                    coords = step.maneuver.location;
                }
                
                if (coords) {
                    return {
                        type: 'Feature',
                        properties: { stepIndex: index },
                        geometry: { type: 'Point', coordinates: coords }
                    };
                }
                return null;
            }).filter(f => f !== null);

            if (map.getLayer('route-steps-points')) map.removeLayer('route-steps-points');
            if (map.getSource('route-steps')) map.removeSource('route-steps');

            map.addSource('route-steps', {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: stepPoints
                }
            });

            map.addLayer({
                id: 'route-steps-points',
                type: 'circle',
                source: 'route-steps',
                paint: {
                    'circle-radius': 8,
                    'circle-color': '#ffffff',
                    'circle-stroke-width': 3,
                    'circle-stroke-color': '#0ea5e9'
                }
            });

            map.on('click', 'route-steps-points', (e) => {
                if (e.features.length > 0) {
                    const idx = e.features[0].properties.stepIndex;
                    highlightTraveledRoute(idx, data);
                    const instructionsEl = document.getElementById('nav-instructions');
                    if (instructionsEl) {
                        const stepEls = instructionsEl.querySelectorAll('.instruction-step');
                        stepEls.forEach(s => s.classList.remove('bg-red-50', 'border-red-200'));
                        if (stepEls[idx]) stepEls[idx].classList.add('bg-red-50', 'border-red-200');
                        if (stepEls[idx]) stepEls[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                }
            });
            map.on('mouseenter', 'route-steps-points', () => { map.getCanvas().style.cursor = 'pointer'; });
            map.on('mouseleave', 'route-steps-points', () => { map.getCanvas().style.cursor = ''; });

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
                    if (map.getLayer('route-traveled')) map.removeLayer('route-traveled');
                    if (map.getSource('route-traveled')) map.removeSource('route-traveled');
                    if (map.getLayer('route-steps-points')) map.removeLayer('route-steps-points');
                    if (map.getSource('route-steps')) map.removeSource('route-steps');
                } 
                
                // Clear Leaflet Route
                if (state.currentRouteLayer) {
                    map.removeLayer(state.currentRouteLayer);
                    state.currentRouteLayer = null;
                }
                if (state.traveledRouteLayer) {
                    map.removeLayer(state.traveledRouteLayer);
                    state.traveledRouteLayer = null;
                }
                if (state.routeStepsLayer) {
                    map.removeLayer(state.routeStepsLayer);
                    state.routeStepsLayer = null;
                }
                
                state.isNavigating = false;

                // Hide the place stats so "Start Navigation" button disappears
                const statsEl = document.getElementById('place-stats');
                if (statsEl) {
                    statsEl.classList.add('hidden');
                }
                
                // Clear selected place state to reset the UI fully
                state.selectedPlace = null;
                state.selectedCoords = null;
                
                if (window.sheetManager) {
                    window.sheetManager.snapTo('bottom');
                }
            };
        }

        modeBtns.forEach(btn => {
            btn.onclick = (e) => {
                e.stopPropagation();
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.currentNavMode = btn.dataset.mode;
                
                // Use fixed navOrigin and navDestination if available
                if (state.navOrigin && state.navDestination) {
                    getRoute(state.navOrigin, state.navDestination, state.currentNavMode);
                } else if (state.userLocation && state.selectedPlace) {
                    const destination = state.selectedCoords || {
                        lat: state.selectedPlace.latitude || state.selectedPlace.lat,
                        lng: state.selectedPlace.longitude || state.selectedPlace.lng
                    };
                    state.navOrigin = { lat: state.userLocation.lat, lng: state.userLocation.lng };
                    state.navDestination = destination;
                    getRoute(state.navOrigin, state.navDestination, state.currentNavMode);
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
                instructionsEl.innerHTML = data.legs[0].steps.map((step, index) => {
                    const type = step.maneuver.type || '';
                    const modifier = step.maneuver.modifier || '';
                    const name = step.name || '';
                    
                    let icon = '●';
                    if (type === 'arrive') {
                        icon = '🏁';
                    } else if (type === 'depart') {
                        icon = '▲';
                    } else if (modifier.includes('right')) {
                        icon = modifier.includes('sharp') || modifier.includes('slight') ? '↗' : '→';
                    } else if (modifier.includes('left')) {
                        icon = modifier.includes('sharp') || modifier.includes('slight') ? '↖' : '←';
                    } else if (modifier === 'straight') {
                        icon = '↑';
                    }

                    // Generate human-readable instruction if undefined (e.g. from OSRM)
                    let instructionText = step.maneuver.instruction;
                    if (!instructionText) {
                        const capitalize = (str) => str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
                        if (type === 'depart') {
                            instructionText = name ? `Head ${modifier} on ${name}` : 'Depart';
                        } else if (type === 'arrive') {
                            instructionText = name ? `Arrive at ${name}` : 'Arrive at destination';
                        } else if (type === 'turn') {
                            instructionText = `Turn ${modifier} ${name ? 'onto ' + name : ''}`.trim();
                        } else if (type === 'continue') {
                            instructionText = `Continue ${modifier} ${name ? 'on ' + name : ''}`.trim();
                        } else if (type === 'fork') {
                            instructionText = `Take the fork ${modifier} ${name ? 'onto ' + name : ''}`.trim();
                        } else if (type === 'merge') {
                            instructionText = `Merge ${modifier} ${name ? 'onto ' + name : ''}`.trim();
                        } else if (type === 'new name') {
                            instructionText = name ? `Continue onto ${name}` : 'Continue straight';
                        } else {
                            const action = capitalize(type) || 'Proceed';
                            const direction = modifier ? ` ${modifier}` : '';
                            const road = name ? ` onto ${name}` : '';
                            instructionText = `${action}${direction}${road}`.replace(/\s+/g, ' ').trim();
                        }
                    }

                    return `
                        <div class="instruction-step flex items-center gap-3 p-2 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors border border-transparent hover:border-gray-100" data-step-index="${index}">
                            <div class="w-6 h-6 flex items-center justify-center bg-[#00ED64]/10 rounded-lg shrink-0 text-[#00ED64] text-[10px] font-bold">
                                ${icon}
                            </div>
                            <div>
                                <p class="text-[11px] text-gray-800 font-bold leading-tight">${instructionText}</p>
                                <p class="text-[9px] text-gray-400 mt-0.5">${(step.distance / 1000).toFixed(2)} km</p>
                            </div>
                        </div>
                    `;
                }).join('');

                const stepEls = instructionsEl.querySelectorAll('.instruction-step');
                stepEls.forEach(el => {
                    el.onclick = () => {
                        const idx = parseInt(el.dataset.stepIndex);
                        console.log(`[Navigation] Step ${idx} clicked`);
                        highlightTraveledRoute(idx, data);
                        
                        // Visual feedback on the list
                        stepEls.forEach(s => s.classList.remove('bg-red-50', 'border-red-200'));
                        if (stepEls[idx]) stepEls[idx].classList.add('bg-red-50', 'border-red-200');
                        
                        // Scroll selected item into view if it was clicked
                        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    };
                });
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

    function highlightTraveledRoute(stepIndex, data) {
        try {
            console.log(`[Navigation] Highlighting route up to step ${stepIndex}`);
            if (!data || !data.legs || !data.legs[0].steps) {
                console.log("[Navigation] Missing data or steps");
                return;
            }
            
            // Extract a subset of the exact main route geometry to ensure perfect overlap
            let traveledCoords = [];
            if (data.geometry && data.geometry.coordinates) {
                const fullRoute = data.geometry.coordinates;
                
                if (stepIndex >= data.legs[0].steps.length - 1) {
                    traveledCoords = [...fullRoute];
                } else {
                    let targetCoord = data.legs[0].steps[stepIndex + 1].maneuver.location;
                    if (!targetCoord && data.legs[0].steps[stepIndex].geometry) {
                        const stepGeom = data.legs[0].steps[stepIndex].geometry.coordinates;
                        targetCoord = stepGeom[stepGeom.length - 1];
                    }
                    
                    if (targetCoord) {
                        let minIdx = -1;
                        let minDist = Infinity;
                        for (let i = 0; i < fullRoute.length; i++) {
                            const dx = fullRoute[i][0] - targetCoord[0];
                            const dy = fullRoute[i][1] - targetCoord[1];
                            const dist = dx*dx + dy*dy;
                            if (dist < minDist) {
                                minDist = dist;
                                minIdx = i;
                            }
                        }
                        if (minIdx !== -1) {
                            traveledCoords = fullRoute.slice(0, minIdx + 1);
                        }
                    }
                }
            }

            console.log(`[Navigation] Accumulated ${traveledCoords.length} coordinates`);

            // Mapbox LineString needs at least 2 points
            if (traveledCoords.length < 2) {
                console.log("[Navigation] Not enough coordinates to draw a line");
                return;
            }

            if (isLeafletMode) {
                if (state.traveledRouteLayer) {
                    map.removeLayer(state.traveledRouteLayer);
                }
                
                const leafletCoords = traveledCoords.map(coord => [coord[1], coord[0]]);
                
                state.traveledRouteLayer = L.polyline(leafletCoords, {
                    color: '#EF4444',
                    weight: 8,
                    opacity: 1.0,
                    lineJoin: 'round',
                    className: 'traveled-route-layer'
                }).addTo(map);

                if (traveledCoords.length > 0) {
                    const lastCoord = traveledCoords[traveledCoords.length - 1];
                    map.flyTo([lastCoord[1], lastCoord[0]], 15, { duration: 1.5 });
                }

            } else {
                const geojson = {
                    type: 'FeatureCollection',
                    features: [{
                        type: 'Feature',
                        properties: {},
                        geometry: {
                            type: 'LineString',
                            coordinates: traveledCoords
                        }
                    }]
                };

                console.log("[Navigation] Drawing traveled geojson:", geojson);

                if (map.getSource('route-traveled')) {
                    map.getSource('route-traveled').setData(geojson);
                    if (!map.getLayer('route-traveled')) {
                        map.addLayer({
                            id: 'route-traveled',
                            type: 'line',
                            source: 'route-traveled',
                            layout: { 'line-join': 'round', 'line-cap': 'round' },
                            paint: { 'line-color': '#EF4444', 'line-width': 8, 'line-opacity': 1.0 }
                        });
                        // Ensure it appears right below points if they exist
                        if (map.getLayer('route-steps-points')) {
                            map.moveLayer('route-traveled', 'route-steps-points');
                        }
                    }
                } else {
                    map.addSource('route-traveled', {
                        type: 'geojson',
                        data: geojson
                    });

                    map.addLayer({
                        id: 'route-traveled',
                        type: 'line',
                        source: 'route-traveled',
                        layout: { 'line-join': 'round', 'line-cap': 'round' },
                        paint: { 'line-color': '#EF4444', 'line-width': 8, 'line-opacity': 1.0 }
                    });
                    
                    // Ensure it appears right below points if they exist
                    if (map.getLayer('route-steps-points')) {
                        map.moveLayer('route-traveled', 'route-steps-points');
                    }
                }

                if (traveledCoords.length > 0) {
                    const lastCoord = traveledCoords[traveledCoords.length - 1];
                    map.flyTo({ center: lastCoord, zoom: 15, duration: 1500 });
                }
            }
        } catch (error) {
            console.error("Error highlighting traveled route:", error);
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

    let lastArrivalCheckTime = 0;

    function checkArrivalProximity(lat, lng) {
        const now = Date.now();
        // Throttle check to at most once every 20 seconds to preserve device battery life
        if (now - lastArrivalCheckTime < 20000) {
            return;
        }
        lastArrivalCheckTime = now;

        const payload = {
            latitude: lat,
            longitude: lng
        };

        // If navigating, include navigated target detail to automatically log navigation arrivals
        if (state.isNavigating && state.selectedPlace) {
            const type = state.selectedPlace.category === 'hotel' || state.selectedPlace.category === 'restaurant' ? 'establishment' : 'attraction';
            // Verify if we already arrived at this specific place during the current session
            if (state.arrivedPlaceIds[type + 's'] && state.arrivedPlaceIds[type + 's'].includes(state.selectedPlace.id)) {
                // Already processed, do nothing
            } else {
                payload.navigated_target_id = state.selectedPlace.id;
                payload.navigated_target_type = type;
            }
        }

        console.log("📡 [Arrival] Verifying physical proximity boundaries with Mangatarem server...", payload);

        fetch('/booking/api/verify-arrival', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (!res.ok) throw new Error('Arrival verification request failed');
            return res.json();
        })
        .then(data => {
            if (data.success) {
                // 1. Handle automatic today's booking check-in success
                if (data.booking_attended) {
                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 5000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                            toast.addEventListener('mouseenter', Swal.stopTimer);
                            toast.addEventListener('mouseleave', Swal.resumeTimer);
                        }
                    });
                    Toast.fire({
                        icon: 'success',
                        iconColor: '#15803d',
                        background: '#f0fdf4',
                        title: `<span style="color: #166534; font-weight: 700;">Arrived & Checked In!</span>`,
                        html: `<p style="color: #1b5e20; margin: 0; font-size: 0.875rem;">Your reservation at <strong>${data.place_name}</strong> is verified and logged automatically.</p>`
                    });
                }

                // 2. Handle navigated target arrival success
                if (data.navigated_arrived && data.target_id && data.target_type) {
                    const type = data.target_type;
                    const id = data.target_id;
                    
                    // Prevent duplicate triggers
                    if (!state.arrivedPlaceIds[type + 's'].includes(id)) {
                        state.arrivedPlaceIds[type + 's'].push(id);
                    }

                    // Stop map navigation by programmatically triggering close-nav click
                    const closeNavBtn = document.getElementById('close-nav');
                    if (closeNavBtn) {
                        closeNavBtn.click();
                    }

                    const placeName = data.place_name || 'Landmark';
                    
                    // Show a gorgeous, custom-styled Emerald and Gold welcome modal
                    Swal.fire({
                        title: `<div class="flex flex-col items-center gap-2">
                                    <div class="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center animate-bounce mb-2">
                                        <svg class="w-10 h-10 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
                                        </svg>
                                    </div>
                                    <span class="text-emerald-800 font-extrabold text-2xl tracking-tight">Welcome to ${placeName}!</span>
                                </div>`,
                        html: `
                            <div class="px-2 text-center">
                                <p class="text-gray-600 mb-6 text-sm leading-relaxed">
                                    You have physically arrived at <strong class="text-gray-800">${placeName}</strong>! 
                                    We have safely registered and logged your visit to your Mangatarem tourist journey.
                                </p>
                                <div class="flex flex-col gap-3">
                                    <button id="swal-review-btn" class="w-full py-3 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl font-bold transition-all shadow-md flex items-center justify-center gap-2 border border-emerald-800 cursor-pointer">
                                        ✍️ Log Journey & Leave Review
                                    </button>
                                    <a href="/attractions/${id}" id="swal-explore-btn" class="w-full py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold transition-all shadow-md flex items-center justify-center gap-2 border border-amber-600 text-center text-sm no-underline block cursor-pointer">
                                        🏛️ Explore Historical Heritage
                                    </a>
                                    <button id="swal-close-btn" class="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-bold transition-all text-sm border border-gray-200 cursor-pointer">
                                        Dismiss
                                    </button>
                                </div>
                            </div>
                        `,
                        showConfirmButton: false,
                        allowOutsideClick: false,
                        customClass: {
                            popup: 'rounded-3xl border border-emerald-100 shadow-2xl p-6 bg-white',
                        },
                        didOpen: () => {
                            const rBtn = document.getElementById('swal-review-btn');
                            const xBtn = document.getElementById('swal-explore-btn');
                            const cBtn = document.getElementById('swal-close-btn');
                            
                            if (rBtn) {
                                rBtn.onclick = () => {
                                    Swal.close();
                                    
                                    // Smoothly pop standard visit modal from user-actions
                                    const visitModal = document.getElementById('visit-modal');
                                    if (visitModal) {
                                        visitModal.classList.remove('hidden');
                                        setTimeout(() => {
                                            visitModal.classList.add('active');
                                        }, 10);
                                        document.body.style.overflow = 'hidden';
                                        
                                        const tIdEl = document.getElementById('visit-target-id');
                                        const tTyEl = document.getElementById('visit-target-type');
                                        const tDtEl = document.getElementById('visit-date');
                                        
                                        if (tIdEl) tIdEl.value = id;
                                        if (tTyEl) tTyEl.value = type;
                                        if (tDtEl) tDtEl.valueAsDate = new Date();
                                    }
                                };
                            }
                            
                            if (xBtn) {
                                if (type === 'establishment') {
                                    xBtn.href = `/business/establishments/${id}`;
                                } else {
                                    xBtn.href = `/attractions/${id}`;
                                }
                            }

                            if (cBtn) {
                                cBtn.onclick = () => {
                                    Swal.close();
                                };
                            }
                        }
                    });
                }
            }
        })
        .catch(err => {
            console.error("❌ [Arrival Verification Error]:", err);
        });
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

                    // Verify arrival proximity immediately on finding initial location
                    checkArrivalProximity(coords.lat, coords.lng);

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
                                // Continuously verify physical proximity limits
                                checkArrivalProximity(p.coords.latitude, p.coords.longitude);
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
    
    window.fetchBookmarks = fetchBookmarks;
});
