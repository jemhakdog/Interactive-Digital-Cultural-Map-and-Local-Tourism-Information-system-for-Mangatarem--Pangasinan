/**
 * CSRF Protection utility for AJAX and Fetch requests
 * Automatically injects the X-CSRFToken header into state-changing requests
 */

(function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    
    if (!csrfToken) {
        console.warn('CSRF token not found in meta tags. AJAX requests may fail.');
        return;
    }

    // Set up Fetch interception
    const originalFetch = window.fetch;
    window.fetch = function(input, init = {}) {
        const url = typeof input === 'string' ? input : input.url;
        const method = (init.method || (typeof input === 'object' && input.method) || 'GET').toUpperCase();
        
        // Only inject for state-changing methods
        const isStateChanging = ['POST', 'PUT', 'DELETE', 'PATCH'].includes(method);
        
        if (isStateChanging) {
            init.headers = init.headers || {};
            
            // Handle different header formats
            if (init.headers instanceof Headers) {
                if (!init.headers.has('X-CSRFToken')) {
                    init.headers.set('X-CSRFToken', csrfToken);
                }
            } else if (Array.isArray(init.headers)) {
                const hasCsrf = init.headers.some(([key]) => key.toLowerCase() === 'x-csrftoken');
                if (!hasCsrf) {
                    init.headers.push(['X-CSRFToken', csrfToken]);
                }
            } else {
                if (!init.headers['X-CSRFToken']) {
                    init.headers['X-CSRFToken'] = csrfToken;
                }
            }
        }
        
        return originalFetch(input, init);
    };

    // Set up XMLHttpRequest interception (for legacy/jQuery AJAX)
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this._method = method.toUpperCase();
        return originalOpen.apply(this, arguments);
    };

    const originalSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function() {
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(this._method)) {
            this.setRequestHeader('X-CSRFToken', csrfToken);
        }
        return originalSend.apply(this, arguments);
    };

    console.log('CSRF Protection initialized');
})();
