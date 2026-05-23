// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const nav = document.getElementById('mainNav');
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });
    
    // Animated counter function with fixed numbers
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 50;
        const updateCounter = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(updateCounter);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    }
    
    // Trigger counter animation when stats section is in view
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Animate each stat with specific numbers
                    const stat1 = document.getElementById('stat1');
                    const stat2 = document.getElementById('stat2');
                    const stat3 = document.getElementById('stat3');
                    const stat4 = document.getElementById('stat4');
                    
                    if (stat1) animateCounter(stat1, 5);
                    if (stat2) animateCounter(stat2, 2);
                    if (stat3) animateCounter(stat3, 15);
                    if (stat4) animateCounter(stat4, 8);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        observer.observe(statsSection);
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add active class to nav links based on current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
});