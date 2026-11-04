// client sign in: the mark fills in as the form does, then opens onto the dashboard
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const form = $('#login');
  if (!form) return;

  const stage = $('.li-stage');
  const fig = $('.li-fig');
  const email = $('#email');
  const mailField = $('.li-mail');
  const pw = $('#pw');
  const pwField = $('.li-pw');
  const eye = $('.li-eye');
  const caps = $('.li-caps');
  const linkHint = $('.li-linkhint');
  const forgot = $('.li-forgot');
  const remember = $('[name="remember"]');
  const err = $('.li-err');
  const go = $('.li-go');
  const goText = $('.li-go-t');
  const status = $('[data-status]');
  const title = $('[data-title]');
  const who = $('.li-who');
  const signin = $('.li-signin');
  const sent = $('.li-sent');
  const rings = $$('.li-rings circle');
  const KEY = 'st-account';
  let mode = 'password';

  const say = t => { status.textContent = t; };
  const toggle = (k, on) => fig.classList.toggle(k, on);
  const emailOk = () => email.value.length > 0 && email.validity.valid;
  const firstName = address => (address.split('@')[0].split(/[._+-]/)[0] || '').replace(/[^a-z]/gi, '').toLowerCase();
  const store = {
    get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } },
    set(v) { try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch (e) {} },
  };

  // the mark follows the form: email → blue disc, password → graphite disc + one ring per character
  const sync = () => {
    const ok = emailOk();
    toggle('st-mail', ok);
    mailField.classList.toggle('ok', ok);
    const n = mode === 'link' ? 0 : pw.value.length;
    toggle('st-pass', mode === 'link' ? ok : n > 0);
    rings.forEach((c, i) => c.classList.toggle('on', i < n));
  };

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
  const busy = (on, text) => {
    go.classList.toggle('busy', on);
    go.disabled = on;
    goText.textContent = text || (mode === 'link' ? 'email me a link' : 'open the dashboard');
  };

  // two ways in: password, or a one-time link by email
  const setMode = m => {
    mode = m;
    const link = m === 'link';
    $$('[name="mode"]').forEach(r => { r.checked = r.value === m; });
    pwField.hidden = link;
    pw.required = !link;
    linkHint.hidden = !link;
    forgot.hidden = link;
    pw.autocomplete = link ? 'off' : 'current-password';
    clear();
    busy(false);
    sync();
  };
  $$('[name="mode"]').forEach(r => r.addEventListener('change', () => setMode(r.value)));
  forgot.addEventListener('click', () => {
    setMode('link');
    say('no password needed. we will email you a link instead.');
    (mailField.hidden ? go : email).focus();
  });

  // a remembered account skips the email step
  const setTitle = name => {
    title.textContent = name ? 'welcome back, ' : 'welcome ';
    const em = document.createElement('em');
    em.textContent = name ? `${name}.` : 'back.';
    title.append(em);
  };
  const known = store.get();
  if (known) {
    email.value = known;
    mailField.hidden = true;
    who.hidden = false;
    const name = firstName(known);
    $('[data-who-i]').textContent = (name[0] || known[0]).toUpperCase();
    $('[data-who-n]').textContent = name || known;
    $('[data-who-m]').textContent = known;
    remember.checked = true;
    setTitle(name);
  }
  $('.li-notyou').addEventListener('click', () => {
    store.set(null);
    who.hidden = true;
    mailField.hidden = false;
    email.value = '';
    remember.checked = false;
    setTitle('');
    sync();
    email.focus();
  });

  email.addEventListener('input', () => { sync(); if (!err.hidden) clear(); });
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

  // depth: rings and mark drift apart under a mouse
  if (!still && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    let raf = 0;
    stage.addEventListener('pointermove', e => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const r = stage.getBoundingClientRect();
        stage.style.setProperty('--px', (((e.clientX - r.left) / r.width) * 2 - 1).toFixed(3));
        stage.style.setProperty('--py', (((e.clientY - r.top) / r.height) * 2 - 1).toFixed(3));
      });
    });
    stage.addEventListener('pointerleave', () => {
      stage.style.setProperty('--px', 0);
      stage.style.setProperty('--py', 0);
    });
  }

  // our work: client names take turns under the line
  const live = $('.li-live-n');
  if (live && !still) {
    let names = [];
    try { names = JSON.parse(live.dataset.clients); } catch (e) {}
    let at = 0;
    if (names.length > 1) setInterval(() => {
      if (document.hidden) return;
      live.classList.add('swap');
      setTimeout(() => {
        at = (at + 1) % names.length;
        live.textContent = names[at];
        live.classList.remove('swap');
      }, 350);
    }, 2800);
  }

  // sydney time, in the brand's mono
  const syd = (o) => new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Sydney', ...o });
  const clock = $('[data-clock]');
  if (clock) {
    const fmt = syd({ hour: '2-digit', minute: '2-digit', hour12: false });
    const tick = () => { clock.textContent = fmt.format(new Date()); };
    tick();
    setInterval(tick, 15000);
  }
  const greeting = name => {
    const h = +syd({ hour: 'numeric', hour12: false }).format(new Date()) % 24;
    const part = h < 12 ? 'morning' : h < 18 ? 'afternoon' : 'evening';
    return `good ${part}${name ? `, ${name}` : ''}.`;
  };

  // link sent / back
  const showSent = to => {
    $('[data-sent-to]').textContent = to;
    signin.hidden = true;
    sent.hidden = false;
    sent.focus();
  };
  $('[data-back]').addEventListener('click', () => {
    sent.hidden = true;
    signin.hidden = false;
    toggle('st-go', false);
    busy(false);
    (mailField.hidden ? go : email).focus();
  });
  const resend = $('.li-resend');
  resend.addEventListener('click', () => {
    say(`we sent another link to ${email.value}`);
    resend.firstChild.textContent = 'sent again ';
    setTimeout(() => { resend.firstChild.textContent = 'send it again '; }, 2400);
  });

  // prototype: nothing is sent. a valid email and a password of 4+ characters sign in;
  // anything shorter shows the error state, so both states can be seen.
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (go.disabled) return;
    clear();
    if (!emailOk()) {
      if (mailField.hidden) $('.li-notyou').click();
      return fail('enter the email address your account uses.', email);
    }
    store.set(remember.checked ? email.value : null);

    if (mode === 'link') {
      busy(true, 'sending…');
      say('sending your sign-in link');
      toggle('st-go', true);
      setTimeout(() => { busy(false); showSent(email.value); }, still ? 0 : 900);
      return;
    }

    if (!pw.value) return fail('enter your password.', pw);
    if (pw.value.length < 4) {
      pw.value = '';
      sync();
      return fail("we don't recognise that email and password together. try again, or get a link by email instead.", pw);
    }
    busy(true, 'opening…');
    say('signed in, opening your dashboard');
    toggle('st-go', true);
    $('[data-hello]').textContent = greeting(firstName(email.value));
    const open = () => { fig.classList.add('st-open'); document.body.classList.add('li-open'); };
    const leave = () => { location.href = form.dataset.next; };
    if (still) { open(); setTimeout(leave, 900); return; }
    setTimeout(open, 700);
    setTimeout(leave, 2500);
  });

  // coming back with the back button: undo the opening
  addEventListener('pageshow', e => {
    if (!e.persisted) return;
    fig.classList.remove('st-open', 'st-go');
    document.body.classList.remove('li-open');
    busy(false);
    pw.value = '';
    sync();
  });

  // browsers restore the chosen radio on reload
  setMode((form.querySelector('[name="mode"]:checked') || {}).value || 'password');
  // desktop: start typing straight away
  if (matchMedia('(min-width: 901px)').matches) (mailField.hidden ? pw : email).focus({ preventScroll: true });
})();
