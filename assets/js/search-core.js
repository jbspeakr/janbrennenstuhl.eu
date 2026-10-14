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
      const section = words.length ? e.sections.find(s => words.some(w => norm(s.title + ' ' + s.text).includes(w))) : null;
      return { entry: e, score, section, words };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score || b.entry.published.localeCompare(a.entry.published));
}
export function snippet(text, words, size = 220) {
  const at = words.length ? Math.max(0, norm(text).indexOf(words[0]) - 70) : 0;
  return (at ? '…' : '') + text.slice(at, at + size) + (text.length > at + size ? '…' : '');
}
export const kindLabel = { essay: 'Essay', guide: 'Field guide', talk: 'Talk', project: 'Project', profile: 'Profile', glossary: 'Glossary' };
