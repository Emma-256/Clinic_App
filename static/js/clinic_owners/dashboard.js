/* ════════════════════════════════════
   CLINIC OWNER DASHBOARD
   File: static/medi_clinics/js/dashboard.js
════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Animate progress bars on load ── */
  function animateProgressBars() {
    document.querySelectorAll('.progress-bar-fill[data-width]').forEach(function (bar) {
      var target = bar.getAttribute('data-width') || '0';
      setTimeout(function () {
        bar.style.width = target + '%';
      }, 200);
    });
  }

  /* ── Stamp today's date in the hero ── */
  function stampDate() {
    var el = document.getElementById('dashDate');
    if (!el) return;
    var now = new Date();
    el.textContent = now.toLocaleDateString('en-GB', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
    });
  }

  /* ── Metric counter animation ── */
  function animateCounters() {
    document.querySelectorAll('.metric-value[data-count]').forEach(function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      if (isNaN(target) || target === 0) { el.textContent = '0'; return; }
      var start     = 0;
      var duration  = 900;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased    = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
        el.textContent = Math.floor(eased * target);
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = target;
      }
      requestAnimationFrame(step);
    });
  }

  /* ── Init ── */
  document.addEventListener('DOMContentLoaded', function () {
    stampDate();
    animateProgressBars();
    animateCounters();
  });

})();
