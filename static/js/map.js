document.addEventListener('DOMContentLoaded', function () {
    // ========================================
    const map = L.map('map').setView([15.7889, 120.2986], 13); // Mangatarem coordinates

    // Use CartoDB Voyager for cleaner, modern aesthetic
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // ========================================
    // 2. DEFINE CUSTOM ICONS (Color-Coded by Category)
    // ========================================
    const iconConfig = {
        Nature: { color: '#10b981', emoji: '🌿' },      // Green
        Historical: { color: '#f59e0b', emoji: '🏛️' },  // Amber
        Religious: { color: '#8b5cf6', emoji: '⛪' },   // Purple
        Food: { color: '#ef4444', emoji: '🍴' },        // Red
        default: { color: '#6b7280', emoji: '📍' }      // Gray
    };

    function getCustomIcon(category) {
        const config = iconConfig[category] || iconConfig.default;
        const svgIcon = `
            <svg width="32" height="40" viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 0C7.163 0 0 7.163 0 16c0 12 16 24 16 24s16-12 16-24c0-8.837-7.163-16-16-16z" 
                      fill="${config.color}" stroke="#fff" stroke-width="2"/>
                <text x="16" y="20" text-anchor="middle" font-size="14" fill="#fff">${config.emoji}</text>
            </svg>
        `;

        return L.divIcon({
            html: svgIcon,
            className: 'custom-marker-icon',
            iconSize: [32, 40],
            iconAnchor: [16, 40],
            popupAnchor: [0, -40]
        });
    }

    // ========================================
    // 3. DATA & MARKER MANAGEMENT
    // ========================================
    let attractionsData = [];

    // Initialize filter variables at the top to avoid temporal dead zone
    let currentCategory = 'all';
    let currentBarangay = 'all';
    let currentSearchTerm = '';

    let markersLayer = L.markerClusterGroup({
        maxClusterRadius: 50,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true,
        iconCreateFunction: function (cluster) {
            const count = cluster.getChildCount();
            return L.divIcon({
                html: `<div class="cluster-icon"><span>${count}</span></div>`,
                className: 'custom-cluster',
                iconSize: [40, 40]
            });
        }
    });
    map.addLayer(markersLayer);

    // Store marker references for flyTo functionality
    const markerMap = {};

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
    // 5. FETCH & RENDER ATTRACTIONS
    // ========================================
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = false;
    let hasMorePages = true;
    const loadingIndicator = document.getElementById('loading-indicator');

    // Generate cache key based on parameters
    function getCacheKey(page, category, barangay) {
        return `attractions_${page}_${category || 'all'}_${barangay || 'all'}`;
    }

    // Check if data is in cache and not expired
    function getCachedData(cacheKey) {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            const now = Date.now();

            // Check if cache is still valid (5 minutes)
            if (now - parsed.timestamp < 5 * 60 * 1000) {
                return parsed.data;
            } else {
                // Remove expired cache
                localStorage.removeItem(cacheKey);
            }
        }
        return null;
    }

    // Save data to cache
    function setCachedData(cacheKey, data) {
        const cacheObj = {
            data: data,
            timestamp: Date.now()
        };
        try {
            localStorage.setItem(cacheKey, JSON.stringify(cacheObj));
        } catch (e) {
            // Storage might be full, clear some old entries
            console.warn('Could not cache data:', e);
        }
    }

    async function fetchAttractions(page = 1, reset = false) {
        if (isLoading) return;

        isLoading = true;

        // Generate cache key
        const cacheKey = getCacheKey(page, currentCategory, currentBarangay);

        // Check if data is in cache
        const cachedData = getCachedData(cacheKey);
        if (cachedData && page === 1 && reset) {
            // Use cached data for initial load
            attractionsData = cachedData.attractions;
            totalPages = cachedData.pagination.pages;
            currentPage = cachedData.pagination.page;
            hasMorePages = cachedData.pagination.has_next;

            renderAttractions(attractionsData);
            addMarkers(attractionsData);
            isLoading = false;
            return;
        }

        // Show loading indicator
        if (page === 1 && reset) {
            const listContainer = document.getElementById('places-content');
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">Loading attractions...</div>';
        } else if (!reset && loadingIndicator) {
            // Show loading indicator at bottom for infinite scroll
            loadingIndicator.classList.remove('hidden');
        }

        try {
            const params = new URLSearchParams({
                page: page,
                per_page: 20
            });

            // Add filter parameters if they exist
            if (currentCategory && currentCategory !== 'all') {
                params.append('category', currentCategory);
            }
            if (currentBarangay && currentBarangay !== 'all') {
                params.append('barangay', currentBarangay);
            }
            if (currentSearchTerm) {
                // Note: search is handled client-side for now, but could be moved to server
            }

            const response = await fetch(`/api/attractions?${params}`);
            const result = await response.json();

            if (reset) {
                attractionsData = result.attractions;
                totalPages = result.pagination.pages;
                currentPage = result.pagination.page;
                hasMorePages = result.pagination.has_next;

                renderAttractions(attractionsData);
                addMarkers(attractionsData);

                // Cache the data for initial page
                if (page === 1) {
                    setCachedData(cacheKey, result);
                }
            } else {
                // Append new data to existing data
                attractionsData = [...attractionsData, ...result.attractions];
                totalPages = result.pagination.pages;
                currentPage = result.pagination.page;
                hasMorePages = result.pagination.has_next;

                // Only render the new attractions if we're doing infinite scroll
                // For now, we'll re-render all for consistency
                renderAttractions(attractionsData);
            }

        } catch (error) {
            console.error('Error fetching attractions:', error);
        } finally {
            isLoading = false;
            // Hide loading indicator
            if (loadingIndicator) {
                loadingIndicator.classList.add('hidden');
            }
        }
    }

    // Initial fetch
    fetchAttractions(1, true);

    // ========================================
    // 10. CARD MANAGEMENT
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

        // Populate data
        cardTitle.textContent = attraction.name;
        cardAddress.textContent = attraction.barangay ? `${attraction.barangay}, Mangatarem` : 'Mangatarem, Pangasinan';
        cardDescription.textContent = attraction.description;

        // Mock data for now (since not in DB)
        cardRating.textContent = (Math.random() * (5.0 - 4.0) + 4.0).toFixed(1);

        // Show card
        placeCard.classList.remove('hidden');
        placeCard.classList.remove('translate-y-full');
    }

    // Close button logic
    const closeCardBtn = placeCard.querySelector('button');
    if (closeCardBtn) {
        closeCardBtn.addEventListener('click', () => {
            placeCard.classList.add('hidden');
        });
    }

    // ========================================
    // 6. FLYTO ANIMATION
    // ========================================
    // ========================================
    // 6. FLYTO ANIMATION
    // ========================================
    function flyToLocation(id, lat, lng) {
        // Validate coordinates
        if (!lat || !lng || isNaN(lat) || isNaN(lng)) {
            console.warn('Invalid coordinates for attraction:', id, { lat, lng });
            alert('This location does not have valid coordinates.');
            return;
        }

        map.flyTo([lat, lng], 16, {
            animate: true,
            duration: 1.5
        });

        // Find attraction data
        const attraction = attractionsData.find(a => a.id === id);

        // Show card after animation
        setTimeout(() => {
            if (attraction) {
                updateCard(attraction);
            }
        }, 1600);
    }

    // Update marker click to show card
    function addMarkers(attractions) {
        // Clear existing markers
        markersLayer.clearLayers();

        // Batch add markers for better performance
        const markersToAdd = [];
        attractions.forEach(attraction => {
            const icon = getCustomIcon(attraction.category);
            const marker = L.marker([attraction.lat, attraction.lng], { icon: icon });

            // Add click event to show card
            marker.on('click', () => {
                updateCard(attraction);

                // Also center map on click (optional, but good UX)
                map.flyTo([attraction.lat, attraction.lng], 16, {
                    animate: true,
                    duration: 1.0
                });
            });

            // Add to cluster layer
            markersToAdd.push(marker);

            // Store reference for flyTo
            markerMap[attraction.id] = marker;
        });

        // Add all markers at once for better performance
        markersLayer.addLayers(markersToAdd);
    }

    function renderAttractions(attractions) {
        const listContainer = document.getElementById('places-content');

        if (attractions.length === 0) {
            listContainer.innerHTML = '<div class="text-center text-gray-500 py-4">No attractions found.</div>';
            return;
        }

        listContainer.innerHTML = '';

        attractions.forEach(attraction => {
            const categoryConfig = iconConfig[attraction.category] || iconConfig.default;
            const categoryLabel = attraction.category.toUpperCase();

            // Generate star rating display (mock for now, replace with real ratings if available)
            const rating = attraction.rating || 4;
            const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
            const reviewCount = attraction.review_count || Math.floor(Math.random() * 50);

            const card = document.createElement('div');
            card.className = 'group bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer overflow-hidden flex flex-row h-32';
            card.innerHTML = `
                <div class="w-1/3 h-full bg-gray-200 relative">
                    <img src="${attraction.image}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt="${attraction.name}">
                    <div class="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded text-[10px] font-bold" style="color: ${categoryConfig.color}">${categoryLabel}</div>
                </div>
                <div class="w-2/3 p-3 flex flex-col justify-between">
                    <div>
                        <h3 class="font-bold text-gray-800 text-sm leading-tight mb-1 group-hover:text-green-700 transition line-clamp-1">${attraction.name}</h3>
                        <p class="text-xs text-gray-500 line-clamp-2">${attraction.description}</p>
                    </div>
                    <div class="flex justify-between items-end mt-2">
                        <div class="text-xs text-amber-500 font-bold">${stars} <span class="text-gray-400 font-normal">(${reviewCount})</span></div>
                        <button class="text-[10px] bg-green-50 text-green-700 px-2 py-1 rounded hover:bg-green-100 transition">View on Map ➔</button>
                    </div>
                </div>
            `;

            // FlyTo functionality
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
    // 7. FILTERING & SEARCH
    // ========================================
    const searchInput = document.getElementById('search-input');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const barangayFilter = document.getElementById('barangay-filter');

    // Debounced search function to reduce API calls
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
        currentPage = 1; // Reset to first page when filtering
        fetchAttractions(currentPage, true);
    }, 300); // Wait 300ms after user stops typing

    function filterAttractions() {
        // Update current search term
        currentSearchTerm = searchInput.value.toLowerCase();

        // Fetch new data based on filters
        debouncedFilterAttractions();
    }

    searchInput.addEventListener('input', filterAttractions);

    // Category filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterBtns.forEach(b => {
                b.classList.remove('bg-green-600', 'text-white');
                b.classList.add('bg-white', 'border', 'border-gray-200', 'text-gray-600');
            });
            btn.classList.remove('bg-white', 'border', 'border-gray-200', 'text-gray-600');
            btn.classList.add('bg-green-600', 'text-white');

            currentCategory = btn.dataset.category;
            currentPage = 1; // Reset to first page when changing category
            fetchAttractions(currentPage, true);
        });
    });

    // Barangay filter
    if (barangayFilter) {
        barangayFilter.addEventListener('change', (e) => {
            currentBarangay = e.target.value;
            currentPage = 1; // Reset to first page when changing barangay
            fetchAttractions(currentPage, true);
        });
    }

    // ========================================
    // 8. INFINITE SCROLL FOR ATTRACTION LIST
    // ========================================
    const contentArea = document.getElementById('content-area');

    let scrollTimeout;
    contentArea.addEventListener('scroll', () => {
        // Clear the previous timeout
        clearTimeout(scrollTimeout);

        // Set a new timeout
        scrollTimeout = setTimeout(() => {
            const { scrollTop, scrollHeight, clientHeight } = contentArea;

            // Check if user has scrolled near the bottom
            if (scrollTop + clientHeight >= scrollHeight - 100 && hasMorePages && !isLoading) {
                // Load next page
                currentPage++;
                fetchAttractions(currentPage, false);
            }
        }, 200); // Delay to prevent too many calls
    });

    // ========================================
    // 9. GEOLOCATION "NEAR ME" FEATURE
    // ========================================
    const locateBtn = document.getElementById('locate-me');
    let userLocationMarker = null;

    locateBtn.addEventListener('click', () => {
        locateBtn.classList.add('animate-pulse');

        map.locate({ setView: true, maxZoom: 15 });
    });

    map.on('locationfound', (e) => {
        locateBtn.classList.remove('animate-pulse');

        // Remove previous user marker
        if (userLocationMarker) {
            map.removeLayer(userLocationMarker);
        }

        // Add blue circle for user location
        userLocationMarker = L.circle(e.latlng, {
            radius: e.accuracy / 2,
            color: '#3b82f6',
            fillColor: '#3b82f6',
            fillOpacity: 0.2,
            weight: 2
        }).addTo(map);

        // Add user marker
        const userIcon = L.divIcon({
            html: '<div class="user-location-marker"></div>',
            className: 'user-marker',
            iconSize: [16, 16]
        });

        L.marker(e.latlng, { icon: userIcon }).addTo(map)
            .bindPopup("You are here!")
            .openPopup();
    });

    map.on('locationerror', () => {
        locateBtn.classList.remove('animate-pulse');
        alert('Unable to get your location. Please check your browser settings.');
    });

    // ========================================
    // 9. FLOATING ROUTES TOGGLE
    // ========================================
    // ========================================
    // 9. FLOATING ROUTES TOGGLE
    // ========================================
    const routesToggle = document.getElementById('routes-toggle');
    if (routesToggle) {
        routesToggle.addEventListener('click', () => switchTab('routes'));
    }

    // ========================================
    // 10. MOBILE BOTTOM SHEET LOGIC
    // ========================================
    const sidebar = document.getElementById('attractions-sidebar');
    const dragHandle = document.getElementById('drag-handle');
    // contentArea is already defined in the infinite scroll section above

    if (sidebar && dragHandle) {
        let startY = 0;
        let currentY = 0;
        let initialTranslateY = 0;
        const headerHeight = 140; // Approx height of header + tabs + filters
        const sheetHeight = sidebar.offsetHeight;

        // Calculate the initial collapsed state (showing only header)
        // transform is set in CSS to: translateY(calc(100% - 140px))
        // We need to manage this via JS for dragging

        let isDragging = false;

        // Helper to get current transform Y value
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
            e.preventDefault(); // Prevent page scroll while dragging sheet

            const deltaY = e.touches[0].clientY - startY;
            const newY = initialTranslateY + deltaY;

            // Constrain movement
            // Max Up: 0 (fully expanded)
            // Max Down: sheetHeight - headerHeight (collapsed)

            const maxDown = sheetHeight - headerHeight;

            if (newY >= 0 && newY <= maxDown) {
                sidebar.style.transform = `translateY(${newY}px)`;
            }
        }, { passive: false });

        document.addEventListener('touchend', (e) => {
            if (!isDragging) return;
            isDragging = false;
            sidebar.classList.remove('is-dragging');

            const currentTransform = getTransformY();
            const maxDown = sheetHeight - headerHeight;
            const threshold = maxDown / 2;

            // Snap logic
            if (currentTransform < threshold) {
                // Snap to top (Open)
                sidebar.style.transform = 'translateY(0)';
                sidebar.classList.add('is-open');
                // Enable content scrolling
                contentArea.style.overflowY = 'auto';
            } else {
                // Snap to bottom (Collapsed)
                sidebar.style.transform = `translateY(calc(100% - ${headerHeight}px))`;
                sidebar.classList.remove('is-open');
                // Disable content scrolling to prevent weirdness when collapsed
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
    // 11. SUGGESTED ROUTES LOGIC (NEW)
    // ========================================

    // Define the paths using [Lat, Lng] coordinates
    // These coordinates match your attractions.json data
    const routeData = {
        nature: [
            [15.6667, 120.2833], // Manleluag Spring
            [15.6500, 120.2200], // Timmanguyob Falls
            [15.7000, 120.2500]  // Daang Kalikasan
        ],
        heritage: [
            [15.7889, 120.2986], // St. Raymund Church
            [15.7895, 120.2990], // Example: Town Plaza (Approx)
            [15.7900, 120.3000]  // Example: Old Municipal Hall (Approx)
        ]
    };

    let currentRouteLine = null;

    // Make these functions available globally so HTML can call them
    window.drawRoute = function (type) {
        // 1. Remove existing line if any
        if (currentRouteLine) {
            map.removeLayer(currentRouteLine);
        }

        // 2. Get coordinates
        const path = routeData[type];
        if (!path) return;

        // 3. Define color based on type
        const color = type === 'nature' ? '#10b981' : '#f59e0b'; // Green or Orange

        // 4. Draw the Polyline using Leaflet
        currentRouteLine = L.polyline(path, {
            color: color,
            weight: 5,
            opacity: 0.8,
            dashArray: '10, 10', // Makes it a dashed line for "walking/travel" feel
            lineCap: 'round'
        }).addTo(map);

        // 5. Zoom map to fit the route
        map.fitBounds(currentRouteLine.getBounds(), { padding: [50, 50] });
    };

    window.clearRoutes = function () {
        if (currentRouteLine) {
            map.removeLayer(currentRouteLine);
            currentRouteLine = null;
        }
        // Reset view to default
        map.flyTo([15.7889, 120.2986], 13);
    };

});
