/**
 * Home Page Interactions
 * Handles scroll reveals, AOS initialization, and newsletter submission
 */
document.addEventListener('DOMContentLoaded', function () {
    // Intersection Observer for Scroll Reveals
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });

    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
    }

    // Newsletter form handler
    window.handleNewsletterSubmit = async function (event) {
        event.preventDefault();
        const form = event.target;
        const input = form.querySelector('input[type="email"]');
        const button = form.querySelector('button');
        const email = input.value;
        const originalButtonText = button.innerHTML;

        try {
            // Loading state
            button.disabled = true;
            button.innerHTML = '<span class="animate-pulse">Subscribing...</span>';

            const response = await fetch('/notifications/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `email=${encodeURIComponent(email)}`
            });

            const data = await response.json();

            if (response.ok) {
                // Success
                button.innerHTML = 'Success!';
                
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        title: 'Joined Successfully! 🌿',
                        text: data.message,
                        icon: 'success',
                        background: '#0a1a14',
                        color: '#ecfdf5',
                        confirmButtonColor: '#059669',
                        customClass: {
                            popup: 'border border-emerald-500/20 rounded-[24px]',
                            title: 'text-2xl font-bold font-display text-white',
                            htmlContainer: 'text-emerald-100/70 text-base',
                            confirmButton: 'px-8 py-3 rounded-full font-bold uppercase tracking-wider text-sm transition-all duration-300'
                        }
                    });
                } else {
                    alert(data.message);
                }
                form.reset();
            } else {
                // Server responded with an error or info message
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        title: data.status === 'info' ? 'Already Subscribed' : 'Notice',
                        text: data.message || 'Subscription failed.',
                        icon: data.status === 'info' ? 'info' : 'warning',
                        background: '#0a1a14',
                        color: '#ecfdf5',
                        confirmButtonColor: '#059669',
                        customClass: {
                            popup: 'border border-emerald-500/20 rounded-[24px]',
                            title: 'text-2xl font-bold font-display text-white',
                            htmlContainer: 'text-emerald-100/70 text-base',
                            confirmButton: 'px-8 py-3 rounded-full font-bold uppercase tracking-wider text-sm transition-all duration-300'
                        }
                    });
                } else {
                    alert(data.message || 'Subscription failed.');
                }
            }
        } catch (error) {
            console.error('Newsletter Error:', error);
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: 'Error',
                    text: 'An error occurred. Please try again later.',
                    icon: 'error',
                    background: '#0a1a14',
                    color: '#ecfdf5',
                    confirmButtonColor: '#059669'
                });
            } else {
                alert('An error occurred. Please try again later.');
            }
        } finally {
            // Restore state after a short delay
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = originalButtonText;
            }, 3000);
        }
        return false;
    };

    // Bind newsletter submit
    const newsletterForm = document.querySelector('form[data-action="newsletter-submit"]');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', window.handleNewsletterSubmit);
    }

});
