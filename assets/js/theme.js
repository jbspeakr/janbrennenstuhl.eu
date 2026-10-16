// Runs before first paint: apply a stored theme choice. Storage may be unavailable; reading must still work.
try {
  const s = JSON.parse(localStorage.getItem('jb-reader') || '{}');
  if (s.theme === 'light' || s.theme === 'dark') document.documentElement.dataset.theme = s.theme;
} catch (_) { /* Follow the system theme. */ }
// Plausible queue stub (the script itself is loaded only on the production host, see head.html).
window.plausible = window.plausible || function () { (window.plausible.q = window.plausible.q || []).push(arguments); };
window.plausible.init = window.plausible.init || function (o) { window.plausible.o = o || {}; };
window.plausible.init();
