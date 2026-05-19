/**
 * Shared JS for User Engagement Actions
 * Handles: Favorite Toggling, Visit Logging Modal
 */

document.addEventListener('DOMContentLoaded', () => {
    const favoriteBtn = document.getElementById('toggle-favorite');
    const visitBtn = document.getElementById('open-visit-modal');
    const modal = document.getElementById('visit-modal');
    const modalContent = document.getElementById('visit-modal-content');
    const closeBtn = document.getElementById('close-visit-modal');
    const backdrop = document.getElementById('visit-modal-backdrop');
    const visitForm = document.getElementById('visit-form');
    const visitFeedback = document.getElementById('visit-feedback');
    const submitBtn = document.getElementById('submit-visit');
    const submitText = document.getElementById('submit-visit-text');
    const submitSpinner = document.getElementById('submit-visit-spinner');

    // -- Favorite Toggle Logic --
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', async () => {
            const targetId = favoriteBtn.dataset.id;
            const targetType = favoriteBtn.dataset.type;
            
            // Add loading state
            favoriteBtn.disabled = true;
            favoriteBtn.style.opacity = '0.7';

            try {
                const response = await fetch('/user/favorites/toggle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                    },
                    body: JSON.stringify({
                        target_id: targetId,
                        target_type: targetType
                    })
                });

                const result = await response.json();

                if (result.success) {
                    // Update UI state
                    const isFavorite = result.action === 'added';
                    const svg = favoriteBtn.querySelector('svg');
                    
                    if (isFavorite) {
                        if (favoriteBtn.classList.contains('fav-icon-only')) {
                            favoriteBtn.classList.add('is-favorited');
                            if (svg) {
                                svg.setAttribute('fill', 'currentColor');
                                svg.classList.add('text-red-500', 'fill-red-500', 'stroke-red-500');
                                svg.classList.remove('fill-none');
                            }
                        } else {
                            favoriteBtn.classList.remove('bg-transparent', 'border-white/20', 'text-white', 'bg-emerald-900/30');
                            favoriteBtn.classList.add('bg-red-500', 'border-red-500', 'text-white');
                            // For business detail which has lighter theme
                            favoriteBtn.classList.add('bg-red-500/20', 'border-red-500/50', 'text-red-300');
                            
                            svg.classList.add('fill-current');
                            svg.classList.remove('fill-none');
                            favoriteBtn.innerHTML = `
                                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                </svg>
                                Saved
                            `;
                        }
                    } else {
                        // Revert classes - this is tricky because of different page themes
                        // We'll just reload the page for now to keep it simple and consistent with the theme
                        location.reload();
                        return;
                    }
                } else {
                    alert(result.error || 'Something went wrong.');
                }
            } catch (err) {
                console.error('Favorite Toggle Error:', err);
                alert('Network error. Please try again.');
            } finally {
                favoriteBtn.disabled = false;
                favoriteBtn.style.opacity = '1';
            }
        });
    }

    // -- Visit Modal Logic --
    const openModal = () => {
        if (!modal) return;
        modal.classList.remove('hidden');
        // Small timeout to allow 'hidden' to be removed before adding 'active' for transitions
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
        document.body.style.overflow = 'hidden';
        
        // Pre-fill target data from favorite button or similar
        const targetId = favoriteBtn?.dataset.id || '';
        const targetType = favoriteBtn?.dataset.type || '';
        
        document.getElementById('visit-target-id').value = targetId;
        document.getElementById('visit-target-type').value = targetType;
        document.getElementById('visit-date').valueAsDate = new Date();
    };

    const closeModal = () => {
        if (!modal) return;
        modal.classList.remove('active');
        // Wait for transition before adding hidden
        setTimeout(() => {
            if (!modal.classList.contains('active')) {
                modal.classList.add('hidden');
            }
        }, 300);
        document.body.style.overflow = '';
        visitFeedback.classList.add('hidden');
    };

    if (visitBtn) visitBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    // -- Visit Form Submission --
    if (visitForm) {
        visitForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            submitBtn.disabled = true;
            submitText.textContent = 'Saving...';
            submitSpinner.classList.remove('hidden');
            visitFeedback.classList.add('hidden');

            const formData = {
                target_id: document.getElementById('visit-target-id').value,
                target_type: document.getElementById('visit-target-type').value,
                visit_date: document.getElementById('visit-date').value,
                notes: document.getElementById('visit-notes').value
            };

            try {
                const response = await fetch('/user/visits/log', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.success) {
                    visitFeedback.textContent = 'Journey log updated!';
                    visitFeedback.className = 'block text-sm font-bold text-center text-emerald-600 mb-4';
                    visitFeedback.classList.remove('hidden');
                    
                    setTimeout(() => {
                        closeModal();
                        // Reset form
                        visitForm.reset();
                    }, 1500);
                } else {
                    visitFeedback.textContent = result.error || 'Failed to log visit.';
                    visitFeedback.className = 'block text-sm font-bold text-center text-red-600 mb-4';
                    visitFeedback.classList.remove('hidden');
                }
            } catch (err) {
                console.error('Visit Log Error:', err);
                visitFeedback.textContent = 'Network error. Please try again.';
                visitFeedback.className = 'block text-sm font-bold text-center text-red-600 mb-4';
                visitFeedback.classList.remove('hidden');
            } finally {
                submitBtn.disabled = false;
                submitText.textContent = 'Log this Visit';
                submitSpinner.classList.add('hidden');
            }
        });
    }
});
