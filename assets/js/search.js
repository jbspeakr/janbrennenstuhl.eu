import { loadIndex, search, snippet, kindLabel } from './search-core.js';

const form = document.querySelector('#search-form');
const query = form.querySelector('#query');
const kind = form.querySelector('#kind');
const topic = form.querySelector('#topic');
const status = document.querySelector('#search-status');
const results = document.querySelector('#search-results');
const fallback = document.querySelector('#search-fallback');
let generation = 0;
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
    const hits = search(await loadIndex(), q, { kind: kind.value, topic: topic.value });
    if (current !== generation) return;
    fallback.hidden = true;
    status.textContent = hits.length ? `${hits.length} ${hits.length === 1 ? 'result' : 'results'}${q ? ` for “${q}”` : ''}.` : 'No results. Try fewer words or clear the filters.';
    for (const { entry, section, words } of hits) {
      const li = el('li', 'row search-hit');
      const a = el('a'); a.href = entry.url; a.append(el('span', 'row-title', entry.title)); li.append(a);
      const meta = el('span', 'row-meta'); meta.append(el('span', '', entry.published.slice(0, 7)), el('span', 'kind', kindLabel[entry.kind] || entry.kind)); li.append(meta);
      if (section) { const s = el('a', 'hit-section', `In this ${entry.kind === 'guide' ? 'entry' : 'article'}: ${section.title}`); s.href = `${entry.url}#${section.id}`; li.append(s); }
      li.append(el('p', 'hit-text', snippet(section ? section.text : entry.description || '', words)));
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
