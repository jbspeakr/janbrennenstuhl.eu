// Runs before first paint: apply a stored theme choice. Storage may be unavailable; reading must still work.
try {
  const s = JSON.parse(localStorage.getItem('jb-reader') || '{}');
  if (s.theme === 'light' || s.theme === 'dark') {
    document.documentElement.dataset.theme = s.theme;
    // The browser's own chrome follows the reader's choice too, not only the system setting.
    for (const m of document.querySelectorAll('meta[name=theme-color]')) m.content = s.theme === 'dark' ? '#16191c' : '#fafbfc';
  }
} catch (_) { /* Follow the system theme. */ }
// Plausible queue stub (the script itself is loaded only on the production host, see baseof.html).
// Events go to our own host; the edge proxies /r/e.json to plausible.io (edge/rules.toml).
window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); };
window.plausible.init = window.plausible.init || function (o) { window.plausible.o = o || {}; };
window.plausible.init({ endpoint: '/r/e.json' });
