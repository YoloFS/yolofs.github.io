// site.js — site-wide shared bootstrap: analytics + top nav.
// Loaded once per page via <script src="site.js" defer>; runs after DOM
// parse but before DOMContentLoaded.
(function () {
  // ── Google Analytics (gtag.js) ─────────────────────────────────────────
  const GA_ID = 'G-SFYLJ3XS27';
  const gaTag = document.createElement('script');
  gaTag.async = true;
  gaTag.src   = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(gaTag);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', GA_ID);

  // ── Top nav ────────────────────────────────────────────────────────────
  const ITEMS = [
    { key: 'home',   href: 'index.html',  label: 'Home' },
    { key: 'study',  href: 'study.html',  label: 'Study' },
    { key: 'design', href: 'design.html', label: 'Design' },
    { key: 'bench',  href: 'bench.html',  label: 'Bench' },
    { key: 'perf',   href: 'perf.html',   label: 'Perf' },
    { key: 'paper',  href: 'paper.pdf',   label: 'Paper' }
  ];

  // All pages currently live at the site root.
  const PREFIX = '';

  // Which nav item should be highlighted? Matches by URL substring.
  function activeKey() {
    const p = location.pathname;
    if (/study\.html/.test(p))  return 'study';
    if (/design\.html/.test(p)) return 'design';
    if (/bench\.html/.test(p))  return 'bench';
    if (/perf\.html/.test(p))   return 'perf';
    return 'home';
  }

  const ACTIVE = activeKey();
  const isExternal = h => /^https?:/.test(h);
  const resolve    = h => isExternal(h) ? h : PREFIX + h;

  function buildNav() {
    const wrap = document.querySelector('.topnav .wrap');
    if (!wrap) return;
    const brand =
      `<a href="${resolve('index.html')}" class="brand">` +
      `<span class="label">YoloFS</span></a>`;
    const links = ITEMS.map(it => {
      const cls = it.key === ACTIVE ? ' class="active"' : '';
      return `<a href="${resolve(it.href)}"${cls}>${it.label}</a>`;
    }).join('');
    wrap.innerHTML = brand + '<nav>' + links + '</nav>';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildNav);
  } else {
    buildNav();
  }
})();
