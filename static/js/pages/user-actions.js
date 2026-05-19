/**
 * Shared JS for User Engagement Actions
 * Handles: Favorite Toggling, Visit Logging Modal
 */

document.addEventListener('DOMContentLoaded', () => {
    const favoriteBtns = document.querySelectorAll('#toggle-favorite, #info-toggle-favorite, .toggle-favorite');
    const visitBtns = document.querySelectorAll('#open-visit-modal, #info-open-visit-modal, .open-visit-modal');
    const modal = document.getElementById('visit-modal');
    const closeBtn = document.getElementById('close-visit-modal');
    const backdrop = document.getElementById('visit-modal-backdrop');
    const visitForm = document.getElementById('visit-form');
    const visitFeedback = document.getElementById('visit-feedback');
    const submitBtn = document.getElementById('submit-visit');
    const submitText = document.getElementById('submit-visit-text');
    const submitSpinner = document.getElementById('submit-visit-spinner');

    // -- Favorite Toggle Logic --
    favoriteBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const targetId = btn.dataset.id;
            const targetType = btn.dataset.type;
            
            if (!targetId || !targetType) return;

            // Add loading state across all matching buttons
            favoriteBtns.forEach(b => {
                b.disabled = true;
                b.style.opacity = '0.7';
            });

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
                    const isFavorite = result.action === 'added';
                    
                    // Synchronously update all favorite buttons in the DOM
                    favoriteBtns.forEach(b => {
                        const svg = b.querySelector('svg');
                        
                        if (isFavorite) {
                            if (b.classList.contains('fav-icon-only')) {
                                b.classList.add('is-favorited');
                                if (svg) {
                                    svg.setAttribute('fill', 'currentColor');
                                    svg.className.value = 'w-5 h-5 text-red-500 fill-red-500 stroke-red-500';
                                }
                            } else {
                                b.className = 'flex-1 flex items-center justify-center gap-2 py-3 border rounded-2xl text-xs font-bold transition-colors bg-red-50 text-red-500 border-red-200 hover:bg-red-100/50';
                                if (svg) {
                                    svg.className.value = 'w-4 h-4 fill-current text-red-500';
                                }
                                const span = b.querySelector('span');
                                if (span) span.textContent = 'Saved';
                            }
                        } else {
                            if (b.classList.contains('fav-icon-only')) {
                                b.classList.remove('is-favorited');
                                if (svg) {
                                    svg.setAttribute('fill', 'none');
                                    svg.className.value = 'w-5 h-5';
                                }
                            } else {
                                b.className = 'flex-1 flex items-center justify-center gap-2 py-3 border rounded-2xl text-xs font-bold transition-colors border-gray-200 text-gray-600 hover:bg-gray-50 hover:border-red-200 hover:text-red-500';
                                if (svg) {
                                    svg.className.value = 'w-4 h-4 fill-none';
                                }
                                const span = b.querySelector('span');
                                if (span) span.textContent = 'Favorite';
                            }
                        }
                    });
                    
                    // If on map, trigger bookmark refetch, otherwise reload to fully reflect visual state
                    if (window.location.pathname.includes('/map') && typeof window.fetchBookmarks === 'function') {
                        window.fetchBookmarks();
                    } else if (result.action === 'removed') {
                        location.reload();
                    }
                } else {
                    alert(result.error || 'Something went wrong.');
                }
            } catch (err) {
                console.error('Favorite Toggle Error:', err);
                alert('Network error. Please try again.');
            } finally {
                favoriteBtns.forEach(b => {
                    b.disabled = false;
                    b.style.opacity = '1';
                });
            }
        });
    });

    // -- Visit Modal Logic --
    const openModal = (e) => {
        if (!modal) return;
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
        document.body.style.overflow = 'hidden';
        
        // Get attributes from clicked element
        const clickedBtn = e.currentTarget;
        const targetId = clickedBtn.dataset.id || '';
        const targetType = clickedBtn.dataset.type || '';
        
        document.getElementById('visit-target-id').value = targetId;
        document.getElementById('visit-target-type').value = targetType;
        document.getElementById('visit-date').valueAsDate = new Date();
    };

    const closeModal = () => {
        if (!modal) return;
        modal.classList.remove('active');
        setTimeout(() => {
            if (!modal.classList.contains('active')) {
                modal.classList.add('hidden');
            }
        }, 300);
        document.body.style.overflow = '';
        visitFeedback.classList.add('hidden');
    };

    // Attach event listeners to any elements that can open or close the modal
    visitBtns.forEach(btn => btn.addEventListener('click', openModal));
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
                        visitForm.reset();
                        
                        // Smart non-disruptive refresh on Map page, reload on attraction details
                        if (window.location.pathname.includes('/map') && typeof window.fetchBookmarks === 'function') {
                            window.fetchBookmarks();
                        } else {
                            location.reload();
                        }
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
