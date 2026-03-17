/**
 * OpenClaw Agency - Organization Chart
 * Interactive JavaScript for accessibility and UX enhancements
 */

(function() {
  'use strict';

  /**
   * DOM Elements
   */
  const orgChart = document.querySelector('.org-chart');
  const nodes = document.querySelectorAll('.org-node');
  const nodeCards = document.querySelectorAll('.node-card');

  /**
   * Initialization
   */
  function init() {
    setupIntersectionObserver();
    setupKeyboardNavigation();
    setupAccessibilityEnhancements();
    addTouchSupport();
    console.log('🌳 Org Chart initialized with', nodes.length, 'nodes');
  }

  /**
   * Intersection Observer for scroll animations
   */
  function setupIntersectionObserver() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Optionally unobserve after animation
          // observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -5% 0px'
    });

    nodes.forEach(node => observer.observe(node));
  }

  /**
   * Enhanced Keyboard Navigation
   * Allows arrow key navigation between nodes at the same level
   */
  function setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      // Only handle navigation when a card is focused
      const focusedCard = document.activeElement.closest('.node-card');
      if (!focusedCard) return;

      const currentNode = focusedCard.closest('.org-node');
      if (!currentNode) return;

      const level = currentNode.dataset.level;
      const sameLevelNodes = Array.from(
        document.querySelectorAll(`.org-level[data-level="${level}"] .org-node`)
      );
      const currentIndex = sameLevelNodes.indexOf(currentNode);

      let targetIndex = null;

      switch (e.key) {
        case 'ArrowLeft':
          if (currentIndex > 0) targetIndex = currentIndex - 1;
          break;
        case 'ArrowRight':
          if (currentIndex < sameLevelNodes.length - 1) targetIndex = currentIndex + 1;
          break;
        case 'ArrowUp':
          // Move to parent level (or previous level if available)
          if (level > 0) {
            const parentLevel = document.querySelector(`.org-level[data-level="${parseInt(level) - 1}"]`);
            if (parentLevel) {
              const parentNode = parentLevel.querySelector('.org-node');
              if (parentNode) {
                const parentCard = parentNode.querySelector('.node-card');
                if (parentCard) targetIndex = -1; // Special case
              }
            }
          }
          break;
        case 'ArrowDown':
          // Move to next level (first child)
          if (level < 2) {
            const childLevel = document.querySelector(`.org-level[data-level="${parseInt(level) + 1}"]`);
            if (childLevel) {
              const firstChild = childLevel.querySelector('.org-node .node-card');
              if (firstChild) targetIndex = -2; // Special case
            }
          }
          break;
        case 'Home':
          // Focus first node in current level
          if (sameLevelNodes.length > 0) {
            targetIndex = 0;
          }
          break;
        case 'End':
          // Focus last node in current level
          if (sameLevelNodes.length > 0) {
            targetIndex = sameLevelNodes.length - 1;
          }
          break;
      }

      if (targetIndex === -1) {
        // Up arrow: focus parent
        e.preventDefault();
        const parentLevel = document.querySelector(`.org-level[data-level="${parseInt(level) - 1}"]`);
        if (parentLevel) {
          const parentCard = parentLevel.querySelector('.node-card');
          if (parentCard) parentCard.focus();
        }
      } else if (targetIndex === -2) {
        // Down arrow: focus first child
        e.preventDefault();
        const childLevel = document.querySelector(`.org-level[data-level="${parseInt(level) + 1}"]`);
        if (childLevel) {
          const firstChildCard = childLevel.querySelector('.org-node .node-card');
          if (firstChildCard) firstChildCard.focus();
        }
      } else if (targetIndex !== null) {
        e.preventDefault();
        const targetCard = sameLevelNodes[targetIndex].querySelector('.node-card');
        if (targetCard) targetCard.focus();
      }
    });
  }

  /**
   * Accessibility Enhancements
   * - Announce node changes
   * - Update ARIA attributes
   */
  function setupAccessibilityEnhancements() {
    // Add role="treeitem" and aria-level attributes
    nodes.forEach((node, index) => {
      const card = node.querySelector('.node-card');
      if (card) {
        card.setAttribute('role', 'treeitem');
        card.setAttribute('aria-level', parseInt(node.dataset.level) + 1);
        card.setAttribute('aria-setsize', nodes.length);
        card.setAttribute('aria-posinset', index + 1);
      }
    });

    // Add live region for dynamic announcements
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'org-chart-live';
    document.body.appendChild(liveRegion);

    // Announce node focus
    nodeCards.forEach(card => {
      card.addEventListener('focus', () => {
        const node = card.closest('.org-node');
        const name = node.querySelector('.name')?.textContent || 'Unknown';
        const title = node.querySelector('.title')?.textContent || '';
        announce(`Focus: ${name}, ${title}`);
      });
    });
  }

  /**
   * Live region announcement
   */
  function announce(message) {
    const liveRegion = document.getElementById('org-chart-live');
    if (liveRegion) {
      liveRegion.textContent = message;
      setTimeout(() => {
        liveRegion.textContent = '';
      }, 1000);
    }
  }

  /**
   * Touch Support for Mobile
   * - Tap to show details
   * - Long press alternative
   */
  function addTouchSupport() {
    let touchTimer = null;
    const LONG_PRESS_MS = 500;

    nodeCards.forEach(card => {
      card.addEventListener('touchstart', () => {
        touchTimer = setTimeout(() => {
          // Long press: toggle details
          const details = card.querySelector('.node-details');
          if (details) {
            const isVisible = details.style.maxHeight && details.style.maxHeight !== '0px';
            details.style.maxHeight = isVisible ? '0px' : '200px';
            details.style.opacity = isVisible ? '0' : '1';
            announce(isVisible ? 'Details hidden' : 'Details shown');
          }
        }, LONG_PRESS_MS);
      }, { passive: true });

      card.addEventListener('touchend', () => {
        if (touchTimer) {
          clearTimeout(touchTimer);
          touchTimer = null;
        }
      });

      card.addEventListener('touchmove', () => {
        if (touchTimer) {
          clearTimeout(touchTimer);
          touchTimer = null;
        }
      }, { passive: true });
    });
  }

  /**
   * Enhance connector lines on high-DPI screens
   */
  function enhanceConnectors() {
    const pixelRatio = window.devicePixelRatio || 1;
    if (pixelRatio > 1) {
      document.body.classList.add('high-dpi');
    }
  }

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Also run after fonts load for proper layout
  document.fonts.ready.then(() => {
    enhanceConnectors();
  });

})();
