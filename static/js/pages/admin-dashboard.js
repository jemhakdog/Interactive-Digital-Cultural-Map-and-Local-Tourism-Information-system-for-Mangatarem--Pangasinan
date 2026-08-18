// Admin dashboard chart initialization
(function() {
    'use strict';

    function initEngagementChart() {
        const chartContainer = document.getElementById('engagement-chart-data');
        if (!chartContainer || typeof Chart === 'undefined') return;

        const dates = JSON.parse(chartContainer.dataset.dates || '[]');
        const counts = JSON.parse(chartContainer.dataset.counts || '[]');

        if (!dates.length || !counts.length) return;

        const ctx = document.getElementById('engagementChart');
        if (!ctx) return;

        const context = ctx.getContext('2d');

        // Custom gradient for chart
        const gradient = context.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(16, 185, 129, 0.4)');
        gradient.addColorStop(1, 'rgba(16, 185, 129, 0)');

        new Chart(context, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Explorer Activity',
                    data: counts,
                    borderColor: '#10b981',
                    borderWidth: 4,
                    backgroundColor: gradient,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#064e3b',
                        titleFont: { family: 'Plus Jakarta Sans', size: 13, weight: 'bold' },
                        bodyFont: { family: 'Plus Jakarta Sans', size: 12 },
                        padding: 12,
                        cornerRadius: 12,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0,0,0,0.03)', drawBorder: false },
                        ticks: { color: '#64748b', font: { size: 11, weight: '600' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b', font: { size: 11, weight: '600' } }
                    }
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEngagementChart);
    } else {
        initEngagementChart();
    }
})();
