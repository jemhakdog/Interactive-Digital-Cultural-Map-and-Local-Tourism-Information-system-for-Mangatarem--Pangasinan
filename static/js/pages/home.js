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
    window.handleNewsletterSubmit = function (event) {
        event.preventDefault();
        const email = event.target.querySelector('input[type="email"]').value;
        // TODO: Implement actual newsletter subscription logic
        alert('Welcome to the Mangatarem Digital Archive!');
        event.target.reset();
        return false;
    };
});
