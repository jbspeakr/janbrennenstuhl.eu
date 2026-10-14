// JWT anatomy viewer: splits and decodes a token locally. It never sends the token anywhere and never verifies signatures.
const root = document.querySelector('[data-explainer="jwt"]');
const app = root?.querySelector('.explainer-app');
if (app) {
  const sample = root.querySelector('.explainer-static code')?.textContent.trim() || '';
  app.innerHTML = `
    <label for="jwt-input">Token</label>
    <textarea id="jwt-input" rows="4" spellcheck="false" autocomplete="off" aria-describedby="jwt-note"></textarea>
    <p class="small" id="jwt-note">Decoded in this browser only. The signature is not checked, so a decoded token proves nothing about who issued it.</p>
    <div class="grid" aria-live="polite">
      <section class="jwt-part jwt-h"><h3>Header</h3><pre></pre></section>
      <section class="jwt-part jwt-p"><h3>Payload</h3><pre></pre></section>
      <section class="jwt-part jwt-s"><h3>Signature</h3><pre></pre></section>
    </div>
    <ul class="verdict"></ul>`;
  app.hidden = false;
  const input = app.querySelector('textarea');
  const [head, body, sig] = app.querySelectorAll('pre');
  const notes = app.querySelector('.verdict');
  const decode = part => {
    const b64 = part.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(part.length / 4) * 4, '=');
    const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    return new TextDecoder().decode(bytes);
  };
  const note = (ok, label, text) => { const li = document.createElement('li'); li.className = ok ? 'ok' : 'bad'; li.innerHTML = '<strong></strong>'; li.firstChild.textContent = label; li.append(text); notes.append(li); };
  const when = s => new Date(s * 1000).toISOString().replace('.000Z', ' UTC').replace('T', ' ');
  function render() {
    notes.replaceChildren();
    const parts = input.value.trim().split('.');
    [head, body, sig].forEach(p => { p.textContent = ''; });
    if (parts.length === 5) { note(false, 'JWE', 'Five parts: this is an encrypted JWT (JWE). Its payload cannot be read without the key.'); return; }
    if (parts.length !== 3) { note(false, 'Format', 'A signed JWT has three parts separated by two dots.'); return; }
    let header, payload;
    try { header = JSON.parse(decode(parts[0])); head.textContent = JSON.stringify(header, null, 2); } catch (_) { note(false, 'Header', 'The first part is not base64url-encoded JSON.'); }
    try { payload = JSON.parse(decode(parts[1])); body.textContent = JSON.stringify(payload, null, 2); } catch (_) { note(false, 'Payload', 'The second part is not base64url-encoded JSON.'); }
    sig.textContent = parts[2] ? `${parts[2].length} base64url characters` : '(empty)';
    if (header) {
      if (String(header.alg).toLowerCase() === 'none' || !parts[2]) note(false, 'alg', 'Unsecured token: no signature. Reject it unless your application explicitly allows "none" (RFC 8725).');
      else note(true, 'alg', `${header.alg}: accept it only if this algorithm is on your allowlist.`);
      if (header.kid) note(true, 'kid', `Key ID "${header.kid}": look it up only in a key set you trust.`);
    }
    if (payload) {
      const now = Date.now() / 1000;
      if (typeof payload.exp === 'number') note(payload.exp > now, 'exp', ` ${when(payload.exp)} (${payload.exp > now ? 'not yet expired' : 'expired'}).`);
      else note(false, 'exp', 'No expiry claim.');
      if (typeof payload.iat === 'number') note(true, 'iat', ` Issued ${when(payload.iat)}.`);
      if (payload.iss) note(true, 'iss', ` Issuer ${payload.iss}: compare with the issuer you expect.`);
      if (payload.aud) note(true, 'aud', ` Audience ${[].concat(payload.aud).join(', ')}: must include your service.`);
      else note(false, 'aud', 'No audience: any service could accept this token.');
    }
  }
  input.value = sample;
  input.addEventListener('input', render);
  render();
}
