/**
 * Org Chart – Theme Toggle & Keyboard Navigation
 * Accessibility: WCAG 2.1 AA
 */

(function() {
  'use strict';

  const STORAGE_KEY = 'org-chart-theme';
  const toggleBtn = document.getElementById('theme-toggle');
  const body = document.body;
  const cards = document.querySelectorAll('.card');

  // Theme management
  function setTheme(theme) {
    body.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggleTheme() {
    const current = body.getAttribute('data-theme') || 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  }

  function initTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      setTheme(saved);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
    }
  }

  // Keyboard navigation (arrow keys within same level)
  function handleKeydown(e) {
    if (!['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Home','End'].includes(e.key)) return;
    const current = document.activeElement;
    if (!current.classList.contains('card')) return;

    const level = parseInt(current.dataset.level, 10);
    const allCards = Array.from(cards).filter(c => parseInt(c.dataset.level, 10) === level);
    const idx = allCards.indexOf(current);
    if (idx === -1) return;

    let nextIdx = idx;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      nextIdx = (idx + 1) % allCards.length;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      nextIdx = (idx - 1 + allCards.length) % allCards.length;
    } else if (e.key === 'Home') {
      nextIdx = 0;
    } else if (e.key === 'End') {
      nextIdx = allCards.length - 1;
    } else {
      return;
    }

    e.preventDefault();
    allCards[nextIdx].focus();
  }

  // Initialize
  initTheme();
  if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleTheme);
  }
  document.addEventListener('keydown', handleKeydown);
})();
