/* ════════════════════════════════════
   MEDI CLINICS — HOME PAGE
   File: static/medi_clinics/js/home.js
════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Scroll-reveal ── */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    els.forEach(function(el) { observer.observe(el); });
  }

  /* ── Animated stat counters ── */
  function animateCounters() {
    var els = document.querySelectorAll('.stat-num[data-count]');
    if (!els.length) return;

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);

        var el       = entry.target;
        var target   = parseInt(el.getAttribute('data-count'), 10);
        var suffix   = el.getAttribute('data-suffix') || '';
        var duration = 1200;
        var start    = null;

        function step(ts) {
          if (!start) start = ts;
          var progress = Math.min((ts - start) / duration, 1);
          var eased    = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.floor(eased * target) + suffix;
          if (progress < 1) requestAnimationFrame(step);
          else el.textContent = target + suffix;
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });

    els.forEach(function(el) { observer.observe(el); });
  }

  /* ── Init ── */
  document.addEventListener('DOMContentLoaded', function () {
    initReveal();
    animateCounters();
  });

})();