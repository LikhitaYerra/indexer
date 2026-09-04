// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Add scroll-based animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all feature cards and demo cards
document.querySelectorAll('.feature-card, .demo-card, .step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// Add active state to navigation on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Terminal typing effect (optional enhancement)
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Add copy-to-clipboard for code blocks
document.querySelectorAll('.code-block').forEach(block => {
    const button = document.createElement('button');
    button.innerHTML = '📋 Copy';
    button.style.cssText = `
        position: absolute;
        right: 0.5rem;
        top: 0.5rem;
        background: rgba(255,255,255,0.1);
        border: none;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.75rem;
    `;
    
    block.style.position = 'relative';
    block.appendChild(button);
    
    button.addEventListener('click', () => {
        const code = Array.from(block.querySelectorAll('code'))
            .map(c => c.textContent)
            .join('\n');
        
        navigator.clipboard.writeText(code).then(() => {
            button.innerHTML = '✓ Copied!';
            setTimeout(() => {
                button.innerHTML = '📋 Copy';
            }, 2000);
        });
    });
});

// Add GitHub star counter (optional - requires GitHub API)
async function fetchGitHubStars() {
    try {
        const response = await fetch('https://api.github.com/repos/LikhitaYerra/indexer');
        const data = await response.json();
        
        // You can display the star count somewhere on the page
        console.log(`GitHub Stars: ${data.stargazers_count}`);
    } catch (error) {
        console.log('Could not fetch GitHub stars');
    }
}

// Uncomment to enable star counter
// fetchGitHubStars();
