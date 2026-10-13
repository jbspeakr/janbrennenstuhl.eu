(() => {
  const form = document.querySelector('#search-form');
  const query = form.querySelector('#query');
  const kind = form.querySelector('#kind');
  const topic = form.querySelector('#topic');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  const fallback = document.querySelector('#search-fallback');
  let indexPromise;
  let generation = 0;
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase('en');
  const text = (tag, value, parent) => { const element = document.createElement(tag); element.textContent = value; parent.append(element); return element; };
  function readURL() {
    const params = new URLSearchParams(location.search);
    query.value = params.get('q') || params.get('keyword') || '';
    kind.value = params.get('kind') || '';
    topic.value = params.get('topic') || '';
  }
  async function search(updateURL = false) {
    const current = ++generation;
    const q = query.value.trim();
    if (updateURL) {
      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (kind.value) params.set('kind', kind.value);
      if (topic.value) params.set('topic', topic.value);
      history.pushState(null, '', location.pathname + (params.size ? '?' + params : ''));
    }
    results.replaceChildren();
    if (!q && !kind.value && !topic.value) {
      fallback.hidden = false;
      status.textContent = 'Enter a phrase to search. You can also browse every entry below.';
      return;
    }
    status.textContent = 'Searching the archive…';
    try {
      indexPromise ||= fetch('/search/index.json').then(response => {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      }).catch(error => { indexPromise = undefined; throw error; });
      const entries = await indexPromise;
      if (current !== generation) return;
      const words = normalize(q).split(/\s+/).filter(Boolean);
      const hits = entries.filter(item => (!kind.value || item.kind === kind.value) && (!topic.value || item.topics.includes(topic.value)))
        .map(item => {
          const haystack = normalize(item.title + ' ' + item.description + ' ' + item.content);
          const match = words.every(word => haystack.includes(word));
          const score = words.reduce((n, word) => n + (normalize(item.title).includes(word) ? 12 : 0) + (normalize(item.description).includes(word) ? 4 : 0), 0);
          return {item, match, score};
        }).filter(hit => hit.match).sort((a, b) => b.score - a.score || b.item.published.localeCompare(a.item.published));
      fallback.hidden = true;
      status.textContent = hits.length ? `${hits.length} ${hits.length === 1 ? 'result' : 'results'}${q ? ` for “${q}”` : ''}.` : 'No results. Try fewer words or clear the filters.';
      for (const {item} of hits) {
        const article = text('article', '', results); article.className = 'search-hit';
        text('small', `${item.kind} / ${item.published.slice(0, 10)}`, article);
        const heading = text('h2', '', article); const link = text('a', item.title, heading); link.href = item.canonical_url;
        const section = words.length && item.sections.find(s => words.some(word => normalize(s.title + ' ' + s.text).includes(word)));
        if (section) { const anchor = text('a', 'In this article: ' + section.title, article); anchor.href = item.canonical_url + '#' + section.id; anchor.className = 'section-link'; }
        const source = section ? section.text : item.description;
        const pos = words.length ? Math.max(0, normalize(source).indexOf(words[0]) - 75) : 0;
        text('p', (pos ? '…' : '') + source.slice(pos, pos + 260) + (source.length > pos + 260 ? '…' : ''), article);
      }
    } catch (_) {
      if (current !== generation) return;
      fallback.hidden = false;
      status.textContent = 'Search could not load. Please retry, or browse the complete archive below.';
    }
  }
  form.addEventListener('submit', event => { event.preventDefault(); search(true); });
  [kind, topic].forEach(select => select.addEventListener('change', () => search(true)));
  window.addEventListener('popstate', () => { readURL(); search(); });
  readURL(); search();
})();
