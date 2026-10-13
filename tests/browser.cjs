/* Run against verified public/. QA dependencies are never shipped to readers. */
const { chromium } = require('playwright');
const { default: AxeBuilder } = require('@axe-core/playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const assert = require('assert/strict');
const origin = 'http://127.0.0.1:8000';
const routes = [['home','/'],['article','/agentic-identity-broker/'],['guide','/knowledge-base/account-security/password-strength-meter/'],['search','/search/?q=password&kind=research'],['topic','/topics/agentic-engineering/']];
const launch = () => chromium.launch({headless:true, ...(process.env.CHROMIUM_EXECUTABLE ? {executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']} : {})});
(async () => {
 const server = spawn(process.env.PYTHON || 'python3',['scripts/serve.py'],{stdio:'ignore'});
 let browser;
 const checks=[];
 try {
  for (let i=0;i<40;i++) { try { await fetch(origin); break; } catch (_) { await new Promise(r=>setTimeout(r,100)); } }
  fs.mkdirSync('test-results',{recursive:true});
  for (const width of [360,768,1440]) for (const theme of ['light','dark']) {
   browser=await launch();
   const context=await browser.newContext({viewport:{width,height:1000},colorScheme:theme});
   const page=await context.newPage();
   for (const [name,path] of routes) {
    const response=await page.goto(origin+path); await page.waitForLoadState('networkidle');
    assert.equal(response.status(),200,path);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`Reflow ${width} ${path}`);
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
    assert.deepEqual(result.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),[],`Accessibility ${width} ${theme} ${path}`);
    if (name==='search') assert.ok(await page.locator('.search-hit').count()>0,'Research is searchable');
    if (['home','article','guide'].includes(name)) await page.screenshot({path:`test-results/${name}-${width}-${theme}.png`,fullPage:width===360});
    checks.push({width,theme,path,axeViolations:0,overflow:false});
   }
   await browser.close();browser=null;
  }
  browser=await launch();let context=await browser.newContext({viewport:{width:320,height:900},reducedMotion:'reduce'});let page=await context.newPage();
  await page.goto(origin+'/');await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').textContent(),'Skip to content');await page.keyboard.press('Enter');assert.equal(await page.locator(':focus').getAttribute('id'),'main');
  await page.locator('.pagination a').click();await page.waitForURL('**/2/');assert.ok((await page.locator('h1').textContent()).includes('Page 2'));await page.locator('.pagination a').first().click();await page.waitForURL(origin+'/');
  await page.locator('#theme').selectOption('dark');await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.locator('#theme').selectOption('system');assert.equal(await page.evaluate(()=>localStorage.getItem('jb-theme')),null);
  await page.goto(origin+'/search/?keyword=password&kind=research');await page.waitForSelector('.search-hit');
  await page.locator('#query').fill('no-matching-item-xyz');await page.locator('#search-form button').click();await page.waitForFunction(()=>document.querySelector('#search-status').textContent.startsWith('No results'));
  await page.goBack();await page.waitForSelector('.search-hit');
  await page.goto(origin+'/agentic-identity-broker/');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.addStyleTag({content:'* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p {margin-bottom:2em!important}'});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'Text spacing reflow');
  const error=await page.goto(origin+'/not-a-real-page/');assert.equal(error.status(),404);assert.ok(await page.locator('h1').textContent());
  await browser.close();browser=await launch();context=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:900}});page=await context.newPage();
  for(const path of ['/agentic-identity-broker/','/search/','/knowledge-base/account-security/password-strength-meter/']){
   await page.goto(origin+path);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'No-JS reflow '+path);
  }
  assert.ok(await page.locator('[data-article-body]').textContent());await page.goto(origin+'/search/');assert.ok(await page.locator('#search-fallback .article-row').count()>=45);
  fs.writeFileSync('test-results/browser.json',JSON.stringify({checks,interactionChecks:'passed',noJavaScript:'passed',narrowReflow:'passed'},null,2));
  console.log(`${checks.length} viewport/theme/page checks passed; keyboard, search history, theme persistence, no-JS, 320px reflow, text spacing, and 404 passed.`);
 } finally { if(browser)await browser.close();server.kill(); }
})().catch(error=>{console.error(error);process.exit(1)});
