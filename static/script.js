// Chart.js global configuration for better aesthetics
Chart.defaults.color = '#f3f4f6';
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif'";

// Global variables to hold chart instances
let barChart = null;
let pieChart = null;

// Global variables to hold assessment data
let assessmentData = null;

// Color palettes for charts
const assessmentColors = [
    '#6366f1', // primary
    '#10b981', // secondary
    '#f59e0b', // accent
    '#ec4899', // pink
    '#8b5cf6', // purple
    '#14b8a6', // teal
    '#f43f5e', // rose
    '#0ea5e9'  // sky
];

// Load the data when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchAssessmentData();
});

// Fetch assessment data from the backend
function fetchAssessmentData() {
    fetch('/api/marks')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data || !data.users || !data.scores) {
                throw new Error("Invalid data format received from server");
            }

            assessmentData = data; // Store the data globally

            // Assuming there's only one user, use the first user's data
            const singleUser = data.users[0];
            const scores = data.scores[singleUser];

            // Initialize charts with the single user's data
            initBarChart(singleUser, scores);
            initPieChart(0, data.assessments[0]);
        })
        .catch(error => {
            console.error('Error fetching assessment data:', error);
            alert('Failed to load assessment data. Please try again later.');
        });
}

// Initialize bar chart for the single user
function initBarChart(user, scores) {
    const ctx = document.getElementById('barChart').getContext('2d');

    if (barChart) barChart.destroy();

    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: assessmentData.assessments,
            datasets: [{
                label: `${user}'s Scores`,
                data: scores,
                backgroundColor: assessmentColors[0],
                borderRadius: 6,
                hoverBackgroundColor: assessmentColors[1]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10, // Assuming max score is 10
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(31, 41, 55, 0.9)',
                    bodyFont: { size: 14 },
                    padding: 10,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `Score: ${context.raw} points`;
                        }
                    }
                }
            },
            animation: { duration: 1000 },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    initPieChart(index, assessmentData.assessments[index]);
                }
            }
        }
    });
}

// Initialize pie chart for the first assessment
function initPieChart(assessmentIndex, assessmentName) {
    const score = assessmentData.scores[assessmentData.users[0]][assessmentIndex];

    document.getElementById('selected-assessment-title').innerText = `${assessmentName} Detail`;

    const ctx = document.getElementById('pieChart').getContext('2d');

    if (pieChart) pieChart.destroy();

    pieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Correct', 'Incorrect'],
            datasets: [{
                data: [score, 10 - score], // Assuming max score is 10
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 5
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: { size: 14 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(31, 41, 55, 0.9)',
                    bodyFont: { size: 14 },
                    padding: 10,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw} points`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}
