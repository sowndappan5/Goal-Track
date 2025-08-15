document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects
    const leaderboardItems = document.querySelectorAll('.leaderboard-item');
    
    leaderboardItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    // Optional: Add animation for points when they change
    function pulseAnimation(element) {
        element.classList.add('pulse');
        setTimeout(() => {
            element.classList.remove('pulse');
        }, 500);
    }
    
    // This would be triggered when points update
    const pointElements = document.querySelectorAll('.points');
    pointElements.forEach(element => {
        // For demo only - in production this would be triggered by actual score changes
        element.addEventListener('click', function() {
            pulseAnimation(this);
        });
    });
});

// Add this to your CSS for the pulse animation
document.head.insertAdjacentHTML('beforeend', `
<style>
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

.pulse {
    animation: pulse 0.5s ease-out;
}
</style>
`);