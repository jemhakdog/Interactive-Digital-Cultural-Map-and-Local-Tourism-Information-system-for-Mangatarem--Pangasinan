// User navigation dropdown toggle (user_nav.html)
(function() {
    'use strict';

    // Prevent multiple initializations
    if (window.userNavInitialized) return;
    window.userNavInitialized = true;

    function initUserNav() {
        const dropdowns = document.querySelectorAll('.user-more-dropdown');
        
        dropdowns.forEach(dropdown => {
            const menu = dropdown.querySelector('.user-more-menu');
            const chevron = dropdown.querySelector('.user-dropdown-chevron');
            const toggleBtn = dropdown.querySelector('.user-more-toggle');

            if (!menu || !chevron || !toggleBtn) return;

            function toggleMenu(e) {
                e.stopPropagation();
                const isHidden = menu.classList.contains('hidden');
                
                // Close other open user dropdowns first
                document.querySelectorAll('.user-more-menu').forEach(otherMenu => {
                    if (otherMenu !== menu) {
                        otherMenu.classList.add('hidden');
                        const otherChevron = otherMenu.parentElement.querySelector('.user-dropdown-chevron');
                        if (otherChevron) otherChevron.style.transform = 'rotate(0deg)';
                    }
                });

                menu.classList.toggle('hidden', !isHidden);
                chevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                
                // Also close admin dropdowns if they exist to avoid overlaps
                document.querySelectorAll('.admin-more-menu').forEach(adminMenu => {
                    adminMenu.classList.add('hidden');
                    const adminChevron = adminMenu.parentElement.querySelector('.more-dropdown-chevron');
                    if (adminChevron) adminChevron.style.transform = 'rotate(0deg)';
                });
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
        document.addEventListener('DOMContentLoaded', initUserNav);
    } else {
        initUserNav();
    }
})();
