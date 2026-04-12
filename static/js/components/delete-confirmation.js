// Generic delete confirmation using SweetAlert2
// This replaces inline confirmDelete functions

(function() {
    'use strict';

    function initDeleteConfirmations() {
        document.addEventListener('click', function(e) {
            const deleteBtn = e.target.closest('[data-delete-url]');
            if (!deleteBtn) return;

            e.preventDefault();
            const url = deleteBtn.dataset.deleteUrl;
            const message = deleteBtn.dataset.deleteMessage || 'Are you sure you want to delete this item? This action cannot be undone.';

            if (confirm(message)) {
                window.location.href = url;
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDeleteConfirmations);
    } else {
        initDeleteConfirmations();
    }
})();
