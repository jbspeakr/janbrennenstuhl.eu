/* Renders the social-card base plates (assets/cards/<topic>.png) from the built topic hubs.
   Run after a build while `python3 scripts/serve.py` is serving on PORT (default 8000).
   Hugo writes each page's title onto these plates at build time (layouts/_partials/social-card.html). */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const base = `http://127.0.0.1:${process.env.PORT || '8000'}`;
const topics = ['agentic-engineering', 'identity-authentication', 'application-security', 'passwords', 'tokens-jwt', 'engineering-practice'];

(async () => {
  const browser = await chromium.launch({ ...(process.env.CHROMIUM_EXECUTABLE ? { executablePath: process.env.CHROMIUM_EXECUTABLE } : {}) });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, colorScheme: 'dark', reducedMotion: 'reduce' });
  const css = fs.readdirSync(path.join(root, 'public/css')).find(f => f.endsWith('.css'));
  for (const topic of [...topics, 'home']) {
    await page.goto(topic === 'home' ? `${base}/` : `${base}/topics/${topic}/`);
    const svg = await page.locator(topic === 'home' ? '.flagship-art svg.diagram' : '.hub-header svg.diagram').evaluate(e => e.outerHTML);
    await page.setContent(`<!doctype html><html data-theme="dark"><head><link rel="stylesheet" href="${base}/css/${css}"><style>
      body{margin:0;width:1200px;height:630px;overflow:hidden;background:#080d16;position:relative}
      .art{position:absolute;inset:-70px 0 auto 0;opacity:.75}.art svg{width:1200px;height:500px}
      .fade{position:absolute;inset:0;background:linear-gradient(180deg,transparent 0,transparent 190px,#080d16 300px)}
      .bar{position:absolute;left:72px;top:540px;width:56px;height:4px;background:#ffb113}
    </style></head><body><div class="art">${svg.replace(/style="view-transition-name:[^"]*"/, '')}</div><div class="fade"></div><div class="bar"></div></body></html>`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(root, `assets/cards/${topic}.png`) });
    console.log(`assets/cards/${topic}.png`);
  }
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
