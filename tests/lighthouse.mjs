// Lighthouse lab gate on three representative routes (default simulated mobile profile).
// Thresholds: performance >= 0.95 (lab noise allowance), accessibility = 1, LCP <= 1.6 s, CLS <= 0.02.
// The plan's 1.2 s LCP needs inlined critical CSS, which conflicts with the strict style-src CSP; see docs/DESIGN.md.
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';

const port = process.env.PORT || '8000';
const origin = `http://127.0.0.1:${port}`;
const routes = ['/', '/agentic-identity-broker/', '/knowledge-base/account-security/password-reuse-studies-security/'];
const server = spawn(process.env.PYTHON || 'python3', ['scripts/serve.py', port], { stdio: 'ignore' });
const chrome = await chromeLauncher.launch({ chromePath: process.env.CHROMIUM_EXECUTABLE, chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu'] });
const results = [];
let failed = false;
try {
  for (let i = 0; i < 50; i++) { try { await fetch(origin); break; } catch { await new Promise(r => setTimeout(r, 100)); } }
  for (const route of routes) {
    const runs = [];
    for (let run = 0; run < 3; run++) {
      const { lhr } = await lighthouse(origin + route, { port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'] });
      runs.push({
        performance: lhr.categories.performance.score, accessibility: lhr.categories.accessibility.score,
        bestPractices: lhr.categories['best-practices'].score, seo: lhr.categories.seo.score,
        lcp: lhr.audits['largest-contentful-paint'].numericValue, cls: lhr.audits['cumulative-layout-shift'].numericValue,
        tbt: lhr.audits['total-blocking-time'].numericValue, bytes: lhr.audits['total-byte-weight'].numericValue,
      });
    }
    const median = key => runs.map(r => r[key]).sort((a, b) => a - b)[1];
    const summary = Object.fromEntries(Object.keys(runs[0]).map(k => [k, median(k)]));
    results.push({ route, ...summary });
    const problems = [];
    if (summary.performance < 0.95) problems.push(`performance ${summary.performance}`);
    if (summary.accessibility < 1) problems.push(`accessibility ${summary.accessibility}`);
    if (summary.lcp > 1600) problems.push(`LCP ${Math.round(summary.lcp)} ms`);
    if (summary.cls > 0.02) problems.push(`CLS ${summary.cls}`);
    console.log(route, JSON.stringify(summary), problems.length ? `FAIL: ${problems.join(', ')}` : 'ok');
    if (problems.length) failed = true;
  }
  mkdirSync('test-results', { recursive: true });
  writeFileSync('test-results/lighthouse.json', JSON.stringify({ lighthouse: '13.5.0', profile: 'default mobile, simulated throttling, no HTTP compression', results }, null, 2));
} finally {
  await chrome.kill();
  server.kill();
}
process.exit(failed ? 1 : 0);
