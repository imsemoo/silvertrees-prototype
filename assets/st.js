(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // loader: once per session, ?loader forces it
  const boot = $('.boot');
  if (boot && document.documentElement.classList.contains('boot-on')) {
    try { sessionStorage.setItem('st-boot', '1'); } catch (e) {}
    setTimeout(() => {
      boot.classList.add('out');
      setTimeout(() => boot.remove(), 700);
    }, still ? 0 : 1150);
  } else if (boot) boot.remove();

  // header
  const top = $('.top');
  const onScroll = () => top.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  const menu = $('.menu-btn');
  menu.addEventListener('click', () => {
    const open = top.classList.toggle('open');
    menu.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
    // keep Tab inside the open menu
    ['main', '.foot'].forEach(q => { const el = $(q); if (el) el.inert = open; });
    if (open) $('.nav a').focus(); else menu.focus();
  });
  addEventListener('keydown', e => {
    if (e.key === 'Escape' && top.classList.contains('open')) menu.click();
  });

  // reveal
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('[data-rise], .grow').forEach(el => io.observe(el));

  // hero: client sites take turns inside the blue disc
  const reel = $$('.shotset image');
  const cap = $('.reel-t');
  const pause = $('.reel-pause');
  if (reel.length > 1 && !still) {
    let i = 0, held = false, stopped = false, seen = true;
    const mark = $('.hero-mark');
    mark.addEventListener('pointerenter', () => { held = true; });
    mark.addEventListener('pointerleave', () => { held = false; });
    mark.addEventListener('focusin', () => { held = true; });
    mark.addEventListener('focusout', () => { held = false; });
    new IntersectionObserver(([e]) => { seen = e.isIntersecting; }).observe(mark);
    pause.addEventListener('click', () => {
      stopped = !stopped;
      pause.textContent = stopped ? 'play' : 'pause';
      pause.setAttribute('aria-pressed', stopped);
    });
    setInterval(() => {
      if (document.hidden || held || stopped || !seen) return;
      reel[i].classList.remove('on');
      i = (i + 1) % reel.length;
      reel[i].classList.add('on');
      cap.href = reel[i].dataset.u;
      cap.firstElementChild.textContent = reel[i].dataset.t;
    }, 3600);
  } else if (pause) pause.remove();

  // work filters
  const grid = $('#work-grid');
  if (grid) {
    const btns = $$('.filters button');
    const apply = f => {
      btns.forEach(b => b.setAttribute('aria-pressed', b.dataset.f === f));
      let n = 0;
      $$('.card', grid).forEach(c => { c.hidden = f !== 'all' && c.dataset.s !== f; if (!c.hidden) n++; });
      $('.count-live').textContent = n === 1 ? '1 project' : `${n} projects`;
    };
    btns.forEach(b => b.addEventListener('click', () => {
      apply(b.dataset.f);
      history.replaceState(null, '', b.dataset.f === 'all' ? location.pathname : '#' + b.dataset.f);
    }));
    const h = location.hash.slice(1);
    if (h && btns.some(b => b.dataset.f === h)) apply(h);
  }

  // lightbox
  const lb = $('dialog.lb');
  const shots = $$('.gallery button');
  if (lb && shots.length) {
    let at = 0;
    const show = n => {
      at = (n + shots.length) % shots.length;
      const b = shots[at];
      $('img', lb).src = b.dataset.full;
      $('img', lb).alt = b.dataset.cap;
      $('.lb-cap', lb).textContent = `${at + 1} / ${shots.length} · ${b.dataset.cap}`;
    };
    shots.forEach((b, n) => b.addEventListener('click', () => { show(n); lb.showModal(); }));
    $('.lb-prev', lb).addEventListener('click', () => show(at - 1));
    $('.lb-next', lb).addEventListener('click', () => show(at + 1));
    $('.lb-x', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') show(at + 1);
      if (e.key === 'ArrowLeft') show(at - 1);
    });
  }

  // prototype form: validate, send nothing
  const form = $('#enquiry');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const bad = $$('[required]', form).find(f => !f.checkValidity());
    if (bad) { bad.focus(); bad.reportValidity(); return; }
    $('.done', form).classList.add('on');
  });
})();

// identity book: replay the mark growing
document.querySelectorAll('[data-replay]').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('svg.replay').forEach(s => { s.classList.remove('go'); void s.getBoundingClientRect(); s.classList.add('go'); });
}));
document.querySelectorAll('svg.replay').forEach(s => s.classList.add('go'));

// home product switcher: ARIA tabs with roving tabindex and arrow keys
(() => {
  const tabs = [...document.querySelectorAll('.pt')];
  if (!tabs.length) return;
  const pick = (t, focus) => {
    tabs.forEach(x => {
      const on = x === t;
      x.setAttribute('aria-selected', on);
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) t.focus();
    t.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(t));
    t.addEventListener('keydown', e => {
      const k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (k) { e.preventDefault(); pick(tabs[(i + k + tabs.length) % tabs.length], true); }
      if (e.key === 'Home') { e.preventDefault(); pick(tabs[0], true); }
      if (e.key === 'End') { e.preventDefault(); pick(tabs[tabs.length - 1], true); }
    });
  });
})();
