// administrator log in: rings light per password character, a wrong password shakes the card
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const form = $('#adlogin');
  if (!form) return;

  const card = $('.ad-card');
  const user = $('#ad-user');
  const pw = $('#ad-pw');
  const eye = $('.ad-eye');
  const caps = $('.ad-caps');
  const err = $('.ad-err');
  const go = $('.ad-go');
  const goText = $('.ad-go-t');
  const status = $('[data-status]');
  const rings = [...document.querySelectorAll('.ad-rings circle')];

  const sync = () => rings.forEach((c, i) => c.classList.toggle('on', i < pw.value.length));
  const shake = () => {
    if (still) return;
    card.classList.remove('shake');
    void card.offsetWidth;
    card.classList.add('shake');
  };
  const fail = (msg, field) => {
    $('.ad-err-t', err).textContent = msg;
    err.hidden = false;
    field.setAttribute('aria-invalid', 'true');
    field.focus();
    shake();
  };
  const clear = () => {
    err.hidden = true;
    user.removeAttribute('aria-invalid');
    pw.removeAttribute('aria-invalid');
  };

  user.addEventListener('input', () => { if (!err.hidden) clear(); });
  pw.addEventListener('input', () => { sync(); if (!err.hidden) clear(); });
  const capsCheck = e => { if (e.getModifierState) caps.hidden = !e.getModifierState('CapsLock'); };
  pw.addEventListener('keydown', capsCheck);
  pw.addEventListener('keyup', capsCheck);
  pw.addEventListener('blur', () => { caps.hidden = true; });

  // show password: ring = hidden, dot = shown
  eye.addEventListener('click', () => {
    const show = pw.type === 'password';
    pw.type = show ? 'text' : 'password';
    eye.setAttribute('aria-pressed', show);
    eye.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    pw.focus({ preventScroll: true });
  });

  // prototype: nothing is sent. any username with a password of 4+ characters logs in;
  // anything shorter shows the error state, so both states can be seen.
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (go.disabled) return;
    clear();
    const name = user.value.trim();
    if (!name) return fail('enter your username or email address.', user);
    if (!pw.value) return fail('enter your password.', pw);
    if (pw.value.length < 4) {
      pw.value = '';
      sync();
      return fail(`the password for ${name} isn't right. try again, or use "lost your password?" above.`, pw);
    }
    go.classList.add('busy');
    go.disabled = true;
    goText.textContent = 'logging in…';
    status.textContent = 'logged in, opening the dashboard';
    document.body.classList.add('ad-ok');
    const leave = () => { location.href = form.dataset.next; };
    if (still) { setTimeout(leave, 300); return; }
    setTimeout(() => document.body.classList.add('ad-out'), 900);
    setTimeout(leave, 1550);
  });

  // coming back with the back button: undo the exit
  addEventListener('pageshow', e => {
    if (!e.persisted) return;
    document.body.classList.remove('ad-ok', 'ad-out');
    go.classList.remove('busy');
    go.disabled = false;
    goText.textContent = 'log in';
    pw.value = '';
    sync();
  });

  // like every CMS: the cursor is waiting in the first field
  if (matchMedia('(min-width: 901px)').matches) user.focus({ preventScroll: true });
})();
