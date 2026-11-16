/* ==========================================================================
   wikiSI · Control de visibilidad de paneles laterales (izquierda/derecha)
   ========================================================================== */
(function () {
  var KEY_NAV = "wikisi_hide_nav";
  var KEY_TOC = "wikisi_hide_toc";

  function readFlag(key) {
    try {
      return window.localStorage.getItem(key) === "1";
    } catch (_) {
      return false;
    }
  }

  function writeFlag(key, value) {
    try {
      window.localStorage.setItem(key, value ? "1" : "0");
    } catch (_) {
      /* Ignorar si localStorage está restringido */
    }
  }

  function hasSidebar(selector) {
    var el = document.querySelector(selector);
    return Boolean(el && !el.hasAttribute("hidden"));
  }

  function applyBodyClasses() {
    var hideNav = readFlag(KEY_NAV);
    var hideToc = readFlag(KEY_TOC);
    document.body.classList.toggle("wikisi-hide-nav", hideNav);
    document.body.classList.toggle("wikisi-hide-toc", hideToc);
    document.body.classList.toggle("wikisi-wide", hideNav || hideToc);
  }

  function syncButtons() {
    var hideNav = document.body.classList.contains("wikisi-hide-nav");
    var hideToc = document.body.classList.contains("wikisi-hide-toc");
    var bothHidden = hideNav && hideToc;

    var btnLeft = document.getElementById("btn-toggle-left");
    var btnBoth = document.getElementById("btn-toggle-both");
    var btnRight = document.getElementById("btn-toggle-right");

    if (btnLeft) {
      btnLeft.textContent = hideNav ? "▶ Mostrar menú" : "◀ Ocultar menú";
      btnLeft.classList.toggle("is-active", hideNav);
      btnLeft.setAttribute("aria-pressed", String(hideNav));
    }
    if (btnRight) {
      btnRight.textContent = hideToc ? "◀ Mostrar índice pág." : "Ocultar índice pág. ▶";
      btnRight.classList.toggle("is-active", hideToc);
      btnRight.setAttribute("aria-pressed", String(hideToc));
    }
    if (btnBoth) {
      btnBoth.textContent = bothHidden ? "🗗 Vista normal" : "⛶ Ancho completo";
      btnBoth.classList.toggle("is-active", bothHidden);
      btnBoth.setAttribute("aria-pressed", String(bothHidden));
    }
  }

  function toggleLeft() {
    var next = !document.body.classList.contains("wikisi-hide-nav");
    writeFlag(KEY_NAV, next);
    applyBodyClasses();
    syncButtons();
  }

  function toggleRight() {
    var next = !document.body.classList.contains("wikisi-hide-toc");
    writeFlag(KEY_TOC, next);
    applyBodyClasses();
    syncButtons();
  }

  function toggleBoth() {
    var hideNav = document.body.classList.contains("wikisi-hide-nav");
    var hideToc = document.body.classList.contains("wikisi-hide-toc");
    var next = !(hideNav && hideToc);
    writeFlag(KEY_NAV, next);
    writeFlag(KEY_TOC, next);
    applyBodyClasses();
    syncButtons();
  }

  function injectToolbar() {
    applyBodyClasses();

    var hasLeft = hasSidebar(".md-sidebar--primary");
    var hasRight = hasSidebar(".md-sidebar--secondary");
    if (!hasLeft && !hasRight) {
      return;
    }

    var container = document.querySelector(".md-content__inner");
    if (!container || document.getElementById("wikisi-layout-toolbar")) {
      syncButtons();
      return;
    }

    var bar = document.createElement("div");
    bar.id = "wikisi-layout-toolbar";
    bar.className = "wikisi-layout-toolbar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Controles de paneles laterales");

    if (hasLeft) {
      var bLeft = document.createElement("button");
      bLeft.type = "button";
      bLeft.id = "btn-toggle-left";
      bLeft.className = "wikisi-layout-btn wikisi-layout-btn--left";
      bLeft.title = "Colapsar o mostrar el menú de navegación izquierdo (tecla [)";
      bLeft.addEventListener("click", toggleLeft);
      bar.appendChild(bLeft);
    }

    if (hasLeft && hasRight) {
      var bBoth = document.createElement("button");
      bBoth.type = "button";
      bBoth.id = "btn-toggle-both";
      bBoth.className = "wikisi-layout-btn wikisi-layout-btn--both";
      bBoth.title = "Alternar ancho completo ocultando o mostrando ambos laterales (tecla \\)";
      bBoth.addEventListener("click", toggleBoth);
      bar.appendChild(bBoth);
    }

    if (hasRight) {
      var bRight = document.createElement("button");
      bRight.type = "button";
      bRight.id = "btn-toggle-right";
      bRight.className = "wikisi-layout-btn wikisi-layout-btn--right";
      bRight.title = "Colapsar o mostrar la tabla de contenidos derecha (tecla ])";
      bRight.addEventListener("click", toggleRight);
      bar.appendChild(bRight);
    }

    var hint = document.createElement("span");
    hint.className = "wikisi-layout-hint";
    hint.textContent = "Atajos: [ izq. · ] der. · \\ ambos";
    bar.appendChild(hint);

    container.insertBefore(bar, container.firstChild);
    syncButtons();
  }

  function onKeydown(e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
    if (tag === "input" || tag === "textarea" || tag === "select" || (e.target && e.target.isContentEditable)) {
      return;
    }
    if (e.key === "[" && hasSidebar(".md-sidebar--primary")) {
      toggleLeft();
    } else if (e.key === "]" && hasSidebar(".md-sidebar--secondary")) {
      toggleRight();
    } else if (e.key === "\\" && hasSidebar(".md-sidebar--primary") && hasSidebar(".md-sidebar--secondary")) {
      toggleBoth();
    }
  }

  if (!window.__wikisiLayoutBound) {
    window.__wikisiLayoutBound = true;
    document.addEventListener("keydown", onKeydown);
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(injectToolbar);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectToolbar);
  } else {
    injectToolbar();
  }
})();
