// Tourism Analytics visitor comparison chart config
(function() {
    'use strict';

    function initDestinationComparisonChart() {
        const sourceElement = document.getElementById('comparison-chart-source');
        if (!sourceElement || typeof Chart === 'undefined') return;

        const rawData = sourceElement.getAttribute('data-chart');
        if (!rawData) return;

        let chartData;
        try {
            chartData = JSON.parse(rawData);
        } catch (e) {
            console.error('Failed to parse comparison chart data:', e);
            return;
        }

        const ctx = document.getElementById('destinationComparisonChart');
        if (!ctx) return;

        const context = ctx.getContext('2d');

        new Chart(context, {
            type: 'bar',
            data: {
                labels: chartData.labels || [],
                datasets: [
                    {
                        label: 'Active Footprint (Visitors)',
                        data: chartData.visitors || [],
                        backgroundColor: '#10b981',
                        borderRadius: 12,
                        borderSkipped: false,
                        maxBarThickness: 24,
                        categoryPercentage: 0.8,
                        barPercentage: 0.7
                    },
                    {
                        label: 'Digital Engagement (Page Views)',
                        data: chartData.page_views || [],
                        backgroundColor: '#06b6d4',
                        borderRadius: 12,
                        borderSkipped: false,
                        maxBarThickness: 24,
                        categoryPercentage: 0.8,
                        barPercentage: 0.7
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: { family: 'Plus Jakarta Sans', size: 11, weight: 'bold' },
                            color: '#064e3b',
                            boxWidth: 12,
                            boxHeight: 12,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: '#064e3b',
                        titleFont: { family: 'Plus Jakarta Sans', size: 13, weight: 'bold' },
                        bodyFont: { family: 'Plus Jakarta Sans', size: 12, weight: 'medium' },
                        padding: 16,
                        cornerRadius: 16,
                        displayColors: true,
                        boxWidth: 8,
                        boxHeight: 8,
                        boxPadding: 4,
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.raw !== null) {
                                    label += context.raw.toLocaleString();
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(6, 78, 59, 0.04)', drawBorder: false },
                        ticks: {
                            color: '#064e3b',
                            font: { family: 'Plus Jakarta Sans', size: 11, weight: 'bold' },
                            callback: function(value) {
                                if (value >= 1000) {
                                    return (value / 1000) + 'k';
                                }
                                return value;
                            }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            color: '#064e3b',
                            font: { family: 'Plus Jakarta Sans', size: 11, weight: 'black' }
                        }
                    }
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDestinationComparisonChart);
    } else {
        initDestinationComparisonChart();
    }
})();
