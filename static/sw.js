const CACHE_NAME = 'gomangatarem-v5';
const MAP_CACHE_NAME = 'mapbox-tiles';
const STATIC_ASSETS = [
    '/static/css/main.css',
    '/static/css/style.css',
    '/static/css/pages/map.css',
    '/static/js/pages/map_v2.js',
    '/manifest.json'
];

// Install Event: Cache static assets
self.addEventListener('install', (event) => {
    self.skipWaiting(); // Force activation
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.allSettled(STATIC_ASSETS.map(url => cache.add(url)));
        })
    );
});

// Activate Event: Cleanup old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        Promise.all([
            self.clients.claim(), // Take control of all clients
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== CACHE_NAME && cacheName !== MAP_CACHE_NAME) {
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
        ])
    );
});

// Fetch Event: Intercept requests
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    const isSameOrigin = url.origin === self.location.origin;

    // 1. Exclude API tile requests and sensitive routes
    const sensitiveRoutes = ['/admin', '/auth', '/user', '/barangay-admin', '/barangay'];
    if (url.pathname.startsWith('/api/tiles/') || sensitiveRoutes.some(route => url.pathname.startsWith(route))) {
        return; 
    }

    // 2. Mapbox Handling (Cross-origin but allowed)
    if (url.hostname.includes('mapbox.com')) {
        event.respondWith(
            caches.open(MAP_CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((response) => {
                    const fetchPromise = fetch(event.request).then((networkResponse) => {
                        if (networkResponse.ok && (url.pathname.includes('/tiles/') || url.pathname.includes('/styles/'))) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => null);
                    return response || fetchPromise;
                });
            })
        );
        return;
    }

    // 3. Only intercept same-origin static/dynamic content
    // For other cross-origin (like Leaflet CDN), let the browser handle it natively
    if (!isSameOrigin) {
        return;
    }

    // Stale-While-Revalidate for local static assets
    const isStatic = url.pathname.startsWith('/static/') || url.pathname.match(/\.(css|js|png|jpg|jpeg|gif|svg|webp|woff|woff2|ico)$/i);
    
    if (isStatic) {
        event.respondWith(
            caches.match(event.request).then((cacheResponse) => {
                const fetchPromise = fetch(event.request).then((networkResponse) => {
                    if (networkResponse.ok && event.request.method === 'GET') {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return networkResponse;
                }).catch(() => null);
                return cacheResponse || fetchPromise;
            })
        );
    } else {
        // Network-First for local dynamic routes
        event.respondWith(
            fetch(event.request).then((networkResponse) => {
                if (networkResponse.ok && event.request.method === 'GET') {
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return networkResponse;
            }).catch(() => {
                return caches.match(event.request);
            })
        );
    }
});

// Message Event: Handle batch pre-fetching
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'PREFETCH_TILES') {
        const urls = event.data.urls;
        caches.open(MAP_CACHE_NAME).then((cache) => {
            urls.forEach(url => {
                cache.match(url).then(response => {
                    if (!response) {
                        fetch(url).then(networkResponse => {
                            if (networkResponse.ok) cache.put(url, networkResponse);
                        }).catch(() => {});
                    }
                });
            });
        });
    }
});

