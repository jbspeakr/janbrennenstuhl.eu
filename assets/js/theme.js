// Runs before first paint: apply stored reading settings. Storage may be unavailable; reading must still work.
try {
  const s = JSON.parse(localStorage.getItem('jb-reader') || '{}');
  const root = document.documentElement;
  if (s.theme === 'light' || s.theme === 'dark') root.dataset.theme = s.theme;
  if (s.size === 's' || s.size === 'l') root.dataset.size = s.size;
  if (s.leading === 'l') root.dataset.leading = 'l';
} catch (_) { /* Follow system defaults. */ }
