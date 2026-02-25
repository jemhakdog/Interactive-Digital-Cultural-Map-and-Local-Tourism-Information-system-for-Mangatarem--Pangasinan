/**
 * Admin Heritage JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // --- heritage_list.html ---
    const searchInput = document.getElementById('heritageSearch');
    const statusFilter = document.getElementById('statusFilter');
    const rows = document.querySelectorAll('.heritage-row');

    if (searchInput && statusFilter && rows.length > 0) {
        function filterTable() {
            const query = searchInput.value.toLowerCase();
            const status = statusFilter.value;

            rows.forEach(row => {
                const name = (row.dataset.name || '').toLowerCase();
                const rowStatus = row.dataset.status || '';
                
                const matchesSearch = name.includes(query);
                const matchesStatus = status === 'all' || rowStatus === status;

                if (matchesSearch && matchesStatus) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        searchInput.addEventListener('input', filterTable);
        statusFilter.addEventListener('change', filterTable);
    }
});
