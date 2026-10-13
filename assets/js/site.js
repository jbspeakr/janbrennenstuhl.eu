(() => {
  const theme = document.querySelector('#theme');
  theme.value = document.documentElement.dataset.theme || 'system';
  theme.closest('label').hidden = false;
  theme.addEventListener('change', () => {
    if (theme.value === 'system') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = theme.value;
    try {
      if (theme.value === 'system') localStorage.removeItem('jb-theme');
      else localStorage.setItem('jb-theme', theme.value);
    } catch (_) { /* Session-only preference when storage is unavailable. */ }
  });
  const feedback = document.querySelector('#feedback');
  async function copy(text, button) {
    try {
      await navigator.clipboard.writeText(text);
      feedback.textContent = 'Copied to clipboard.';
      const label = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = label; }, 1800);
    } catch (_) { feedback.textContent = 'Could not copy. Select the text and copy it manually.'; }
  }
  if (navigator.clipboard && window.isSecureContext) {
    document.querySelectorAll('[data-copy]').forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => copy(button.dataset.copy, button));
    });
    document.querySelectorAll('.highlight').forEach(block => {
      const code = block.querySelector('code');
      if (!code) return;
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'copy-code'; button.textContent = 'Copy code';
      button.addEventListener('click', () => copy(code.textContent, button));
      block.append(button);
    });
  }
  // Tables and code scroll independently, including with keyboard navigation.
  document.querySelectorAll('.prose table:not(.table-scroll table)').forEach(table => {
    const region = document.createElement('div');
    region.className = 'table-scroll'; region.tabIndex = 0;
    region.setAttribute('role', 'region'); region.setAttribute('aria-label', 'Scrollable table');
    table.before(region); region.append(table);
  });
  document.querySelectorAll('pre').forEach(pre => { pre.tabIndex = 0; });
})();
