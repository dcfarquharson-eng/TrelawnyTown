document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // Toggle icon between hamburger and close (simple text based for now)
            if (navLinks.classList.contains('active')) {
                menuToggle.innerHTML = '&#10005;'; // X symbol
            } else {
                menuToggle.innerHTML = '&#9776;'; // Hamburger symbol
            }
        });
    }

    // Scroll Animation (Fade In Up)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.text-block, .event-card, .section h2, .dedication');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });

    // Helper to trigger the animation
    setInterval(() => {
        document.querySelectorAll('.visible').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    }, 100);

    // Prevent Right-Click on Images
    document.addEventListener('contextmenu', (e) => {
        if (e.target.tagName === 'IMG') {
            e.preventDefault();
        }
    });

    // Book Waitlist Form
    const waitlistForm = document.getElementById('book-waitlist-form');
    if (waitlistForm) {
        waitlistForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('waitlist-email');
            const messageDiv = document.getElementById('waitlist-message');
            const submitButton = waitlistForm.querySelector('button[type="submit"]');

            const email = emailInput.value.trim();
            if (!email) return;

            submitButton.disabled = true;
            submitButton.textContent = "Joining...";
            messageDiv.style.display = 'none';
            messageDiv.className = 'waitlist-message';

            try {
                const response = await fetch('https://trelawny-backend.onrender.com/api/join_waitlist', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email })
                });

                const data = await response.json();

                if (response.ok) {
                    messageDiv.textContent = "Success! You are on the VIP waitlist.";
                    messageDiv.classList.add('success');
                    emailInput.value = '';
                } else {
                    messageDiv.textContent = data.detail || "An error occurred. Please try again.";
                    messageDiv.classList.add('error');
                }
            } catch (err) {
                messageDiv.textContent = "Network error. Please try again later.";
                messageDiv.classList.add('error');
            }

            messageDiv.style.display = 'block';
            submitButton.disabled = false;
            submitButton.textContent = "Join the Waitlist";
        });
    }
});
