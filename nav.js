// nav.js — single source of truth for the top nav across all YoloFS pages.
// Auto-detects the active link from window.location and prepends the right
// number of `../` so links work both on yolofs.github.io and locally.
(function () {
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
  const resolve   = h => isExternal(h) ? h : PREFIX + h;

  function build() {
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
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
