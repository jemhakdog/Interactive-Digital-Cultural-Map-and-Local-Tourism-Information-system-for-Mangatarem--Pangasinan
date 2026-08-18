/**
 * Events Page Interactions
 * Handles event filtering and Add to Calendar functionality
 */
// Filter Functionality
document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const eventItems = document.querySelectorAll('.event-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            eventItems.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                    // Add fade-in effect
                    item.animate([
                        { opacity: 0, transform: 'translateY(20px)' },
                        { opacity: 1, transform: 'translateY(0)' }
                    ], { duration: 600, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' });
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});

// Add to Calendar Functionality
window.addToCalendar = function(title, location, dateStr) {
    const date = new Date(dateStr);
    const endDate = new Date(date.getTime() + (2 * 60 * 60 * 1000)); // Assume 2 hours duration

    const formatDate = (d) => d.toISOString().replace(/-|:|\.\d\d\d/g, "");

    const href = encodeURI(
        'data:text/calendar;charset=utf8,' + [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'BEGIN:VEVENT',
            'URL:' + document.URL,
            'DTSTART:' + formatDate(date),
            'DTEND:' + formatDate(endDate),
            'SUMMARY:' + title,
            'DESCRIPTION:Join us for ' + title + ' at ' + location,
            'LOCATION:' + location,
            'END:VEVENT',
            'END:VCALENDAR'
        ].join('\n')
    );

    const link = document.createElement('a');
    link.href = href;
    link.setAttribute('download', title + '.ics');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

// Interactive Calendar Logic
document.addEventListener('DOMContentLoaded', function () {
    const calendarDays = document.getElementById('calendarDays');
    const currentMonthYear = document.getElementById('currentMonthYear');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const eventItems = document.querySelectorAll('.event-item');
    
    // Extract dates that have events
    const eventDates = new Set();
    eventItems.forEach(item => {
        const dateStr = item.getAttribute('data-date');
        if (dateStr) {
            eventDates.add(dateStr);
        }
    });

    let currentDate = new Date();
    let currentFilterDate = null; // Used to track if a specific date is filtered

    function renderCalendar() {
        calendarDays.innerHTML = '';
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        // Update Header
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        currentMonthYear.textContent = `${monthNames[month]} ${year}`;

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Empty slots before first day
        for (let i = 0; i < firstDay; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.classList.add('cal-day', 'empty');
            calendarDays.appendChild(emptyDiv);
        }

        // Days of the month
        const today = new Date();
        for (let i = 1; i <= daysInMonth; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('cal-day');
            dayDiv.textContent = i;

            // Format YYYY-MM-DD
            const formattedMonth = String(month + 1).padStart(2, '0');
            const formattedDay = String(i).padStart(2, '0');
            const dateString = `${year}-${formattedMonth}-${formattedDay}`;

            if (year === today.getFullYear() && month === today.getMonth() && i === today.getDate()) {
                dayDiv.classList.add('today');
            }

            if (eventDates.has(dateString)) {
                dayDiv.classList.add('has-event');
            }

            if (currentFilterDate === dateString) {
                dayDiv.classList.add('active-filter');
            }

            dayDiv.addEventListener('click', () => {
                if (currentFilterDate === dateString) {
                    // Deselect if already selected
                    currentFilterDate = null;
                } else {
                    currentFilterDate = dateString;
                }
                renderCalendar();
                filterEventsByDate(currentFilterDate);
            });

            calendarDays.appendChild(dayDiv);
        }
    }

    function filterEventsByDate(dateString) {
        let anyVisible = false;
        eventItems.forEach(item => {
            const itemDate = item.getAttribute('data-date');
            
            // Respect existing category filter if possible, but let's prioritize date here
            // Removing active class from category buttons to avoid confusion
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            // Set 'All' as active visually if no date filter
            if (!dateString) {
                document.querySelector('.filter-btn[data-filter="all"]').classList.add('active');
            }
            
            if (!dateString || itemDate === dateString) {
                item.style.display = 'block';
                item.animate([
                    { opacity: 0, transform: 'translateY(20px)' },
                    { opacity: 1, transform: 'translateY(0)' }
                ], { duration: 600, easing: 'cubic-bezier(0.23, 1, 0.32, 1)' });
                anyVisible = true;
            } else {
                item.style.display = 'none';
            }
        });
        
        // If filtering by date that has no events, we could show a message, 
        // but since we only allow clicking days, and has-event is visual, it's fine.
    }

    if (prevMonthBtn && nextMonthBtn) {
        prevMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            renderCalendar();
        });

        nextMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            renderCalendar();
        });
        
        // Initial render
        renderCalendar();
    }
});
