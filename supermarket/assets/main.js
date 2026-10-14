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

  var x = 0, y = 0, cx = 0, cy = 0, raf = null, on = false, placed = false;

  /* The loop only runs while the preview is still easing toward the
     cursor; once it settles it stops and waits for the next event.  */
  function start() {
    if (!raf) raf = requestAnimationFrame(loop);
  }

  function loop() {
    cx += (x - cx) * 0.16;
    cy += (y - cy) * 0.16;
    preview.style.transform =
      'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%) scale(' + (on ? 1 : 0.96) + ')';
    if (Math.abs(x - cx) < 0.1 && Math.abs(y - cy) < 0.1) {
      raf = null;
      return;
    }
    raf = requestAnimationFrame(loop);
  }

  index.addEventListener('pointermove', function (e) {
    x = e.clientX + 130;
    y = e.clientY;
    if (!placed) { cx = x; cy = y; placed = true; }
    start();
  });

  index.addEventListener('pointerover', function (e) {
    var row = e.target.closest('[data-img]');
    if (!row) return;
    img.src = row.getAttribute('data-img');
    on = true;
    preview.setAttribute('data-on', 'true');
    start();
  });

  index.addEventListener('pointerout', function (e) {
    if (e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest('[data-img]')) return;
    on = false;
    preview.setAttribute('data-on', 'false');
    start();
  });

  index.addEventListener('pointerleave', function () {
    on = false;
    preview.setAttribute('data-on', 'false');
    start();
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


/* ---- Paper bend on scroll ----
   Todo el contenido de la página (imágenes y textos) entra desde el borde
   inferior de la pantalla curvado como una hoja de papel y se aplana a medida
   que sube. Ajustá todo desde CFG.

   Se aplica solo, sin clases ni marcado extra: cualquier <img>, título,
   párrafo, ítem de lista, leyenda o botón (incluido el título del hero).
   Quedan planos a propósito:
     · el video del hero, el header y el menú
     · videos e iframes (YouTube/Vimeo) y el formulario
     · el módulo "sheet" (sus imágenes forman una sola continua)
     · las marquesinas animadas y la vista "index" de works
   Para excluir algo más, agregá su selector a SKIP.

   Cómo funciona: cada elemento cercano a la zona se parte en tiras
   horizontales que se inclinan en cadena (rotateX + perspectiva). Cuánto se
   inclina cada tira depende de qué tan cerca está del borde inferior de la
   pantalla. Mientras el elemento está plano se muestra el original.        */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  var CFG = {
    settle: 0.80,       // altura de la pantalla (0 = arriba, 1 = abajo) desde donde empieza a curvarse
    angle: 34,          // curvatura máxima en el borde inferior, en grados (0 = sin efecto)
    strips: 256,         // máximo de tiras por elemento (los chicos usan menos)
    perspective: 1000,  // px: menor = perspectiva más marcada
    shade: 0,           // sombra en la zona curvada (0 = sin sombra, 0.55 = intensa)
    images: true,       // false = no tocar imágenes
    text: true,         // false = no tocar textos
    hero: true          // false = dejar plano el texto del hero
  };
  var TXT_SEL = 'h1,h2,h3,h4,h5,h6,p,li,dt,dd,figcaption,blockquote,.btn,.footer__cta,.work__back,.pager__side > span';
  var SKIP = '.header, .skip, .nav, .index, .preview, .marquee, .form, .shot--sheet, [aria-hidden="true"]';

  /* propiedades que se copian a la versión en tiras de cada texto */
  var PROPS = ['font-family', 'font-size', 'font-weight', 'font-style', 'font-stretch',
    'font-variation-settings', 'font-feature-settings', 'line-height', 'letter-spacing',
    'word-spacing', 'text-transform', 'text-align', 'text-indent', 'text-decoration-line',
    'text-decoration-color', 'text-wrap', 'white-space', 'word-break', 'overflow-wrap',
    'hyphens', 'color', 'display', 'max-width', 'margin-top', 'margin-bottom',
    'padding-top', 'padding-right', 'padding-bottom', 'padding-left', 'list-style-type',
    'flex-direction', 'justify-content', 'align-items', 'gap', 'background-color',
    'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
    'border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style',
    'border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color',
    'border-top-left-radius', 'border-top-right-radius', 'border-bottom-right-radius', 'border-bottom-left-radius'];

  var items = [], raf = null, lastY = window.scrollY, vel = 0;

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  function add(el, kind) {
    var it = { kind: kind, el: el, frame: kind === 'img' ? el.parentElement : null, stage: null,
               strips: [], n: 0, h: 0, w: 0, hh: 0, vis: false, built: false, on: false, skip: false };
    el._bend = it;
    items.push(it);
    return it;
  }

  if (CFG.images) {
    Array.prototype.forEach.call(document.querySelectorAll('img'), function (img) {
      if (img.closest(SKIP) || (!CFG.hero && img.closest('.hero'))) return;
      var it = add(img, 'img');
      img.addEventListener('load', function () { start(); });
    });
  }
  if (CFG.text) {
    Array.prototype.forEach.call(document.querySelectorAll(TXT_SEL), function (el) {
      if (el.closest(SKIP) || (!CFG.hero && el.closest('.hero'))) return;
      if (el.querySelector(TXT_SEL)) return;            // se usa el elemento más interno
      if (!el.textContent.trim()) return;
      add(el, 'txt');
    });
  }
  if (!items.length) return;

  function ready(it) {
    if (it.kind === 'img') return it.el.complete && it.el.naturalWidth > 0;
    return !document.fonts || document.fonts.status !== 'loading';
  }

  function inlineStyles(src, dst) {
    var cs = getComputedStyle(src), out = '';
    for (var i = 0; i < PROPS.length; i++) out += PROPS[i] + ':' + cs.getPropertyValue(PROPS[i]) + ';';
    dst.style.cssText = out;
    dst.removeAttribute('id');
    for (var j = 0; j < src.children.length; j++) inlineStyles(src.children[j], dst.children[j]);
  }

  function build(it, r) {
    var W = r.width, H = r.height;
    if (W < 2 || H < 2) return false;
    if (it.kind === 'img' && (W < 60 || H < 60)) { it.skip = true; return false; }   // íconos, logos
    var n = clamp(Math.round(H / 12), 6, CFG.strips), h = H / n;

    it.stage = document.createElement('div');
    it.stage.setAttribute('aria-hidden', 'true');
    it.stage.style.cssText = 'position:absolute;left:0;top:0;display:none;pointer-events:none;z-index:1;' +
      'perspective:' + CFG.perspective + 'px;width:' + W + 'px;height:' + H + 'px';
    document.body.appendChild(it.stage);
    it.strips = [];

    var tpl, cs, src, disp;
    if (it.kind === 'img') {
      cs = getComputedStyle(it.el); src = it.el.currentSrc || it.el.src;
    } else {
      tpl = it.el.cloneNode(true);
      inlineStyles(it.el, tpl);
      disp = getComputedStyle(it.el).display;
      disp = /flex/.test(disp) ? 'flex' : /grid/.test(disp) ? 'grid' : 'block';
    }

    for (var k = 0; k < n; k++) {
      var el = document.createElement('div');
      el.style.cssText = 'position:absolute;left:0;right:0;overflow:hidden;transform-origin:50% 0;' +
        'top:' + (k * h) + 'px;height:' + (k === n - 1 ? h : h + 1.5) + 'px';   // solape: sin costuras
      var c;
      if (it.kind === 'img') {
        c = document.createElement('img');
        c.alt = ''; c.decoding = 'async'; c.src = src;
        c.style.cssText = 'position:absolute;left:0;display:block;margin:0;max-width:none;' +
          'width:' + W + 'px;height:' + H + 'px;top:' + (-k * h) + 'px;' +
          'object-fit:' + cs.objectFit + ';object-position:' + cs.objectPosition;
      } else {
        c = tpl.cloneNode(true);
        c.style.position = 'absolute'; c.style.left = '0'; c.style.top = (-k * h) + 'px';
        c.style.margin = '0'; c.style.width = W + 'px'; c.style.boxSizing = 'border-box';
        c.style.display = disp; c.style.height = 'auto'; c.style.maxWidth = 'none';
        c.style.transition = 'none';
      }
      el.appendChild(c);
      var sh = null;
      if (CFG.shade > 0) {
        sh = document.createElement('i');
        sh.style.cssText = 'position:absolute;left:0;top:0;right:0;bottom:0;background:#000;opacity:0;pointer-events:none';
        el.appendChild(sh);
      }
      it.stage.appendChild(el);
      it.strips.push({ el: el, sh: sh });
    }
    it.n = n; it.h = h; it.w = W; it.hh = H; it.built = true;
    return true;
  }

  function flat(it) {
    it.on = false;
    it.el.style.removeProperty('visibility');
    if (it.frame) it.frame.style.removeProperty('background-color');   // vuelve el gris de carga del marco
    if (it.stage) it.stage.style.display = 'none';
  }

  function teardown(it) {
    if (it.on) flat(it);
    if (it.stage) { it.stage.remove(); it.stage = null; }
    it.strips = []; it.built = false;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var it = en.target._bend;
      if (it) it.vis = en.isIntersecting;
    });
    start();
  }, { rootMargin: '120px 0px' });
  items.forEach(function (it) { io.observe(it.el); });

  function start() { if (!raf) raf = requestAnimationFrame(loop); }

  function loop() {
    var vh = window.innerHeight, vw = window.innerWidth, y = window.scrollY, x = window.scrollX;
    vel += ((y - lastY) - vel) * 0.15; lastY = y;
    var amp = CFG.angle * (1 + clamp(Math.abs(vel) / 40, 0, 1) * 0.35);   // scroll rápido = más elástico
    // al llegar al final de la página el efecto se apaga, para que el footer quede plano
    var rest = document.documentElement.scrollHeight - (y + vh);
    amp *= clamp(rest / (vh * 0.35), 0, 1);
    var zone = vh * CFG.settle, span = vh - zone;

    items.forEach(function (it) {
      if (it.skip) return;
      if (!it.vis) { if (it.built) teardown(it); return; }

      var r = it.el.getBoundingClientRect();   // el original conserva su layout aunque esté oculto
      if (r.bottom < zone - 120 || r.top > vh + 300) { if (it.on) flat(it); return; }   // lejos de la zona

      if (it.built && (Math.abs(r.width - it.w) > 1 || Math.abs(r.height - it.hh) > 1)) teardown(it);
      if (!it.built && !(ready(it) && build(it, r))) return;

      if (r.bottom < zone || r.top > vh + 10) { if (it.on) flat(it); return; }

      if (!it.on) {
        it.on = true;
        it.el.style.visibility = 'hidden';
        if (it.frame) it.frame.style.backgroundColor = 'transparent';   // sin gris detrás mientras se deforma
        it.stage.style.display = 'block';
      }
      it.stage.style.left = (r.left + x) + 'px';
      it.stage.style.top = (r.top + y) + 'px';
      // el "ojo" de la perspectiva es el centro de la pantalla
      it.stage.style.perspectiveOrigin = (vw / 2 - r.left).toFixed(1) + 'px ' + (vh / 2 - r.top).toFixed(1) + 'px';

      var yy = 0, zz = 0, h = it.h;
      for (var k = 0; k < it.n; k++) {
        var u = clamp((r.top + k * h + h * 0.5 - zone) / span, 0, 1);
        var phi = amp * u * u, rad = phi * Math.PI / 180, st = it.strips[k];
        st.el.style.transform = 'translate3d(0,' + (yy - k * h).toFixed(2) + 'px,' + zz.toFixed(2) + 'px) rotateX(' + phi.toFixed(2) + 'deg)';
        if (st.sh) st.sh.style.opacity = ((1 - Math.cos(rad)) * CFG.shade).toFixed(3);
        yy += h * Math.cos(rad); zz += h * Math.sin(rad);
      }
    });

    raf = (Math.abs(vel) > 0.5) ? requestAnimationFrame(loop) : null;
  }

  window.addEventListener('scroll', start, { passive: true });
  window.addEventListener('resize', function () { items.forEach(teardown); start(); });
  window.addEventListener('load', start);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { items.forEach(teardown); start(); });
  start();
})();
