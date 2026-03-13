/**
 * Japan Travel Guide – Theme Toggle & Interactions
 * Simple, accessible, persistent theme selection
 */

(function() {
    'use strict';

    const STORAGE_KEY = 'japan-travel-theme';
    const toggleBtn = document.getElementById('theme-toggle');
    const body = document.body;

    // Set initial theme from localStorage or system preference
    function initTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            body.setAttribute('data-theme', saved);
        } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            body.setAttribute('data-theme', 'dark');
        }
    }

    // Toggle theme
    function toggleTheme() {
        const current = body.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', next);
        localStorage.setItem(STORAGE_KEY, next);
    }

    // Event listeners
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleTheme);
    }

    // Init
    initTheme();

    // Optional: smooth scroll for anchor links (if added later)
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

    // Make list item titles clickable → Google search for more info
    document.querySelectorAll('.highlights li').forEach(li => {
        const strong = li.querySelector('strong');
        if (strong) {
            const title = strong.textContent.trim();
            const article = li.closest('article');
            const city = article ? article.dataset.city : '';
            const query = encodeURIComponent(`${title} ${city.charAt(0).toUpperCase() + city.slice(1)}`);
            const url = `https://www.google.com/search?q=${query}`;
            const a = document.createElement('a');
            a.href = url;
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.style.color = 'inherit';
            a.style.textDecoration = 'underline';
            a.appendChild(strong.cloneNode(true));
            strong.replaceWith(a);
        }
    });

})();
