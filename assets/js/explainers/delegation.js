// Steps through the token exchange one step at a time. The full list stays readable without JavaScript.
const root = document.querySelector('[data-explainer="delegation"]');
const list = root?.querySelector('.explainer-static ol');
const app = root?.querySelector('.explainer-app');
if (list && app) {
  const steps = [...list.children];
  list.classList.add('step-list');
  app.innerHTML = `<div class="stepper-controls"><button type="button" data-dir="-1">Previous step</button><button type="button" data-dir="1">Next step</button><span role="status" aria-live="polite"></span></div>`;
  app.hidden = false;
  root.querySelector('.explainer-static').after(app);
  const [prev, next] = app.querySelectorAll('button');
  const status = app.querySelector('[role="status"]');
  let at = 0;
  const show = () => {
    steps.forEach((li, i) => { if (i === at) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); });
    prev.disabled = at === 0; next.disabled = at === steps.length - 1;
    status.textContent = `Step ${at + 1} of ${steps.length}`;
  };
  app.addEventListener('click', e => { const d = Number(e.target.dataset.dir); if (d) { at = Math.min(steps.length - 1, Math.max(0, at + d)); show(); } });
  show();
}
