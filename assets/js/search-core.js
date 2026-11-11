// Shared by the search page and the command palette. The search engine is Pagefind, built from the
// rendered pages by scripts/search-index.sh. It loads on first use and then fetches only the index
// chunks and page fragments a query needs, so the cost no longer grows with every essay.
const bundle = '/pagefind/pagefind.js'; // a variable, so the bundler leaves this import to the browser
let enginePromise;
export function loadEngine() {
  enginePromise ||= import(bundle)
    .then(async engine => { await engine.options({ excerptLength: 28 }); return engine; })
    .catch(error => { enginePromise = undefined; throw error; });
  return enginePromise;
}

// When no indexed word starts with a query word, Pagefind falls back to a loosely related word, so
// nonsense still "finds" pages. A word counts as known only if its best page marks a word that starts like it.
const known = new Map();
async function isKnown(engine, word) {
  if (!known.has(word)) known.set(word, (async () => {
    const top = (await engine.search(word)).results[0];
    if (!top) return false;
    const marks = (await top.data()).excerpt.match(/<mark>.*?<\/mark>/g) || [];
    return marks.some(m => m.slice(6, -7).toLocaleLowerCase('en').replace(/^[^\p{L}\p{N}]+/u, '').startsWith(word.slice(0, 2)));
  })());
  return known.get(word);
}

// Up to `limit` hits, best first; with no words, everything the filters allow, newest first.
export async function search(query, { kind = '', topic = '', limit = 20 } = {}) {
  const engine = await loadEngine();
  const q = query.trim();
  const words = [...new Set(q.toLocaleLowerCase('en').split(/[^\p{L}\p{N}_]+/u).filter(w => w.length > 1))].slice(0, 8);
  if (!(await Promise.all(words.map(w => isKnown(engine, w)))).every(Boolean)) return { total: 0, hits: [] };
  const filters = { ...(kind && { kind }), ...(topic && { topic }) };
  const found = await engine.search(q || null, { filters, ...(!q && { sort: { date: 'desc' } }) });
  const hits = await Promise.all(found.results.slice(0, limit).map(async result => {
    const page = await result.data();
    // The section with the most matches, so the excerpt shows what was searched for.
    let best = null;
    if (q) for (const sub of page.sub_results || []) if (!best || (sub.locations || []).length > (best.locations || []).length) best = sub;
    const section = best && best.url.includes('#') ? { title: best.title, url: best.url } : null;
    return { url: page.url, title: page.meta.title, kind: page.meta.kind, date: page.meta.date, section, excerpt: (best || page).excerpt };
  }));
  return { total: found.results.length, hits };
}

// A Pagefind excerpt as nodes. Pagefind encodes the page text and adds only <mark> elements.
export function excerptNodes(html) {
  const holder = document.createElement('template');
  holder.innerHTML = html;
  return holder.content;
}
const monthYear = new Intl.DateTimeFormat('en-GB', { month: 'short', year: 'numeric', timeZone: 'UTC' });
export const shortDate = iso => (iso ? monthYear.format(new Date(iso.slice(0, 10))) : '');
export const kindLabel = { essay: 'Essay', guide: 'Field guide', talk: 'Talk', project: 'Project', profile: 'Profile', glossary: 'Glossary' };
