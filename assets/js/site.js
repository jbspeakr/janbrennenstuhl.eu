const root = document.documentElement;
const feedback = document.querySelector('#feedback');
const announce = message => { feedback.textContent = ''; requestAnimationFrame(() => { feedback.textContent = message; }); };

// Reading settings: theme, text size, line spacing. Stored locally only.
const reader = document.querySelector('.reader');
if (reader) {
  let state = {};
  try { state = JSON.parse(localStorage.getItem('jb-reader') || '{}'); } catch (_) { /* session only */ }
  const apply = () => {
    for (const [key, attr, def] of [['theme', 'theme', 'system'], ['size', 'size', 'm'], ['leading', 'leading', 'm']]) {
      const value = state[key] || def;
      if (value === def) delete root.dataset[attr]; else root.dataset[attr] = value;
      const input = reader.querySelector(`input[name="${key}"][value="${value}"]`);
      if (input) input.checked = true;
    }
  };
  apply();
  reader.hidden = false;
  reader.addEventListener('change', event => {
    state[event.target.name] = event.target.value;
    apply();
    try { localStorage.setItem('jb-reader', JSON.stringify(state)); } catch (_) { /* session only */ }
  });
  document.addEventListener('click', event => { if (reader.open && !reader.contains(event.target)) reader.open = false; });
  reader.addEventListener('keydown', event => { if (event.key === 'Escape' && reader.open) { reader.open = false; reader.querySelector('summary').focus(); } });
}

// Copy actions: links, citations, quotes with their anchor URL, code blocks.
const canCopy = navigator.clipboard && window.isSecureContext;
async function copy(text, button, done = 'Copied') {
  try {
    await navigator.clipboard.writeText(text);
    announce('Copied to clipboard.');
    const label = button.textContent;
    button.textContent = done;
    setTimeout(() => { button.textContent = label; }, 1600);
  } catch (_) { announce('Could not copy. Select the text and copy it manually.'); }
}
if (canCopy) {
  const title = document.querySelector('h1')?.textContent.trim();
  document.querySelectorAll('[data-copy]').forEach(b => { b.hidden = false; b.addEventListener('click', () => copy(b.dataset.copy, b)); });
  document.querySelectorAll('[data-quote]').forEach(b => {
    b.hidden = false;
    b.addEventListener('click', () => copy(`“${b.dataset.quote}” (Jan Brennenstuhl, ${title}) ${b.dataset.quoteUrl}`, b));
  });
  document.querySelectorAll('figure.code').forEach(figure => {
    const code = figure.querySelector('code');
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'link-button copy-code'; button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code');
    button.addEventListener('click', () => copy(code.textContent, button));
    figure.append(button);
  });
}

// Table of contents: collapsed in the HTML so narrow screens keep the text close; opened where it has its own column.
const tocBox = document.querySelector('.toc-box');
if (tocBox && matchMedia('(min-width: 70rem)').matches) tocBox.open = true;

// Table of contents: mark the section being read.
const tocLinks = [...document.querySelectorAll('.toc a[href^="#"]')];
if (tocLinks.length && 'IntersectionObserver' in window) {
  const byId = new Map(tocLinks.map(a => [decodeURIComponent(a.hash.slice(1)), a]));
  const headings = [...byId.keys()].map(id => document.getElementById(id)).filter(Boolean);
  let current;
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      current?.removeAttribute('aria-current');
      current = byId.get(entry.target.id);
      current?.setAttribute('aria-current', 'true');
    }
  }, { rootMargin: '0px 0px -70% 0px' });
  headings.forEach(h => observer.observe(h));
}

// Command palette: loaded on demand with ⌘K / Ctrl+K or the search button. The link still works without JS.
const trigger = document.querySelector('[data-palette]');
if (trigger && 'HTMLDialogElement' in window) {
  const mac = /Mac|iPhone|iPad/.test(navigator.platform);
  const kbd = trigger.querySelector('kbd');
  if (kbd && matchMedia('(pointer: fine)').matches) { kbd.textContent = mac ? '⌘K' : 'Ctrl K'; kbd.hidden = false; }
  let palette;
  const open = async () => {
    try {
      palette ||= await import(trigger.dataset.palette);
      palette.open();
    } catch (_) { location.href = trigger.href; }
  };
  trigger.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (location.pathname === '/search/') return;
    event.preventDefault(); open();
  });
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); open(); }
  });
}
