/**
 * Framework Comparison — Interactive Logic
 * Propagation Framework Explorer
 */

(function() {
  'use strict';

  // Parameter counts
  const PARAMS = {
    pf: 3,      // 3 axioms, 0 free parameters
    sm: 19,     // 19+ free parameters in Standard Model
    st: 500     // 10^500 vacua (we'll show as 10^500)
  };

  let counting = false;

  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    initParameterCounter();
  });

  function initParameterCounter() {
    const button = document.getElementById('count-params');
    if (!button) return;

    button.addEventListener('click', () => {
      if (counting) return;
      counting = true;
      button.textContent = 'Counting...';
      
      // Animate counts
      animateCount('pf-count', 0, PARAMS.pf, 1000, () => {
        animateCount('sm-count', 0, PARAMS.sm, 1500, () => {
          // For string theory, show 10^500
          const stCount = document.getElementById('st-count');
          if (stCount) {
            stCount.textContent = '10^500';
            stCount.classList.add('st');
          }
          counting = false;
          button.textContent = 'Count Again';
        });
      });
    });
  }

  function animateCount(elementId, start, end, duration, callback) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const range = end - start;
    const startTime = performance.now();
    
    element.classList.add('pf');

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease-out quart
      const eased = 1 - Math.pow(1 - progress, 4);
      const current = Math.floor(start + range * eased);
      
      element.textContent = current.toLocaleString();
      
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.classList.add('complete');
        if (callback) callback();
      }
    }

    requestAnimationFrame(update);
  }

  // Add hover effects to table rows
  document.querySelectorAll('.comparison-table tbody tr').forEach(row => {
    row.addEventListener('mouseenter', () => {
      row.querySelectorAll('td').forEach(cell => {
        cell.style.background = 'rgba(0, 207, 255, 0.08)';
      });
    });
    
    row.addEventListener('mouseleave', () => {
      row.querySelectorAll('td').forEach(cell => {
        cell.style.background = '';
      });
    });
  });

  // Add click-to-expand for falsify cards
  document.querySelectorAll('.falsify-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('expanded');
    });
  });

  // Add scale segment tooltips
  document.querySelectorAll('.scale-segment').forEach(segment => {
    segment.addEventListener('mouseenter', () => {
      const frameworks = segment.getAttribute('data-frameworks') || segment.getAttribute('data-framework');
      if (frameworks) {
        segment.style.transform = 'scale(1.05)';
        segment.style.zIndex = '10';
      }
    });
    
    segment.addEventListener('mouseleave', () => {
      segment.style.transform = '';
      segment.style.zIndex = '';
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      // Close any expanded cards
      document.querySelectorAll('.falsify-card.expanded').forEach(card => {
        card.classList.remove('expanded');
      });
    }
  });

  console.log('Framework Comparison loaded — PF: 3 axioms, SM: 19 params, String: 10^500 vacua');

})();
