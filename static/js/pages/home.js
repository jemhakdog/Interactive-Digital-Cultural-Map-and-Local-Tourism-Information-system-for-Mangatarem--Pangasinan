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
                button.classList.remove('bg-emerald-600');
                button.classList.add('bg-emerald-500');
                
                // Show a nice notification if you have a toast system, 
                // otherwise alert is fine for now but alert is a bit jarring
                alert(data.message);
                form.reset();
            } else {
                // Error from server
                alert(data.error || 'Subscription failed.');
            }
        } catch (error) {
            console.error('Newsletter Error:', error);
            alert('An error occurred. Please try again later.');
        } finally {
            // Restore state after a short delay
            setTimeout(() => {
                button.disabled = false;
                button.innerHTML = originalButtonText;
                button.classList.remove('bg-emerald-50');
                button.classList.add('bg-emerald-600');
            }, 3000);
        }
        return false;
    };

});
