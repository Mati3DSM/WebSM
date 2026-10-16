/* Supermarket — page slide transitions (cross-document View Transitions).
   Se carga en el <head>, sin defer: tiene que correr antes del primer render
   de la página nueva. Solo decide la DIRECCIÓN del slide y la deja escrita en
   <html data-nav="forwards|backwards">; la animación vive en styles.css.

   Orden = el del menú. Ir a una página que está más a la derecha en el menú
   ("forwards") hace que la actual salga hacia la izquierda y la nueva entre
   desde la derecha; ir a una que está más a la izquierda ("backwards"), al
   revés. Las fichas de proyecto (work/*.html) cuentan como un paso después de
   Works: Works → proyecto entra desde la derecha, proyecto → Works vuelve.
   Navegadores sin soporte simplemente navegan sin animación.              */
(function () {
  var ORDER = ['index', 'services', 'works', 'about', 'reel', 'contact'];   // igual que NAV en build.py
  var root = document.documentElement;

  function idx(url) {
    var p;
    try { p = new URL(url, location.href).pathname; } catch (e) { return -1; }
    if (/\/work\//.test(p)) return ORDER.indexOf('works') + 0.5;   // fichas de proyecto: un nivel después de Works
    var name = p.replace(/\/+$/, '').split('/').pop().replace(/\.html$/, '');
    return ORDER.indexOf(name || 'index');
  }

  function direction(fromUrl, toUrl, act) {
    var a = idx(fromUrl), b = idx(toUrl);
    if (a >= 0 && b >= 0 && a !== b) return b > a ? 'forwards' : 'backwards';
    // misma sección (p. ej. de un proyecto a otro): se usa el historial si hay botón atrás/adelante
    if (act && act.navigationType === 'traverse' && act.from && act.entry) {
      return act.entry.index < act.from.index ? 'backwards' : 'forwards';
    }
    return 'forwards';
  }

  function apply(from, to, act) { root.setAttribute('data-nav', direction(from, to, act)); }

  /* Página que entra: se decide ahora mismo, antes del primer render, sin
     depender de ningún evento que pueda llegar tarde. */
  try {
    var act = window.navigation && window.navigation.activation;
    if (act && act.from && act.entry) {
      apply(act.from.url, act.entry.url, act);
    } else if (document.referrer && new URL(document.referrer).origin === location.origin) {
      apply(document.referrer, location.href, null);   // navegadores sin navigation.activation
    }
  } catch (e) { /* sin dirección: queda el slide hacia adelante */ }

  /* Página que se va: misma regla, por si el navegador anima con los estilos de esta. */
  window.addEventListener('pageswap', function (e) {
    try {
      if (e.activation && e.activation.from && e.activation.entry) {
        apply(e.activation.from.url, e.activation.entry.url, e.activation);
      }
    } catch (x) { /* nada */ }
  });
})();
