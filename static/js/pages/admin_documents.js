/**
 * Admin Documents JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // --- documents_dashboard.html ---
    const docSearch = document.getElementById('doc-search');
    if (docSearch) {
        docSearch.addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.document-row');
            
            rows.forEach(row => {
                const label = row.getAttribute('data-label') || '';
                const category = row.getAttribute('data-category') || '';
                
                if (label.includes(term) || category.includes(term)) {
                    row.style.display = 'table-row';
                    row.style.opacity = '1';
                    row.style.transform = 'translateY(0)';
                } else {
                    row.style.display = 'none';
                    row.style.opacity = '0';
                    row.style.transform = 'translateY(10px)';
                }
            });
        });
    }

    // --- documents_edit.html ---
    const textarea = document.getElementById('json_editor');
    const badge = document.getElementById('json-badge');
    const submitBtn = document.getElementById('submit-btn');

    if (textarea && badge && submitBtn) {
        textarea.addEventListener('input', function() {
            try {
                JSON.parse(textarea.value);
                badge.textContent = 'VALID';
                badge.className = 'px-2 py-0.5 bg-emerald-500/10 text-emerald-400 text-[10px] rounded border border-emerald-500/20 font-mono';
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } catch (e) {
                badge.textContent = 'INVALID';
                badge.className = 'px-2 py-0.5 bg-red-500/10 text-red-400 text-[10px] rounded border border-red-500/20 font-mono';
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
            }
        });
    }

    // --- documents_editor.html ---
    const documentCanvas = document.getElementById('document-canvas');
    if (documentCanvas) {
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                if (typeof window.saveDocument === 'function') {
                    window.saveDocument();
                }
            }
        });
    }
});

// Global functions
window.updateFileName = function() {
    const input = document.getElementById('fileInput');
    const display = document.getElementById('fileName');
    if (input && display && input.files[0]) {
        display.innerText = input.files[0].name;
        display.classList.add('text-emerald-600');
    }
};

window.formatJSON = function() {
    const textarea = document.getElementById('json_editor');
    if (textarea) {
        try {
            const obj = JSON.parse(textarea.value);
            textarea.value = JSON.stringify(obj, null, 2);
        } catch (e) {
            alert('Cannot format invalid JSON');
        }
    }
};

window.saveDocument = function() {
    const data = {
        paragraphs: [],
        tables: []
    };
    
    // Collect paragraphs
    document.querySelectorAll('.document-para').forEach((el) => {
        const indexStr = el.dataset.index;
        if (indexStr) {
            data.paragraphs.push({
                index: parseInt(indexStr),
                text: el.innerText.trim(),
                style: "Normal"
            });
        }
    });
    
    // Collect tables
    document.querySelectorAll('.document-table').forEach((table) => {
        const indexStr = table.dataset.index;
        if (indexStr) {
            const tableData = {
                table_index: parseInt(indexStr),
                rows: table.rows.length,
                columns: table.rows.length > 0 ? table.rows[0].cells.length : 0,
                content: []
            };
            
            Array.from(table.rows).forEach((row) => {
                const rowData = Array.from(row.cells).map(cell => cell.innerText.trim());
                tableData.content.push(rowData);
            });
            
            data.tables.push(tableData);
        }
    });
    
    // Set in hidden input and submit
    const inputStr = document.getElementById('structured_data_input');
    const form = document.getElementById('save-form');
    if (inputStr && form) {
        inputStr.value = JSON.stringify(data);
        form.submit();
    }
};
