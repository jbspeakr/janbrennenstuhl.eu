/* Browser contracts against the verified public/ build. QA dependencies are never shipped to readers. */
const { chromium } = require('playwright');
const { default: AxeBuilder } = require('@axe-core/playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const assert = require('assert/strict');

const port = process.env.PORT || '8000';
const origin = `http://127.0.0.1:${port}`;
const routes = [
  ['home', '/'],
  ['article', '/agentic-identity-broker/'],
  ['guide', '/knowledge-base/account-security/password-reuse/'],
  ['explainer', '/knowledge-base/oidc/jwt-anatomy/'],
  ['search', '/search/?q=password&kind=guide'],
  ['topic', '/topics/agentic-engineering/'],
  ['glossary', '/glossary/'],
];
const launch = () => chromium.launch({ headless: true, ...(process.env.CHROMIUM_EXECUTABLE ? { executablePath: process.env.CHROMIUM_EXECUTABLE, args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'] } : {}) });
const overflow = page => page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
// QA never calls the analytics host; the page must behave identically when the script is blocked.
const offline = context => context.route('https://plausible.io/**', r => r.abort());

(async () => {
  const server = spawn(process.env.PYTHON || 'python3', ['scripts/serve.py', port], { stdio: 'ignore' });
  let browser;
  const checks = [];
  try {
    for (let i = 0; i < 50; i++) { try { await fetch(origin); break; } catch (_) { await new Promise(r => setTimeout(r, 100)); } }
    fs.mkdirSync('test-results', { recursive: true });

    // Accessibility and reflow matrix: 7 page types × 3 widths × 2 themes.
    for (const width of [360, 768, 1440]) for (const theme of ['light', 'dark']) {
      browser = await launch();
      const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme: theme, reducedMotion: 'reduce' });
      await offline(context);
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      for (const [name, path] of routes) {
        const response = await page.goto(origin + path, { waitUntil: 'networkidle' });
        assert.equal(response.status(), 200, path);
        assert.equal(await overflow(page), false, `Horizontal overflow ${width} ${theme} ${path}`);
        const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
        assert.deepEqual(result.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) })), [], `Accessibility ${width} ${theme} ${path}`);
        if (name === 'search') assert.ok(await page.locator('.search-hit').count() > 0, 'Field guide entries are searchable');
        if (['home', 'article', 'guide'].includes(name)) await page.screenshot({ path: `test-results/${name}-${width}-${theme}.png`, fullPage: width === 360 });
        checks.push({ width, theme, path, axeViolations: 0, overflow: false });
      }
      assert.deepEqual(errors, [], `Script errors at ${width} ${theme}`);
      await browser.close(); browser = null;
    }

    browser = await launch();
    let context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await offline(context);
    let page = await context.newPage();

    // Keyboard: skip link, then the command palette.
    await page.goto(origin + '/');
    await page.keyboard.press('Tab');
    assert.equal((await page.locator(':focus').textContent()).trim(), 'Skip to content');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('id'), 'main');
    await page.keyboard.press('Control+k');
    await page.waitForSelector('dialog.palette[open]');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'palette-q');
    await page.keyboard.type('passkeys');
    await page.waitForFunction(() => /^\d+ results?\./.test(document.querySelector('.palette-status').textContent));
    assert.ok(await page.locator('.palette-results a').count() > 0, 'Palette finds results');
    await page.keyboard.press('ArrowDown');
    assert.ok(await page.evaluate(() => document.activeElement.closest('.palette-results') !== null), 'Arrow keys reach results');
    const axePalette = await new AxeBuilder({ page }).include('dialog.palette').withTags(['wcag2a', 'wcag2aa']).analyze();
    assert.deepEqual(axePalette.violations.map(v => v.id), [], 'Palette accessibility');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('dialog.palette[open]').count(), 0, 'Escape closes the palette');

    // Theme toggle switches to the other theme, persists across reloads, and names its next action.
    const toggle = page.locator('.theme-toggle');
    const shown = await toggle.getAttribute('data-current');
    const next = shown === 'dark' ? 'light' : 'dark';
    await toggle.click();
    await page.reload();
    assert.equal(await page.locator('html').getAttribute('data-theme'), next);
    assert.equal(await toggle.getAttribute('aria-label'), `Switch to ${shown} theme`);
    await page.evaluate(() => localStorage.removeItem('jb-reader'));
    await page.reload();
    assert.equal(await page.locator('html').getAttribute('data-theme'), null);

    // Search page: legacy query parameter, empty result, history.
    await page.goto(origin + '/search/?keyword=password&kind=research');
    await page.waitForSelector('.search-hit');
    await page.locator('#query').fill('no-matching-item-xyz');
    await page.locator('#search-form button').click();
    await page.waitForFunction(() => document.querySelector('#search-status').textContent.startsWith('No results'));
    await page.goBack();
    await page.waitForSelector('.search-hit');

    // Explainers enhance static content.
    await page.goto(origin + '/knowledge-base/oidc/jwt-anatomy/');
    await page.locator('#jwt-input').fill('eyJhbGciOiJub25lIn0.eyJzdWIiOiJ4In0.');
    await page.waitForFunction(() => /Unsecured token/.test(document.querySelector('[data-explainer="jwt"] .verdict').textContent));
    await page.goto(origin + '/knowledge-base/account-security/password-policy-requirements/');
    await page.locator('input[name="min"]').fill('15');
    assert.match(await page.locator('[data-explainer="password-policy"] .verdict li').first().textContent(), /checks fail|checks pass/);
    await page.goto(origin + '/knowledge-base/agent-identity/token-exchange/');
    await page.locator('[data-dir="1"]').click();
    assert.equal(await page.locator('.step-list li[aria-current="step"]').count(), 1);
    assert.match(await page.locator('.stepper-controls [role="status"]').textContent(), /Step 2 of/);

    // Narrow reflow and increased text spacing (WCAG 1.4.10, 1.4.12).
    await context.close();
    context = await browser.newContext({ viewport: { width: 320, height: 900 } });
    await offline(context);
    page = await context.newPage();
    await page.goto(origin + '/agentic-identity-broker/');
    assert.equal(await overflow(page), false, '320px reflow');
    await page.addStyleTag({ content: '* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p {margin-bottom:2em!important}' });
    assert.equal(await overflow(page), false, 'Text spacing reflow');
    const missing = await page.goto(origin + '/not-a-real-page/');
    assert.equal(missing.status(), 404);
    assert.ok(await page.locator('h1').textContent());

    // Old routes redirect to their new home.
    await page.goto(origin + '/tags/jwt/');
    await page.waitForURL('**/topics/tokens-jwt/');

    // Without JavaScript everything is still reachable.
    await context.close();
    context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 360, height: 900 } });
    await offline(context);
    page = await context.newPage();
    for (const path of ['/agentic-identity-broker/', '/search/', '/knowledge-base/oidc/jwt-anatomy/']) {
      await page.goto(origin + path);
      assert.equal(await overflow(page), false, 'No-JS reflow ' + path);
    }
    const catalog = JSON.parse(fs.readFileSync('public/catalog.json', 'utf8'));
    await page.goto(origin + '/search/');
    assert.equal(await page.locator('#search-fallback .row').count(), catalog.items.length, 'No-JS search lists every entry');
    assert.equal(await page.locator('.theme-toggle').isVisible(), false, 'The theme toggle needs JavaScript and stays hidden');
    await page.goto(origin + '/knowledge-base/oidc/jwt-anatomy/');
    assert.ok((await page.locator('.explainer-static').textContent()).includes('Header'), 'Explainer has a static explanation');

    // Agents: Markdown twins by URL and by content negotiation.
    const md = await fetch(origin + '/agentic-identity-broker/', { headers: { Accept: 'text/markdown' } });
    assert.match(md.headers.get('content-type'), /text\/markdown/);
    assert.match(await md.text(), /^---\nauthor: Jan Brennenstuhl/);

    fs.writeFileSync('test-results/browser.json', JSON.stringify({ checks, interactions: 'passed', noJavaScript: 'passed', reflow: 'passed' }, null, 2));
    console.log(`${checks.length} page/width/theme checks passed; keyboard, palette, theme toggle, search history, explainers, reflow, text spacing, redirects, 404, no-JS and Markdown negotiation passed.`);
  } finally {
    if (browser) await browser.close();
    server.kill();
  }
})().catch(error => { console.error(error); process.exit(1); });
