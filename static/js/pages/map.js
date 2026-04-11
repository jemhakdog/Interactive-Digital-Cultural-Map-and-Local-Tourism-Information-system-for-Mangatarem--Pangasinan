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
    // ========================================
    // 1. MAP INITIALIZATION
    // ========================================
    mapboxgl.accessToken = window.MAPBOX_TOKEN;

    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [120.2986, 15.7889], // Mangatarem coordinates [lng, lat]
        zoom: 13.5,
        pitch: 65,      // Tilted view for 3D effect
        bearing: -15,   // Rotated view
        attributionControl: true,
        antialias: true // Smoother 3D edges
    });

    // Add navigation controls
    map.addControl(new mapboxgl.NavigationControl(), 'top-left');

    // Force resize calculation for mobile layout
    map.on('load', () => {
        setTimeout(() => map.resize(), 500);
    });

    // ========================================
    // 2. CATEGORY ICON CONFIGURATION
    // ========================================
    const iconConfig = {
        Nature: { color: '#10b981', emoji: '🌿' },      // Green
        Historical: { color: '#f59e0b', emoji: '🏛️' },  // Amber
        Religious: { color: '#8b5cf6', emoji: '⛪' },   // Purple
        Food: { color: '#ef4444', emoji: '🍴' },        // Red
        default: { color: '#6b7280', emoji: '📍' }      // Gray
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
    map.on('load', () => {
        setupMVTSource();
        setupMVTLayers();
        init3DLayers();
        fetchAttractions(1, true); // Fetch for sidebar list
    });

    // Re-add layers when style changes
    map.on('style.load', () => {
        // Remove layers first (they depend on the source)
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
                        'Religious', '#8b5cf6',
                        'Food', '#ef4444',
                        '#6b7280' // default
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
                        <strong class="text-green-800">${feature.properties.name}</strong>
                        <div class="text-xs text-gray-600">${feature.properties.category}</div>
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
    const tabRoutes = document.getElementById('tab-routes');
    const placesContent = document.getElementById('places-content');
    const routesContent = document.getElementById('routes-content');

    function switchTab(tab) {
        if (tab === 'places') {
            tabPlaces.classList.add('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold');
            tabPlaces.classList.remove('text-gray-500', 'font-medium');
            tabRoutes.classList.remove('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold');
            tabRoutes.classList.add('text-gray-500', 'font-medium');

            placesContent.classList.remove('hidden');
            routesContent.classList.add('hidden');
        } else {
            tabRoutes.classList.add('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold');
            tabRoutes.classList.remove('text-gray-500', 'font-medium');
            tabPlaces.classList.remove('text-green-700', 'border-green-700', 'bg-green-50', 'font-semibold');
            tabPlaces.classList.add('text-gray-500', 'font-medium');

            routesContent.classList.remove('hidden');
            placesContent.classList.add('hidden');
        }
    }

    tabPlaces.addEventListener('click', () => switchTab('places'));
    tabRoutes.addEventListener('click', () => switchTab('routes'));

    // ========================================
    // 5. CACHING
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

            const response = await fetch(`/api/attractions?${params}`);
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

    // Style Switcher Logic
    window.changeMapStyle = function(styleId) {
        const styleUrl = `mapbox://styles/mapbox/${styleId}`;
        map.setStyle(styleUrl);

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
    const cardDistance = document.getElementById('card-distance');
    const cardDescription = document.getElementById('card-description');

    function updateCard(attraction) {
        if (!placeCard) return;

        cardTitle.textContent = attraction.name;
        cardAddress.textContent = attraction.barangay ? `${attraction.barangay}, Mangatarem` : 'Mangatarem, Pangasinan';
        cardDescription.textContent = attraction.description;
        cardRating.textContent = (Math.random() * (5.0 - 4.0) + 4.0).toFixed(1);

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
            alert('This location does not have valid coordinates.');
            return;
        }

        map.flyTo({
            center: [lng, lat],
            zoom: 16,
            duration: 1500
        });

        const attraction = attractionsData.find(a => a.id === id);

        setTimeout(() => {
            if (attraction) {
                updateCard(attraction);
            }
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

            const card = document.createElement('div');
            card.className = 'group bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32';
            card.innerHTML = `
                <div class="w-1/3 h-full bg-gray-200 relative flex-shrink-0">
                    <img src="${attraction.image}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${attraction.name}" onerror="this.src='https://via.placeholder.com/300x200?text=No+Image'">
                    <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${categoryConfig.color}">${categoryLabel}</div>
                </div>
                <div class="w-2/3 p-3 flex flex-col justify-between bg-white" style="background-color: #ffffff !important;">
                    <div>
                        <h3 class="font-bold text-sm leading-tight mb-1 line-clamp-1" style="color: #111827 !important; -webkit-text-fill-color: #111827 !important;">${attraction.name}</h3>
                        <p class="text-xs line-clamp-2 mt-1" style="color: #374151 !important; -webkit-text-fill-color: #374151 !important;">${attraction.description}</p>
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
            filterBtns.forEach(b => {
                b.classList.remove('bg-green-600', 'text-white');
                b.classList.add('bg-white', 'border', 'border-gray-200', 'text-gray-600');
            });
            btn.classList.remove('bg-white', 'border', 'border-gray-200', 'text-gray-600');
            btn.classList.add('bg-green-600', 'text-white');

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
    // 12. GEOLOCATION "NEAR ME"
    // ========================================
    const locateBtn = document.getElementById('locate-me');
    let userLocationMarker = null;

    locateBtn.addEventListener('click', () => {
        locateBtn.classList.add('animate-pulse');

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    locateBtn.classList.remove('animate-pulse');
                    const { latitude, longitude, accuracy } = position.coords;

                    // Remove previous marker
                    if (userLocationMarker) {
                        userLocationMarker.remove();
                    }

                    // Create user location marker
                    const el = document.createElement('div');
                    el.className = 'user-location-marker';
                    el.style.cssText = `
                        width: 16px;
                        height: 16px;
                        background: #3b82f6;
                        border: 3px solid white;
                        border-radius: 50%;
                        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
                    `;

                    userLocationMarker = new mapboxgl.Marker(el)
                        .setLngLat([longitude, latitude])
                        .addTo(map);

                    // Fly to location
                    map.flyTo({
                        center: [longitude, latitude],
                        zoom: 15,
                        duration: 1500
                    });

                    // Show popup
                    new mapboxgl.Popup({ offset: 25 })
                        .setLngLat([longitude, latitude])
                        .setHTML('<strong>You are here!</strong>')
                        .addTo(map);
                },
                (error) => {
                    locateBtn.classList.remove('animate-pulse');
                    alert('Unable to get your location. Please check your browser settings.');
                    console.error('Geolocation error:', error);
                },
                { enableHighAccuracy: true, timeout: 10000 }
            );
        } else {
            locateBtn.classList.remove('animate-pulse');
            alert('Geolocation is not supported by your browser.');
        }
    });

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

    if (sidebar && dragHandle) {
        let startY = 0;
        let initialTranslateY = 0;
        const headerHeight = 140;
        const sheetHeight = sidebar.offsetHeight;
        let isDragging = false;

        const getTransformY = () => {
            const style = window.getComputedStyle(sidebar);
            try {
                if (window.DOMMatrix) {
                    return new DOMMatrix(style.transform).m42;
                }
                return new WebKitCSSMatrix(style.transform).m42;
            } catch (e) {
                return 0;
            }
        };

        dragHandle.addEventListener('touchstart', (e) => {
            isDragging = true;
            startY = e.touches[0].clientY;
            initialTranslateY = getTransformY();
            sidebar.classList.add('is-dragging');
        }, { passive: false });

        document.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();

            const deltaY = e.touches[0].clientY - startY;
            const newY = initialTranslateY + deltaY;
            const maxDown = sheetHeight - headerHeight;

            if (newY >= 0 && newY <= maxDown) {
                sidebar.style.transform = `translateY(${newY}px)`;
            }
        }, { passive: false });

        document.addEventListener('touchend', () => {
            if (!isDragging) return;
            isDragging = false;
            sidebar.classList.remove('is-dragging');

            const currentTransform = getTransformY();
            const maxDown = sheetHeight - headerHeight;
            const threshold = maxDown / 2;

            if (currentTransform < threshold) {
                sidebar.style.transform = 'translateY(0)';
                sidebar.classList.add('is-open');
                contentArea.style.overflowY = 'auto';
            } else {
                sidebar.style.transform = `translateY(calc(100% - ${headerHeight}px))`;
                sidebar.classList.remove('is-open');
                contentArea.style.overflowY = 'hidden';
            }
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                if (sidebar.style.transform) {
                    sidebar.style.transform = '';
                    sidebar.classList.remove('is-open', 'is-dragging');
                    contentArea.style.overflowY = '';
                }
            }
        });
    }

    // ========================================
    // 15. SUGGESTED ROUTES (POLYLINES)
    // ========================================
    const routeData = {
        nature: [
            [120.2833, 15.6667], // Manleluag Spring
            [120.2200, 15.6500], // Timmanguyob Falls
            [120.2500, 15.7000]  // Daang Kalikasan
        ],
        heritage: [
            [120.2986, 15.7889], // St. Raymund Church
            [120.2990, 15.7895], // Town Plaza
            [120.3000, 15.7900]  // Old Municipal Hall
        ]
    };

    let currentRouteLayer = null;
    let currentRouteSource = null;

    window.drawRoute = function (type) {
        // Remove existing route
        if (currentRouteLayer && map.getLayer(currentRouteLayer)) {
            map.removeLayer(currentRouteLayer);
        }
        if (currentRouteSource && map.getSource(currentRouteSource)) {
            map.removeSource(currentRouteSource);
        }

        const path = routeData[type];
        if (!path) return;

        const sourceId = `route-${type}`;
        const layerId = `route-line-${type}`;
        const color = type === 'nature' ? '#10b981' : '#f59e0b';

        map.addSource(sourceId, {
            type: 'geojson',
            data: {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: path
                }
            }
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
                'line-color': color,
                'line-width': 5,
                'line-opacity': 0.8,
                'line-dasharray': [2, 2]
            }
        });

        currentRouteLayer = layerId;
        currentRouteSource = sourceId;

        // Fit bounds to route
        const bounds = path.reduce((bounds, coord) => {
            return bounds.extend(coord);
        }, new mapboxgl.LngLatBounds(path[0], path[0]));

        map.fitBounds(bounds, { padding: 50 });
    };

    window.clearRoutes = function () {
        if (currentRouteLayer && map.getLayer(currentRouteLayer)) {
            map.removeLayer(currentRouteLayer);
        }
        if (currentRouteSource && map.getSource(currentRouteSource)) {
            map.removeSource(currentRouteSource);
        }
        currentRouteLayer = null;
        currentRouteSource = null;

        // Reset view
        map.flyTo({
            center: [120.2986, 15.7889],
            zoom: 13,
            duration: 1500
        });
    };

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

});
