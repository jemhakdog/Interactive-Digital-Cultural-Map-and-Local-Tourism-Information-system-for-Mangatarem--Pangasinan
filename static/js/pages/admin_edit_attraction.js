/**
 * Admin Edit Attraction JavaScript
 */
document.addEventListener('DOMContentLoaded', function () {
    const imageUpload = document.getElementById('imageUpload');
    const imageUrlInput = document.getElementById('imageUrlInput');
    const imagePreview = document.getElementById('imagePreview');
    const placeholder = document.getElementById('previewPlaceholder');

    function updatePreview(src) {
        if (src) {
            imagePreview.src = src;
            imagePreview.classList.remove('hidden');
            if (placeholder) placeholder.classList.add('hidden');
        }
    }

    if (imageUpload) {
        imageUpload.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    updatePreview(event.target.result);
                }
                reader.readAsDataURL(file);
            }
        });
    }

    if (imageUrlInput) {
        imageUrlInput.addEventListener('input', function () {
            if (this.value) {
                updatePreview(this.value);
            }
        });
    }
});
