// Shared by the search page and the command palette. The index is fetched once, on first use.
let indexPromise;
export function loadIndex() {
  indexPromise ||= fetch('/search/index.json').then(r => {
    if (!r.ok) throw new Error('Search index unavailable');
    return r.json();
  }).catch(error => { indexPromise = undefined; throw error; });
  return indexPromise;
}
const norm = v => v.normalize('NFKC').toLocaleLowerCase('en');
export function search(entries, query, { kind = '', topic = '' } = {}) {
  const words = norm(query).split(/\s+/).filter(Boolean);
  return entries
    .filter(e => (!kind || e.kind === kind) && (!topic || e.topics.includes(topic)))
    .map(e => {
      const title = norm(e.title), desc = norm(e.description || ''), body = norm(e.content || '');
      if (!words.every(w => title.includes(w) || desc.includes(w) || body.includes(w))) return null;
      const score = words.reduce((n, w) => n + (title.includes(w) ? 12 : 0) + (desc.includes(w) ? 4 : 0), 0);
      // The section that holds the most of the words, so the snippet shows what was searched for.
      let section = null, most = 0;
      for (const s of words.length ? e.sections : []) {
        const text = norm(s.title + ' ' + s.text), n = words.filter(w => text.includes(w)).length;
        if (n > most) { most = n; section = s; }
      }
      return { entry: e, score, section, words };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score || b.entry.published.localeCompare(a.entry.published));
}
export function snippet(text, words, size = 220) {
  const low = norm(text), found = words.map(w => low.indexOf(w)).filter(i => i >= 0);
  const at = found.length ? Math.max(0, Math.min(...found) - 70) : 0;
  return (at ? '…' : '') + text.slice(at, at + size) + (text.length > at + size ? '…' : '');
}
// The text as nodes, with each searched word wrapped in <mark>. Built from text nodes only, never from markup.
export function marked(text, words) {
  const out = document.createDocumentFragment(), low = text.toLocaleLowerCase('en');
  const terms = low.length === text.length ? words.filter(Boolean) : [];
  let at = 0;
  while (terms.length) {
    let next = -1, len = 0;
    for (const w of terms) { const i = low.indexOf(w, at); if (i >= 0 && (next < 0 || i < next || (i === next && w.length > len))) { next = i; len = w.length; } }
    if (next < 0) break;
    out.append(text.slice(at, next));
    const m = document.createElement('mark'); m.textContent = text.slice(next, next + len); out.append(m);
    at = next + len;
  }
  out.append(text.slice(at));
  return out;
}
const monthYear = new Intl.DateTimeFormat('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' });
export const shortDate = iso => monthYear.format(new Date(iso.slice(0, 10)));
export const kindLabel = { essay: 'Essay', guide: 'Field guide', talk: 'Talk', project: 'Project', profile: 'Profile', glossary: 'Glossary' };
