/**
 * Global Delete Confirmation
 * Uses SweetAlert2 with fallback to native confirm
 */

// Define confirmDelete globally for backwards compatibility
window.confirmDelete = function(url, message = "You won't be able to revert this!") {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Are you sure?',
            text: message,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444', // Tailwind Rose 500
            cancelButtonColor: '#6b7280',  // Tailwind Gray 500
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel',
            customClass: {
                popup: 'rounded-3xl shadow-xl border border-gray-100'
            }
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = url;
            }
        });
    } else {
        // Fallback to native browser confirmation if SweetAlert2 is not loaded
        if (confirm(message)) {
            window.location.href = url;
        }
    }
};

// Automatically attach SweetAlert2 to elements with data-delete-url globally
(function() {
    'use strict';

    function initDeleteConfirmations() {
        document.addEventListener('click', function(e) {
            // Find closest element with data-delete-url attribute
            const deleteBtn = e.target.closest('[data-delete-url]');
            if (!deleteBtn) return;

            e.preventDefault();
            const url = deleteBtn.dataset.deleteUrl;
            const message = deleteBtn.dataset.deleteMessage || deleteBtn.dataset.msg || "You won't be able to revert this!";
            
            window.confirmDelete(url, message);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDeleteConfirmations);
    } else {
        initDeleteConfirmations();
    }
})();

