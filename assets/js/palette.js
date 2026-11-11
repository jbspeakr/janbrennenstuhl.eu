import { search, kindLabel } from './search-core.js';

let dialog, input, kind, topic, list, status, lastFocus, generation = 0;

function build() {
  dialog = document.createElement('dialog');
  dialog.className = 'palette';
  dialog.setAttribute('aria-label', 'Search');
  dialog.innerHTML = `
    <form role="search" method="dialog">
      <label class="sr-only" for="palette-q">Search the site</label>
      <input id="palette-q" type="search" placeholder="Search essays, field guide, talks…" autocomplete="off" aria-describedby="palette-status">
      <div class="filters">
        <label>Type <select id="palette-kind"><option value="">All</option><option value="essay">Essays</option><option value="guide">Field guide</option><option value="talk">Talks</option><option value="project">Projects</option></select></label>
        <label>Topic <select id="palette-topic"><option value="">All</option></select></label>
      </div>
    </form>
    <ol class="palette-results" aria-label="Results"></ol>
    <p class="palette-status" id="palette-status" role="status" aria-live="polite"></p>`;
  document.body.append(dialog);
  input = dialog.querySelector('input');
  kind = dialog.querySelector('#palette-kind');
  topic = dialog.querySelector('#palette-topic');
  list = dialog.querySelector('.palette-results');
  status = dialog.querySelector('.palette-status');
  let labels = {};
  try { labels = JSON.parse(document.querySelector('[data-topics]')?.dataset.topics || '{}'); } catch (_) { /* no topic filter */ }
  for (const [id, title] of Object.entries(labels)) topic.append(new Option(title, id));
  if (topic.options.length === 1) topic.closest('label').hidden = true;
  let timer;
  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 80); });
  kind.addEventListener('change', run);
  topic.addEventListener('change', run);
  dialog.addEventListener('close', () => lastFocus?.focus());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.querySelector('form').addEventListener('submit', event => {
    event.preventDefault();
    const first = list.querySelector('a');
    if (first) location.href = first.href;
  });
  dialog.addEventListener('keydown', event => {
    const links = [...list.querySelectorAll('a')];
    const at = links.indexOf(document.activeElement);
    if (event.key === 'ArrowDown') { event.preventDefault(); (links[at + 1] || links[0])?.focus(); }
    else if (event.key === 'ArrowUp') { event.preventDefault(); at <= 0 ? input.focus() : links[at - 1].focus(); }
    else if (event.key.length === 1 && at >= 0 && !event.metaKey && !event.ctrlKey) input.focus();
  });
}

async function run() {
  const current = ++generation;
  const q = input.value.trim();
  if (!q && !kind.value && !topic.value) { list.replaceChildren(); status.textContent = 'Type to search. Arrow keys move through results; Enter opens the first.'; return; }
  status.textContent = 'Searching…';
  try {
    const { total, hits } = await search(q, { kind: kind.value, topic: topic.value, limit: 12 });
    if (current !== generation) return;
    list.replaceChildren();
    for (const hit of hits) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = hit.section ? hit.section.url : hit.url;
      a.textContent = hit.title;
      const small = document.createElement('small');
      small.textContent = `${kindLabel[hit.kind] || hit.kind} · ${(hit.date || '').slice(0, 4)}${hit.section ? ` · ${hit.section.title}` : ''}`;
      a.append(small);
      li.append(a);
      list.append(li);
    }
    status.textContent = total ? `${total} result${total === 1 ? '' : 's'}${total > hits.length ? `, showing ${hits.length}` : ''}.` : 'No results. Try fewer words or clear the filters.';
  } catch (_) {
    if (current !== generation) return;
    list.replaceChildren();
    status.textContent = 'Search could not load. Use the search page instead.';
  }
}

export function open() {
  if (!dialog) build();
  if (dialog.open) return;
  lastFocus = document.activeElement;
  dialog.showModal();
  input.select();
  run();
}
