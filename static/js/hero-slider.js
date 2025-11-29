document.addEventListener('DOMContentLoaded', function () {
    const sliderSection = document.getElementById('hero-slider-section');
    if (!sliderSection) return;

    const destinations = [
        {
            name: "DAANG KALIKASAN",
            desc: "A scenic road offering breathtaking views of the mountains and nature. It's a popular spot for sightseeing and photography, showcasing the raw beauty of Mangatarem.",
            img: "https://asensopangasinan.com/wp-content/uploads/2020/02/Daang-Kalikasan-3.jpg",
            rating: 5
        },
        {
            name: "AGKAPITA",
            desc: "A beautiful destination known for its serene atmosphere and stunning landscapes. Perfect for those seeking tranquility and a connection with nature.",
            img: "https://images.smartparenting.com.ph/smartpar/images/2022/01/22/Screen-Shot-2022-01-22-at-4.48.32-PM.jpg",
            rating: 5
        },
        {
            name: "PACALAT RIVER",
            desc: "Relax by the refreshing waters of Pacalat River. A perfect spot for nature lovers, picnics, and enjoying the cool, clear water flowing from the mountains.",
            img: "https://scontent.fmnl17-3.fna.fbcdn.net/v/t1.6435-9/86460255_142873250516171_2885019314719555584_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeH1xzxgwtur1DJVmyT0ppoFBFjxVOAkUFwEWPFU4CRQXOUVbqQZBz5jjfRisTXSXr5uTec--iph_JvIvBcM1dbo&_nc_ohc=KIbugSUetkUQ7kNvwH9W-8G&_nc_oc=Adnk6DNdNdBkhjrCMWDNkPVMv01LKseroId_IFqzceeD8XTOtRRa5Q47Q8HohlMSO9I&_nc_zt=23&_nc_ht=scontent.fmnl17-3.fna&_nc_gid=ZFVwXLmrSZJ5keMLFd6ltQ&oh=00_Afg3YbIoMRoZuCpuC6zz5Cppb_ucKQieuTI-17tiRhqY0g&oe=69522116",
            rating: 4
        }
    ];

    let currentIndex = 0;
    let isAnimating = false;
    let autoSlideInterval;

    const bgContainer = sliderSection.querySelector('.slider-bg-container');
    const cardTrack = sliderSection.querySelector('.card-slider-track');
    const textContainer = sliderSection.querySelector('.slider-content-left');
    const titleEl = sliderSection.querySelector('.slider-title');
    const descEl = sliderSection.querySelector('.slider-description');
    const mainContainer = sliderSection.querySelector('.slider-container');

    function init() {
        // 1. Create Backgrounds
        destinations.forEach((dest, index) => {
            const img = document.createElement('img');
            img.src = dest.img;
            img.classList.add('bg-image');
            if (index === 0) img.classList.add('active');
            bgContainer.appendChild(img);
        });

        // 2. Create Cards
        destinations.forEach((dest, index) => {
            const card = document.createElement('div');
            card.classList.add('slider-card');

            let starsHTML = '';
            for (let s = 0; s < 5; s++) starsHTML += s < dest.rating ? '<i class="fas fa-star" style="color:#f39c12"></i>' : '<i class="far fa-star" style="color:#f39c12"></i>';

            card.innerHTML = `
                <img src="${dest.img}" alt="${dest.name}">
                <div class="bookmark-icon"><i class="far fa-bookmark"></i></div>
                <div class="card-overlay">
                    <div style="font-weight:600; font-size:1.1rem; color: white;">${dest.name}</div>
                    <div style="margin-top:5px; font-size:0.8rem">${starsHTML}</div>
                </div>
            `;

            card.onclick = () => {
                if (index !== currentIndex && !isAnimating) jumpToSlide(index);
            };

            cardTrack.appendChild(card);
        });

        // 3. Initial Render
        updateText(0, true);
        updateCardPositions();

        // 4. Start Auto Play
        startAutoPlay();
    }

    function startAutoPlay() {
        clearInterval(autoSlideInterval);
        autoSlideInterval = setInterval(() => {
            nextSlide(true); // true indicates auto-triggered
        }, 5000);
    }

    function stopAutoPlay() {
        clearInterval(autoSlideInterval);
    }

    // Hover Pausing Logic
    mainContainer.addEventListener('mouseenter', stopAutoPlay);
    mainContainer.addEventListener('mouseleave', startAutoPlay);

    function updateCardPositions() {
        const cards = Array.from(cardTrack.children);
        cards.forEach((card, index) => {
            card.classList.remove('slot-active', 'slot-1', 'slot-2', 'slot-3', 'slot-next');
            let diff = (index - currentIndex + destinations.length) % destinations.length;

            if (diff === 0) card.classList.add('slot-active');
            else if (diff === 1) card.classList.add('slot-1');
            else if (diff === 2) card.classList.add('slot-2');
            else if (diff === 3) card.classList.add('slot-3');
            else card.classList.add('slot-next');
        });
    }

    function updateBackground() {
        const images = bgContainer.querySelectorAll('.bg-image');
        images.forEach((img, idx) => {
            if (idx === currentIndex) img.classList.add('active');
            else img.classList.remove('active');
        });
    }

    function updateText(index, instant = false) {
        const dest = destinations[index];
        if (instant) {
            titleEl.textContent = dest.name;
            descEl.textContent = dest.desc;
            return;
        }
        textContainer.classList.remove('text-visible');
        textContainer.classList.add('text-exit');
        setTimeout(() => {
            titleEl.textContent = dest.name;
            descEl.textContent = dest.desc;
            textContainer.classList.remove('text-exit');
            void textContainer.offsetWidth; // Force Reflow
            textContainer.classList.add('text-visible');
        }, 500);
    }

    window.nextSlide = function (auto = false) {
        if (isAnimating) return;
        isAnimating = true;

        // If manually clicked, reset the timer so it doesn't jump immediately after
        if (!auto) startAutoPlay();

        currentIndex = (currentIndex + 1) % destinations.length;
        updateBackground();
        updateCardPositions();
        updateText(currentIndex);
        setTimeout(() => { isAnimating = false; }, 800);
    }

    window.prevSlide = function () {
        if (isAnimating) return;
        isAnimating = true;

        // Reset timer on manual click
        startAutoPlay();

        currentIndex = (currentIndex - 1 + destinations.length) % destinations.length;
        updateBackground();
        updateCardPositions();
        updateText(currentIndex);
        setTimeout(() => { isAnimating = false; }, 800);
    }

    function jumpToSlide(index) {
        if (isAnimating) return;
        isAnimating = true;

        startAutoPlay();

        currentIndex = index;
        updateBackground();
        updateCardPositions();
        updateText(currentIndex);
        setTimeout(() => { isAnimating = false; }, 800);
    }

    init();
});
