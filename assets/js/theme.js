// Runs before first paint. Storage denial must never prevent reading.
try {
  const theme = localStorage.getItem('jb-theme');
  if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
} catch (_) { /* Follow the system preference. */ }
