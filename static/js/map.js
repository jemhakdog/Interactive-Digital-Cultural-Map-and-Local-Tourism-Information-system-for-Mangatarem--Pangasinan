document.addEventListener('DOMContentLoaded', function () {
    // Sidebar Toggle Functionality
    const sidebar = document.getElementById('attractions-sidebar');
    const toggleBtn = document.getElementById('toggle-sidebar');
    const openBtn = document.getElementById('open-sidebar-btn');
    const toggleIconClose = document.getElementById('toggle-icon-close');
    const toggleIconOpen = document.getElementById('toggle-icon-open');
    const mapContainer = document.getElementById('map');

    let sidebarCollapsed = false;

    function toggleSidebar() {
        sidebarCollapsed = !sidebarCollapsed;

        if (sidebarCollapsed) {
            // Collapse sidebar to the left
            sidebar.classList.add('md:-translate-x-full', 'md:w-0', 'md:min-w-0');
            sidebar.classList.remove('md:w-1/3', 'lg:w-1/4');
            mapContainer.classList.remove('md:w-2/3', 'lg:w-3/4');
            mapContainer.classList.add('md:w-full');
            openBtn.classList.remove('md:hidden');
            openBtn.classList.add('md:block');

            // Swap icons
            toggleIconClose.classList.add('hidden');
            toggleIconOpen.classList.remove('hidden');
        } else {
            // Expand sidebar
            sidebar.classList.remove('md:-translate-x-full', 'md:w-0', 'md:min-w-0');
            sidebar.classList.add('md:w-1/3', 'lg:w-1/4');
            mapContainer.classList.add('md:w-2/3', 'lg:w-3/4');
            mapContainer.classList.remove('md:w-full');
            openBtn.classList.add('md:hidden');
            openBtn.classList.remove('md:block');

            // Swap icons
            toggleIconClose.classList.remove('hidden');
            toggleIconOpen.classList.add('hidden');
        }

        // Invalidate map size after animation completes
        setTimeout(() => {
            map.invalidateSize();
        }, 300);
    }

    toggleBtn.addEventListener('click', toggleSidebar);
    openBtn.addEventListener('click', toggleSidebar);

    // Initialize Map centered on Mangatarem
    const map = L.map('map').setView([15.7889, 120.2986], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let markers = [];
    let attractionsData = [];

    // Fetch attractions
    fetch('/api/attractions')
        .then(response => response.json())
        .then(data => {
            attractionsData = data;
            renderList(data);
            addMarkers(data);
        })
        .catch(error => console.error('Error fetching attractions:', error));

    const listContainer = document.getElementById('attractions-list');
    const searchInput = document.getElementById('search-input');
    const filterBtns = document.querySelectorAll('.filter-btn');

    function addMarkers(attractions) {
        // Clear existing markers
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];

        attractions.forEach(attraction => {
            const marker = L.marker([attraction.lat, attraction.lng])
                .addTo(map)
                .bindTooltip(`
                    <div class="flex gap-3 p-2 min-w-[250px] max-w-[300px] bg-white shadow-xl rounded-lg border border-gray-100">
                        <img src="${attraction.image}" class="w-20 h-20 object-cover rounded-md flex-shrink-0" alt="${attraction.name}">
                        <div class="flex flex-col justify-center overflow-hidden">
                            <h3 class="font-bold text-gray-800 text-sm leading-tight mb-1 truncate">${attraction.name}</h3>
                            <span class="inline-block bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded-full w-fit mb-1">${attraction.category}</span>
                            <p class="text-xs text-gray-500 line-clamp-2 leading-tight">${attraction.description}</p>
                        </div>
                    </div>
                `, {
                    direction: 'top',
                    offset: [0, -30],
                    className: 'custom-tooltip'
                });

            // Click to view details page
            marker.on('click', () => {
                window.location.href = `/attraction/${attraction.id}`;
            });

            markers.push(marker);
        });
    }

    function renderList(attractions) {
        listContainer.innerHTML = '';
        if (attractions.length === 0) {
            listContainer.innerHTML = '<div class="text-center text-gray-500">No attractions found.</div>';
            return;
        }

        attractions.forEach(attraction => {
            const item = document.createElement('div');
            item.className = 'bg-gray-50 p-3 rounded-lg hover:bg-green-50 cursor-pointer transition border border-gray-200';
            item.innerHTML = `
                <div class="flex gap-3">
                    <img src="${attraction.image}" class="w-20 h-20 object-cover rounded" alt="${attraction.name}">
                    <div>
                        <h4 class="font-bold text-gray-800">${attraction.name}</h4>
                        <span class="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">${attraction.category}</span>
                        <p class="text-xs text-gray-500 mt-1 line-clamp-2">${attraction.description}</p>
                    </div>
                </div>
            `;
            item.addEventListener('click', () => {
                // Fly to marker
                map.flyTo([attraction.lat, attraction.lng], 15);
                // Find and open popup
                // Note: This is a simple implementation. For better performance with many markers, use a map/dictionary.
                // Here we just re-create the popup or find the marker index if we tracked it better.
                // Let's just re-center for now.
            });
            listContainer.appendChild(item);
        });
    }

    const barangayFilter = document.getElementById('barangay-filter');
    let currentCategory = 'all';
    let currentBarangay = 'all';

    function filterAttractions() {
        const term = searchInput.value.toLowerCase();

        const filtered = attractionsData.filter(a => {
            const matchesSearch = a.name.toLowerCase().includes(term) || a.description.toLowerCase().includes(term);
            const matchesCategory = currentCategory === 'all' || a.category === currentCategory;
            const matchesBarangay = currentBarangay === 'all' || a.barangay === currentBarangay;

            return matchesSearch && matchesCategory && matchesBarangay;
        });

        renderList(filtered);
        addMarkers(filtered);
    }

    // Search functionality
    searchInput.addEventListener('input', filterAttractions);

    // Category Filter functionality
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterBtns.forEach(b => {
                b.classList.remove('bg-green-100', 'text-green-700');
                b.classList.add('bg-gray-100', 'text-gray-600');
            });
            btn.classList.remove('bg-gray-100', 'text-gray-600');
            btn.classList.add('bg-green-100', 'text-green-700');

            currentCategory = btn.dataset.category;
            filterAttractions();
        });
    });

    // Barangay Filter functionality
    if (barangayFilter) {
        barangayFilter.addEventListener('change', (e) => {
            currentBarangay = e.target.value;
            filterAttractions();
        });
    }
});
