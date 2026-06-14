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
            ? filtered.map(b => {
                const code = `BRGY-${b.name.substring(0, 3).toUpperCase()}-${b.name.length * 12 + 100}`;
                const brgyClass = b.attraction_count > 3 ? 'Urban' : 'Rural';
                const eventsCount = Math.floor(b.attraction_count * 2 / 3) || 1;
                const tagsHtml = (b.tags || []).slice(0, 2).map(tag => 
                    `<span class="text-[10px] font-bold uppercase tracking-wider bg-[#2d2d2d] text-gray-300 px-2 py-0.5 rounded-full">${tag}</span>`
                ).join('');

                return `
                <div class="discovery-card">
                    <!-- Feature image: large, beautifully-rounded -->
                    <div class="relative w-full aspect-video rounded-xl overflow-hidden mb-4">
                        <img src="${b.image_url || 'https://placehold.co/400x250?text=' + b.name}" class="w-full h-full object-cover" alt="${b.name}">
                    </div>
                    
                    <!-- Barangay name left of a lime-green View button -->
                    <div class="flex justify-between items-center mb-4 gap-2">
                        <h4 class="text-lg font-bold text-white leading-tight truncate">${b.name}</h4>
                        <a href="/barangay/${b.name}" class="inline-flex items-center justify-center bg-[#a3e635] text-black hover:bg-[#85e024] font-semibold px-4 py-1.5 rounded-xl text-xs transition-colors duration-200 shrink-0">View</a>
                    </div>

                    <!-- Labeled statistics boxes: small dark containers -->
                    <div class="grid grid-cols-3 gap-2 mb-4">
                        <div class="bg-[#121212] border border-[#222222] rounded-xl p-2 text-center">
                            <span class="block text-[9px] uppercase tracking-wider text-gray-500 font-bold">Spots</span>
                            <span class="text-xs font-bold text-white">${b.attraction_count || 0}</span>
                        </div>
                        <div class="bg-[#121212] border border-[#222222] rounded-xl p-2 text-center">
                            <span class="block text-[9px] uppercase tracking-wider text-gray-500 font-bold">Events</span>
                            <span class="text-xs font-bold text-white">${eventsCount}</span>
                        </div>
                        <div class="bg-[#121212] border border-[#222222] rounded-xl p-2 text-center">
                            <span class="block text-[9px] uppercase tracking-wider text-gray-500 font-bold">Class</span>
                            <span class="text-xs font-bold text-white">${brgyClass}</span>
                        </div>
                    </div>

                    <!-- Key information fields at the bottom -->
                    <div class="space-y-2 pt-3 border-t border-[#2d2d2d]/60 font-sans">
                        <div class="flex items-center justify-between gap-2">
                            <span class="text-[10px] text-gray-400 font-mono bg-[#121212] border border-[#222222] px-2.5 py-1 rounded-lg">Code: ${code}</span>
                            <div class="flex flex-wrap gap-1 max-w-[60%] justify-end">
                                ${tagsHtml}
                            </div>
                        </div>
                    </div>
                </div>
                `;
            }).join('')
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
