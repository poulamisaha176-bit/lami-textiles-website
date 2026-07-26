/* Scroll motion for lami textiles.
   Replaces the design-tool runtime: same behaviour, no framework. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function scan() {
    var vh = window.innerHeight;
    var sy = window.scrollY || document.documentElement.scrollTop;
    var n = 0;

    // Fade sections in as they enter the viewport, staggered.
    document.querySelectorAll('[data-reveal]:not(.in)').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.9) {
        el.style.transitionDelay = (r.bottom > 0 ? n++ * 90 : 0) + 'ms';
        el.classList.add('in');
      }
    });

    if (reduceMotion) return;

    document.querySelectorAll('[data-parallax]').forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      var p = (box.top + box.height / 2 - vh / 2) / vh;
      var amt = parseFloat(el.dataset.parallax) || 40;
      var shift = -Math.max(-1.4, Math.min(1.4, p)) * amt;
      el.style.transform = 'translate3d(0,' + shift.toFixed(1) + 'px,0)';
    });

    var hero = document.querySelector('[data-hero]');
    if (hero) {
      hero.style.transform = 'translate3d(0,' + (sy * 0.22).toFixed(1) + 'px,0) scale(' +
        (1 + Math.min(sy / vh, 1) * 0.07).toFixed(3) + ')';
    }

    var cap = document.querySelector('[data-hero-cap]');
    if (cap) cap.style.opacity = Math.max(0, 1 - sy / (vh * 0.45));
  }

  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; scan(); });
  }

  // Landing on a #hash: reveal everything first, then jump clear of the
  // sticky header, otherwise the target sits underneath it.
  function goHash() {
    var h = (location.hash || '').replace('#', '');
    if (!h) return;
    var el = document.getElementById(h);
    if (!el) return;
    document.querySelectorAll('[data-reveal]').forEach(function (e) {
      e.classList.add('in');
    });
    var y = el.getBoundingClientRect().top + (window.scrollY || 0) - 72;
    window.scrollTo(0, Math.max(0, y));
  }

  // Home hero: the hovered panel widens, the others give up the space.
  document.querySelectorAll('[data-panel]').forEach(function (panel) {
    panel.addEventListener('mouseenter', function () {
      if (!reduceMotion) panel.style.flex = '1.7';
    });
    panel.addEventListener('mouseleave', function () {
      panel.style.flex = '1';
    });
  });

  // Images settle late, so re-run once they land and positions are final.
  [0, 120, 400, 900, 1600].forEach(function (t) { setTimeout(goHash, t); });
  window.addEventListener('hashchange', goHash);
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  window.addEventListener('load', scan);
  setInterval(scan, 400);
  scan();
})();
