import { search, excerptNodes, shortDate, kindLabel } from './search-core.js';

const form = document.querySelector('#search-form');
const query = form.querySelector('#query');
const kind = form.querySelector('#kind');
const topic = form.querySelector('#topic');
const status = document.querySelector('#search-status');
const results = document.querySelector('#search-results');
const fallback = document.querySelector('#search-fallback');
let generation = 0;

// Name the one shortcut this reader has; none on touch devices. Without JS the page names both.
const hint = document.querySelector('.shortcut-hint');
if (hint) {
  if (!matchMedia('(pointer: fine)').matches) hint.remove();
  else { const key = document.createElement('kbd'); key.textContent = /Mac|iPhone|iPad/.test(navigator.platform) ? '⌘K' : 'Ctrl K'; hint.replaceChildren('Press ', key, ' anywhere for quick search.'); }
}

const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; };

function readURL() {
  const p = new URLSearchParams(location.search);
  query.value = p.get('q') || p.get('keyword') || '';
  kind.value = p.get('kind') === 'research' ? 'guide' : p.get('kind') || '';
  topic.value = p.get('topic') || '';
}

async function run(push = false) {
  const current = ++generation;
  const q = query.value.trim();
  if (push) {
    const p = new URLSearchParams();
    if (q) p.set('q', q);
    if (kind.value) p.set('kind', kind.value);
    if (topic.value) p.set('topic', topic.value);
    history.pushState(null, '', location.pathname + (p.size ? `?${p}` : ''));
  }
  results.replaceChildren();
  if (!q && !kind.value && !topic.value) { fallback.hidden = false; status.textContent = 'Enter a phrase to search, or browse everything below.'; return; }
  status.textContent = 'Searching…';
  try {
    const { total, hits } = await search(q, { kind: kind.value, topic: topic.value, limit: 30 });
    if (current !== generation) return;
    fallback.hidden = true;
    const shown = total > hits.length ? ` Showing the first ${hits.length}.` : '';
    status.textContent = total ? `${total} ${total === 1 ? 'result' : 'results'}${q ? ` for “${q}”` : ''}.${shown}` : 'No results. Try fewer words or clear the filters.';
    for (const hit of hits) {
      const li = el('li', 'row search-hit');
      const a = el('a'); a.href = hit.url; a.append(el('span', 'row-title', hit.title)); li.append(a);
      const meta = el('span', 'row-meta'); meta.append(el('span', '', shortDate(hit.date)), el('span', 'kind', kindLabel[hit.kind] || hit.kind)); li.append(meta);
      if (hit.section) { const s = el('a', 'hit-section', `In this ${hit.kind === 'guide' ? 'entry' : 'article'}: ${hit.section.title}`); s.href = hit.section.url; li.append(s); }
      const text = el('p', 'hit-text'); text.append(excerptNodes(hit.excerpt)); li.append(text);
      results.append(li);
    }
  } catch (_) {
    if (current !== generation) return;
    fallback.hidden = false;
    status.textContent = 'Search could not load. Browse everything below, or try again.';
  }
}

form.addEventListener('submit', event => { event.preventDefault(); run(true); });
[kind, topic].forEach(s => s.addEventListener('change', () => run(true)));
addEventListener('popstate', () => { readURL(); run(); });
readURL(); run();
