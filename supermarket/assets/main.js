/* Supermarket — shared behaviour. No dependencies. */

/* ---- Mobile navigation ---- */
(function () {
  var toggle = document.querySelector('.nav__toggle');
  var nav = document.getElementById('nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    var open = nav.getAttribute('data-open') === 'true';
    nav.setAttribute('data-open', String(!open));
    toggle.setAttribute('aria-expanded', String(!open));
    toggle.textContent = open ? 'Menu' : 'Close';
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
      nav.setAttribute('data-open', 'false');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Menu';
      toggle.focus();
    }
  });
})();

/* ---- Works index: cursor-following preview ----
   Each row carries data-img. Swap those URLs for the real
   project thumbnails and nothing else needs to change.      */
(function () {
  var index = document.querySelector('[data-index]');
  if (!index) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (window.matchMedia('(hover: none)').matches) return;

  var preview = document.createElement('div');
  preview.className = 'preview';
  preview.innerHTML = '<img alt="">';
  document.body.appendChild(preview);
  var img = preview.querySelector('img');

  var x = 0, y = 0, cx = 0, cy = 0, raf = null, on = false;

  function loop() {
    cx += (x - cx) * 0.16;
    cy += (y - cy) * 0.16;
    preview.style.transform =
      'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%) scale(' + (on ? 1 : 0.96) + ')';
    raf = requestAnimationFrame(loop);
  }

  index.addEventListener('pointermove', function (e) {
    x = e.clientX + 130;
    y = e.clientY;
    if (!raf) { cx = x; cy = y; loop(); }
  });

  index.addEventListener('pointerover', function (e) {
    var row = e.target.closest('[data-img]');
    if (!row) return;
    img.src = row.getAttribute('data-img');
    on = true;
    preview.setAttribute('data-on', 'true');
  });

  index.addEventListener('pointerout', function (e) {
    if (e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest('[data-img]')) return;
    on = false;
    preview.setAttribute('data-on', 'false');
  });

  index.addEventListener('pointerleave', function () {
    on = false;
    preview.setAttribute('data-on', 'false');
  });
})();

/* ---- Contact form ----
   Front-end states only. Point `action` at your endpoint
   (Formspree, Webflow, a serverless function) to go live.  */
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var ok = document.querySelector('.form__msg--ok');
  var err = document.querySelector('.form__msg--err');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    ok.setAttribute('data-show', 'false');
    err.setAttribute('data-show', 'false');

    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    var message = form.elements.message.value.trim();
    var valid = name && message && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    if (!valid) {
      err.setAttribute('data-show', 'true');
      err.focus && err.focus();
      return;
    }
    ok.setAttribute('data-show', 'true');
    form.reset();
  });
})();

/* ---- Works: grid / index view switch ---- */
(function () {
  var box = document.getElementById('works');
  if (!box) return;
  var btns = document.querySelectorAll('.views__btn');
  Array.prototype.forEach.call(btns, function (btn) {
    btn.addEventListener('click', function () {
      var view = btn.getAttribute('data-view');
      box.setAttribute('data-current', view);
      Array.prototype.forEach.call(btns, function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
    });
  });
})();
