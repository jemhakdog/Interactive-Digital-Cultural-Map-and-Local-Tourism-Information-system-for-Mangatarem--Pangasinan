/**
 * Multimedia Gallery Interactions
 * Handles gallery filtering, sorting, and lightbox
 */
document.addEventListener('DOMContentLoaded', () => {
    // Premium Filtering Logic
    const filterBtns = document.querySelectorAll('.filter-btn');
    const barangayFilter = document.getElementById('barangay-filter');
    const sortFilter = document.getElementById('sort-filter');
    const galleryGrid = document.getElementById('gallery-grid');
    const items = Array.from(document.querySelectorAll('.gallery-item'));

    function applyFilters() {
        const activeFilterBtn = document.querySelector('.filter-btn.active');
        if (!activeFilterBtn) return;
        
        const typeFilter = activeFilterBtn.dataset.filter;
        const locationFilter = barangayFilter ? barangayFilter.value : 'all';

        items.forEach((item, index) => {
            const itemType = item.dataset.type;
            const itemLocation = item.dataset.barangay;

            const typeMatch = typeFilter === 'all' || itemType === typeFilter;
            const locationMatch = locationFilter === 'all' || itemLocation === locationFilter;

            if (typeMatch && locationMatch) {
                item.style.display = 'block';
                item.style.animationDelay = `${index * 50}ms`;
                item.classList.add('staggered-entry');
            } else {
                item.style.display = 'none';
                item.classList.remove('staggered-entry');
            }
        });
    }

    function applySort() {
        if (!sortFilter || !galleryGrid) return;
        const sortValue = sortFilter.value;
        const visibleItems = items.filter(item => item.style.display !== 'none');

        visibleItems.sort((a, b) => {
            const dateA = new Date(a.dataset.date);
            const dateB = new Date(b.dataset.date);
            return sortValue === 'newest' ? dateB - dateA : dateA - dateB;
        });

        visibleItems.forEach(item => galleryGrid.appendChild(item));
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => {
                b.classList.remove('active', 'bg-white', 'text-emerald-900', 'shadow-sm');
                b.classList.add('text-gray-500');
            });
            btn.classList.add('active', 'bg-white', 'text-emerald-900', 'shadow-sm');
            btn.classList.remove('text-gray-500');
            applyFilters();
        });
    });

    if (barangayFilter) barangayFilter.addEventListener('change', applyFilters);
    if (sortFilter) sortFilter.addEventListener('change', applySort);

    // Initial explicit global bind for inline clicks
    window.handleItemClick = handleItemClick;
    window.closeLightbox = closeLightbox;

    // Cinematic Lightbox Logic
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxVideo = document.getElementById('lightbox-video');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxLocation = document.getElementById('lightbox-location');
    const lightboxCredit = document.getElementById('lightbox-credit');

    function handleItemClick(el) {
        const url = el.dataset.url;
        const caption = el.dataset.caption;
        const type = el.dataset.type;
        const location = el.dataset.barangay;
        const credit = el.dataset.username;
        openLightbox(url, caption, type, location, credit);
    }

    function openLightbox(url, caption, type, location, credit) {
        if (!lightbox) return;
        lightbox.classList.remove('hidden');
        setTimeout(() => lightbox.classList.remove('opacity-0'), 10);

        if (lightboxCaption) lightboxCaption.textContent = caption;
        if (lightboxLocation) lightboxLocation.textContent = location;
        if (lightboxCredit) lightboxCredit.textContent = credit;

        if (type === 'photo') {
            if (lightboxImg) {
                lightboxImg.src = url;
                lightboxImg.classList.remove('hidden');
            }
            if (lightboxVideo) {
                lightboxVideo.classList.add('hidden');
                lightboxVideo.pause();
            }
        } else {
            if (lightboxVideo) {
                lightboxVideo.src = url;
                lightboxVideo.classList.remove('hidden');
                lightboxVideo.play();
            }
            if (lightboxImg) {
                lightboxImg.classList.add('hidden');
            }
        }

        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.add('opacity-0');
        setTimeout(() => {
            lightbox.classList.add('hidden');
            if (lightboxImg) lightboxImg.src = '';
            const video = lightboxVideo;
            if (video) {
                video.pause();
                video.src = '';
            }
        }, 500);
        document.body.style.overflow = '';
    }

    // Modal Events
    if (lightbox) {
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox || e.target.closest('.flex-col')) {
                if (e.target.tagName !== 'IMG' && e.target.tagName !== 'VIDEO' && !e.target.closest('h3')) {
                    // closeLightbox(); // Intentional comment in original
                }
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });
});
