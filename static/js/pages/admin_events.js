/**
 * Admin Events JavaScript
 */
document.addEventListener('DOMContentLoaded', function () {
    // Search functionality
    const eventSearch = document.getElementById('eventSearch');
    if (eventSearch) {
        eventSearch.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.event-row');

            rows.forEach(row => {
                const titleNode = row.querySelector('.event-title');
                const categoryNode = row.querySelector('.event-category');
                const locationNode = row.querySelector('.event-location');

                if (titleNode && categoryNode && locationNode) {
                    const title = titleNode.textContent.toLowerCase();
                    const category = categoryNode.textContent.toLowerCase();
                    const location = locationNode.textContent.toLowerCase();

                    if (title.includes(searchTerm) || category.includes(searchTerm) || location.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        });
    }
});

// Global function for confirmation
window.confirmAction = function(url, message = 'Are you sure you want to perform this action? This cannot be undone.') {
    if (confirm(message)) {
        window.location.href = url;
    }
}
