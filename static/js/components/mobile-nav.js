/**
 * Mobile Navigation Toggle
 * Handles opening/closing of mobile menu
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');

        if (btn && menu) {
            btn.addEventListener('click', function() {
                menu.classList.toggle('hidden');
            });
        }
    });
})();
