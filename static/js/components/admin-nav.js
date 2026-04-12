// Admin navigation dropdown toggle (admin_nav.html)
(function() {
    'use strict';

    function initAdminNav() {
        const dropdown = document.getElementById('admin-more-dropdown');
        if (!dropdown) return;

        const menu = document.getElementById('admin-more-menu');
        const chevron = document.getElementById('more-dropdown-chevron');
        const toggleBtn = dropdown.querySelector('button');

        if (!menu || !chevron || !toggleBtn) return;

        function toggleMenu() {
            const isHidden = menu.classList.contains('hidden');
            menu.classList.toggle('hidden', !isHidden);
            chevron.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
        }

        function closeMenu() {
            menu.classList.add('hidden');
            chevron.style.transform = 'rotate(0deg)';
        }

        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleMenu();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!dropdown.contains(event.target)) {
                closeMenu();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAdminNav);
    } else {
        initAdminNav();
    }
})();
