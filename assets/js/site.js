/* Bishop & Adkins — minimal progressive enhancement.
   Only the mobile menu and the accordion. Layout is pure CSS flex so that
   every section maps cleanly onto a native Elementor widget. */
(function () {
  'use strict';

  /* ---- Mobile navigation ------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  var backdrop = document.querySelector('.nav-backdrop');

  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    nav.classList.toggle('open', open);
    if (backdrop) backdrop.classList.toggle('open', open);
    document.body.classList.toggle('nav-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
  }
  if (backdrop) backdrop.addEventListener('click', function () { setNav(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setNav(false);
  });

  /* Sub-menu opens on tap below the desktop breakpoint, hover above it. */
  var subParent = document.querySelector('.has-sub > a');
  if (subParent) {
    subParent.addEventListener('click', function (e) {
      if (window.innerWidth > 1024) return;      // desktop keeps the hover behaviour
      e.preventDefault();
      var sub = this.parentNode.querySelector('.sub');
      var open = sub.classList.toggle('open');
      this.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* Reset state when resizing back up to desktop. */
  var lastWide = window.innerWidth > 1024;
  window.addEventListener('resize', function () {
    var wide = window.innerWidth > 1024;
    if (wide !== lastWide) {
      lastWide = wide;
      setNav(false);
      var sub = document.querySelector('.sub');
      if (sub && wide) sub.classList.remove('open');
    }
  });

  /* ---- Accordion ---------------------------------------------------- */
  var heads = document.querySelectorAll('.acc-head');
  Array.prototype.forEach.call(heads, function (head) {
    head.addEventListener('click', function () {
      var expanded = head.getAttribute('aria-expanded') === 'true';
      var panel = document.getElementById(head.getAttribute('aria-controls'));
      head.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      if (panel) panel.classList.toggle('open', !expanded);
    });
  });

  /* ---- Contact form (static build — no back end) -------------------- */
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = document.getElementById('form-status');
      if (note) {
        note.textContent =
          'This is a static preview — the form is not yet connected. ' +
          'Please call the office at (410) 893-7453.';
        note.style.color = '#2D335B';
      }
    });
  }
})();
