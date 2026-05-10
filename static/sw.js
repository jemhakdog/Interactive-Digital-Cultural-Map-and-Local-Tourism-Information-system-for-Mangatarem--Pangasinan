const CACHE_NAME = 'gomangatarem-v3';
const MAP_CACHE_NAME = 'mapbox-tiles';
const STATIC_ASSETS = [
    '/map',
    '/static/css/main.css',
    '/static/css/style.css',
    '/static/css/pages/map.css',
    '/static/js/pages/map.js',
    '/manifest.json'
];

// Install Event: Cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Use Promise.allSettled to ensure installation doesn't fail 
            // if a single asset (like the manifest) fails on protected deployments
            return Promise.allSettled(STATIC_ASSETS.map(url => cache.add(url)));
        })
    );
});

// Activate Event: Cleanup old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== MAP_CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch Event: Intercept requests
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Exclude API tile requests from caching (they're dynamic and large)
    if (url.pathname.startsWith('/api/tiles/')) {
        // Let tile requests go to network directly
        return;
    }

    // Special handling for Mapbox Tiles and Styles
    if (url.hostname.includes('mapbox.com')) {
        event.respondWith(
            caches.open(MAP_CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((response) => {
                    const fetchPromise = fetch(event.request).then((networkResponse) => {
                        // Only cache successful tile/style requests
                        if (networkResponse.ok && (url.pathname.includes('/tiles/') || url.pathname.includes('/styles/'))) {
                            // Check if response is cacheable
                            const canCache = networkResponse.type === 'basic' || 
                                             networkResponse.type === 'cors' || 
                                             networkResponse.type === 'default';
                            
                            if (canCache) {
                                cache.put(event.request, networkResponse.clone());
                            }
                        }
                        return networkResponse;
                    }).catch(() => {
                        return null; // Return null on fetch failure
                    });
                    // Return cache if available, else fetch from network (with fallback)
                    return response || fetchPromise.then(res => res || new Response('Map Error', { status: 503 }));
                });
            })
        );
        return;
    }

    // Exclude sensitive/authenticated routes from caching
    const sensitiveRoutes = ['/admin', '/auth', '/user', '/barangay-admin', '/barangay'];
    if (sensitiveRoutes.some(route => url.pathname.startsWith(route))) {
        return; // Let the browser handle these normally (from network)
    }

    // Stale-While-Revalidate for static assets
    const staleWhileRevalidate = () => {
        return caches.match(event.request).then((cacheResponse) => {
            // Always fetch from network to get fresh content
            const fetchPromise = fetch(event.request).then((networkResponse) => {
                // Only cache successful GET requests that are cacheable
                if (networkResponse.ok && event.request.method === 'GET') {
                    const canCache = networkResponse.type === 'basic' || 
                                     networkResponse.type === 'cors' || 
                                     networkResponse.type === 'default';
                    
                    if (canCache) {
                        // Clone before caching so the original can be returned
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                }
                return networkResponse;
            }).catch(() => {
                // If fetch fails and no cache, we'll return the error later
                return null;
            });
            
            // Return cached response if available, otherwise wait for fetch
            return cacheResponse || fetchPromise.then(res => res || new Response('Offline or Network Error', {
                status: 503,
                statusText: 'Service Unavailable',
                headers: new Headers({ 'Content-Type': 'text/plain' })
            }));
        });
    };

    // Network-First for dynamic routes
    const networkFirst = () => {
        return fetch(event.request).then((networkResponse) => {
            // Only cache successful GET requests that are cacheable
            if (networkResponse.ok && event.request.method === 'GET') {
                const canCache = networkResponse.type === 'basic' || 
                                 networkResponse.type === 'cors' || 
                                 networkResponse.type === 'default';
                
                if (canCache) {
                    // Clone before caching so the original can be returned
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
            }
            return networkResponse;
        }).catch(() => {
            return caches.match(event.request).then(cached => {
                return cached || new Response('Network Error', {
                    status: 503,
                    headers: new Headers({ 'Content-Type': 'text/plain' })
                });
            });
        });
    };

    const isStaticObject = url.pathname.startsWith('/static/') || url.pathname.match(/\.(css|js|png|jpg|jpeg|gif|svg|webp|woff|woff2|ico)$/i);

    if (isStaticObject) {
        event.respondWith(staleWhileRevalidate());
    } else {
        event.respondWith(networkFirst());
    }
});

// Message Event: Handle batch pre-fetching
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'PREFETCH_TILES') {
        const urls = event.data.urls;
        caches.open(MAP_CACHE_NAME).then((cache) => {
            urls.forEach(url => {
                // Check if already in cache before fetching
                cache.match(url).then(response => {
                    if (!response) {
                        fetch(url).then(networkResponse => {
                            if (networkResponse.ok) {
                                cache.put(url, networkResponse);
                                // Notify client about progress
                                self.clients.matchAll().then(clients => {
                                    clients.forEach(client => {
                                        client.postMessage({
                                            type: 'TILES_PROGRESS',
                                            url: url
                                        });
                                    });
                                });
                            }
                        }).catch(err => console.error('Prefetch failed for:', url, err));
                    }
                });
            });
        });
    }
});
