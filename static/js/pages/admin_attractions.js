/**
 * Admin Attractions JavaScript
 */
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('attractionSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.attraction-row');

            rows.forEach(row => {
                const nameNode = row.querySelector('.attraction-name');
                const categoryNode = row.querySelector('.attraction-category');

                if (nameNode && categoryNode) {
                    const name = nameNode.textContent.toLowerCase();
                    const category = categoryNode.textContent.toLowerCase();

                    if (name.includes(searchTerm) || category.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            });

            // Handle empty table after search
            // const visibleRows = document.querySelectorAll('.attraction-row:not([style*="display: none"])');
            // Optional: you could show a "No results" row here if visibleRows.length === 0
        });
    }
});
