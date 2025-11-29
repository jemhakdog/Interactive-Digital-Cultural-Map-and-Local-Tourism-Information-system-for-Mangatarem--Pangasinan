// Optimized Animations with Performance Improvements
document.addEventListener('DOMContentLoaded', function () {
    // Typing Animation
    const text = "Where Heritage Meets Nature";
    const typingTextElement = document.getElementById('typing-text');

    if (typingTextElement) {
        let index = 0;
        function type() {
            if (index < text.length) {
                typingTextElement.textContent += text.charAt(index);
                index++;
                setTimeout(type, 80);
            }
        }
        setTimeout(type, 500);
    }

    // Initialize AOS (Animate On Scroll) - Lazy loaded
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100,
            disable: 'mobile' // Disable animations on mobile for better performance
        });
    }

    // Optimized Parallax Scroll Effect with Throttling
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        let ticking = false;
        let lastScrollY = 0;

        function updateParallax() {
            const scrolled = lastScrollY;
            const parallaxSpeed = 0.5;
            heroBackground.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            lastScrollY = window.pageYOffset;

            if (!ticking) {
                window.requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });
    }

    // Carousel Functionality
    const track = document.querySelector('.carousel-track');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevButton = document.querySelector('.carousel-button.prev');
    const nextButton = document.querySelector('.carousel-button.next');

    if (track && slides.length > 0) {
        let currentIndex = 0;
        const slidesToShow = window.innerWidth < 769 ? 1 : window.innerWidth < 1025 ? 2 : 3;
        const maxIndex = Math.max(0, slides.length - slidesToShow);

        function updateCarousel() {
            const slideWidth = slides[0].offsetWidth;
            const gap = 32; // 2rem gap
            const offset = currentIndex * (slideWidth + gap);
            track.style.transform = `translateX(-${offset}px)`;

            // Update button states
            if (prevButton) prevButton.disabled = currentIndex === 0;
            if (nextButton) nextButton.disabled = currentIndex >= maxIndex;
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateCarousel();
                }
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                if (currentIndex < maxIndex) {
                    currentIndex++;
                    updateCarousel();
                }
            });
        }

        // Touch/Swipe support for mobile
        let touchStartX = 0;
        let touchEndX = 0;

        track.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        track.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            if (touchEndX < touchStartX - 50 && currentIndex < maxIndex) {
                currentIndex++;
                updateCarousel();
            }
            if (touchEndX > touchStartX + 50 && currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        }

        // Debounced resize handler
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                updateCarousel();
            }, 250);
        }, { passive: true });

        updateCarousel();
    }

    // Lazy Load Images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        }, {
            rootMargin: '50px'
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});
