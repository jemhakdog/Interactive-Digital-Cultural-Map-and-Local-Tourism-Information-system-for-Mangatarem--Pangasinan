document.addEventListener('DOMContentLoaded', function() {
    // Typing Animation
    const text = "Where Heritage Meets Nature";
    const typingTextElement = document.getElementById('typing-text');
    const cursorElement = document.querySelector('.cursor');
    
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

    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100
        });
    }

    // Parallax Scroll Effect for Hero Background
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxSpeed = 0.5;
            heroBackground.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        });
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
        });

        track.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });

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

        // Update on window resize
        window.addEventListener('resize', () => {
            updateCarousel();
        });

        updateCarousel();
    }
});
