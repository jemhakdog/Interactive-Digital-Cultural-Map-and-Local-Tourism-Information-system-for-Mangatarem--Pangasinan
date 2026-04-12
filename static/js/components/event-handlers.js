// Universal event handler delegation for inline onclick/onsubmit/onchange
// This replaces all inline event handlers with delegated listeners

(function() {
    'use strict';

    function initEventHandlers() {
        document.addEventListener('click', handleClick);
        document.addEventListener('submit', handleSubmit);
        document.addEventListener('change', handleChange);
    }

    function handleClick(e) {
        const target = e.target.closest('[data-action]');
        if (!target) return;

        const action = target.dataset.action;

        switch (action) {
            case 'scroll-to-top':
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
                break;

            case 'toggle-modal':
                e.preventDefault();
                const modalId = target.dataset.modalId;
                const modal = document.getElementById(modalId);
                if (modal) modal.classList.toggle('hidden');
                break;

            case 'close-modal':
                e.preventDefault();
                const closeId = target.dataset.modalId;
                const closeBtnModal = document.getElementById(closeId);
                if (closeBtnModal) closeBtnModal.classList.add('hidden');
                break;

            case 'open-modal':
                e.preventDefault();
                const openId = target.dataset.modalId;
                const openModal = document.getElementById(openId);
                if (openModal) openModal.classList.remove('hidden');
                break;

            case 'draw-route':
                e.preventDefault();
                const routeType = target.dataset.routeType;
                if (typeof drawRoute === 'function') drawRoute(routeType);
                break;

            case 'clear-routes':
                e.preventDefault();
                if (typeof clearRoutes === 'function') clearRoutes();
                break;

            case 'change-map-style':
                e.preventDefault();
                const style = target.dataset.mapStyle;
                if (typeof changeMapStyle === 'function') changeMapStyle(style);
                break;

            case 'add-to-calendar':
                e.preventDefault();
                const title = target.dataset.eventTitle;
                const location = target.dataset.eventLocation;
                const date = target.dataset.eventDate;
                if (typeof addToCalendar === 'function') addToCalendar(title, location, date);
                break;

            case 'handle-item-click':
                e.preventDefault();
                if (typeof handleItemClick === 'function') handleItemClick(target);
                break;

            case 'close-lightbox':
                e.preventDefault();
                if (typeof closeLightbox === 'function') closeLightbox();
                break;

            case 'format-json':
                e.preventDefault();
                if (typeof formatJSON === 'function') formatJSON();
                break;

            case 'save-document':
                e.preventDefault();
                if (typeof saveDocument === 'function') saveDocument();
                break;

            case 'toggle-barangay':
                e.preventDefault();
                const select = target;
                if (typeof toggleBarangay === 'function') toggleBarangay(select);
                break;

            case 'update-file-name':
                const fileInput = target;
                if (fileInput.files && fileInput.files.length > 0) {
                    const label = target.dataset.labelId;
                    const labelEl = document.getElementById(label);
                    if (labelEl) labelEl.textContent = fileInput.files[0].name;
                }
                break;
        }
    }

    function handleSubmit(e) {
        const form = e.target;
        const action = form.dataset.action;

        switch (action) {
            case 'confirm-delete':
                const message = form.dataset.confirmMessage || 'Are you sure?';
                if (!confirm(message)) e.preventDefault();
                break;

            case 'auto-submit':
                // Form submits normally, no prevention needed
                break;

            case 'newsletter-submit':
                e.preventDefault();
                if (typeof handleNewsletterSubmit === 'function') {
                    handleNewsletterSubmit(e);
                } else {
                    form.submit();
                }
                break;
        }
    }

    function handleChange(e) {
        const target = e.target;

        if (target.dataset.action === 'auto-submit-form') {
            const form = target.closest('form');
            if (form) form.submit();
        }

        if (target.dataset.action === 'update-file-name') {
            handleClick(e);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEventHandlers);
    } else {
        initEventHandlers();
    }
})();
