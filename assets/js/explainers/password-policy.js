// Compares a password policy with NIST SP 800-63B-4, Section 3.1.1.2. Runs locally; nothing is submitted.
const root = document.querySelector('[data-explainer="password-policy"]');
const app = root?.querySelector('.explainer-app');
if (app) {
  app.innerHTML = `
    <form class="grid" aria-describedby="pp-help">
      <label>Minimum length <input name="min" type="number" min="1" max="256" value="8" inputmode="numeric"></label>
      <label>Maximum length <input name="max" type="number" min="1" max="4096" value="32" inputmode="numeric"></label>
      <label><input name="mfa" type="checkbox"> Always used with a second factor</label>
      <label><input name="composition" type="checkbox" checked> Requires digits, symbols or mixed case</label>
      <label><input name="rotation" type="checkbox" checked> Requires changes every few months</label>
      <label><input name="blocklist" type="checkbox"> Checks a blocklist of breached and common passwords</label>
      <label><input name="hints" type="checkbox"> Offers hints or security questions</label>
      <label><input name="paste" type="checkbox"> Blocks paste or password managers</label>
      <label><input name="truncate" type="checkbox"> Truncates long passwords</label>
      <label><input name="ratelimit" type="checkbox" checked> Rate-limits failed logins</label>
    </form>
    <p class="small" id="pp-help">Change the settings to match your policy. Results update as you go.</p>
    <ul class="verdict" aria-live="polite"></ul>`;
  app.hidden = false;
  const form = app.querySelector('form');
  const out = app.querySelector('.verdict');
  const add = (ok, level, text) => { const li = document.createElement('li'); li.className = ok ? 'ok' : 'bad'; const s = document.createElement('strong'); s.textContent = ok ? 'Meets' : `Fails ${level}`; li.append(s, text); out.append(li); };
  function evaluate() {
    const f = Object.fromEntries(new FormData(form));
    const min = Number(f.min) || 0, max = Number(f.max) || 0, mfa = 'mfa' in f;
    out.replaceChildren();
    const need = mfa ? 8 : 15;
    add(min >= need, 'SHALL', ` Minimum ${min}: ${mfa ? 'with a second factor' : 'as the only factor'} the minimum is ${need}.`);
    add(max >= 64, 'SHOULD', ` Maximum ${max}: accept at least 64 characters.`);
    add(!('composition' in f), 'SHALL NOT', ' Composition rules are not allowed.');
    add(!('rotation' in f), 'SHALL NOT', ' Periodic changes are not allowed; force a change only on evidence of compromise.');
    add('blocklist' in f, 'SHALL', ' New passwords must be checked against a blocklist, with a reason when rejected.');
    add(!('hints' in f), 'SHALL NOT', ' No hints for unauthenticated users and no security questions.');
    add(!('paste' in f), 'SHALL', ' Password managers and autofill must work; paste should be allowed.');
    add(!('truncate' in f), 'SHALL', ' The whole password must be verified, never a truncated one.');
    add('ratelimit' in f, 'SHALL', ' Failed attempts must be rate-limited.');
    const failed = out.querySelectorAll('.bad').length;
    const summary = document.createElement('li');
    summary.className = failed ? 'bad' : 'ok';
    summary.textContent = failed ? `${failed} of 9 checks fail.` : 'All 9 checks pass.';
    out.prepend(summary);
  }
  form.addEventListener('input', evaluate);
  form.addEventListener('submit', e => e.preventDefault());
  evaluate();
}
