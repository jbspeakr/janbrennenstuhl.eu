/* Renders the social-card base plates from the built site: one per topic hub (assets/cards/<topic>.png)
   and one per article from its own drawing (assets/cards/pages/<id>.png).
   Run after a build while `python3 scripts/serve.py` is serving on PORT (default 8000).
   Hugo writes each page's title onto these plates at build time (layouts/_partials/social-card.html). */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const base = `http://127.0.0.1:${process.env.PORT || '8000'}`;
const topics = ['agentic-engineering', 'identity-authentication', 'application-security', 'passwords', 'tokens-jwt', 'engineering-practice'];
const kinds = ['essay', 'guide', 'talk', 'project'];

(async () => {
  const browser = await chromium.launch({ ...(process.env.CHROMIUM_EXECUTABLE ? { executablePath: process.env.CHROMIUM_EXECUTABLE } : {}) });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, colorScheme: 'dark', reducedMotion: 'reduce' });
  const css = fs.readdirSync(path.join(root, 'public/css')).find(f => f.endsWith('.css'));
  const catalog = JSON.parse(fs.readFileSync(path.join(root, 'public/catalog.json'), 'utf8'));
  const plates = [
    ...[...topics, 'home'].map(topic => ({ url: topic === 'home' ? '/' : `/topics/${topic}/`, selector: topic === 'home' ? '.flagship-art svg.diagram' : '.hub-header svg.diagram', out: `assets/cards/${topic}.png` })),
    ...catalog.items.filter(i => kinds.includes(i.kind)).map(i => ({ url: new URL(i.canonical_url).pathname, selector: '.article-art svg.diagram', out: `assets/cards/pages/${i.id}.png` })),
  ];
  fs.mkdirSync(path.join(root, 'assets/cards/pages'), { recursive: true });
  for (const plate of plates) {
    await page.goto(`${base}${plate.url}`);
    const svg = await page.locator(plate.selector).evaluate(e => e.outerHTML);
    await page.setContent(`<!doctype html><html data-theme="dark"><head><link rel="stylesheet" href="${base}/css/${css}"><style>
      body{margin:0;width:1200px;height:630px;overflow:hidden;background:#16191c;position:relative}
      .art{position:absolute;inset:-40px 0 auto 0;opacity:.7}.art svg{width:1200px;height:400px}.art .d-ground{fill:#16191c}
      .fade{position:absolute;inset:0;background:linear-gradient(180deg,transparent 0,transparent 170px,#16191c 290px)}
      .bar{position:absolute;left:72px;top:540px;width:40px;height:2px;background:#e2a4ae}
    </style></head><body><div class="art">${svg.replace(/style="view-transition-name:[^"]*"/, '')}</div><div class="fade"></div><div class="bar"></div></body></html>`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(root, plate.out) });
    console.log(plate.out);
  }
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
