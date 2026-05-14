// Admin navigation dropdown toggle (admin_nav.html)
(function() {
    'use strict';

    // Prevent multiple initializations
    if (window.adminNavInitialized) return;
    window.adminNavInitialized = true;

    function initAdminNav() {
        const dropdowns = document.querySelectorAll('.admin-more-dropdown');
        
        dropdowns.forEach(dropdown => {
            const menu = dropdown.querySelector('.admin-more-menu');
            const chevron = dropdown.querySelector('.more-dropdown-chevron');
            const toggleBtn = dropdown.querySelector('.admin-more-toggle');

            if (!menu || !chevron || !toggleBtn) return;

            function toggleMenu(e) {
                e.stopPropagation();
                const isHidden = menu.classList.contains('hidden');
                
                // Close other open admin dropdowns first
                document.querySelectorAll('.admin-more-menu').forEach(otherMenu => {
                    if (otherMenu !== menu) {
                        otherMenu.classList.add('hidden');
                        const otherChevron = otherMenu.parentElement.querySelector('.more-dropdown-chevron');
                        if (otherChevron) otherChevron.style.transform = 'rotate(0deg)';
                    }
                });

                menu.classList.toggle('hidden', !isHidden);
                chevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
            }

            function closeMenu() {
                menu.classList.add('hidden');
                chevron.style.transform = 'rotate(0deg)';
            }

            toggleBtn.addEventListener('click', toggleMenu);
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!dropdown.contains(event.target)) {
                    closeMenu();
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAdminNav);
    } else {
        initAdminNav();
    }
})();
