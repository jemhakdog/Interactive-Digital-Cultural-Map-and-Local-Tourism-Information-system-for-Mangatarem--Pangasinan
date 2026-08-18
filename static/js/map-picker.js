/**
 * Map Picker Utility for PGIS Functionality
 * Synchronizes a Leaflet map with Latitude/Longitude inputs.
 */
class MapPicker {
    constructor(config) {
        this.mapId = config.mapId;
        this.latInput = document.getElementById(config.latInputId);
        this.lngInput = document.getElementById(config.lngInputId);
        this.defaultLocation = config.defaultLocation || [15.7889, 120.2986]; // Mangatarem Center
        this.zoom = config.zoom || 14;
        
        if (!this.latInput || !this.lngInput) {
            console.error("MapPicker: Lat/Lng inputs not found.");
            return;
        }

        this.init();
    }

    init() {
        // Initialize Map
        this.map = L.map(this.mapId, {
            scrollWheelZoom: 'center'
        }).setView(this.defaultLocation, this.zoom);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(this.map);

        // Marker initialization with specific style for picker
        const initialLat = parseFloat(this.latInput.value) || this.defaultLocation[0];
        const initialLng = parseFloat(this.lngInput.value) || this.defaultLocation[1];

        this.marker = L.marker([initialLat, initialLng], {
            draggable: true,
            icon: L.divIcon({
                html: `
                    <div class="relative">
                        <div class="absolute -top-10 -left-4 bg-emerald-600 text-white text-[10px] font-bold px-2 py-1 rounded shadow-lg whitespace-nowrap"> Drag me </div>
                        <svg width="32" height="40" viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16 0C7.163 0 0 7.163 0 16c0 12 16 24 16 24s16-12 16-24c0-8.837-7.163-16-16-16z" 
                                  fill="#059669" stroke="#fff" stroke-width="2"/>
                            <circle cx="16" cy="16" r="6" fill="#fff"/>
                        </svg>
                    </div>`,
                className: 'custom-picker-icon',
                iconSize: [32, 40],
                iconAnchor: [16, 40]
            })
        }).addTo(this.map);

        // Map Click Event
        this.map.on('click', (e) => {
            this.updateMarker(e.latlng);
        });

        // Marker Drag Event
        this.marker.on('drag', (e) => {
            this.updateInputs(e.target.getLatLng());
        });
        
        // Manual input sync (Typing in coordinates moves marker)
        const syncInputs = () => {
            const lat = parseFloat(this.latInput.value);
            const lng = parseFloat(this.lngInput.value);
            if (!isNaN(lat) && !isNaN(lng)) {
                this.updateMarker(L.latLng(lat, lng), false);
            }
        };

        this.latInput.addEventListener('input', syncInputs);
        this.lngInput.addEventListener('input', syncInputs);

        // Trigger map invalidate size on next tick to handle hidden modals/containers
        setTimeout(() => {
            this.map.invalidateSize();
            // If we have initial coordinates, pan to them
            if (this.latInput.value && this.lngInput.value) {
                this.map.panTo([initialLat, initialLng]);
            }
        }, 100);
    }

    updateMarker(latlng, updateInputs = true) {
        this.marker.setLatLng(latlng);
        if (updateInputs) {
            this.updateInputs(latlng);
        }
        this.map.panTo(latlng);
    }

    updateInputs(latlng) {
        this.latInput.value = latlng.lat.toFixed(6);
        this.lngInput.value = latlng.lng.toFixed(6);
        // Trigger input event for any other listeners
        this.latInput.dispatchEvent(new Event('input'));
        this.lngInput.dispatchEvent(new Event('input'));
    }

    locate() {
        this.map.locate({ setView: true, maxZoom: 16 });
        const onLocationFound = (e) => {
            this.updateMarker(e.latlng);
            this.map.off('locationfound', onLocationFound);
        };
        this.map.on('locationfound', onLocationFound);
        this.map.on('locationerror', (e) => {
            alert("Could not get location: " + e.message);
        });
    }
}
