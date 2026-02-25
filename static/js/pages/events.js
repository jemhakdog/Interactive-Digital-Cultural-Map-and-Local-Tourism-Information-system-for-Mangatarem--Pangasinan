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
