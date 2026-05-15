/**
 * Barangay Directory - Mobile Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('mobileBarangaySearch');
    const filterBtn = document.getElementById('mobileFilterBtn');
    const bottomSheet = document.getElementById('filterBottomSheet');
    const sheetOverlay = document.getElementById('sheetOverlay');
    const closeSheetBtn = document.getElementById('applyFiltersBtn');
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    
    const popularGrid = document.getElementById('popularBarangays');
    const discoveryList = document.getElementById('discoveryList');
    
    // Data store access
    const dataStore = document.getElementById('barangays-data-store');
    const allBarangays = JSON.parse(dataStore.dataset.barangays || '[]');

    /**
     * Filter Logic
     */
    let activeCategory = 'all';
    let searchQuery = '';

    const renderBarangays = () => {
        const filtered = allBarangays.filter(b => {
            const matchesSearch = b.name.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesCategory = activeCategory === 'all' || (b.tags && b.tags.includes(activeCategory));
            return matchesSearch && matchesCategory;
        });

        // Update Discovery List
        discoveryList.innerHTML = filtered.length > 0 
            ? filtered.map(b => `
                <a href="/barangay/${b.name}" class="discovery-card !mb-0">
                    <img src="${b.image_url || 'https://placehold.co/100x100?text=' + b.name}" class="discovery-card-img" alt="${b.name}">
                    <div class="discovery-card-content">
                        <h4>${b.name}</h4>
                        <div class="discovery-card-meta">
                            <span>📍 Mangatarem</span>
                            <span>🏰 ${b.attraction_count} Spots</span>
                        </div>
                    </div>
                </a>
            `).join('')
            : '<div class="col-span-full text-center py-10 text-gray-400 font-serif italic">No locations found matching your search.</div>';
    };

    // Search input handler
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value;
            renderBarangays();
        });
    }

    // Bottom Sheet Handlers (Mobile only)
    const closeSheet = () => {
        if (bottomSheet) bottomSheet.classList.remove('active');
        if (sheetOverlay) sheetOverlay.classList.remove('active');
        document.body.style.overflow = '';
    };

    if (filterBtn) {
        filterBtn.addEventListener('click', () => {
            bottomSheet.classList.add('active');
            sheetOverlay.classList.add('active');
            document.body.style.overflow = 'hidden'; 
        });
    }

    if (sheetOverlay) sheetOverlay.addEventListener('click', closeSheet);
    
    if (closeSheetBtn) {
        closeSheetBtn.addEventListener('click', () => {
            closeSheet();
            renderBarangays();
        });
    }

    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', () => {
            activeCategory = 'all';
            document.querySelectorAll('.filter-chip').forEach(c => {
                c.classList.toggle('active', c.dataset.category === 'all');
            });
            closeSheet();
            renderBarangays();
        });
    }

    // Category Chip Selection (Works for both Sidebar and Bottom Sheet)
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            // Find ALL chips with this category (both in sidebar and bottom sheet)
            const category = chip.dataset.category;
            
            // Update UI for all chips
            document.querySelectorAll('.filter-chip').forEach(c => {
                c.classList.toggle('active', c.dataset.category === category);
            });
            
            activeCategory = category;
            
            // If on desktop, render immediately. On mobile, wait for "Apply" button or render immediately?
            // Usually desktop should be instant. 
            if (window.innerWidth >= 768) {
                renderBarangays();
            }
        });
    });

    // Smooth Scroll for "See all" link
    document.querySelectorAll('.view-all-link').forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Initial Render
    renderBarangays();
});
