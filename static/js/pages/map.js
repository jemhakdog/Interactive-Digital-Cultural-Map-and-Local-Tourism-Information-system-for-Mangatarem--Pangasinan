/**
 * Mapbox GL JS Map Implementation for GoMangatarem
 * High-Performance MVT (Mapbox Vector Tile) Implementation
 * 
 * Architecture:
 * - Consumes MVT tiles from /api/tiles/{z}/{x}/{y}.pbf endpoint
 * - Multi-layer support for attractions, heritage, events
 * - Client-side filtering and styling
 * - Optimized for high-concurrency with Vercel Edge Cache
 */

document.addEventListener('DOMContentLoaded', function () {
    const PLACEHOLDER_IMG = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22300%22%20height%3D%22200%22%20xmlns%3D%22http%3D%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Crect%20width%3D%22300%22%20height%3D%22200%22%20fill%3D%22%23eee%22%2F%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20font-family%3D%22sans-serif%22%20font-size%3D%2216%22%20fill%3D%22%23aaa%22%20text-anchor%3D%22middle%22%20dy%3D%22.3em%22%3ENo%20Image%3C%2Ftext%3E%3C%2Fsvg%3E';

    const escapeHTML = (str) => {
        if (!str) return '';
        const p = document.createElement('p');
        p.textContent = str;
        return p.innerHTML;
    };

    // ========================================
    // 1. MAP INITIALIZATION
    // ========================================
    const hasMapboxToken = window.MAPBOX_TOKEN && window.MAPBOX_TOKEN !== 'None' && window.MAPBOX_TOKEN !== '';
    const isLeafletMode = !hasMapboxToken;

    if (!isLeafletMode) {
        mapboxgl.accessToken = window.MAPBOX_TOKEN;
    } else {
        console.warn("⚠️ Mapbox token missing. Switching to LeafletJS fallback.");
    }

    let map;
    let isNavigating = false;
    let customUserMarker = null;
    let currentDestination = null;
    let realTimeRouteLayer = null;
    let realTimeRouteSource = null;
    if (!isLeafletMode) {
        map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [120.2986, 15.7889], // Mangatarem coordinates [lng, lat]
            zoom: 13.5,
            pitch: 65,      // Tilted view for 3D effect
            bearing: -15,   // Rotated view
            attributionControl: true,
            antialias: true // Smoother 3D edges
        });
    } else {
        map = L.map('map', {
            zoomControl: false
        }).setView([15.7889, 120.2986], 14);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        }).addTo(map);
        
        L.control.zoom({ position: 'topleft' }).addTo(map);
    }

    // Add navigation controls
    if (!isLeafletMode) {
        map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    } else {
        L.control.zoom({ position: 'topleft' }).addTo(map);
    }

    // ========================================
    // 1.1 GEOLOCATION ENGINE INITIALIZATION
    // ========================================
    // Initialize standard GeolocateControl but hide its default button via CSS
    // We will trigger it using our custom #locate-me button
    let geolocate;
    if (!isLeafletMode) {
        geolocate = new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            trackUserLocation: true,
            showUserHeading: true,
            showAccuracyCircle: true
        });

        map.addControl(geolocate);
    }

    // Force resize calculation for mobile layout
    const onMapLoad = () => {
        setTimeout(() => {
            if (!isLeafletMode) map.resize();
            else map.invalidateSize();
        }, 500);
        setTimeout(() => {
            if (!isLeafletMode) map.resize();
            else map.invalidateSize();
        }, 1500); 
    };

    if (!isLeafletMode) {
        map.on('load', onMapLoad);
    } else {
        onMapLoad();
    }

    window.addEventListener('resize', () => {
        if (!isLeafletMode) map.resize();
        else map.invalidateSize();
    });

    // ========================================
    // 2. CATEGORY ICON CONFIGURATION
    // ========================================
    const iconConfig = {
        // Core Categories
        Nature: { color: '#10b981', emoji: '🌿' },      // Emerald Green
        Historical: { color: '#f59e0b', emoji: '🏛️' },  // Amber
        Religious: { color: '#6366f1', emoji: '⛪' },   // Indigo
        
        // Establishments & Services
        Food: { color: '#f43f5e', emoji: '🍽️' },        // Rose Red
        Restaurant: { color: '#f43f5e', emoji: '🍽️' }, 
        Cafe: { color: '#f43f5e', emoji: '☕' },
        Fastfood: { color: '#f43f5e', emoji: '🍔' },
        Lodging: { color: '#0ea5e9', emoji: '🏨' },     // Sky Blue
        Inn: { color: '#0ea5e9', emoji: '🏨' },
        
        // Heritage & Culture
        Built: { color: '#f59e0b', emoji: '🏛️' },
        Movable: { color: '#8b5cf6', emoji: '🏺' },
        Intangible: { color: '#ec4899', emoji: '🎭' },
        Personality: { color: '#64748b', emoji: '👤' },
        Institution: { color: '#06b6d4', emoji: '🏫' },
        
        // Events
        Events: { color: '#eab308', emoji: '📅' },      // Yellow
        Civic: { color: '#3b82f6', emoji: '🏛️' },       // Blue
        
        default: { color: '#94a3b8', emoji: '📍' }      // Slate Gray
    };

    // ========================================
    // 3. MVT TILE SOURCE SETUP
    // ========================================
    let attractionsData = [];
    let currentCategory = 'all';
    let currentBarangay = 'all';
    let currentSearchTerm = '';
    
    // Pagination state (for sidebar list, not map tiles)
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = false;
    let hasMorePages = true;
    const loadingIndicator = document.getElementById('loading-indicator');

    // Add MVT tile source when map loads
    if (!isLeafletMode) {
        map.on('load', () => {
            setupMVTSource();
            setupMVTLayers();
            init3DLayers();
            fetchAttractions(1, true); // Fetch for sidebar list
        });
    } else {
        // In Leaflet mode, we skip MVT and 3D
        fetchAttractions(1, true);
    }

    // Re-add layers when style changes
    if (!isLeafletMode) {
        map.on('style.load', () => {
            // Remove layers first (they depend on the source)
            if (map.getLayer('mvt-heritage-glow')) {
                map.removeLayer('mvt-heritage-glow');
            }
            if (map.getLayer('mvt-points')) {
                map.removeLayer('mvt-points');
            }
            if (map.getLayer('mvt-labels')) {
                map.removeLayer('mvt-labels');
            }
            
            // Then remove source
            if (map.getSource('mvt-tiles')) {
                map.removeSource('mvt-tiles');
            }
            
            // Re-add everything
            setupMVTSource();
            setupMVTLayers();
            init3DLayers();
        });
    }

    function setupMVTSource() {
        // Guard: Check if source already exists
        if (map.getSource('mvt-tiles')) {
            return;
        }

        // Create absolute URL for tiles (Mapbox requires absolute URLs)
        const tileUrl = `${window.location.origin}/api/tiles/{z}/{x}/{y}.pbf?layer=attractions`;

        // Add vector tile source
        map.addSource('mvt-tiles', {
            type: 'vector',
            tiles: [tileUrl],
            minzoom: 0,
            maxzoom: 20,
            scheme: 'xyz',
            promoteId: 'id' // Enable feature state for hover effects
        });
    }

    function setupMVTLayers() {
        // Get layer order from existing style
        const layers = map.getStyle().layers;
        const labelLayerId = layers?.find(
            (layer) => layer.type === 'symbol' && layer.layout?.['text-field']
        )?.id;

        // Add a golden/bronze heritage glow layer for dual-marker representation
        if (!map.getLayer('mvt-heritage-glow')) {
            map.addLayer({
                id: 'mvt-heritage-glow',
                type: 'circle',
                source: 'mvt-tiles',
                'source-layer': 'layer',
                minzoom: 10,
                filter: ['in', 'category', 'Built', 'Movable', 'Intangible', 'Personality', 'Institution', 'Historical'],
                paint: {
                    'circle-radius': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        10, 8,
                        14, 15,
                        16, 22
                    ],
                    'circle-color': '#d97706',
                    'circle-opacity': 0.45,
                    'circle-blur': 0.6
                }
            }, labelLayerId);
        }

        // Add circle layer for points (styled by category)
        if (!map.getLayer('mvt-points')) {
            map.addLayer({
                id: 'mvt-points',
                type: 'circle',
                source: 'mvt-tiles',
                'source-layer': 'layer',
                minzoom: 10,
                paint: {
                    'circle-radius': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        10, 4,
                        14, 8,
                        16, 12
                    ],
                    'circle-color': [
                        'match',
                        ['get', 'category'],
                        'Nature', '#10b981',
                        'Historical', '#f59e0b',
                        'Religious', '#6366f1',
                        'Food', '#f43f5e',
                        'Restaurant', '#f43f5e',
                        'Cafe', '#f43f5e',
                        'Fastfood', '#f43f5e',
                        'Lodging', '#0ea5e9',
                        'Inn', '#0ea5e9',
                        'Built', '#f59e0b',
                        'Movable', '#8b5cf6',
                        'Intangible', '#ec4899',
                        'Personality', '#64748b',
                        'Institution', '#06b6d4',
                        'Events', '#eab308',
                        'Civic', '#3b82f6',
                        '#94a3b8' // default
                    ],
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff',
                    'circle-opacity': 0.9
                }
            }, labelLayerId);
        }

        // Add icon layer (using text as emoji placeholder)
        if (!map.getLayer('mvt-labels')) {
            map.addLayer({
                id: 'mvt-labels',
                type: 'symbol',
                source: 'mvt-tiles',
                'source-layer': 'layer',
                minzoom: 14,
                layout: {
                    'text-field': ['get', 'name'],
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Regular'],
                    'text-size': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        14, 10,
                        16, 12
                    ],
                    'text-offset': [0, 1.2],
                    'text-anchor': 'top',
                    'text-allow-overlap': false,
                    'text-ignore-placement': false
                },
                paint: {
                    'text-color': '#333333',
                    'text-halo-color': '#ffffff',
                    'text-halo-width': 1.5
                }
            }, labelLayerId);
        }

        // Add hover effect using feature-state
        map.on('mouseenter', 'mvt-points', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'mvt-points', () => {
            map.getCanvas().style.cursor = '';
        });

        // Click handler for points
        map.on('click', 'mvt-points', (e) => {
            const feature = e.features[0];
            if (!feature) return;

            const attraction = {
                id: feature.properties.id,
                name: feature.properties.name,
                category: feature.properties.category,
                barangay: feature.properties.barangay_id,
                description: feature.properties.description || '',
                image: feature.properties.image_url || '',
                opening_hours: feature.properties.opening_hours || '',
                entrance_fee: feature.properties.entrance_fee || '',
                contact_info: feature.properties.contact_info || '',
                facilities: feature.properties.facilities || '',
                advisory_message: feature.properties.advisory_message || '',
                advisory_status: feature.properties.advisory_status || '',
                lat: e.lngLat.lat,
                lng: e.lngLat.lng
            };

            // Fly to location
            map.flyTo({
                center: [feature.geometry.coordinates[0], feature.geometry.coordinates[1]],
                zoom: 16,
                duration: 1500
            });

            // Update card
            setTimeout(() => {
                updateCard(attraction);
            }, 1600);
        });

        // Hover popup
        let popup = null;
        map.on('mousemove', 'mvt-points', (e) => {
            const feature = e.features[0];
            if (!feature) return;

            if (popup) {
                popup.remove();
            }

            popup = new mapboxgl.Popup({ offset: 10, closeButton: false })
                .setLngLat(e.lngLat)
                .setHTML(`
                    <div class="text-sm">
                        <strong class="text-green-800">${escapeHTML(feature.properties.name)}</strong>
                        <div class="text-xs text-gray-600">${escapeHTML(feature.properties.category)}</div>
                    </div>
                `)
                .addTo(map);
        });

        map.on('mouseleave', 'mvt-points', () => {
            if (popup) {
                popup.remove();
                popup = null;
            }
        });
    }

    // ========================================
    // 4. TAB SYSTEM
    // ========================================
    const tabPlaces = document.getElementById('tab-places');
    const tabRecommended = document.getElementById('tab-recommended');
    const tabRoutes = document.getElementById('tab-routes');
    const placesContent = document.getElementById('places-content');
    const routesContent = document.getElementById('routes-content');

    function switchTab(tab) {
        // Reset all tabs
        [tabPlaces, tabRecommended, tabRoutes].forEach(btn => {
            if (btn) {
                btn.classList.remove('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold', 'border-b-2');
                btn.classList.add('text-gray-500', 'font-medium');
            }
        });

        // Hide all content
        [placesContent, routesContent].forEach(content => content?.classList.add('hidden'));

        if (tab === 'places') {
            tabPlaces.classList.add('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold', 'border-b-2');
            placesContent.classList.remove('hidden');
            fetchAttractions(1, true);
        } else if (tab === 'recommended') {
            tabRecommended.classList.add('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold', 'border-b-2');
            placesContent.classList.remove('hidden'); // Use same container but different fetch
            fetchRecommendations();
        } else if (tab === 'routes') {
            tabRoutes.classList.add('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold', 'border-b-2');
            routesContent.classList.remove('hidden');
        }
    }

    tabPlaces.addEventListener('click', () => switchTab('places'));
    tabRecommended.addEventListener('click', () => switchTab('recommended'));
    tabRoutes.addEventListener('click', () => switchTab('routes'));

    async function fetchRecommendations() {
        const listContainer = document.getElementById('places-content');
        listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">Finding the best spots for you...</div>';
        
        try {
            // Fetch featured attractions
            const response = await fetch('/attractions/api?is_featured=true&per_page=10');
            const result = await response.json();
            
            // Fetch featured establishments
            const estResponse = await fetch('/business/api?is_featured=true&per_page=10');
            const estResult = await estResponse.json();
            
            // Combine and render
            const combined = [...result.attractions, ...estResult.establishments];
            
            if (combined.length === 0) {
                listContainer.innerHTML = '<div class="text-center text-gray-500 py-8"><div class="text-3xl mb-2">✨</div>No recommendations yet. Explore our Places!</div>';
            } else {
                // Mix them up or sort by rating
                combined.sort((a, b) => (b.rating || b.rating_avg || 0) - (a.rating || a.rating_avg || 0));
                
                // Clear and render manually since they might be different types
                listContainer.innerHTML = '';
                combined.forEach(item => {
                    if (item.category) { // It's an attraction
                        renderSingleAttraction(item, listContainer);
                    } else { // It's an establishment
                        renderSingleEstablishment(item, listContainer);
                    }
                });
            }
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            listContainer.innerHTML = '<div class="text-center text-red-500 py-4">Error loading recommendations.</div>';
        }
    }

    // Helper to render a single attraction card
    function renderSingleAttraction(attraction, container) {
        const categoryConfig = iconConfig[attraction.category] || iconConfig.default;
        const safeName = escapeHTML(attraction.name);
        const safeDescription = escapeHTML(attraction.description);
        const safeImage = attraction.image || PLACEHOLDER_IMG;

        const card = document.createElement('div');
        card.className = 'group bg-white rounded-xl shadow-sm border border-emerald-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32 relative';
        card.innerHTML = `
            <div class="absolute -top-1 -left-1 bg-amber-400 text-white text-[8px] font-bold px-2 py-0.5 rounded-br-lg z-10 shadow-sm uppercase tracking-widest">Recommended</div>
            <div class="w-1/3 h-full bg-gray-200 relative flex-shrink-0">
                <img src="${safeImage}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${safeName}">
                <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${categoryConfig.color}">${attraction.category.toUpperCase()}</div>
            </div>
            <div class="w-2/3 p-3 flex flex-col justify-between">
                <div>
                    <h3 class="font-bold text-sm leading-tight mb-1 line-clamp-1">${safeName}</h3>
                    <p class="text-xs text-gray-600 line-clamp-2 mt-1">${safeDescription}</p>
                </div>
                <div class="flex justify-between items-end mt-2">
                    <div class="text-xs font-bold text-amber-500">★★★★★ <span class="text-gray-400 font-normal">(4.5)</span></div>
                    <button class="text-[10px] px-2 py-1 bg-emerald-50 text-emerald-700 rounded transition font-semibold">View ➔</button>
                </div>
            </div>
        `;
        card.addEventListener('click', () => flyToLocation(attraction.id, attraction.latitude, attraction.longitude));
        container.appendChild(card);
    }

    // Helper to render a single establishment card
    function renderSingleEstablishment(est, container) {
        const cfg = estTypeConfig[est.type] || { color: '#6b7280', emoji: '📍', label: est.type };
        const safeName = escapeHTML(est.name);

        const card = document.createElement('div');
        card.className = 'group bg-white rounded-xl shadow-sm border border-orange-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32 relative';
        card.innerHTML = `
            <div class="absolute -top-1 -left-1 bg-amber-400 text-white text-[8px] font-bold px-2 py-0.5 rounded-br-lg z-10 shadow-sm uppercase tracking-widest">Featured</div>
            <div class="w-1/3 h-full bg-gray-200 relative flex-shrink-0">
                <img src="${est.cover_image_url || PLACEHOLDER_IMG}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${safeName}">
                <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${cfg.color}">${cfg.emoji} ${cfg.label.toUpperCase()}</div>
            </div>
            <div class="w-2/3 p-3 flex flex-col justify-between">
                <div>
                    <h3 class="font-bold text-sm leading-tight mb-1 line-clamp-1">${safeName}</h3>
                    <p class="text-xs text-gray-600 line-clamp-2 mt-1">${escapeHTML(est.description)}</p>
                </div>
                <div class="flex justify-between items-end mt-2">
                    <div class="text-[10px] font-bold text-gray-500">★ ${est.rating_avg.toFixed(1)} · ${est.barangay}</div>
                    <button class="text-[10px] px-2 py-1 bg-orange-50 text-orange-700 rounded transition font-semibold">View ➔</button>
                </div>
            </div>
        `;
        card.addEventListener('click', () => flyToEstablishmentLocation(est));
        container.appendChild(card);
    }

    // ========================================
    // 2. CONFIGURATIONS
    // ========================================
    function getCacheKey(page, category, barangay) {
        return `attractions_${page}_${category || 'all'}_${barangay || 'all'}`;
    }

    function getCachedData(cacheKey) {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            const now = Date.now();
            if (now - parsed.timestamp < 5 * 60 * 1000) {
                return parsed.data;
            } else {
                localStorage.removeItem(cacheKey);
            }
        }
        return null;
    }

    function setCachedData(cacheKey, data) {
        const cacheObj = {
            data: data,
            timestamp: Date.now()
        };
        try {
            localStorage.setItem(cacheKey, JSON.stringify(cacheObj));
        } catch (e) {
            console.warn('Could not cache data:', e);
        }
    }

    // ========================================
    // 6. FETCH & RENDER ATTRACTIONS (for sidebar list)
    // ========================================
    async function fetchAttractions(page = 1, reset = false) {
        if (isLoading) return;
        isLoading = true;

        const cacheKey = getCacheKey(page, currentCategory, currentBarangay);
        const cachedData = getCachedData(cacheKey);

        if (cachedData && page === 1 && reset) {
            attractionsData = cachedData.attractions;
            totalPages = cachedData.pagination.pages;
            currentPage = cachedData.pagination.page;
            hasMorePages = cachedData.pagination.has_next;

            renderAttractions(attractionsData);
            isLoading = false;
            return;
        }

        if (page === 1 && reset) {
            const listContainer = document.getElementById('places-content');
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">Loading attractions...</div>';
        } else if (!reset && loadingIndicator) {
            loadingIndicator.classList.remove('hidden');
        }

        try {
            const params = new URLSearchParams({
                page: page,
                per_page: 20
            });

            if (currentCategory && currentCategory !== 'all') {
                params.append('category', currentCategory);
            }
            if (currentBarangay && currentBarangay !== 'all') {
                params.append('barangay', currentBarangay);
            }

            const response = await fetch(`/attractions/api?${params}`);
            const result = await response.json();

            if (reset) {
                attractionsData = result.attractions;
                totalPages = result.pagination.pages;
                currentPage = result.pagination.page;
                hasMorePages = result.pagination.has_next;

                renderAttractions(attractionsData);

                if (page === 1) {
                    setCachedData(cacheKey, result);
                }
            } else {
                attractionsData = [...attractionsData, ...result.attractions];
                totalPages = result.pagination.pages;
                currentPage = result.pagination.page;
                hasMorePages = result.pagination.has_next;

                renderAttractions(attractionsData);
            }

        } catch (error) {
            console.error('Error fetching attractions:', error);
        } finally {
            isLoading = false;
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
        }
    }

    // ========================================
    // 7. 3D LAYERS (Terrain, Buildings, Sky)
    // ========================================
    function init3DLayers() {
        if (isLeafletMode) return;
        // 1. ADD 3D TERRAIN
        if (!map.getSource('mapbox-dem')) {
            map.addSource('mapbox-dem', {
                'type': 'raster-dem',
                'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
                'tileSize': 512,
                'maxzoom': 14
            });
        }
        map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });

        // 2. ADD SKY LAYER (Atmosphere)
        if (!map.getLayer('sky')) {
            map.addLayer({
                'id': 'sky',
                'type': 'sky',
                'paint': {
                    'sky-type': 'atmosphere',
                    'sky-atmosphere-sun': [0.0, 0.0],
                    'sky-atmosphere-sun-intensity': 15
                }
            });
        }

        // 3. ADD 3D BUILDINGS
        if (!map.getLayer('add-3d-buildings')) {
            const layers = map.getStyle().layers;
            const labelLayerId = layers?.find(
                (layer) => layer.type === 'symbol' && layer.layout?.['text-field']
            )?.id;

            if (labelLayerId) {
                map.addLayer(
                    {
                        'id': 'add-3d-buildings',
                        'source': 'composite',
                        'source-layer': 'building',
                        'filter': ['==', 'extrude', 'true'],
                        'type': 'fill-extrusion',
                        'minzoom': 15,
                        'paint': {
                            'fill-extrusion-color': '#aaa',
                            'fill-extrusion-height': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                15,
                                0,
                                15.05,
                                ['get', 'height']
                            ],
                            'fill-extrusion-base': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                15,
                                0,
                                15.05,
                                ['get', 'min_height']
                            ],
                            'fill-extrusion-opacity': 0.6
                        }
                    },
                    labelLayerId
                );
            }
        }
    }

    // ========================================
    // GEMINI LIVE API INTERFACE
    // ========================================
    window.geminiPanMap = function(lat, lng, zoom = 16) {
        console.log(`[Gemini] Panning map to ${lat}, ${lng} at zoom ${zoom}`);
        if (!isLeafletMode) {
            map.flyTo({
                center: [lng, lat],
                zoom: zoom,
                duration: 2000
            });
        } else {
            map.flyTo([lat, lng], zoom, {
                duration: 2
            });
        }
    };

    // Style Switcher Logic
    window.changeMapStyle = function(styleId) {
        if (!isLeafletMode) {
            const styleUrl = `mapbox://styles/mapbox/${styleId}`;
            map.setStyle(styleUrl);
        } else {
            // Leaflet Style Switching (simplified)
            const tiles = {
                'streets-v12': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                'satellite-streets-v12': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                'dark-v11': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                'outdoors-v12': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
            };
            
            if (tiles[styleId]) {
                map.eachLayer(layer => {
                    if (layer._url) map.removeLayer(layer);
                });
                L.tileLayer(tiles[styleId], {
                    attribution: '&copy; OpenStreetMap &copy; CARTO'
                }).addTo(map);
            }
        }

        // Update active button UI
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.classList.remove('active', 'border-green-500', 'bg-green-50');
            if (btn.getAttribute('onclick').includes(styleId)) {
                btn.classList.add('active', 'border-green-500', 'bg-green-50');
            }
        });
    };

    // ========================================
    // 8. PLACE CARD MANAGEMENT
    // ========================================
    const placeCard = document.getElementById('place-card');
    const cardTitle = document.getElementById('card-title');
    const cardAddress = document.getElementById('card-address');
    const cardRating = document.getElementById('card-rating');
    const cardHours = document.getElementById('card-hours');
    const cardFee = document.getElementById('card-fee');
    const cardContact = document.getElementById('card-contact');
    const cardFacilities = document.getElementById('card-facilities');
    const cardAdvisoryBanner = document.getElementById('card-advisory-banner');
    const cardAdvisoryText = document.getElementById('card-advisory-text');
    const cardDescription = document.getElementById('card-description');
    const feedbackAttractionId = document.getElementById('feedback-attraction-id');

    function updateCard(attraction) {
        if (!placeCard) return;

        currentDestination = {
            lat: attraction.lat || attraction.latitude,
            lng: attraction.lng || attraction.longitude
        };

        cardTitle.textContent = attraction.name;
        cardAddress.textContent = attraction.barangay ? `${attraction.barangay}, Mangatarem` : 'Mangatarem, Pangasinan';
        cardDescription.textContent = attraction.description;
        cardRating.textContent = (Math.random() * (5.0 - 4.0) + 4.0).toFixed(1);

        // New Practical Fields
        if (cardHours) cardHours.textContent = attraction.opening_hours || 'N/A';
        if (cardFee) cardFee.textContent = attraction.entrance_fee || 'Free';
        if (cardContact) cardContact.textContent = attraction.contact_info || 'N/A';
        if (cardFacilities) cardFacilities.textContent = attraction.facilities || 'N/A';
        if (feedbackAttractionId) feedbackAttractionId.value = attraction.id || '';

        // Advisory Handling
        if (cardAdvisoryBanner && cardAdvisoryText) {
            if (attraction.advisory_message) {
                cardAdvisoryText.textContent = attraction.advisory_message;
                cardAdvisoryBanner.classList.remove('hidden');
                
                // Styling based on status
                cardAdvisoryBanner.className = 'mb-3 mt-1 p-2 rounded-lg text-xs font-bold border flex items-center gap-2 ';
                if (attraction.advisory_status === 'Danger') {
                    cardAdvisoryBanner.className += 'bg-red-50 border-red-200 text-red-700';
                } else if (attraction.advisory_status === 'Warning') {
                    cardAdvisoryBanner.className += 'bg-amber-50 border-amber-200 text-amber-700';
                } else {
                    cardAdvisoryBanner.className += 'bg-sky-50 border-sky-200 text-sky-700';
                }
            } else {
                cardAdvisoryBanner.classList.add('hidden');
            }
        }

        placeCard.classList.remove('hidden');
        placeCard.classList.remove('translate-y-full');
    }

    function updateEstablishmentCard(est) {
        if (!placeCard) return;

        currentDestination = {
            lat: est.lat || est.latitude,
            lng: est.lng || est.longitude
        };

        cardTitle.textContent = est.name;
        cardAddress.textContent = est.address || (est.barangay ? `${est.barangay}, Mangatarem` : 'Mangatarem, Pangasinan');
        cardDescription.textContent = est.description;

        // Show actual rating if available
        if (est.rating_avg > 0) {
            cardRating.textContent = est.rating_avg.toFixed(1);
        } else {
            cardRating.textContent = 'New';
        }

        // Update hours with contact number if available
        if (cardHours && est.contact_number) {
            cardHours.textContent = `📞 ${est.contact_number}`;
        }

        // Update distance if available
        if (cardDistance && est.distance) {
            cardDistance.textContent = `${est.distance} km away`;
        }

        placeCard.classList.remove('hidden');
        placeCard.classList.remove('translate-y-full');
    }

    const closeCardBtn = placeCard?.querySelector('button');
    if (closeCardBtn) {
        closeCardBtn.addEventListener('click', () => {
            placeCard.classList.add('hidden');
        });
    }

    // ========================================
    // 9. FLYTO ANIMATION
    // ========================================
    function flyToLocation(id, lat, lng) {
        // Validate coordinates
        if (!lat || !lng || isNaN(lat) || isNaN(lng)) {
            console.warn('Invalid coordinates for attraction:', id, { lat, lng });
            Swal.fire('Error', 'This location does not have valid coordinates.', 'error');
            return;
        }

        if (!isLeafletMode) {
            map.flyTo({
                center: [lng, lat],
                zoom: 16,
                duration: 1500
            });
        } else {
            map.flyTo([lat, lng], 16, {
                animate: true,
                duration: 1.5
            });
            
            // Add a temporary marker for Leaflet since MVT layers are missing
            if (window.activeMarker) map.removeLayer(window.activeMarker);
            window.activeMarker = L.marker([lat, lng]).addTo(map);
        }

        const attraction = attractionsData.find(a => a.id === id);

        setTimeout(() => {
            if (attraction) {
                updateCard(attraction);
            }
        }, 1600);
    }

    function flyToEstablishmentLocation(est) {
        if (!est.latitude || !est.longitude || isNaN(est.latitude) || isNaN(est.longitude)) {
            console.warn('Invalid coordinates for establishment:', est.id, { lat: est.latitude, lng: est.longitude });
            Swal.fire('Error', 'This location does not have valid coordinates.', 'error');
            return;
        }

        if (!isLeafletMode) {
            map.flyTo({
                center: [est.longitude, est.latitude],
                zoom: 16,
                duration: 1500
            });
        } else {
            map.flyTo([est.latitude, est.longitude], 16, {
                animate: true,
                duration: 1.5
            });
            
            if (window.activeMarker) map.removeLayer(window.activeMarker);
            window.activeMarker = L.marker([est.latitude, est.longitude]).addTo(map);
        }

        setTimeout(() => {
            updateEstablishmentCard(est);
        }, 1600);
    }

    function renderAttractions(attractions) {
        const listContainer = document.getElementById('places-content');

        if (attractions.length === 0) {
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">No attractions found.</div>';
            return;
        }

        // Deduplicate attractions by ID to prevent duplicates
        const seen = new Set();
        const uniqueAttractions = attractions.filter(attraction => {
            if (seen.has(attraction.id)) {
                return false;
            }
            seen.add(attraction.id);
            return true;
        });

        listContainer.innerHTML = '';

        uniqueAttractions.forEach(attraction => {
            const categoryConfig = iconConfig[attraction.category] || iconConfig.default;
            const categoryLabel = attraction.category.toUpperCase();

            const rating = attraction.rating || 4;
            const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
            const reviewCount = attraction.review_count || Math.floor(Math.random() * 50);

            const safeName = escapeHTML(attraction.name);
            const safeDescription = escapeHTML(attraction.description);
            const safeImage = attraction.image ? attraction.image.replace(/"/g, '&quot;') : PLACEHOLDER_IMG;

            const card = document.createElement('div');
            card.className = 'group bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32';
            card.innerHTML = `
                <div class="w-1/3 h-full bg-gray-200 relative flex-shrink-0">
                    <img src="${safeImage}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${safeName}" onerror="this.src='${PLACEHOLDER_IMG}'">
                    <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${categoryConfig.color}">${categoryLabel}</div>
                </div>
                <div class="w-2/3 p-3 flex flex-col justify-between bg-white" style="background-color: #ffffff !important;">
                    <div>
                        <h3 class="font-bold text-sm leading-tight mb-1 line-clamp-1" style="color: #111827 !important; -webkit-text-fill-color: #111827 !important;">${safeName}</h3>
                        <p class="text-xs line-clamp-2 mt-1" style="color: #374151 !important; -webkit-text-fill-color: #374151 !important;">${safeDescription}</p>
                    </div>
                    <div class="flex justify-between items-end mt-2">
                        <div class="text-xs font-bold" style="color: #f59e0b !important;">${stars} <span style="color: #9ca3af !important;">(${reviewCount})</span></div>
                        <button class="text-[10px] px-2 py-1 rounded transition font-semibold" style="background-color: #ecfdf5 !important; color: #047857 !important;">View on Map ➔</button>
                    </div>
                </div>
            `;

            card.addEventListener('click', () => {
                // Use latitude/longitude from API (not lat/lng)
                const lat = attraction.latitude || attraction.lat;
                const lng = attraction.longitude || attraction.lng;
                flyToLocation(attraction.id, lat, lng);
            });
            listContainer.appendChild(card);
        });
    }

    // ========================================
    // 10. FILTERING & SEARCH
    // ========================================
    const searchInput = document.getElementById('search-input');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const barangayFilter = document.getElementById('barangay-filter');

    let searchTimeout;
    function debounce(func, wait) {
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(searchTimeout);
                func(...args);
            };
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(later, wait);
        };
    }

    const debouncedFilterAttractions = debounce(() => {
        currentPage = 1;
        fetchAttractions(currentPage, true);
    }, 300);

    function filterAttractions() {
        currentSearchTerm = searchInput.value.toLowerCase();
        debouncedFilterAttractions();
    }

    searchInput.addEventListener('input', filterAttractions);

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Reset all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            
            // Set current as active
            btn.classList.add('active');

            currentCategory = btn.dataset.category;
            currentPage = 1;
            fetchAttractions(currentPage, true);
        });
    });

    if (barangayFilter) {
        barangayFilter.addEventListener('change', (e) => {
            currentBarangay = e.target.value;
            currentPage = 1;
            fetchAttractions(currentPage, true);
        });
    }

    // ========================================
    // 11. INFINITE SCROLL
    // ========================================
    const contentArea = document.getElementById('content-area');
    let scrollTimeout;

    contentArea.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const { scrollTop, scrollHeight, clientHeight } = contentArea;
            if (scrollTop + clientHeight >= scrollHeight - 100 && hasMorePages && !isLoading) {
                currentPage++;
                fetchAttractions(currentPage, false);
            }
        }, 200);
    });

    // ========================================
    // 12. ESTABLISHMENTS (NEARBY)
    // ========================================
    let establishmentsData = [];
    let currentEstType = null;
    let estPage = 1;
    let estTotalPages = 1;
    let estHasMore = true;
    let estUserLat = null;
    let estUserLng = null;
    let estMarkersSource = null;

    const estTypeConfig = {
        restaurant: { color: '#f97316', emoji: '🍽️', label: 'Restaurant' },
        cafe: { color: '#d97706', emoji: '☕', label: 'Café' },
        fastfood: { color: '#ef4444', emoji: '🍔', label: 'Fast Food' },
        inn: { color: '#3b82f6', emoji: '🏨', label: 'Inn' },
    };

    // Establishment filter buttons
    const estFilterBtns = document.querySelectorAll('.est-filter-btn');
    const estNearMeBtn = document.getElementById('est-near-me-btn');

    estFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const isActive = btn.classList.contains('active');

            // Toggle active state
            if (isActive) {
                btn.classList.remove('active');
                btn.style.backgroundColor = '';
                btn.style.borderColor = '';
                currentEstType = null;
            } else {
                // Clear other active states
                estFilterBtns.forEach(b => {
                    b.classList.remove('active');
                    b.style.backgroundColor = '';
                    b.style.borderColor = '';
                });

                // Set active
                const type = btn.dataset.estType;
                const cfg = estTypeConfig[type];
                btn.classList.add('active');
                btn.style.backgroundColor = cfg.color;
                btn.style.borderColor = cfg.color;

                currentEstType = type;
            }

            estPage = 1;
            fetchEstablishments(estPage, true);
        });
    });

    // Near Me button for establishments
    if (estNearMeBtn) {
        estNearMeBtn.addEventListener('click', () => {
            estNearMeBtn.classList.add('animate-pulse');

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        estNearMeBtn.classList.remove('animate-pulse');
                        estUserLat = position.coords.latitude;
                        estUserLng = position.coords.longitude;

                        // If no type selected, default to showing all
                        if (!currentEstType) {
                            // Activate first establishment filter (restaurant)
                            const firstBtn = estFilterBtns[0];
                            if (firstBtn) {
                                firstBtn.click();
                            }
                        } else {
                            estPage = 1;
                            fetchEstablishments(estPage, true);
                        }
                    },
                    (error) => {
                        estNearMeBtn.classList.remove('animate-pulse');
                        Swal.fire('Location Error', 'Unable to get your location. Please check your browser settings.', 'error');
                    },
                    { enableHighAccuracy: true, timeout: 10000 }
                );
            } else {
                estNearMeBtn.classList.remove('animate-pulse');
                Swal.fire('Not Supported', 'Geolocation is not supported by your browser.', 'error');
            }
        });
    }

    async function fetchEstablishments(page = 1, reset = false) {
        if (isLoading || !currentEstType) return;
        isLoading = true;

        if (reset) {
            const listContainer = document.getElementById('places-content');
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">Loading nearby establishments...</div>';

            // Clear existing establishment markers
            if (estMarkersSource && map.getSource(estMarkersSource)) {
                map.getSource(estMarkersSource).setData({ type: 'FeatureCollection', features: [] });
            }
        }

        try {
            const params = new URLSearchParams({
                page: page,
                per_page: 20,
                type: currentEstType,
            });

            if (estUserLat && estUserLng) {
                params.append('lat', estUserLat);
                params.append('lng', estUserLng);
                params.append('radius', 15);
            }

            const response = await fetch(`/business/api?${params}`);
            const result = await response.json();

            if (reset) {
                establishmentsData = result.establishments;
                estTotalPages = result.pagination.pages;
                estPage = result.pagination.page;
                estHasMore = result.pagination.has_next;

                renderEstablishments(establishmentsData);
                addEstablishmentMarkers(establishmentsData);
            } else {
                establishmentsData = [...establishmentsData, ...result.establishments];
                estTotalPages = result.pagination.pages;
                estPage = result.pagination.page;
                estHasMore = result.pagination.has_next;

                renderEstablishments(establishmentsData);
                addEstablishmentMarkers(establishmentsData);
            }
        } catch (error) {
            console.error('Error fetching establishments:', error);
        } finally {
            isLoading = false;
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
        }
    }

    function renderEstablishments(establishments) {
        const listContainer = document.getElementById('places-content');

        if (establishments.length === 0) {
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">No establishments found nearby. Try expanding your search or check back later.</div>';
            return;
        }

        // Deduplicate
        const seen = new Set();
        const uniqueEst = establishments.filter(est => {
            if (seen.has(est.id)) return false;
            seen.add(est.id);
            return true;
        });

        listContainer.innerHTML = '';

        uniqueEst.forEach(est => {
            const cfg = estTypeConfig[est.type] || { color: '#6b7280', emoji: '📍', label: est.type };
            const priceLabel = est.price_range ? { budget: '₱ Budget', moderate: '₱₱ Moderate', premium: '₱₱₱ Premium' }[est.price_range] : '';
            const distText = est.distance ? `${est.distance} km away` : '';

            const card = document.createElement('div');
            card.className = 'group bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32';
            card.innerHTML = `
                <div class="w-1/3 h-full bg-gray-200 relative flex-shrink-0">
                    <img src="${est.cover_image_url || PLACEHOLDER_IMG}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${est.name}" onerror="this.src='${PLACEHOLDER_IMG}'">
                    <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${cfg.color}">${cfg.emoji} ${cfg.label.toUpperCase()}</div>
                </div>
                <div class="w-2/3 p-3 flex flex-col justify-between bg-white" style="background-color: #ffffff !important;">
                    <div>
                        <h3 class="font-bold text-sm leading-tight mb-1 line-clamp-1" style="color: #111827 !important;">${est.name}</h3>
                        <p class="text-xs line-clamp-2 mt-1" style="color: #374151 !important;">${est.description}</p>
                    </div>
                    <div class="flex justify-between items-end mt-2">
                        <div class="text-[10px] font-bold" style="color: #6b7280 !important;">
                            ${est.rating_avg > 0 ? `★ ${est.rating_avg.toFixed(1)}` : ''} ${priceLabel ? '· ' + priceLabel : ''} ${distText ? '· ' + distText : ''}
                        </div>
                        <button class="text-[10px] px-2 py-1 rounded transition font-semibold" style="background-color: #ecfdf5 !important; color: #047857 !important;">View on Map ➔</button>
                    </div>
                </div>
            `;

            card.addEventListener('click', () => {
                flyToEstablishmentLocation(est);
            });
            listContainer.appendChild(card);
        });
    }

    let establishmentMarkersLayer = null;

    function addEstablishmentMarkers(establishments) {
        if (isLeafletMode) {
            if (establishmentMarkersLayer) map.removeLayer(establishmentMarkersLayer);
            establishmentMarkersLayer = L.layerGroup().addTo(map);
            
            establishments.forEach(est => {
                const cfg = estTypeConfig[est.type] || estTypeConfig.restaurant;
                const marker = L.circleMarker([est.latitude, est.longitude], {
                    radius: 8,
                    fillColor: cfg.color,
                    color: "#fff",
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.9
                }).addTo(establishmentMarkersLayer);
                
                marker.bindPopup(`<strong>${est.name}</strong><br>${est.type}`);
                marker.on('click', () => updateEstablishmentCard(est));
            });
            return;
        }
        // Use GeoJSON source for establishment markers
        const sourceId = 'establishments-geojson';

        if (!map.getSource(sourceId)) {
            map.addSource(sourceId, {
                type: 'geojson',
                data: { type: 'FeatureCollection', features: [] }
            });

            // Circle layer
            map.addLayer({
                id: 'est-circles',
                type: 'circle',
                source: sourceId,
                paint: {
                    'circle-radius': [
                        'interpolate', ['linear'], ['zoom'],
                        10, 5,
                        14, 10,
                        16, 14
                    ],
                    'circle-color': ['get', 'color'],
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff',
                    'circle-opacity': 0.9
                }
            }, 'mvt-labels');

            // Label layer
            map.addLayer({
                id: 'est-labels',
                type: 'symbol',
                source: sourceId,
                layout: {
                    'text-field': ['get', 'name'],
                    'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Regular'],
                    'text-size': 10,
                    'text-offset': [0, 1.5],
                    'text-anchor': 'top',
                    'text-allow-overlap': false
                },
                paint: {
                    'text-color': '#333333',
                    'text-halo-color': '#ffffff',
                    'text-halo-width': 1.5
                }
            }, 'mvt-labels');

            // Click handler for establishment markers
            map.on('click', 'est-circles', (e) => {
                const feature = e.features[0];
                if (!feature) return;

                const props = feature.properties;
                map.flyTo({
                    center: feature.geometry.coordinates,
                    zoom: 16,
                    duration: 1500
                });

                setTimeout(() => {
                    updateEstablishmentCard({
                        id: props.id,
                        name: props.name,
                        type: props.type,
                        barangay: props.barangay,
                        description: props.description,
                        cover_image_url: props.cover_image_url,
                        lat: feature.geometry.coordinates[1],
                        lng: feature.geometry.coordinates[0],
                        rating_avg: props.rating_avg,
                        price_range: props.price_range,
                        address: props.address,
                        contact_number: props.contact_number
                    });
                }, 1600);
            });

            map.on('mouseenter', 'est-circles', () => {
                map.getCanvas().style.cursor = 'pointer';
            });

            map.on('mouseleave', 'est-circles', () => {
                map.getCanvas().style.cursor = '';
            });
        }

        // Build GeoJSON features
        const features = establishments.map(est => ({
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [est.longitude, est.latitude]
            },
            properties: {
                id: est.id,
                name: est.name,
                type: est.type,
                color: (estTypeConfig[est.type] || estTypeConfig.restaurant).color,
                description: est.description,
                barangay: est.barangay,
                cover_image_url: est.cover_image_url,
                distance: est.distance,
                rating_avg: est.rating_avg,
                price_range: est.price_range,
                address: est.address,
                contact_number: est.contact_number
            }
        }));

        map.getSource(sourceId).setData({
            type: 'FeatureCollection',
            features: features
        });
    }

    // Override infinite scroll to handle establishments
    contentArea.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const { scrollTop, scrollHeight, clientHeight } = contentArea;
            if (scrollTop + clientHeight >= scrollHeight - 100 && !isLoading) {
                if (currentEstType && estHasMore) {
                    estPage++;
                    fetchEstablishments(estPage, false);
                } else if (hasMorePages) {
                    currentPage++;
                    fetchAttractions(currentPage, false);
                }
            }
        }, 200);
    });

    // ========================================
    // 13. GEOLOCATION "NEAR ME" & REAL-TIME ENGINE
    // ========================================
    const locateBtn = document.getElementById('locate-me');
    let userLocationRadius = null;

    // Link custom button to Mapbox Geolocate engine
    locateBtn.addEventListener('click', () => {
        if (!isLeafletMode) {
            // Toggle tracking
            geolocate.trigger();
        } else {
            map.locate({ setView: true, maxZoom: 16 });
        }
        locateBtn.classList.add('animate-pulse');
    });

    // Smart Find Nearest Logic
    window.findNearest = async function(category, type = 'establishment') {
        if (!navigator.geolocation) {
            Swal.fire('Not Supported', 'Geolocation is not supported by your browser.', 'error');
            return;
        }

        // Show loading state
        const listContainer = document.getElementById('places-content');
        listContainer.innerHTML = `<div class="text-center text-gray-500 py-4">Finding nearest ${category}...</div>`;
        
        navigator.geolocation.getCurrentPosition(async (position) => {
            const { latitude, longitude } = position.coords;
            estUserLat = latitude;
            estUserLng = longitude;

            try {
                const endpoint = type === 'establishment' ? '/business/api' : '/attractions/api';
                const params = new URLSearchParams({
                    lat: latitude,
                    lng: longitude,
                    radius: 20, // 20km radius
                    per_page: 5
                });
                
                if (type === 'establishment') {
                    params.append('type', category);
                } else {
                    params.append('category', category);
                }

                const response = await fetch(`${endpoint}?${params}`);
                const result = await response.json();
                const items = type === 'establishment' ? result.establishments : result.attractions;

                if (items.length === 0) {
                    listContainer.innerHTML = `<div class="text-center text-gray-500 py-4">No ${category} found within 20km.</div>`;
                    return;
                }

                // Render and Focus
                if (type === 'establishment') {
                    renderEstablishments(items);
                    addEstablishmentMarkers(items);
                    flyToEstablishmentLocation(items[0]);
                } else {
                    renderAttractions(items);
                    flyToLocation(items[0].id, items[0].latitude, items[0].longitude);
                }

            } catch (error) {
                console.error('Error finding nearest:', error);
                Swal.fire('Error', 'Error finding nearest locations.', 'error');
            }
        }, (error) => {
            Swal.fire('Location Error', 'Unable to get your location.', 'error');
        });
    };

    if (!isLeafletMode) {
        geolocate.on('geolocate', (position) => {
            locateBtn.classList.remove('animate-pulse');
            locateBtn.classList.add('bg-green-100'); // Indicate tracking is active

            const { latitude, longitude, heading } = position.coords;

            // Handle custom car marker for navigation
            if (isNavigating) {
                // Hide default dot
                const defaultDot = document.querySelector('.mapboxgl-user-location-dot');
                if (defaultDot) defaultDot.style.display = 'none';

                if (!customUserMarker) {
                    const el = document.createElement('div');
                    el.className = 'custom-user-car-marker';
                    el.style.width = '40px';
                    el.style.height = '40px';
                    el.style.backgroundImage = 'url("/static/img/car-icon.png")';
                    el.style.backgroundSize = 'contain';
                    el.style.backgroundRepeat = 'no-repeat';
                    el.style.backgroundPosition = 'center';
                    el.style.transition = 'transform 0.5s ease';
                    
                    customUserMarker = new mapboxgl.Marker({ element: el, rotationAlignment: 'map' })
                        .setLngLat([longitude, latitude])
                        .addTo(map);
                } else {
                    customUserMarker.setLngLat([longitude, latitude]);
                }
                
                // Rotate based on heading if available
                if (heading !== null && !isNaN(heading)) {
                    customUserMarker.setRotation(heading);
                }
            } else {
                // Not navigating, remove car marker if exists
                if (customUserMarker) {
                    customUserMarker.remove();
                    customUserMarker = null;
                }
                // Show default dot
                const defaultDot = document.querySelector('.mapboxgl-user-location-dot');
                if (defaultDot) defaultDot.style.display = 'block';
            }

            // Store for establishment searches
            estUserLat = latitude;
            estUserLng = longitude;

            // Update "Near Me" filters dynamically if currently viewing establishments
            if (currentEstType) {
                estPage = 1;
                fetchEstablishments(estPage, true);
            }

            // Custom radius visual (Optional: Enhanced for GoMangatarem "Search Area")
            const radiusMeters = 5000;
            const radiusSourceId = 'user-radius';

            if (!map.getSource(radiusSourceId)) {
                map.addSource(radiusSourceId, {
                    type: 'geojson',
                    data: {
                        type: 'Feature',
                        geometry: {
                            type: 'Polygon',
                            coordinates: [generateCircleCoordinates(longitude, latitude, radiusMeters)]
                        }
                    }
                });

                map.addLayer({
                    id: 'user-radius-fill',
                    type: 'fill',
                    source: radiusSourceId,
                    paint: {
                        'fill-color': '#3b82f6',
                        'fill-opacity': 0.05
                    }
                });

                map.addLayer({
                    id: 'user-radius-line',
                    type: 'line',
                    source: radiusSourceId,
                    paint: {
                        'line-color': '#3b82f6',
                        'line-width': 1,
                        'line-dasharray': [4, 4],
                        'line-opacity': 0.3
                    }
                });
            } else {
                map.getSource(radiusSourceId).setData({
                    type: 'Feature',
                    geometry: {
                        type: 'Polygon',
                        coordinates: [generateCircleCoordinates(longitude, latitude, radiusMeters)]
                    }
                });
            }
        });

        geolocate.on('error', (error) => {
            locateBtn.classList.remove('animate-pulse');
            Swal.fire('Location Access', 'Location access denied or unavailable. Please enable GPS.', 'warning');
            console.error('Geolocation error:', error);
        });

        geolocate.on('trackuserlocationstart', () => {
            console.log('Real-time tracking started');
            locateBtn.title = "Tracking Mode: ON (Click to re-center)";
            locateBtn.classList.add('tracking-active');
        });

        geolocate.on('trackuserlocationend', () => {
            console.log('Real-time tracking paused/ended');
            locateBtn.classList.remove('bg-green-100', 'tracking-active');
            locateBtn.title = "Find my location";
        });
    } else {
        map.on('locationfound', (e) => {
            locateBtn.classList.remove('animate-pulse');
            locateBtn.classList.add('bg-green-100');
            estUserLat = e.latlng.lat;
            estUserLng = e.latlng.lng;
            if (currentEstType) fetchEstablishments(1, true);
        });
        
        map.on('locationerror', () => {
            locateBtn.classList.remove('animate-pulse');
            Swal.fire('Location Access', 'Enable GPS to find nearest spots.', 'warning');
        });
    }

    // ========================================
    // 13.5 REAL-TIME ROUTING LOGIC
    // ========================================
    const startRouteBtn = document.getElementById('start-route-btn');
    if (startRouteBtn) {
        startRouteBtn.addEventListener('click', () => {
            if (!currentDestination) {
                if (typeof Swal !== 'undefined') Swal.fire('Error', 'Please select a destination first.', 'error');
                return;
            }
            if (!navigator.geolocation) {
                if (typeof Swal !== 'undefined') Swal.fire('Not Supported', 'Geolocation is not supported by your browser.', 'error');
                return;
            }
            
            const btnText = startRouteBtn.querySelector('span');
            if (isNavigating) {
                // Stop navigation
                isNavigating = false;
                if (btnText) btnText.textContent = 'Start Route';
                startRouteBtn.classList.remove('bg-red-600', 'hover:bg-red-700', 'text-white');
                
                // Clear route
                if (map.getSource('real-time-route')) {
                    map.removeLayer('real-time-route');
                    map.removeSource('real-time-route');
                }
                
                if (customUserMarker) {
                    customUserMarker.remove();
                    customUserMarker = null;
                }
                const defaultDot = document.querySelector('.mapboxgl-user-location-dot');
                if (defaultDot) defaultDot.style.display = 'block';
                return;
            }
            
            // Get user location to start route
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    isNavigating = true;
                    
                    if (btnText) btnText.textContent = 'Stop Navigation';
                    startRouteBtn.classList.add('bg-red-600', 'hover:bg-red-700', 'text-white');
                    
                    if (!isLeafletMode && typeof geolocate !== 'undefined') {
                        geolocate.trigger(); // Ensure tracking is active
                    }
                    
                    drawRealTimeRoute(latitude, longitude, currentDestination.lat, currentDestination.lng);
                    
                    // Hide place card after starting route
                    if (placeCard) placeCard.classList.add('hidden');
                },
                (error) => {
                    if (typeof Swal !== 'undefined') Swal.fire('Location Error', 'Unable to get your location for routing.', 'error');
                },
                { enableHighAccuracy: true, timeout: 10000 }
            );
        });
    }

    async function drawRealTimeRoute(startLat, startLng, destLat, destLng) {
        if (isLeafletMode) return;
        
        try {
            const query = await fetch(
                `https://api.mapbox.com/directions/v5/mapbox/driving/${startLng},${startLat};${destLng},${destLat}?geometries=geojson&access_token=${mapboxgl.accessToken}`
            );
            const json = await query.json();
            if (!json.routes || json.routes.length === 0) return;
            
            const data = json.routes[0];
            const route = data.geometry.coordinates;
            const geojson = {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: route
                }
            };
            
            if (map.getSource('real-time-route')) {
                map.getSource('real-time-route').setData(geojson);
            } else {
                map.addSource('real-time-route', {
                    type: 'geojson',
                    data: geojson
                });
                map.addLayer({
                    id: 'real-time-route',
                    type: 'line',
                    source: 'real-time-route',
                    layout: {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    paint: {
                        'line-color': '#3b82f6',
                        'line-width': 6,
                        'line-opacity': 0.8
                    }
                });
            }
            
            // Fit bounds to route
            const bounds = route.reduce((bounds, coord) => {
                return bounds.extend(coord);
            }, new mapboxgl.LngLatBounds(route[0], route[0]));
            
            map.fitBounds(bounds, { padding: 60 });
        } catch (error) {
            console.error('Error fetching directions', error);
        }
    }

    // ========================================
    // 13. ROUTES TOGGLE
    // ========================================
    const routesToggle = document.getElementById('routes-toggle');
    if (routesToggle) {
        routesToggle.addEventListener('click', () => switchTab('routes'));
    }

    // ========================================
    // 14. MOBILE BOTTOM SHEET
    // ========================================
    const sidebar = document.getElementById('attractions-sidebar');
    const dragHandle = document.getElementById('drag-handle');
    // contentArea is already declared at line 860

    if (sidebar && dragHandle) {
        let isDragging = false;
        let startY = 0;
        let initialTranslateY = 0;
        
        // Define Snap Points (as % of viewport height)
        const SNAP_POINTS = {
            FULL: 0,      // Top
            HALF: 50,     // Middle
            PEEK: 88      // Bottom (only header visible)
        };

        const getTransformY = () => {
            const style = window.getComputedStyle(sidebar);
            const transform = style.transform;
            if (!transform || transform === 'none') return 0;
            
            try {
                const matrix = transform.includes('matrix3d') 
                    ? new DOMMatrix(transform) 
                    : new DOMMatrix(transform);
                return matrix.m42;
            } catch (e) {
                // Fallback: manually parse translateY(X%) or translateY(Xpx)
                const match = transform.match(/translateY\(([-\d.]+)%\)/);
                if (match) {
                    return (parseFloat(match[1]) / 100) * window.innerHeight;
                }
                return 0;
            }
        };

        const setPosition = (percentage) => {
            sidebar.style.transform = `translateY(${percentage}%)`;
            sidebar.dataset.currentPos = percentage;
        };

        // Initialize at Peek
        if (window.innerWidth < 768) {
            setPosition(SNAP_POINTS.PEEK);
        }

        dragHandle.addEventListener('touchstart', (e) => {
            if (sidebar.classList.contains('layout-popup')) return;
            isDragging = true;
            startY = e.touches[0].clientY;
            initialTranslateY = getTransformY();
            sidebar.classList.add('is-dragging');
            sidebar.style.transition = 'none';
        }, { passive: false });

        document.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            
            const currentY = e.touches[0].clientY;
            const deltaY = currentY - startY;
            const height = window.innerHeight;
            const newY = initialTranslateY + deltaY;
            const percentage = (newY / height) * 100;
            
            // Clamp between Full and bit past Peek
            const clamped = Math.max(0, Math.min(percentage, 95));
            sidebar.style.transform = `translateY(${clamped}%)`;
        }, { passive: false });

        document.addEventListener('touchend', () => {
            if (!isDragging) return;
            isDragging = false;
            sidebar.classList.remove('is-dragging');
            
            const currentY = getTransformY();
            const height = window.innerHeight;
            const percentage = (currentY / height) * 100;

            // Snap to closest point with better thresholds
            let closest = SNAP_POINTS.PEEK;
            if (percentage < 30) {
                closest = SNAP_POINTS.FULL;
            } else if (percentage < 70) {
                closest = SNAP_POINTS.HALF;
            } else {
                closest = SNAP_POINTS.PEEK;
            }
            
            sidebar.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.1)'; // Slight bounce
            setPosition(closest);
            
            if (contentArea) {
                contentArea.style.overflowY = (closest === SNAP_POINTS.FULL) ? 'auto' : 'hidden';
            }
        });
        
        window.minimizeFilters = () => {
            if (window.innerWidth < 768 && !sidebar.classList.contains('layout-popup')) {
                sidebar.style.transition = 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                setPosition(SNAP_POINTS.PEEK);
            }
        };

        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                sidebar.style.transform = '';
                sidebar.style.transition = '';
                if (contentArea) contentArea.style.overflowY = '';
            }
        });
    }

    // ========================================
    // 15. ROUTE OPTIMIZATION ENGINE
    // ========================================
    let routeWaypoints = [];
    let optimizedRouteData = null;
    let selectedProfile = 'driving-car';
    let routeLayerId = null;
    let routeSourceId = null;
    let waypointMarkers = [];

    // DOM Elements
    const optimizeBtn = document.getElementById('optimize-route-btn');
    const clearRouteBtn = document.getElementById('clear-route-btn');
    const waypointListEl = document.getElementById('waypoint-list');
    const emptyWaypointMsg = document.getElementById('empty-waypoint-msg');
    const waypointCountEl = document.getElementById('waypoint-count');
    const routeSummaryEl = document.getElementById('route-summary');
    const routeItineraryEl = document.getElementById('route-itinerary');
    const profileBtns = document.querySelectorAll('.route-profile-btn');
    
    // Add to Route button in place card
    const addToRouteBtn = document.getElementById('add-to-route-btn');
    if (addToRouteBtn) {
        addToRouteBtn.addEventListener('click', () => {
            if (!currentDestination) return;
            
            // Check if already in route
            if (routeWaypoints.find(w => w.id === currentDestination.id)) {
                if (typeof Swal !== 'undefined') Swal.fire('Already Added', 'This place is already in your itinerary.', 'info');
                return;
            }
            
            // Add waypoint
            routeWaypoints.push({
                id: currentDestination.id,
                name: document.getElementById('card-title').textContent,
                lat: currentDestination.lat,
                lng: currentDestination.lng
            });
            
            updateWaypointUI();
            
            // Show routes tab
            switchTab('routes');
        });
    }

    // Profile selection
    profileBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            profileBtns.forEach(b => {
                b.classList.remove('bg-emerald-100', 'text-emerald-800', 'border-emerald-500');
                b.classList.add('bg-white', 'text-gray-600', 'border-gray-100');
            });
            btn.classList.remove('bg-white', 'text-gray-600', 'border-gray-100');
            btn.classList.add('bg-emerald-100', 'text-emerald-800', 'border-emerald-500');
            selectedProfile = btn.dataset.profile;
        });
    });

    function updateWaypointUI() {
        if (!waypointCountEl) return;
        waypointCountEl.textContent = `${routeWaypoints.length} stops`;
        
        if (routeWaypoints.length === 0) {
            waypointListEl.innerHTML = '';
            waypointListEl.appendChild(emptyWaypointMsg);
            emptyWaypointMsg.classList.remove('hidden');
            optimizeBtn.disabled = true;
            return;
        }
        
        emptyWaypointMsg.classList.add('hidden');
        waypointListEl.innerHTML = '';
        
        routeWaypoints.forEach((wp, index) => {
            const el = document.createElement('div');
            el.className = 'flex items-center justify-between p-2 bg-white border border-gray-200 rounded-lg shadow-sm';
            el.innerHTML = `
                <div class="flex items-center gap-2 overflow-hidden">
                    <span class="flex-shrink-0 w-6 h-6 rounded-full bg-gray-100 text-gray-600 flex items-center justify-center text-xs font-bold border border-gray-300">${index + 1}</span>
                    <span class="text-sm font-bold text-gray-800 truncate">${wp.name}</span>
                </div>
                <button class="remove-waypoint-btn text-gray-400 hover:text-red-500 transition-colors p-1" data-index="${index}">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            `;
            waypointListEl.appendChild(el);
        });
        
        // Add remove listeners
        document.querySelectorAll('.remove-waypoint-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = parseInt(e.currentTarget.dataset.index);
                routeWaypoints.splice(idx, 1);
                updateWaypointUI();
            });
        });
        
        optimizeBtn.disabled = routeWaypoints.length < 2;
    }

    if (optimizeBtn) {
        optimizeBtn.addEventListener('click', async () => {
            if (routeWaypoints.length < 2) return;
            
            optimizeBtn.disabled = true;
            optimizeBtn.innerHTML = '<svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Optimizing...';
            
            try {
                // Determine start coords (using first waypoint for now, or geolocation if available)
                let startCoords = { lng: routeWaypoints[0].lng, lat: routeWaypoints[0].lat };
                
                // Get current location if possible, otherwise just use first waypoint
                if (navigator.geolocation) {
                    try {
                        const pos = await new Promise((resolve, reject) => {
                            navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 3000 });
                        });
                        startCoords = { lng: pos.coords.longitude, lat: pos.coords.latitude };
                    } catch (e) {
                        console.log("Could not get GPS for start, using first waypoint.");
                    }
                }

                const response = await fetch('/api/v1/routing/optimize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        attraction_ids: routeWaypoints.map(w => w.id),
                        start: startCoords,
                        profile: selectedProfile,
                        round_trip: true
                    })
                });
                
                const result = await response.json();
                
                if (!result.success) {
                    throw new Error(result.error || 'Optimization failed');
                }
                
                optimizedRouteData = result;
                renderOptimizedRoute(result);
                
                clearRouteBtn.classList.remove('hidden');
                
            } catch (error) {
                console.error(error);
                if (typeof Swal !== 'undefined') Swal.fire('Routing Error', error.message, 'error');
            } finally {
                optimizeBtn.disabled = false;
                optimizeBtn.innerHTML = '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> Optimize Route';
            }
        });
    }
    
    if (clearRouteBtn) {
        clearRouteBtn.addEventListener('click', () => window.clearRoutes());
    }

    function renderOptimizedRoute(data) {
        if (isLeafletMode) return; // Basic support or separate implementation for Leaflet
        
        window.clearRoutes();
        
        const sourceId = `route-opt-source-${Date.now()}`;
        const layerId = `route-opt-layer-${Date.now()}`;
        
        // Add Route Line
        if (data.geometry) {
            map.addSource(sourceId, {
                type: 'geojson',
                data: data.geometry
            });
            
            map.addLayer({
                id: layerId,
                type: 'line',
                source: sourceId,
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                paint: {
                    'line-color': '#10b981',
                    'line-width': 5,
                    'line-opacity': 0.8,
                    'line-dasharray': [2, 2]
                }
            });
            
            routeLayerId = layerId;
            routeSourceId = sourceId;
            
            // Fit bounds
            const bounds = data.geometry.coordinates.reduce((b, coord) => {
                return b.extend(coord);
            }, new mapboxgl.LngLatBounds(data.geometry.coordinates[0], data.geometry.coordinates[0]));
            
            map.fitBounds(bounds, { padding: 50 });
        }
        
        // Add numbered markers
        data.optimized_order.forEach((stop, index) => {
            const el = document.createElement('div');
            el.className = 'w-8 h-8 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center border-2 border-white shadow-lg z-10';
            el.textContent = index + 1;
            
            const marker = new mapboxgl.Marker({ element: el })
                .setLngLat([stop.longitude, stop.latitude])
                .addTo(map);
                
            waypointMarkers.push(marker);
        });
        
        // Update UI
        document.getElementById('route-distance').textContent = data.summary.distance_km;
        document.getElementById('route-duration').textContent = data.summary.duration_minutes;
        document.getElementById('route-stops').textContent = data.summary.stops;
        routeSummaryEl.classList.remove('hidden');
        
        // Build Itinerary
        routeItineraryEl.innerHTML = '<h4 class="text-xs font-bold text-gray-500 uppercase mt-4 mb-2 px-1">Itinerary Details</h4>';
        data.optimized_order.forEach((stop, index) => {
            const div = document.createElement('div');
            div.className = 'flex gap-3 bg-white p-3 rounded-xl border border-gray-100 shadow-sm';
            div.innerHTML = `
                <div class="flex flex-col items-center">
                    <div class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs font-bold">${index + 1}</div>
                    ${index < data.optimized_order.length - 1 ? '<div class="w-0.5 h-full bg-gray-200 my-1"></div>' : ''}
                </div>
                <div class="flex-1 pb-2">
                    <div class="font-bold text-sm text-gray-900">${stop.name}</div>
                    <div class="text-xs text-gray-500 flex justify-between mt-1">
                        <span>Arrival: +${stop.arrival_minutes} min</span>
                    </div>
                </div>
            `;
            routeItineraryEl.appendChild(div);
        });
        routeItineraryEl.classList.remove('hidden');
    }

    window.clearRoutes = function () {
        if (routeLayerId && map.getLayer(routeLayerId)) {
            map.removeLayer(routeLayerId);
        }
        if (routeSourceId && map.getSource(routeSourceId)) {
            map.removeSource(routeSourceId);
        }
        
        waypointMarkers.forEach(m => m.remove());
        waypointMarkers = [];
        
        routeLayerId = null;
        routeSourceId = null;
        optimizedRouteData = null;
        
        if (routeSummaryEl) routeSummaryEl.classList.add('hidden');
        if (routeItineraryEl) routeItineraryEl.classList.add('hidden');
        if (clearRouteBtn) clearRouteBtn.classList.add('hidden');
        
        // Reset view
        map.flyTo({
            center: [120.2986, 15.7889],
            zoom: 13,
            duration: 1500
        });
    };

    // Load Suggested Routes
    async function loadSuggestedRoutes() {
        try {
            const res = await fetch('/api/v1/routing/suggested');
            const data = await res.json();
            if (data.success && data.routes) {
                const list = document.getElementById('suggested-routes-list');
                if (!list) return;
                
                list.innerHTML = '';
                data.routes.forEach(route => {
                    const el = document.createElement('div');
                    el.className = 'p-4 bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md cursor-pointer transition-all';
                    el.innerHTML = `
                        <div class="flex items-start gap-3">
                            <div class="text-2xl">${route.icon}</div>
                            <div>
                                <h5 class="font-bold text-gray-900 text-sm">${route.name}</h5>
                                <p class="text-xs text-gray-500 mt-1">${route.description}</p>
                                <div class="flex gap-2 mt-2">
                                    <span class="text-[10px] font-bold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">${route.estimated_duration_min} min</span>
                                    <span class="text-[10px] font-bold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">${route.estimated_distance_km} km</span>
                                </div>
                            </div>
                        </div>
                    `;
                    el.addEventListener('click', () => {
                        if (route.attractions && route.attractions.length > 0) {
                            routeWaypoints = route.attractions.map(a => ({
                                id: a.id,
                                name: a.name,
                                lat: a.latitude,
                                lng: a.longitude
                            }));
                            selectedProfile = route.profile;
                            
                            // Update profile buttons
                            profileBtns.forEach(b => {
                                if (b.dataset.profile === selectedProfile) {
                                    b.classList.remove('bg-white', 'text-gray-600', 'border-gray-100');
                                    b.classList.add('bg-emerald-100', 'text-emerald-800', 'border-emerald-500');
                                } else {
                                    b.classList.remove('bg-emerald-100', 'text-emerald-800', 'border-emerald-500');
                                    b.classList.add('bg-white', 'text-gray-600', 'border-gray-100');
                                }
                            });
                            
                            updateWaypointUI();
                            optimizeBtn.click();
                        }
                    });
                    list.appendChild(el);
                });
            }
        } catch (e) {
            console.error("Failed to load suggested routes:", e);
        }
    }
    
    // Call on load
    loadSuggestedRoutes();

    // ========================================
    // 16. OFFLINE MAP DOWNLOAD LOGIC
    // ========================================
    const offlineDownloadBtn = document.getElementById('offline-download-btn');
    const downloadCard = document.getElementById('download-card');
    const downloadProgressBar = document.getElementById('download-progress-bar');
    const downloadStatus = document.getElementById('download-status');
    const downloadPercentage = document.getElementById('download-percentage');
    const cancelDownloadBtn = document.getElementById('cancel-download-btn');

    // Mangatarem Bounding Box
    const MANGATAREM_BBOX = [120.14, 15.71, 120.37, 15.86];

    function lng2tile(lon, zoom) {
        return Math.floor((lon + 180) / 360 * Math.pow(2, zoom));
    }

    function lat2tile(lat, zoom) {
        return Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom));
    }

    function calculateTileUrls(bbox, minZoom, maxZoom) {
        const urls = [];
        const accessToken = mapboxgl.accessToken;
        const styleId = 'streets-v12'; // Default style for offline

        for (let z = minZoom; z <= maxZoom; z++) {
            const minX = lng2tile(bbox[0], z);
            const maxX = lng2tile(bbox[2], z);
            const minY = lat2tile(bbox[3], z);
            const maxY = lat2tile(bbox[1], z);

            for (let x = minX; x <= maxX; x++) {
                for (let y = minY; y <= maxY; y++) {
                    // Vector Tiles
                    urls.push(`https://api.mapbox.com/v4/mapbox.mapbox-streets-v8/${z}/${x}/${y}.vector.pbf?access_token=${accessToken}`);
                    // Glyph/Font assets (subset)
                    if (urls.length % 50 === 0) {
                        urls.push(`https://api.mapbox.com/fonts/v1/mapbox/DIN%20Offc%20Pro%20Medium,Arial%20Unicode%20MS%20Bold/0-255.pbf?access_token=${accessToken}`);
                    }
                }
            }
        }
        return urls;
    }

    if (offlineDownloadBtn) {
        offlineDownloadBtn.addEventListener('click', () => {
            downloadCard.classList.remove('hidden');
            downloadStatus.textContent = 'Calculating tiles...';

            const tileUrls = calculateTileUrls(MANGATAREM_BBOX, 13, 16);
            const totalTiles = tileUrls.length;
            let downloadedCount = 0;

            downloadStatus.textContent = `Downloading ${totalTiles} tiles...`;

            if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
                navigator.serviceWorker.controller.postMessage({
                    type: 'PREFETCH_TILES',
                    urls: tileUrls
                });

                // Listen for progress
                const progressHandler = (event) => {
                    if (event.data && event.data.type === 'TILES_PROGRESS') {
                        downloadedCount++;
                        const percent = Math.round((downloadedCount / totalTiles) * 100);
                        downloadProgressBar.style.width = `${percent}%`;
                        downloadPercentage.textContent = `${percent}%`;

                        if (downloadedCount >= totalTiles) {
                            downloadStatus.textContent = 'Download Complete!';
                            navigator.serviceWorker.removeEventListener('message', progressHandler);
                            setTimeout(() => {
                                downloadCard.classList.add('hidden');
                            }, 2000);
                        }
                    }
                };

                navigator.serviceWorker.addEventListener('message', progressHandler);
            } else {
                downloadStatus.textContent = 'Service Worker not ready.';
            }
        });
    }

    if (cancelDownloadBtn) {
        cancelDownloadBtn.addEventListener('click', () => {
            downloadCard.classList.add('hidden');
        });
    }

    // ========================================
    // HELPER: Generate circle coordinates for GeoJSON polygon
    // ========================================
    function generateCircleCoordinates(centerLng, centerLat, radiusMeters, steps = 64) {
        const coordinates = [];
        const earthRadius = 6378137; // meters
        const distanceKm = radiusMeters / 1000;
        const radiusRad = distanceKm / (earthRadius / 1000);

        for (let i = 0; i < steps; i++) {
            const angle = (i * 2 * Math.PI) / steps;
            const lat2 = Math.asin(
                Math.sin(centerLat * Math.PI / 180) * Math.cos(radiusRad) +
                Math.cos(centerLat * Math.PI / 180) * Math.sin(radiusRad) * Math.cos(angle)
            );
            const lng2 = centerLng * Math.PI / 180 + Math.atan2(
                Math.sin(angle) * Math.sin(radiusRad) * Math.cos(centerLat * Math.PI / 180),
                Math.cos(radiusRad) - Math.sin(centerLat * Math.PI / 180) * Math.sin(lat2)
            );

            coordinates.push([lng2 * 180 / Math.PI, lat2 * 180 / Math.PI]);
        }

        // Close the polygon
        coordinates.push(coordinates[0]);
        return coordinates;
    }

    // ========================================
    // 17. LAYOUT MANAGEMENT
    // ========================================
    function initLayoutSystem() {
        const toggles = document.querySelectorAll('.layout-toggle-btn');
        const sidebar = document.getElementById('attractions-sidebar');
        const closeSidebarBtn = document.getElementById('close-sidebar');
        
        if (toggles.length === 0 || !sidebar) return;
        
        const updateToggleButtons = (isPopup) => {
            toggles.forEach(btn => {
                const isHeaderBtn = btn.parentElement.classList.contains('flex-items-center'); // Simplified check
                const iconSize = "w-5 h-5"; 
                
                if (isPopup) {
                    btn.title = "Switch to Sidebar/Swipe Layout";
                    btn.innerHTML = `
                        <svg class="${iconSize} text-emerald-600 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path>
                        </svg>
                    `;
                } else {
                    btn.title = "Switch to Floating Popup Layout";
                    btn.innerHTML = `
                        <svg class="${iconSize} text-emerald-600 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path>
                        </svg>
                    `;
                }
            });
        };

        // Load preference
        const savedLayout = localStorage.getItem('map_layout') || 'sidebar';
        if (savedLayout === 'popup') {
            sidebar.classList.add('layout-popup');
            updateToggleButtons(true);
        } else {
            updateToggleButtons(false);
        }
        
        // Handle Close Button
        if (closeSidebarBtn) {
            closeSidebarBtn.addEventListener('click', () => {
                sidebar.classList.add('is-hidden');
                setTimeout(() => map.resize(), 600);
            });
        }
        
        toggles.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();

                // If sidebar is hidden, show it first
                if (sidebar.classList.contains('is-hidden')) {
                    sidebar.classList.remove('is-hidden');
                } else {
                    // Otherwise toggle the layout mode
                    const isPopup = sidebar.classList.toggle('layout-popup');
                    localStorage.setItem('map_layout', isPopup ? 'popup' : 'sidebar');
                    updateToggleButtons(isPopup);

                    // If switching back to Swipe mode on mobile, force Peek state
                    if (!isPopup && window.innerWidth < 768) {
                        if (typeof setPosition === 'function') {
                            setPosition(88); // SNAP_POINTS.PEEK
                        } else {
                            sidebar.style.transform = 'translateY(88%)';
                        }
                    }
                }
                
                setTimeout(() => {
                    map.resize();
                }, 600);
            });
        });
    }

    initLayoutSystem();

    // ========================================
    // SENIOR-FRIENDLY "GABAY MODE" CONTROLLER
    // ========================================
    let easyModeActive = false;
    let easyModeLanguage = 'tl'; // 'tl' or 'en'
    let easyModeCategory = null;
    let easyModeIndex = 0;
    let easyModeFilteredSpots = [];
    let speechUtterance = null;

    const easyOverlay = document.getElementById('easy-mode-overlay');
    const easyToggle = document.getElementById('easy-mode-toggle');
    const easyExit = document.getElementById('easy-mode-exit');
    const easyLangTl = document.getElementById('easy-lang-tl');
    const easyLangEn = document.getElementById('easy-lang-en');
    const easyViewCategories = document.getElementById('easy-view-categories');
    const easyViewDetail = document.getElementById('easy-view-detail');
    const easySpotImg = document.getElementById('easy-spot-img');
    const easySpotCatBadge = document.getElementById('easy-spot-cat-badge');
    const easySpotTitle = document.getElementById('easy-spot-title');
    const easySpotSubtitle = document.getElementById('easy-spot-subtitle');
    const easySpotDesc = document.getElementById('easy-spot-desc');
    const easySpeakBtn = document.getElementById('easy-speak-btn');
    const easyNavBack = document.getElementById('easy-nav-back');
    const easyNavMenu = document.getElementById('easy-nav-menu');
    const easyNavNext = document.getElementById('easy-nav-next');

    // Language buttons
    if (easyLangTl) {
        easyLangTl.addEventListener('click', () => setEasyLanguage('tl'));
    }
    if (easyLangEn) {
        easyLangEn.addEventListener('click', () => setEasyLanguage('en'));
    }

    function setEasyLanguage(lang) {
        easyModeLanguage = lang;
        if (lang === 'tl') {
            easyLangTl.classList.add('bg-[#C25A3F]', 'text-white');
            easyLangTl.classList.remove('text-[#1C1C1C]', 'hover:bg-gray-100');
            easyLangEn.classList.remove('bg-[#C25A3F]', 'text-white');
            easyLangEn.classList.add('text-[#1C1C1C]', 'hover:bg-gray-100');
            
            document.querySelectorAll('.lang-tl').forEach(el => el.classList.remove('hidden'));
            document.querySelectorAll('.lang-en').forEach(el => el.classList.add('hidden'));
        } else {
            easyLangEn.classList.add('bg-[#C25A3F]', 'text-white');
            easyLangEn.classList.remove('text-[#1C1C1C]', 'hover:bg-gray-100');
            easyLangTl.classList.remove('bg-[#C25A3F]', 'text-white');
            easyLangTl.classList.add('text-[#1C1C1C]', 'hover:bg-gray-100');
            
            document.querySelectorAll('.lang-en').forEach(el => el.classList.remove('hidden'));
            document.querySelectorAll('.lang-tl').forEach(el => el.classList.add('hidden'));
        }
        
        // Stop current speech and re-render/update descriptions
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        if (easySpeakBtn) easySpeakBtn.classList.remove('playing');
        
        if (easyModeFilteredSpots.length > 0) {
            renderCurrentEasySpot();
        }
    }

    // Toggle button handler
    if (easyToggle) {
        easyToggle.addEventListener('click', () => {
            toggleEasyMode(true);
        });
    }

    if (easyExit) {
        easyExit.addEventListener('click', () => {
            toggleEasyMode(false);
        });
    }

    function toggleEasyMode(active) {
        easyModeActive = active;
        
        const sidebar = document.getElementById('attractions-sidebar');
        if (sidebar) {
            if (active) {
                sidebar.classList.add('is-hidden');
            } else {
                sidebar.classList.remove('is-hidden');
            }
        }
        
        if (active) {
            easyOverlay.classList.remove('hidden');
            toggleMapGestures(false); // Lock gestures!
            
            // Go to categories menu initially
            showEasyMenu();
        } else {
            easyOverlay.classList.add('hidden');
            toggleMapGestures(true); // Restore gestures!
            
            if (window.speechSynthesis) window.speechSynthesis.cancel();
            if (easySpeakBtn) easySpeakBtn.classList.remove('playing');
        }

        // Trigger map resize so canvas expands cleanly to full screen
        setTimeout(() => {
            if (map) {
                if (isLeafletMode) {
                    map.invalidateSize();
                } else if (typeof map.resize === 'function') {
                    map.resize();
                }
            }
        }, 300);
    }

    function toggleMapGestures(enable) {
        if (isLeafletMode) {
            if (enable) {
                map.dragging.enable();
                map.touchZoom.enable();
                map.doubleClickZoom.enable();
            } else {
                map.dragging.disable();
                map.touchZoom.disable();
                map.doubleClickZoom.disable();
            }
            return;
        }
        
        const handlers = [
            map.dragPan,
            map.scrollZoom,
            map.boxZoom,
            map.dragRotate,
            map.keyboard,
            map.doubleClickZoom,
            map.touchZoomRotate
        ];
        
        handlers.forEach(handler => {
            if (handler) {
                enable ? handler.enable() : handler.disable();
            }
        });
    }

    // Category button click handlers
    document.querySelectorAll('.easy-cat-card').forEach(btn => {
        btn.addEventListener('click', () => {
            const cat = btn.getAttribute('data-easy-cat');
            loadEasyCategory(cat);
        });
    });

    async function loadEasyCategory(category) {
        easyModeCategory = category;
        easyModeIndex = 0;
        
        // Show loading screen in details area
        easyViewCategories.classList.add('hidden');
        easyViewDetail.classList.remove('hidden');
        easySpotTitle.textContent = easyModeLanguage === 'tl' ? "Sandali lamang..." : "Loading spots...";
        easySpotSubtitle.textContent = "";
        easySpotDesc.textContent = easyModeLanguage === 'tl' ? "Kinukuha namin ang listahan ng mga magagandang lugar..." : "Retrieving location list from Mangatarem database...";
        easySpotImg.src = "";
        
        easyNavBack.classList.add('hidden');
        easyNavMenu.classList.remove('hidden');
        easyNavNext.classList.add('hidden');
        
        try {
            if (category === 'Historical' || category === 'Nature') {
                const response = await fetch(`/api/attractions?category=${category}&per_page=50`);
                const data = await response.json();
                easyModeFilteredSpots = data.attractions || [];
            } else if (category === 'Food') {
                const response = await fetch(`/business/api?per_page=50`);
                const data = await response.json();
                // Filter businesses that match restaurant, cafe, fastfood, eatery
                const foodTypes = ['restaurant', 'cafe', 'fastfood'];
                easyModeFilteredSpots = (data.establishments || []).filter(est => foodTypes.includes(est.type));
            } else if (category === 'Lodging') {
                const response = await fetch(`/business/api?per_page=50`);
                const data = await response.json();
                // Filter businesses that match lodging, inn, hotel
                const stayTypes = ['hotel', 'inn', 'lodging', 'homestay', 'resort'];
                easyModeFilteredSpots = (data.establishments || []).filter(est => stayTypes.includes(est.type));
            }
            
            if (easyModeFilteredSpots.length === 0) {
                easySpotTitle.textContent = easyModeLanguage === 'tl' ? "Walang nahanap" : "No locations found";
                easySpotDesc.textContent = easyModeLanguage === 'tl' ? "Paumanhin, walang mahanap na mga lugar sa kategoryang ito sa ngayon." : "Sorry, no entries in this category were found in the database.";
            } else {
                renderCurrentEasySpot();
            }
            
        } catch (err) {
            console.error("Error loading easy mode spots:", err);
            easySpotTitle.textContent = "Error";
            easySpotDesc.textContent = easyModeLanguage === 'tl' ? "Nagkaroon ng problema sa pagkonekta sa database. Paki-subukan muli." : "Failed to connect to the server database. Please try again.";
        }
    }

    function renderCurrentEasySpot() {
        if (easyModeFilteredSpots.length === 0) return;
        const spot = easyModeFilteredSpots[easyModeIndex];
        
        // Populate standard visual items
        const isAttraction = spot.category !== undefined;
        const name = spot.name;
        const barangay = spot.barangay || spot.barangay_id || 'Mangatarem';
        const description = spot.description || (easyModeLanguage === 'tl' ? "Kasalukuyang inaayos ang kuwento para sa pamanang ito." : "A detailed description is currently being curated.");
        const image = spot.image || spot.cover_image_url || spot.image_url || '/static/img/mangatarem_map_teaser.webp';
        const categoryLabel = (isAttraction ? spot.category : (spot.type || 'Establishment')).toUpperCase();
        
        easySpotTitle.textContent = name;
        easySpotSubtitle.textContent = `${barangay}, Mangatarem`;
        easySpotDesc.textContent = description;
        easySpotImg.src = image;
        easySpotCatBadge.textContent = categoryLabel;
        
        // Show/hide navigation keys based on indices
        easyNavMenu.classList.remove('hidden');
        
        if (easyModeIndex > 0) {
            easyNavBack.classList.remove('hidden');
        } else {
            easyNavBack.classList.add('hidden');
        }
        
        if (easyModeIndex < easyModeFilteredSpots.length - 1) {
            easyNavNext.classList.remove('hidden');
        } else {
            easyNavNext.classList.add('hidden');
        }
        
        // Auto-navigate map smoothly
        const lat = parseFloat(spot.latitude || spot.lat || spot.latitude);
        const lng = parseFloat(spot.longitude || spot.lng || spot.longitude);
        if (lat && lng && !isNaN(lat) && !isNaN(lng)) {
            easyModeFlyTo(lat, lng);
        }
    }

    function showEasyMenu() {
        easyViewCategories.classList.remove('hidden');
        easyViewDetail.classList.add('hidden');
        
        easyNavBack.classList.add('hidden');
        easyNavMenu.classList.add('hidden');
        easyNavNext.classList.add('hidden');
        
        easyModeFilteredSpots = [];
        easyModeIndex = 0;
        
        if (window.speechSynthesis) window.speechSynthesis.cancel();
        if (easySpeakBtn) easySpeakBtn.classList.remove('playing');
    }

    if (easyNavMenu) {
        easyNavMenu.addEventListener('click', showEasyMenu);
    }
    
    if (easyNavBack) {
        easyNavBack.addEventListener('click', () => {
            if (easyModeIndex > 0) {
                easyModeIndex--;
                renderCurrentEasySpot();
                if (window.speechSynthesis) window.speechSynthesis.cancel();
                if (easySpeakBtn) easySpeakBtn.classList.remove('playing');
            }
        });
    }

    if (easyNavNext) {
        easyNavNext.addEventListener('click', () => {
            if (easyModeIndex < easyModeFilteredSpots.length - 1) {
                easyModeIndex++;
                renderCurrentEasySpot();
                if (window.speechSynthesis) window.speechSynthesis.cancel();
                if (easySpeakBtn) easySpeakBtn.classList.remove('playing');
            }
        });
    }

    // Text to Speech Narrator
    if (easySpeakBtn) {
        easySpeakBtn.addEventListener('click', () => {
            if ('speechSynthesis' in window) {
                if (window.speechSynthesis.speaking) {
                    window.speechSynthesis.cancel();
                    easySpeakBtn.classList.remove('playing');
                    return;
                }
                
                const spot = easyModeFilteredSpots[easyModeIndex];
                if (!spot) return;
                
                const name = spot.name;
                const barangay = spot.barangay || spot.barangay_id || 'Mangatarem';
                const description = spot.description || '';
                
                let narrationText = "";
                if (easyModeLanguage === 'tl') {
                    narrationText = `Narito po tayo sa ${name}, sa barangay ${barangay}. ${description}`;
                } else {
                    narrationText = `We are at ${name}, located in barangay ${barangay}. ${description}`;
                }
                
                easySpeakBtn.classList.add('playing');
                
                speechUtterance = new SpeechSynthesisUtterance(narrationText);
                speechUtterance.lang = easyModeLanguage === 'tl' ? 'fil-PH' : 'en-US';
                speechUtterance.rate = 0.82; // Slightly slow and extremely clear
                
                speechUtterance.onend = () => {
                    easySpeakBtn.classList.remove('playing');
                };
                
                speechUtterance.onerror = () => {
                    easySpeakBtn.classList.remove('playing');
                };
                
                window.speechSynthesis.speak(speechUtterance);
            } else {
                Swal.fire("Paumanhin / Sorry", "Hindi suportado ng iyong browser ang pagbasa ng kuwento. / Speech synthesis not supported by your device browser.", "warning");
            }
        });
    }

    // Feedback Event Listeners
    const feedbackBtn = document.getElementById('feedback-btn');
    const feedbackModal = document.getElementById('map-feedback-modal');
    const feedbackForm = document.getElementById('map-feedback-form');

    if (feedbackBtn && feedbackModal) {
        feedbackBtn.addEventListener('click', () => {
            feedbackModal.classList.remove('hidden');
        });
    }

    if (feedbackForm) {
        feedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const attractionId = document.getElementById('feedback-attraction-id').value;
            const type = document.getElementById('feedback-type').value;
            const message = document.getElementById('feedback-message').value;

            try {
                const response = await fetch('/api/map-feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        attraction_id: attractionId,
                        type: type,
                        message: message
                    })
                });

                if (response.ok) {
                    Swal.fire("Thank You!", "Your feedback has been submitted successfully.", "success");
                    feedbackModal.classList.add('hidden');
                    feedbackForm.reset();
                } else {
                    Swal.fire("Error", "Could not submit feedback at this time.", "error");
                }
            } catch (error) {
                console.error("Feedback error:", error);
                Swal.fire("Error", "An unexpected error occurred.", "error");
            }
        });
    }

});
