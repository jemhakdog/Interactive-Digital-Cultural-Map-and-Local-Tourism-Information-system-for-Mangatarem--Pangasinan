/**
 * reviews.js — Interactive review system for attraction detail pages.
 * Handles: rating fetch + render, star selector, file drag-drop, AJAX submit.
 */

(function () {
  'use strict';

  // ─── DOM refs ────────────────────────────────────────────────────────────
  const section       = document.getElementById('reviews-section');
  if (!section) return;                         // page doesn't have reviews

  const attractionId  = section.dataset.attractionId;
  const feed          = document.getElementById('reviews-feed');
  const loading       = document.getElementById('reviews-loading');
  const summary       = document.getElementById('review-summary');
  const avgEl         = document.getElementById('avg-rating');
  const avgStarsEl    = document.getElementById('avg-stars');
  const totalEl       = document.getElementById('total-reviews');
  const distEl        = document.getElementById('rating-distribution');
  const loadMoreWrap  = document.getElementById('load-more-container');
  const loadMoreBtn   = document.getElementById('load-more-btn');

  // form elements (may be absent for guests)
  const form          = document.getElementById('review-form');
  const starSelector  = document.getElementById('star-selector');
  const ratingInput   = document.getElementById('rating-input');
  const ratingError   = document.getElementById('rating-error');
  const commentArea   = document.getElementById('review-comment');
  const charCount     = document.getElementById('char-count');
  const dropZone      = document.getElementById('drop-zone');
  const photoInput    = document.getElementById('photo-input');
  const photoPreview  = document.getElementById('photo-preview');
  const feedback      = document.getElementById('review-feedback');
  const submitBtn     = document.getElementById('review-submit');

  // ─── Pagination state ────────────────────────────────────────────────────
  let currentPage   = 1;
  let hasMore       = false;
  let isLoading     = false;

  // ─── Helpers ─────────────────────────────────────────────────────────────
  function starHTML(rating, total) {
    let html = '';
    for (let i = 1; i <= 5; i++) {
      html += `<svg class="w-4 h-4 ${i <= Math.round(rating) ? 'text-amber-400' : 'text-emerald-900/15'}" fill="currentColor" viewBox="0 0 20 20">
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
      </svg>`;
    }
    return html;
  }

  function timeAgo(isoString) {
    const date  = new Date(isoString + 'Z');
    const secs  = Math.floor((Date.now() - date.getTime()) / 1000);
    if (secs < 60)   return 'just now';
    if (secs < 3600) return `${Math.floor(secs / 60)}m ago`;
    if (secs < 86400) return `${Math.floor(secs / 3600)}h ago`;
    return date.toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  function renderReviewCard(r) {
    const initial = (r.username || 'V')[0].toUpperCase();
    const photosHTML = (r.photos || []).map(p =>
      `<a href="${p.url}" target="_blank" class="w-16 h-16 rounded-xl overflow-hidden flex-shrink-0 hover:scale-105 transition-transform">
         <img src="${p.url}" alt="Review photo" class="w-full h-full object-cover" loading="lazy">
       </a>`
    ).join('');

    return `<div class="bg-white border border-emerald-900/5 rounded-3xl p-8 shadow-sm hover:shadow-md transition-shadow">
      <div class="flex items-start gap-5">
        <div class="w-11 h-11 rounded-2xl bg-emerald-100 flex items-center justify-center text-emerald-700 font-black text-lg flex-shrink-0">
          ${initial}
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-3 flex-wrap mb-1">
            <span class="font-bold text-emerald-950 text-sm">${r.username || 'Visitor'}</span>
            <span class="flex items-center gap-0.5">${starHTML(r.rating)}</span>
            <span class="text-[10px] text-emerald-900/40 font-bold">${timeAgo(r.created_at)}</span>
          </div>
          ${r.comment ? `<p class="text-emerald-950/75 text-sm leading-relaxed mt-2">${r.comment}</p>` : ''}
          ${photosHTML ? `<div class="flex flex-wrap gap-2 mt-4">${photosHTML}</div>` : ''}
        </div>
      </div>
    </div>`;
  }

  function renderDistribution(dist, total) {
    let html = '';
    for (let i = 5; i >= 1; i--) {
      const count = dist[i] || 0;
      const pct   = total > 0 ? Math.round((count / total) * 100) : 0;
      html += `<div class="flex items-center gap-3 text-[11px] font-bold text-emerald-900/60 mb-2">
        <span class="w-4 text-right">${i}</span>
        <svg class="w-3 h-3 text-amber-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
        <div class="flex-1 bg-emerald-100 rounded-full h-2 overflow-hidden">
          <div class="h-full bg-amber-400 rounded-full transition-all duration-700" style="width:${pct}%"></div>
        </div>
        <span class="w-8">${count}</span>
      </div>`;
    }
    return html;
  }

  // ─── Fetch + render reviews ───────────────────────────────────────────────
  async function loadReviews(page = 1, append = false) {
    if (isLoading) return;
    isLoading = true;

    try {
      const res  = await fetch(`/attractions/${attractionId}/reviews?page=${page}&per_page=6`);
      const data = await res.json();

      // Summary
      if (data.summary && data.summary.total > 0) {
        avgEl.textContent       = data.summary.average;
        avgStarsEl.innerHTML    = starHTML(data.summary.average);
        totalEl.textContent     = `${data.summary.total} review${data.summary.total !== 1 ? 's' : ''}`;
        distEl.innerHTML        = renderDistribution(data.summary.distribution, data.summary.total);
        summary.classList.remove('hidden');
      }

      // Remove loading spinner on first load
      if (!append && loading) loading.remove();

      // No reviews state
      if (!append && data.reviews.length === 0) {
        feed.innerHTML = `<div class="py-12 text-center">
          <div class="text-4xl mb-3">💬</div>
          <p class="font-bold text-emerald-900/60 text-sm">No reviews yet.</p>
          <p class="text-emerald-900/30 text-[11px] mt-1">Be the first to share your experience!</p>
        </div>`;
        return;
      }

      // Render cards
      const html = data.reviews.map(renderReviewCard).join('');
      if (append) {
        feed.insertAdjacentHTML('beforeend', html);
      } else {
        feed.innerHTML = html;
      }

      // Pagination
      hasMore = data.pagination.has_next;
      currentPage = page;
      if (loadMoreWrap) {
        loadMoreWrap.classList.toggle('hidden', !hasMore);
      }
    } catch (err) {
      console.error('Reviews load error:', err);
      if (!append && loading) loading.remove();
    } finally {
      isLoading = false;
    }
  }

  // Initial load
  loadReviews(1);

  // Load more
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => loadReviews(currentPage + 1, true));
  }

  // ─── Star Selector ────────────────────────────────────────────────────────
  if (starSelector) {
    const starBtns = starSelector.querySelectorAll('.star-btn');

    starBtns.forEach(btn => {
      const val = parseInt(btn.dataset.value, 10);

      btn.addEventListener('mouseenter', () => highlightStars(val));
      btn.addEventListener('mouseleave', () => highlightStars(parseInt(ratingInput.value, 10) || 0));
      btn.addEventListener('click', () => {
        ratingInput.value = val;
        highlightStars(val);
        if (ratingError) ratingError.classList.add('hidden');
      });
    });

    function highlightStars(upTo) {
      starBtns.forEach(b => {
        const v = parseInt(b.dataset.value, 10);
        b.style.color = v <= upTo ? '#f59e0b' : '';
        b.style.textShadow = v <= upTo ? '0 0 8px rgba(245,158,11,0.4)' : '';
      });
    }
  }

  // ─── Char count ───────────────────────────────────────────────────────────
  if (commentArea && charCount) {
    commentArea.addEventListener('input', () => {
      const len = commentArea.value.length;
      charCount.textContent = `${len} / 1000`;
      if (len > 1000) commentArea.value = commentArea.value.slice(0, 1000);
    });
  }

  // ─── Photo drag & drop ────────────────────────────────────────────────────
  let selectedFiles = [];

  function addFiles(newFiles) {
    for (const file of newFiles) {
      if (selectedFiles.length >= 5) break;
      if (!file.type.startsWith('image/')) continue;
      if (file.size > 5 * 1024 * 1024) {
        showFeedback(`"${file.name}" exceeds 5MB limit.`, 'error');
        continue;
      }
      selectedFiles.push(file);
    }
    renderPreviews();
  }

  function renderPreviews() {
    if (!photoPreview) return;
    photoPreview.innerHTML = '';
    selectedFiles.forEach((file, idx) => {
      const url = URL.createObjectURL(file);
      const el  = document.createElement('div');
      el.className = 'relative w-20 h-20 rounded-2xl overflow-hidden shadow-md flex-shrink-0 group';
      el.innerHTML = `
        <img src="${url}" class="w-full h-full object-cover">
        <button type="button" data-idx="${idx}"
          class="remove-photo absolute top-1 right-1 w-6 h-6 bg-black/60 text-white rounded-full text-xs font-bold flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
          ✕
        </button>`;
      photoPreview.appendChild(el);
    });

    photoPreview.querySelectorAll('.remove-photo').forEach(btn => {
      btn.addEventListener('click', e => {
        selectedFiles.splice(parseInt(e.currentTarget.dataset.idx, 10), 1);
        renderPreviews();
      });
    });
  }

  if (dropZone) {
    dropZone.addEventListener('click', () => photoInput && photoInput.click());
    dropZone.addEventListener('dragover', e => {
      e.preventDefault();
      dropZone.classList.add('border-emerald-400', 'bg-emerald-50/50');
    });
    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('border-emerald-400', 'bg-emerald-50/50');
    });
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.classList.remove('border-emerald-400', 'bg-emerald-50/50');
      addFiles(Array.from(e.dataTransfer.files));
    });
  }

  if (photoInput) {
    photoInput.addEventListener('change', () => addFiles(Array.from(photoInput.files)));
  }

  // ─── Feedback toast ───────────────────────────────────────────────────────
  function showFeedback(msg, type = 'success') {
    if (!feedback) return;
    feedback.className = `mb-4 px-6 py-4 rounded-2xl text-sm font-bold
      ${type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                           : 'bg-red-50 text-red-700 border border-red-200'}`;
    feedback.textContent = msg;
    feedback.classList.remove('hidden');
    setTimeout(() => feedback.classList.add('hidden'), 6000);
  }

  // ─── Form submit ──────────────────────────────────────────────────────────
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();

      // Validate rating
      if (!ratingInput.value) {
        if (ratingError) ratingError.classList.remove('hidden');
        starSelector && starSelector.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      // Build FormData
      const fd = new FormData(form);
      // Replace photos with our curated list
      fd.delete('photos');
      selectedFiles.forEach(f => fd.append('photos', f));

      // UI loading state
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"/><path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" class="opacity-75"/></svg> Submitting...';
      }

      try {
        const res  = await fetch(form.action, { method: 'POST', body: fd });
        const data = await res.json();

        if (res.ok && data.success) {
          showFeedback('✅ ' + data.message, 'success');
          // Reset form
          form.reset();
          ratingInput.value = '';
          selectedFiles = [];
          renderPreviews();
          if (starSelector) {
            starSelector.querySelectorAll('.star-btn').forEach(b => {
              b.style.color = '';
              b.style.textShadow = '';
            });
          }
        } else {
          showFeedback('❌ ' + (data.error || 'Something went wrong. Please try again.'), 'error');
        }
      } catch (err) {
        showFeedback('❌ Network error. Please check your connection and try again.', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
          </svg> Submit Review`;
        }
      }
    });
  }

})();
