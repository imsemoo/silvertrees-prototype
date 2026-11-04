// client sign in: the mark fills in as the form does, then opens onto the dashboard
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fig = $('.li-fig');
  const form = $('#login');
  const email = $('#email');
  const pw = $('#pw');
  const eye = $('.li-eye');
  const caps = $('.li-caps');
  const err = $('.li-err');
  const go = $('.li-go');
  const status = $('[data-status]');
  const rings = [...document.querySelectorAll('.li-rings circle')];
  if (!form) return;

  const stage = (k, on) => fig.classList.toggle(k, on);
  const say = t => { status.textContent = t; };
  const fail = (msg, field) => {
    $('.li-err-t', err).textContent = msg;
    err.hidden = false;
    field.setAttribute('aria-invalid', 'true');
    field.focus();
  };
  const clear = () => {
    err.hidden = true;
    email.removeAttribute('aria-invalid');
    pw.removeAttribute('aria-invalid');
  };

  // email → the blue disc
  email.addEventListener('input', () => {
    stage('st-mail', email.value.length > 0 && email.validity.valid);
    if (!err.hidden) clear();
  });

  // password → the graphite disc, and one growth ring per character (never the characters themselves)
  pw.addEventListener('input', () => {
    const n = pw.value.length;
    stage('st-pass', n > 0);
    rings.forEach((c, i) => c.classList.toggle('on', i < n));
    if (!err.hidden) clear();
  });
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

  // sydney time, in the brand's mono
  const clock = $('[data-clock]');
  if (clock) {
    const fmt = new Intl.DateTimeFormat('en-AU', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Australia/Sydney' });
    const tick = () => { clock.textContent = fmt.format(new Date()); };
    tick();
    setInterval(tick, 15000);
  }

  // prototype: nothing is sent. a valid email and a password of 4+ characters sign in;
  // anything shorter shows the error state, so both states can be seen.
  form.addEventListener('submit', e => {
    e.preventDefault();
    clear();
    if (!email.value || !email.validity.valid) return fail('enter the email address your account uses.', email);
    if (!pw.value) return fail('enter your password.', pw);
    if (pw.value.length < 4) {
      stage('st-pass', false);
      rings.forEach(c => c.classList.remove('on'));
      return fail("we don't recognise that email and password together. try again, or reset your password.", pw);
    }
    go.disabled = true;
    $('.li-go-t', go).textContent = 'opening…';
    say('signed in, opening your dashboard');
    stage('st-go', true);
    const open = () => { fig.classList.add('st-open'); document.body.classList.add('li-open'); };
    const leave = () => { location.href = form.dataset.next; };
    if (still) { open(); setTimeout(leave, 350); return; }
    setTimeout(open, 650);
    setTimeout(leave, 1750);
  });
})();
