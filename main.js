document.addEventListener('DOMContentLoaded', async () => {
    // Load Branding
    try {
        const response = await fetch('branding.json');
        const branding = await response.json();
        applyBranding(branding);
    } catch (e) {
        console.log("No branding found, using defaults");
    }

    function applyBranding(branding) {
        if (branding.primary_color) {
            document.documentElement.style.setProperty('--accent', branding.primary_color);
            document.documentElement.style.setProperty('--accent-glow', branding.primary_color + '44');
        }
        if (branding.name) {
            document.querySelector('.logo').innerHTML = `<span class="logo-accent">${branding.name.split(' ')[0]}</span> ${branding.name.split(' ').slice(1).join(' ')}`;
            document.title = branding.name + " | The Professional Distro Framework";
            document.querySelector('.footer-logo').textContent = branding.name;
        }
        if (branding.hero_icon) {
            document.querySelectorAll('.feature-card .icon')[0].textContent = branding.hero_icon;
        }
    }

    async function fetchLatestRelease() {
        try {
            const response = await fetch('releases.json');
            const data = await response.json();
            const latest = data[0];

            document.querySelector('.version-tag').textContent = 'v' + latest.version;
            document.querySelector('.release-date').textContent = latest.date;

            const list = document.getElementById('release-points');
            list.innerHTML = latest.highlights.map(h => `<li>${h}</li>`).join('');
        } catch (e) {
            document.getElementById('latest-release').style.display = 'none';
        }
    }

    fetchLatestRelease();

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Simple scroll animation for cards
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .showcase-content, .showcase-visual').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Navbar transparency toggle
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
            navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.8)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Terminal typing simulation (one-time)
    const terminalLines = document.querySelectorAll('.terminal-body .line');
    terminalLines.forEach((line, index) => {
        line.style.opacity = '0';
        setTimeout(() => {
            line.style.opacity = '1';
        }, 800 * (index + 1));
    });
});
