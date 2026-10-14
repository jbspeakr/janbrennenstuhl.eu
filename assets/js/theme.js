// Runs before first paint: apply a stored theme choice. Storage may be unavailable; reading must still work.
try {
  const s = JSON.parse(localStorage.getItem('jb-reader') || '{}');
  if (s.theme === 'light' || s.theme === 'dark') document.documentElement.dataset.theme = s.theme;
} catch (_) { /* Follow the system theme. */ }
