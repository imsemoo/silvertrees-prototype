"""Build the Silvertrees prototype: home, work, products, hosting, about, news, contact, 404.

python tools/build.py          (images are converted once into assets/work/)
"""
import html, json, re
from pathlib import Path

from content import (APP_SHOT, COMPANY, COMPARE, FIX_FEATURES, GROUPS, HOSTING, IN_USE, NEWS, PRODUCTS, RELATED,
                     SECTORS, STEPS, WORK)

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "research"
V = 10
BASE404 = "/silvertrees-prototype/"
YEAR = 2026

cat = json.loads((RES / "catalog.json").read_text(encoding="utf-8"))
raw = {p["slug"]: p for p in cat["projects"]}


TYPOS = {"Portfoli ": "Portfolio ", "FileXhange": "FileXchange", "Tirms": "Trims", "E therapy": "e-therapy",
         "e therapy": "e-therapy", "FileXchage": "FileXchange", "Life-Style": "lifestyle"}


def clean(s):
    s = s.replace("�", "–").replace("\r", "").strip()
    for a, b in TYPOS.items():
        s = s.replace(a, b)
    s = re.sub(r"\s*\.{3,}\s*$", "…", s)
    s = re.sub(r"\s*\.{2,}\s*", "… ", s)
    s = re.sub(r"\s+-\s+", " – ", s)
    return re.sub(r"\s+", " ", s).strip()


def esc(s):
    return html.escape(s, quote=True)


# ---------- images ----------
def photos():
    from PIL import Image
    out = ROOT / "assets" / "work"
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted((RES / "shots").glob("*.jpg")):
        dest = out / (f.stem + ".webp")
        if not dest.exists():
            Image.open(f).convert("RGB").save(dest, "WEBP", quality=80, method=6)


def items(group):
    """Merge scraped facts with curated copy."""
    spec = WORK if group == "web" else PRODUCTS
    out = []
    for slug, meta in spec.items():
        r = raw[slug]
        paras = [clean(p) for p in r["paras"]]
        paras = [p for p in paras if p and not p.lower().startswith(("click the enquiry", "click here", "our products include"))]
        if slug == "sesmo":
            paras = paras[1:]
        feats = meta.get("features") or FIX_FEATURES.get(slug) or [clean(f) for f in r["features"] if clean(f)]
        feats = [f.rstrip(". ") .replace(" …", "") for f in feats]
        links = [l for l in r["links"] if "silvertrees.net:7443" not in l["href"]]
        site = meta.get("site") or (links[0]["href"].strip() if links else None)
        shots = [dict(file=s["file"].replace(".jpg", ".webp"), caption=clean(s["caption"])) for s in r["shots"]]
        out.append(dict(slug=slug, paras=paras, features=feats, site=site, shots=shots,
                        extra=[dict(label=clean(l["label"]), href=l["href"].strip()) for l in links[1:]],
                        **{k: v for k, v in meta.items() if k not in ("features", "site")}))
    return out


SITES = items("web")
TOOLS = items("product")
HOST = raw["silvertrees-hosting"]


# ---------- shared svg ----------
def mark_svg(cls="", ident="m"):
    return f'''<svg class="{cls}" viewBox="0 0 240 240" aria-hidden="true"><defs>
<mask id="{ident}g" maskUnits="userSpaceOnUse" x="0" y="0" width="240" height="240"><rect width="240" height="240" fill="#fff"/><circle cx="88" cy="152" r="74"/><circle cx="188.9" cy="41.8" r="27"/></mask>
<mask id="{ident}b" maskUnits="userSpaceOnUse" x="0" y="0" width="240" height="240"><rect width="240" height="240" fill="#fff"/><circle cx="48.1" cy="199.5" r="25"/></mask></defs>
<g mask="url(#{ident}g)"><circle class="g" cx="140" cy="100" r="80" fill="#4D4C4A"/></g><circle class="s1" cx="188.9" cy="41.8" r="17" fill="#4D4C4A"/>
<g mask="url(#{ident}b)"><circle class="b" cx="88" cy="152" r="66" fill="#02A3FD"/></g><circle class="s2" cx="48.1" cy="199.5" r="15" fill="#02A3FD"/></svg>'''


def rings(cx, cy, radii, cls="rings", view="0 0 1000 1000", style=""):
    cs = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for r in radii)
    return f'<svg class="{cls}" viewBox="{view}" aria-hidden="true" style="{style}">{cs}</svg>'


RINGS = [70, 104, 132, 168, 196, 236, 262, 300, 344, 372, 420, 470]


def glyph(kind, size=54, dark=True):
    """Each product gets a figure built only from the brand's discs and seeds."""
    g, s, p = ("#9a9893" if dark else "#4D4C4A"), "#02A3FD", ("#1f1e1d" if dark else "#fff")
    body = {
        "expo": f'<circle cx="14" cy="34" r="10" fill="{g}"/><circle cx="32" cy="34" r="10" fill="{s}" stroke="{p}" stroke-width="3"/><circle cx="50" cy="34" r="10" fill="{g}" stroke="{p}" stroke-width="3"/><circle cx="32" cy="14" r="4" fill="{s}"/>',
        "news": f'<circle cx="30" cy="32" r="24" fill="{g}"/><path d="M18 26h24M18 33h24M18 40h14" stroke="{p}" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="12" r="7" fill="{s}" stroke="{p}" stroke-width="3"/>',
        "org": "".join(f'<circle cx="{32 + 20 * __import__("math").cos(a * 0.5236)}" cy="{32 + 20 * __import__("math").sin(a * 0.5236)}" r="{4 if a else 6}" fill="{s if a == 0 else g}"/>' for a in range(12)),
        "desk": f'<circle cx="32" cy="32" r="24" fill="none" stroke="{g}" stroke-width="5"/><circle cx="32" cy="32" r="12" fill="{s}"/><circle cx="49" cy="15" r="6" fill="#FEB916" stroke="{p}" stroke-width="3"/>',
        "survey": f'<circle cx="12" cy="44" r="8" fill="{g}"/><circle cx="30" cy="38" r="12" fill="{g}"/><circle cx="50" cy="28" r="12" fill="{s}" stroke="{p}" stroke-width="3"/><circle cx="50" cy="10" r="4" fill="{s}"/>',
        "swap": f'<circle cx="22" cy="36" r="17" fill="{g}"/><circle cx="42" cy="28" r="17" fill="{s}" stroke="{p}" stroke-width="4"/><path d="M34 28h16m-5-5 5 5-5 5" stroke="{p}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "stack": f'<circle cx="32" cy="46" r="15" fill="{g}"/><circle cx="32" cy="32" r="15" fill="{g}" stroke="{p}" stroke-width="3"/><circle cx="32" cy="18" r="15" fill="{s}" stroke="{p}" stroke-width="3"/>',
        "talk": f'<circle cx="24" cy="30" r="18" fill="none" stroke="{g}" stroke-width="5"/><circle cx="42" cy="34" r="18" fill="none" stroke="{s}" stroke-width="5"/><circle cx="12" cy="52" r="4" fill="{g}"/><circle cx="54" cy="54" r="4" fill="{s}"/>',
        "web": f'<circle class="g" cx="38" cy="28" r="22" fill="{g}"/><circle cx="24" cy="44" r="18" fill="{s}" stroke="{p}" stroke-width="3"/><circle cx="54" cy="10" r="5" fill="{g}" stroke="{p}" stroke-width="3"/>',
        "tools": f'<circle class="g" cx="20" cy="22" r="13" fill="{g}"/><circle cx="44" cy="22" r="13" fill="{s}"/><circle cx="20" cy="46" r="13" fill="{s}"/><circle cx="44" cy="46" r="13" fill="{g}"/>',
        "host": f'<circle class="g" cx="32" cy="16" r="10" fill="{g}"/><circle cx="32" cy="34" r="14" fill="{g}" stroke="{p}" stroke-width="3"/><circle cx="32" cy="50" r="10" fill="{s}" stroke="{p}" stroke-width="3"/>',
    }[kind]
    return f'<svg class="glyph" viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">{body}</svg>'


NAV = [("work", "work.html"), ("products", "products.html"), ("hosting", "hosting.html"), ("about", "about.html"), ("news", "news.html"), ("contact", "contact.html")]


def page(path, title, desc, body, current="", boot=False, R=None):
    depth = path.count("/")
    R = ("../" * depth) if R is None else R
    nav = "".join(f'<a href="{R}{h}"{" aria-current=page" if current == n else ""}>{n}</a>' for n, h in NAV)
    boot_html = ""
    if boot:
        boot_html = f'''<div class="boot" aria-hidden="true">{mark_svg("", "bt")}<p class="tag">from small beginnings</p></div>'''
    full = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{R}assets/brand/og.png">
<link rel="icon" href="{R}assets/brand/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{R}assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}assets/st.css?v={V}">
<script>document.documentElement.classList.add('js');{"try{if(!sessionStorage.getItem('st-boot')||location.search.includes('loader'))document.documentElement.classList.add('boot-on')}catch(e){}" if boot else ""}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{boot_html}
<header class="top" id="top">
  <div class="wrap">
    <a class="brand" href="{R}home.html" aria-label="Silvertrees web development, home">
      <img src="{R}assets/brand/mark.svg" width="40" height="40" alt="">
      <span><b>silvertrees</b><small>web development</small></span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn hat" href="{R}contact.html#start">start a project</a></nav>
    <a class="btn hat" href="{R}contact.html#start">start a project</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg viewBox="0 0 28 28" aria-hidden="true"><circle cx="9" cy="14" r="5" fill="#4D4C4A"/><circle cx="20" cy="14" r="5" fill="#02A3FD"/></svg></button>
  </div>
</header>
<main id="main">
{body}
</main>
{footer(R)}
<dialog class="lb" aria-label="Screenshot"><div class="bar"><span class="lb-cap"></span><span><button class="lb-prev" aria-label="Previous">←</button> <button class="lb-next" aria-label="Next">→</button> <button class="lb-x">close</button></span></div><img alt=""></dialog>
<script src="{R}assets/st.js?v={V}" defer></script>
</body>
</html>
'''
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(full, encoding="utf-8")
    PAGES.append(path)


PAGES = []


def footer(R):
    sectors = "".join(f'<li><a href="{R}work.html#{k}">{v}</a></li>' for k, v in SECTORS.items())
    tools = "".join(f'<li><a href="{R}products/{t["slug"]}.html">{esc(t["title"])}</a></li>' for t in TOOLS)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{R}home.html"><img src="{R}assets/brand/mark-night.svg" width="40" height="40" alt=""><span><b>silvertrees</b><small>web development</small></span></a>
        <p style="max-width:32ch;margin:20px 0 0">Websites and online tools for Australian businesses. Making online business simpler.</p>
        <p style="margin:18px 0 0"><a href="tel:{COMPANY["tel"]}">{COMPANY["phone"]}</a><br><a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></p>
      </div>
      <div><h4>work</h4><ul>{sectors}</ul></div>
      <div><h4>products</h4><ul>{tools}</ul></div>
      <div><h4>clients</h4><ul>
        <li><a href="{COMPANY["webmail"]}">Webmail</a></li>
        <li><a href="{COMPANY["mailadmin"]}">Mail admin</a></li>
        <li><a href="mailto:{COMPANY["support"]}">Technical support</a></li>
        <li><a href="{R}hosting.html">Hosting</a></li>
        <li><a href="{COMPANY["invoices"]}">Easy Invoices</a></li>
      </ul></div>
    </div>
    <p class="big" aria-hidden="true">silver<span>trees</span></p>
    <div class="legal"><span>© {YEAR} {COMPANY["name"]} · Sydney, Australia</span><span><a href="{R}index.html">identity</a> · redesign prototype</span></div>
  </div>
</footer>'''


def shot(R, s, alt, cls="", lazy=True):
    return f'<img src="{R}assets/work/{s["file"]}" alt="{esc(alt)}" width="640" height="480"{" loading=lazy decoding=async" if lazy else ""}>'


def host_of(item):
    site = item.get("site")
    if site:
        return re.sub(r"^https?://(www\.)?", "", site).rstrip("/")
    return item["title"] + " · by Silvertrees"


def browser(R, item, s, alt, lazy=True, cls=""):
    return f'''<figure class="browser {cls}"><div class="bar" aria-hidden="true"><i></i><i></i><i></i><span class="url">{esc(host_of(item))}</span></div>{shot(R, s, alt, lazy=lazy)}</figure>'''


def app_shot(t):
    return t["shots"][min(APP_SHOT.get(t["slug"], 1), len(t["shots"])) - 1]


def card(R, w, cls="", tone=""):
    s = w["shots"][0]
    return f'''<a class="card {cls}" href="{R}work/{w["slug"]}.html" data-s="{w["sector"]}" data-rise>
  <div class="frame notch {tone}"><div class="notch-in" style="height:100%">{shot(R, s, w["title"] + ", home page")}</div></div>
  <div class="meta"><h3 class="d4">{esc(w["title"].lower())}</h3><span class="sector">{SECTORS[w["sector"]]}</span></div>
  <p>{esc(w["line"])}</p>
</a>'''


def head(tag, title, lede="", side=""):
    return f'''<div class="head"><p class="tag">{tag}</p><h2 class="d2">{title}</h2>{side}{f'<p class="lede">{lede}</p>' if lede else ""}</div>'''


# ---------- home ----------
def home():
    R = ""
    reel = [w for w in SITES if w["slug"] in ("global-knives", "myflowermarket", "penthouse-on-bright-point", "scanpan", "online-curtains", "nepean-motor-group", "classic-building", "bhf-couriers")]
    imgs = "".join(
        f'<image href="assets/work/{w["shots"][0]["file"]}" x="10" y="86" width="176" height="132" preserveAspectRatio="xMidYMin slice" data-t="{esc(w["title"])}" data-u="work/{w["slug"]}.html"{" class=\"on\"" if i == 0 else ""}/>'
        for i, w in enumerate(reel))
    ring_c = "".join(f'<circle cx="140" cy="100" r="{r}"/>' for r in [96, 112, 134, 152, 178, 200, 232, 262, 300, 330])
    hero = f'''<section class="hero" aria-labelledby="h1">
  <div class="wrap">
    <div class="copy">
      <p class="tag">web development · sydney</p>
      <h1 class="d1" id="h1"><span class="line">making online</span><span class="line">business</span><span class="line"><em>simpler.</em></span></h1>
      <p class="lede">Silvertrees designs, builds and hosts the websites and online tools Australian businesses run on, and keeps them simple enough for anyone on your team to manage.</p>
      <div class="acts"><a class="btn hat" href="contact.html#start">start a project</a><a class="btn line" href="work.html">see the work</a></div>
      <ul class="facts"><li><span class="seed live"></span>{len(SITES)} sites on show</li><li><span class="seed live"></span>{len(TOOLS)} products of our own</li><li><span class="seed live"></span>hosted in Alexandria, Sydney</li></ul>
    </div>
    <div class="hero-mark">
      <svg viewBox="0 0 240 240" role="img" aria-labelledby="hm-t"><title id="hm-t">The Silvertrees mark, with a client site showing inside the blue disc</title>
        <defs>
          <mask id="hg" maskUnits="userSpaceOnUse" x="-200" y="-200" width="640" height="640"><rect x="-200" y="-200" width="640" height="640" fill="#fff"/><circle cx="88" cy="152" r="73"/><circle cx="188.9" cy="41.8" r="26"/></mask>
          <mask id="hb" maskUnits="userSpaceOnUse" x="0" y="0" width="240" height="240"><rect width="240" height="240" fill="#fff"/><circle cx="48.1" cy="199.5" r="24"/></mask>
          <clipPath id="hc"><circle cx="88" cy="152" r="66"/></clipPath>
          <filter id="duo" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".2126 .7152 .0722 0 0  .2126 .7152 .0722 0 0  .2126 .7152 .0722 0 0  0 0 0 1 0"/>
            <feComponentTransfer><feFuncR type="table" tableValues="0 0 .008"/><feFuncG type="table" tableValues=".11 .3 .639"/><feFuncB type="table" tableValues=".2 .55 .992"/></feComponentTransfer></filter>
        </defs>
        <g class="rings" style="color:var(--silver-2)" mask="url(#hg)">{ring_c}</g>
        <g class="hg" mask="url(#hg)"><circle cx="140" cy="100" r="80" fill="#4D4C4A"/></g>
        <circle class="hs1" cx="188.9" cy="41.8" r="17" fill="#4D4C4A"/>
        <text class="count" x="166" y="84" text-anchor="middle">{len(SITES)}</text>
        <text class="count-l" x="166" y="97" text-anchor="middle">sites built</text>
        <g mask="url(#hb)"><g clip-path="url(#hc)">
          <rect x="20" y="84" width="140" height="140" fill="#02A3FD"/>
          <g class="shotset" filter="url(#duo)">{imgs}</g>
        </g></g>
        <circle class="hs2" cx="48.1" cy="199.5" r="15" fill="#02A3FD"/>
      </svg>
      <p class="cap"><span class="seed live" style="color:var(--sky)"></span><span>now showing <a class="reel-t" href="work/{reel[0]["slug"]}.html"><b>{esc(reel[0]["title"])}</b></a></span><button class="reel-pause" type="button" aria-pressed="false" aria-label="Pause the client reel">pause</button></p>
    </div>
  </div>
</section>'''

    tracks = f'''<section class="band" aria-labelledby="t-what">
  <div class="wrap">
    {head("what we do", '<span id="t-what">three things, <em>done properly.</em></span>', "Most clients use all three: we build the site, add the tools it needs, and keep it running.")}
    <div class="tracks">
      <a class="track" href="work.html" data-rise>{glyph("web", 76, False)}<p class="num">01</p><h3 class="d3">web development</h3><p>Websites and online systems that talk to the public and quietly automate the office behind them.</p>
        <ul><li><span class="seed"></span>Brochure sites to full e-commerce</li><li><span class="seed"></span>Bookings, quotes, search, stock control</li><li><span class="seed"></span>Our own CMS, run by your staff</li></ul><span class="more">see {len(SITES)} projects <span class="seed"></span></span></a>
      <a class="track" href="products.html" data-rise>{glyph("tools", 76, False)}<p class="num">02</p><h3 class="d3">products</h3><p>Tools we built once and keep improving, so you get cutting-edge technology without the development bill.</p>
        <ul><li><span class="seed"></span>Online Expos and Newsletters</li><li><span class="seed"></span>Help Desk, Surveys in Seconds</li><li><span class="seed"></span>FileXchange and Online Doc Store</li></ul><span class="more">see {len(TOOLS)} products <span class="seed"></span></span></a>
      <a class="track" href="hosting.html" data-rise>{glyph("host", 76, False)}<p class="num">03</p><h3 class="d3">hosting</h3><p>Secure servers in a state-of-the-art data centre in Alexandria, Sydney, looked after by the people who built your site.</p>
        <ul><li><span class="seed"></span>Daily backups and support</li><li><span class="seed"></span>Standard and business packages</li><li><span class="seed"></span>Webmail for your whole team</li></ul><span class="more">hosting packages <span class="seed"></span></span></a>
    </div>
  </div>
</section>'''

    pick = ["global-knives", "myflowermarket", "online-curtains", "penthouse-on-bright-point", "scanpan", "bhf-couriers", "classic-building"]
    by = {w["slug"]: w for w in SITES}
    layout = [("wide", ""), ("", "sky"), ("", ""), ("", "sky"), ("", ""), ("half", "sky"), ("half", "")]
    cards = "".join(card("", by[s], c, t) for s, (c, t) in zip(pick, layout))
    work = f'''<section class="band mist" aria-labelledby="t-work">
  <div class="wrap">
    {head("selected work", '<span id="t-work">sites that <em>do things.</em></span>', "", '<a class="more" href="work.html">all {0} projects <span class="seed"></span></a>'.format(len(SITES)))}
    <div class="grid">{cards}</div>
  </div>
</section>'''

    grow = f'''<section class="band" aria-labelledby="t-grow">
  <div class="wrap">
    {head("how we work", '<span id="t-grow">from small beginnings, <em>sites that grow.</em></span>', "Every project is carefully architected and personally managed, start to finish. Then it keeps growing with the business.")}
    <ol class="grow">
      <li><div class="stage"><i></i></div><p class="num">01 · idea</p><h3 class="d4">a conversation</h3><p>We work to realise people's ideas online. It starts with what you need the site to do.</p></li>
      <li><div class="stage"><i></i></div><p class="num">02 · plan</p><h3 class="d4">architected</h3><p>Pages, data and admin mapped out before any design, with a clear eye on budget.</p></li>
      <li><div class="stage"><i></i></div><p class="num">03 · build</p><h3 class="d4">built in-house</h3><p>Design, function and technology, on our own modular content management system.</p></li>
      <li><div class="stage"><i></i></div><p class="num">04 · launch</p><h3 class="d4">live and hosted</h3><p>On our servers in Sydney, backed up daily, supported by the people who built it.</p></li>
      <li><div class="stage"><i></i></div><p class="num">05 · grow</p><h3 class="d4">add-ons, not rebuilds</h3><p>New components plug into the site as the market changes. No starting over.</p></li>
    </ol>
  </div>
</section>'''

    tabs = "".join(f'''<button class="pt" role="tab" id="pt-{t["slug"]}" aria-controls="pp-{t["slug"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" type="button">{glyph(t["glyph"], 36)}<span><b>{esc(t["title"])}</b><small>{esc(t["line"])}</small></span></button>''' for i, t in enumerate(TOOLS))
    panels = "".join(f'''<div class="pp" role="tabpanel" id="pp-{t["slug"]}" aria-labelledby="pt-{t["slug"]}"{" hidden" if i else ""}>
      {browser("", t, app_shot(t), t["title"] + ": " + app_shot(t)["caption"], lazy=i > 0, cls="dark")}
      <div class="pp-copy"><p class="num" style="color:#8d8b86">{i + 1:02d} / {len(TOOLS):02d}{" · free account" if t.get("free") else ""}</p><h3 class="d3">{esc(t["title"].lower())}</h3>
        <ul class="ticks">{"".join(f'<li><span class="seed live"></span>{esc(f)}</li>' for f in t["features"][:3])}</ul>
        <a class="btn on-dark line" href="products/{t["slug"]}.html">see {esc(t["title"])}</a></div>
    </div>''' for i, t in enumerate(TOOLS))
    products = f'''<section class="band dark" aria-labelledby="t-tools">
  {rings(1000, 0, [120, 200, 260, 340, 420, 470, 560, 640], "rings", "0 0 1000 600", "inset:0;width:100%;height:100%")}
  <div class="wrap" style="position:relative">
    <div class="head"><p class="tag on-dark">our products</p><h2 class="d2" id="t-tools">tools we built <em style="color:var(--sky-night)">once,</em> for everyone.</h2><p class="lede">Inexpensive answers to complex parts of running a business: trade shows, newsletters, support tickets, surveys and secure files.</p><a class="more" href="products.html" style="color:#fff">all {len(TOOLS)} products <span class="seed"></span></a></div>
    <div class="switch">
      <div class="pts" role="tablist" aria-label="Silvertrees products">{tabs}</div>
      <div class="pps">{panels}</div>
    </div>
  </div>
</section>'''

    dots = "".join('<i></i>' for _ in range(COMPANY["devs"])) + "".join('<i class="d"></i>' for _ in range(COMPANY["designers"])) + '<i class="w"></i><i class="w"></i>'
    crew = f'''<section class="band" aria-labelledby="t-crew">
  <div class="wrap crew">
    <div>
      <p class="tag">the team</p>
      <h2 class="d2" id="t-crew" style="margin-top:20px">small team, <em>no compromise.</em></h2>
      <div class="stat"><div><b>{COMPANY["devs"]}</b><span>developers</span></div><div><b>{COMPANY["designers"]}</b><span>designers</span></div></div>
      <p style="margin:18px 0 0;color:var(--ink-2)">plus copywriters and content editors</p>
    </div>
    <div>
      <div class="dots" role="img" aria-label="Six developers, two designers and two writers">{dots}</div>
      <p class="lede" style="margin-top:32px;max-width:44ch">Ideas come from everyone on the team, and one person manages your project from first call to launch. <a href="about.html">More about Silvertrees</a></p>
    </div>
  </div>
</section>'''

    notes = "".join(f'''<a class="note" href="news/{n["slug"]}.html" data-rise><p class="num">news · 0{i + 1}</p><h3 class="d4">{esc(n["title"].lower())}</h3><p>{esc(n["line"])}</p><span class="more">read <span class="seed"></span></span></a>''' for i, n in enumerate(NEWS))
    news = f'''<section class="band tight" aria-labelledby="t-news" style="padding-top:0">
  <div class="wrap">
    {head("news", '<span id="t-news">lately.</span>', "", '<a class="more" href="news.html">all news <span class="seed"></span></a>')}
    <div class="notes">{notes}</div>
  </div>
</section>'''

    page("home.html", "Silvertrees — web development, Sydney", "Silvertrees designs, builds and hosts websites and online tools for Australian businesses. Making online business simpler.",
         hero + tracks + work + grow + products + crew + news + start(R), current="", boot=True)


def start(R):
    return f'''<section class="start" aria-labelledby="t-start">
  {rings(800, 200, RINGS, "rings", "0 0 1000 1000")}
  <div class="wrap">
    <div>
      <p class="tag">start a project</p>
      <h2 class="d1" id="t-start" style="margin-top:22px">let's build it.</h2>
      <p class="lede" style="color:#3b2c00;margin-top:24px">Tell us what you want online. We'll tell you plainly how we'd build it and what it would cost.</p>
    </div>
    <div class="lines">
      <a href="tel:{COMPANY["tel"]}">{COMPANY["phone"]}</a>
      <a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a>
      <p style="margin:18px 0 0"><a class="btn" href="{R}contact.html#start" style="font-size:16px;letter-spacing:0">tell us about it</a></p>
    </div>
  </div>
</section>'''


def phead(R, crumbs, tag, title, lede="", extra=""):
    cr = " ".join(f'<a href="{R}{h}">{esc(t)}</a> <span aria-hidden="true">/</span>' for t, h in crumbs)
    return f'''<section class="phead">
  {rings(900, 120, RINGS, "rings", "0 0 1000 1000")}
  <div class="wrap" style="position:relative">
    <nav class="crumbs" aria-label="Breadcrumb">{cr} <span aria-current="page">{esc(tag)}</span></nav>
    <h1 class="d1">{title}</h1>
    {f'<p class="lede">{lede}</p>' if lede else ""}
    {extra}
  </div>
</section>'''


# ---------- work ----------
def work_index():
    R = ""
    counts = {k: sum(1 for w in SITES if w["sector"] == k) for k in SECTORS}
    filters = f'<button type="button" aria-pressed="true" data-f="all"><span class="seed"></span>everything <span class="n">{len(SITES)}</span></button>' + "".join(
        f'<button type="button" aria-pressed="false" data-f="{k}"><span class="seed"></span>{v} <span class="n">{counts[k]}</span></button>' for k, v in SECTORS.items())
    pattern = ["wide", "", "", "", "", "wide", "half", "half"]
    cards = "".join(card(R, w, "", "sky" if i % 3 == 1 else "") for i, w in enumerate(SITES))
    body = phead(R, [("home", "home.html")], "work", "the work.", f"{len(SITES)} websites and online systems, from a podiatry practice to a marketplace that pays florists directly. Almost all of them run on our own content management system.") + f'''
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter by sector">{filters}</div>
    <p class="count-live" role="status">{len(SITES)} projects</p>
    <div class="grid" id="work-grid">{cards}</div>
  </div>
</section>''' + start(R)
    page("work.html", "Work — Silvertrees", f"{len(SITES)} websites and online systems built by Silvertrees.", body, current="work")


def gallery(R, item):
    figs = "".join(f'''<li><figure><button type="button" data-full="{R}assets/work/{s["file"]}" data-cap="{esc(s["caption"])}" aria-label="Enlarge: {esc(s["caption"])}">{shot(R, s, item["title"] + ": " + s["caption"])}</button><figcaption><span class="num">{i + 1:02d}</span>{esc(s["caption"])}</figcaption></figure></li>''' for i, s in enumerate(item["shots"]))
    return f'<ul class="gallery">{figs}</ul>'


def case(item, i, items_, folder, label, kind_label):
    R = "../"
    prev_, next_ = items_[i - 1], items_[(i + 1) % len(items_)]
    site = item.get("site")
    feats = "".join(f'<li><span class="seed live"></span>{esc(f)}</li>' for f in item["features"])
    paras = "".join(f"<p>{esc(p)}</p>" for p in item["paras"])
    is_work = folder == "work"
    rows = []
    if is_work:
        rows += [("sector", SECTORS[item["sector"]]), ("type", item["kind"])]
    else:
        rows += [("type", "Silvertrees product")] + ([("price", "free account")] if item.get("free") else [])
    rows += [("built on", "Silvertrees CMS" if item["slug"] != "sesmo" else "WordPress"), ("screens", str(len(item["shots"])))]
    if site:
        host = re.sub(r"^https?://(www\.)?", "", site).rstrip("/")
        rows.append(("live", f'<a href="{esc(site)}" rel="noopener">{esc(host)} ↗</a>'))
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    extra_links = "".join(f'<li><span class="seed"></span><a href="{esc(l["href"])}" rel="noopener">{esc(l["label"])} ↗</a></li>' for l in item.get("extra", []))
    related = ""
    if is_work and item["slug"] == "sold-expo":
        related = '<p class="more" style="margin-top:24px"><a class="more" href="../products/online-expos.html">runs on Online Expos <span class="seed"></span></a></p>'
    if is_work and item["slug"] == "classic-building":
        related = '<p style="margin-top:24px"><a class="more" href="../products/filexchange.html">uses FileXchange <span class="seed"></span></a></p>'
    lead = item["shots"][0]
    tone = "sky" if i % 2 else ""
    top_glyph = "" if is_work else f'<div style="margin-bottom:8px">{glyph(item["glyph"], 88, False)}</div>'
    body = phead(R, [("home", "home.html"), (label, f"{folder}.html")], item["title"], esc(item["title"].lower()) + ("." if is_work else ""), esc(item["line"]), top_glyph) + f'''
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="lead-shot notch {tone}" style="--n:44px;margin-top:0"><div class="notch-in frame">{shot(R, lead, item["title"] + ": " + lead["caption"], lazy=False)}</div></div>
    <div class="case-top" style="margin-top:clamp(48px,6vw,88px)">
      <div class="prose">
        <p class="tag" style="margin-bottom:20px">the brief</p>
        {paras}
        {f'<ul class="feat" style="margin-top:28px">{extra_links}</ul>' if extra_links else ""}
        {related}
      </div>
      <div>
        <dl class="facts-tbl">{dl}</dl>
        {f'<p class="tag" style="margin:40px 0 8px">what it does</p><ul class="feat">{feats}</ul>' if feats else ""}
      </div>
    </div>
  </div>
</section>
<section class="band mist">
  <div class="wrap">
    {head("screens", "a look inside.", "Screens from the finished site.")}
    {gallery(R, item)}
  </div>
</section>
<section class="band tight">
  <div class="wrap">
    <nav class="pager" aria-label="More {label}">
      <a href="{prev_["slug"]}.html"><span class="num">← previous</span><span class="d3">{esc(prev_["title"].lower())}</span></a>
      <a href="{next_["slug"]}.html"><span class="num">next →</span><span class="d3">{esc(next_["title"].lower())}</span></a>
    </nav>
  </div>
</section>''' + start(R)
    page(f"{folder}/{item['slug']}.html", f"{item['title']} — {kind_label} — Silvertrees", item["line"], body, current=label)


# ---------- products ----------
def products_index():
    R = ""
    by = {t["slug"]: t for t in TOOLS}
    groups = ""
    n = 0
    for gi, (name, line, slugs) in enumerate(GROUPS):
        rows = ""
        for slug in slugs:
            t = by[slug]
            n += 1
            used = IN_USE.get(slug)
            rows += f'''<article class="prow">
        {browser(R, t, app_shot(t), t["title"] + ": " + app_shot(t)["caption"])}
        <div class="prow-copy">
          <div class="prow-top">{glyph(t["glyph"], 44, False)}<p class="num">{n:02d}</p>{'<span class="flag"><span class="seed live" style="color:var(--hat)"></span>free account</span>' if t.get("free") else ""}</div>
          <h3 class="d3"><a href="products/{t["slug"]}.html">{esc(t["title"].lower())}</a></h3>
          <p class="lede" style="font-size:18px">{esc(t["line"])}</p>
          <ul class="ticks light">{"".join(f'<li><span class="seed live"></span>{esc(f)}</li>' for f in t["features"][:3])}</ul>
          {f'<p class="used">in use on {", ".join(f"<a href=\"{h}\">{esc(u)}</a>" for u, h, _ in used)}</p>' if used else ""}
          <p class="acts"><a class="btn line" href="products/{t["slug"]}.html">how {esc(t["title"])} works</a>{f'<a class="more" href="{esc(t["site"])}" rel="noopener">{esc(host_of(t))} ↗</a>' if t.get("site") else ""}</p>
        </div>
      </article>'''
        groups += f'''<section class="band{" mist" if gi % 2 else ""}" aria-labelledby="g{gi}">
  <div class="wrap">
    <div class="ghead"><p class="tag">{gi + 1:02d} · {name}</p><h2 class="d2" id="g{gi}">{esc(line.lower().rstrip("."))}.</h2></div>
    <div class="prows">{rows}</div>
  </div>
</section>'''
    idx = "".join(f'<a href="#g{gi}"><span class="num">{gi + 1:02d}</span>{name}</a>' for gi, (name, _, _) in enumerate(GROUPS))
    cmp_rows = "".join(f"<tr><th scope=row>{k}</th><td>{a_}</td><td>{b_}</td></tr>" for k, a_, b_ in COMPARE)
    body = phead(R, [("home", "home.html")], "products", "our products.", "Innovative business tools from Silvertrees: secure ways to do business online, systems that automate routine work, and cutting-edge technology without the development overheads or the risk.",
                 f'<nav class="gidx" aria-label="Product groups">{idx}</nav>') + groups + f'''
<section class="band" aria-labelledby="t-cmp">
  <div class="wrap">
    <div class="head"><p class="tag">which file tool</p><h2 class="d2" id="t-cmp">filexchange or <em>online doc store?</em></h2><p class="lede">Same security, different size. FileXchange is the light-weight version of Online Doc Store.</p></div>
    <div class="tbl-wrap"><table class="cmp"><thead><tr><th scope="col"><span class="vh">Feature</span></th><th scope="col">{glyph("swap", 32, False)}<a href="products/filexchange.html">FileXchange</a></th><th scope="col">{glyph("stack", 32, False)}<a href="products/online-doc-store.html">Online Doc Store</a></th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
  </div>
</section>
<section class="band mist">
  <div class="wrap split">
    <div><p class="tag">why products</p><h2 class="d2" style="margin-top:20px">build once, <em>share the cost.</em></h2></div>
    <div class="prose"><p>Our main focus is cost-effective online solutions: an inexpensive, reliable presence with add-on components that plug straight into the website.</p><p>The products are those add-ons. Classic Building's site uses FileXchange for client files, and Sold Expo runs on Online Expos.</p><p><a class="more" href="contact.html#start">ask about a product <span class="seed"></span></a></p></div>
  </div>
</section>''' + start(R)
    page("products.html", "Products — Silvertrees", "Online Expos, Newsletters, the Organiser, Help Desk, Surveys in Seconds, FileXchange, Online Doc Store and e-therapy.", body, current="products")


def product_page(t, i):
    R = "../"
    by = {x["slug"]: x for x in TOOLS}
    steps = STEPS.get(t["slug"], [])
    steps_html = "".join(f'<li><span class="sn">{k + 1}</span><h3 class="d4">{esc(h)}</h3><p>{esc(d)}</p></li>' for k, (h, d) in enumerate(steps))
    feats = "".join(f'<li><span class="seed live"></span>{esc(f)}</li>' for f in t["features"])
    paras = "".join(f"<p>{esc(x)}</p>" for x in t["paras"])
    used = IN_USE.get(t["slug"], [])
    used_html = "".join(f'<a class="note" href="{R}{h}"><p class="num">in use on</p><h3 class="d4">{esc(u.lower())}</h3><p>{esc(d)}</p><span class="more">see it <span class="seed"></span></span></a>' for u, h, d in used)
    extra = "".join(f'<a class="note" href="{esc(l["href"])}" rel="noopener"><p class="num">live</p><h3 class="d4">{esc(host_of({"site": l["href"]}))} ↗</h3><p>{esc(l["label"])}</p></a>' for l in t.get("extra", []) if "classicbuilding" not in l["href"] and "sold-expo" not in l["href"])
    rel = "".join(f'<a class="rel" href="{x}.html">{glyph(by[x]["glyph"], 40, False)}<span><b>{esc(by[x]["title"])}</b><small>{esc(by[x]["line"])}</small></span></a>' for x in RELATED.get(t["slug"], []))
    app = app_shot(t)
    prev_, next_ = TOOLS[i - 1], TOOLS[(i + 1) % len(TOOLS)]
    acts = f'<a class="btn hat" href="{R}contact.html#start">ask about {esc(t["title"])}</a>' + (f'<a class="btn line" href="{esc(t["site"])}" rel="noopener">visit {esc(host_of(t))} ↗</a>' if t.get("site") else "")
    body = f'''<section class="phead prod-hero">
  {rings(900, 120, RINGS, "rings", "0 0 1000 1000")}
  <div class="wrap" style="position:relative">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{R}home.html">home</a> <span aria-hidden="true">/</span> <a href="{R}products.html">products</a> <span aria-hidden="true">/</span> <span aria-current="page">{esc(t["title"])}</span></nav>
    <div class="ph-grid">
      <div class="ph-copy">
        <div class="prow-top">{glyph(t["glyph"], 64, False)}{'<span class="flag"><span class="seed live" style="color:var(--hat)"></span>free account</span>' if t.get("free") else ""}</div>
        <h1 class="d1">{esc(t["title"].lower())}.</h1>
        <p class="lede">{esc(t["line"])}</p>
        <p class="acts">{acts}</p>
      </div>
      {browser(R, t, app, t["title"] + ": " + app["caption"], lazy=False, cls="lift")}
    </div>
  </div>
</section>
{f'''<section class="band mist" aria-labelledby="t-how"><div class="wrap">
  <div class="head"><p class="tag">how it works</p><h2 class="d2" id="t-how">{len(steps)} steps, <em>that's it.</em></h2></div>
  <ol class="steps" style="--n:{len(steps)}">{steps_html}</ol>
</div></section>''' if steps else ""}
<section class="band">
  <div class="wrap case-top">
    <div class="prose"><p class="tag" style="margin-bottom:20px">about {esc(t["title"])}</p>{paras}</div>
    <div><p class="tag" style="margin-bottom:8px">what you get</p><ul class="feat">{feats}</ul></div>
  </div>
</section>
{f'<section class="band tight" style="padding-top:0"><div class="wrap"><div class="notes">{used_html}{extra}</div></div></section>' if used_html or extra else ""}
<section class="band mist">
  <div class="wrap">
    {head("screens", "a look inside.", f"{len(t['shots'])} screens from {t['title']}.")}
    {gallery(R, t)}
  </div>
</section>
<section class="band tight">
  <div class="wrap">
    <p class="tag" style="margin-bottom:18px">works well with</p>
    <div class="rels">{rel}</div>
    <nav class="pager" aria-label="More products" style="margin-top:48px">
      <a href="{prev_["slug"]}.html"><span class="num">← previous</span><span class="d3">{esc(prev_["title"].lower())}</span></a>
      <a href="{next_["slug"]}.html"><span class="num">next →</span><span class="d3">{esc(next_["title"].lower())}</span></a>
    </nav>
  </div>
</section>''' + start(R)
    page(f"products/{t['slug']}.html", f"{t['title']} — Products — Silvertrees", t["line"], body, current="products")


# ---------- hosting ----------
def hosting():
    R = ""
    plans = "".join(f'''<div class="plan notch {"sky" if p.get("lead") else ""}" style="--n:22px"><p class="tag">{p["name"]}</p><h2 class="d3">{esc(p["line"].lower().rstrip("."))}.</h2><ul class="feat">{"".join(f'<li><span class="seed live"></span>{esc(x)}</li>' for x in p["items"])}</ul><a class="more" href="contact.html#start" style="margin-top:auto">ask for pricing <span class="seed"></span></a></div>''' for p in HOSTING["plans"])
    body = phead(R, [("home", "home.html")], "hosting", "hosting with <em>peace of mind.</em>", HOSTING["intro"]) + f'''
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="plans">{plans}</div>
  </div>
</section>
<section class="band dark">
  {rings(500, 300, [60, 110, 150, 200, 240, 300, 350, 420, 480], "rings", "0 0 1000 600", "inset:0;width:100%;height:100%")}
  <div class="wrap split" style="position:relative">
    <div><p class="tag on-dark">where it lives</p><h2 class="d2" style="margin-top:20px">alexandria, <em style="color:var(--sky-night)">sydney.</em></h2></div>
    <div class="prose" style="color:#cfcdc8"><p>Your site sits on secure servers in a state-of-the-art data centre in Alexandria, with daily backups and technical support from the team that built it.</p><p>Large online storage? Dedicated servers are available. Already a client? Reach your mail from anywhere.</p>
      <p style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn" href="{COMPANY["webmail"]}" style="--b:#fff;--fg:var(--ink);--dotc:var(--sky)">webmail</a><a class="btn line on-dark" href="{COMPANY["mailadmin"]}">mail admin</a></p></div>
  </div>
</section>''' + start(R)
    page("hosting.html", "Hosting — Silvertrees", "Hosting packages on secure servers in Alexandria, Sydney, with daily backups and webmail.", body, current="hosting")


# ---------- about ----------
def about():
    R = ""
    clients = "".join(f'<li><a href="work/{w["slug"]}.html"><span class="seed live"></span>{esc(w["title"])}</a></li>' for w in SITES)
    body = phead(R, [("home", "home.html")], "about", "making life <em>easier, not harder.</em>", "Silvertrees is a Sydney web development company. We provide business ideas, advice and solutions through the intelligent use of computers and the internet.") + f'''
<section class="band" style="padding-top:0">
  <div class="wrap split">
    <div class="prose">
      <p class="tag" style="margin-bottom:20px">how we work</p>
      <p>A broad range of services, skills, alliances and vendor partnerships, all coupled to a dedicated, long-term approach and services tailored to each client.</p>
      <p>Our main focus is cost-effective online solutions built from a series of products: an inexpensive and reliable online presence, with a growing selection of add-on components that integrate seamlessly into the basic website. It lets a site respond to changing market conditions, always with a good eye on financial constraints.</p>
      <p>We create systems that talk to the public, and also save time and automate office processes, in a way that is easily understood and operated. That is the key to what we do.</p>
    </div>
    <div>
      <p class="tag" style="margin-bottom:8px">what our tools give a business</p>
      <ul class="feat">
        <li><span class="seed live"></span>Secure, efficient ways to do business online</li>
        <li><span class="seed live"></span>Reliable systems that automate routine work, so staff can do the profitable work</li>
        <li><span class="seed live"></span>Cutting-edge technology without the development overheads and risk</li>
        <li><span class="seed live"></span>Inexpensive solutions to complex areas of business</li>
      </ul>
    </div>
  </div>
</section>
<section class="band mist">
  <div class="wrap crew">
    <div><p class="tag">the team</p><h2 class="d2" style="margin-top:20px">{COMPANY["devs"]} developers. {COMPANY["designers"]} designers. <em>one process.</em></h2></div>
    <div class="prose"><p>Plus copywriters and content editors. Ideas come from everyone, and every project is planned carefully and managed personally from start to finish.</p><p style="font-size:22px;font-weight:600;letter-spacing:-.01em;color:var(--ink)">“Silvertrees delivers the best, literally without compromise.”</p></div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("brought to you by silvertrees", "the clients.", "Every one of these sites was designed, built and is managed on Silvertrees systems.")}
    <ul class="feat" style="columns:3 240px;column-gap:40px;display:block">{clients}</ul>
  </div>
</section>''' + start(R)
    body = body.replace('<ul class="feat" style="columns', '<ul class="feat clients" style="columns')
    page("about.html", "About — Silvertrees", "Silvertrees is a Sydney web development company building cost-effective websites and online tools.", body, current="about")


# ---------- news ----------
def news_pages():
    R = ""
    notes = "".join(f'''<a class="note" href="news/{n["slug"]}.html"><p class="num">news · 0{i + 1}</p><h2 class="d3">{esc(n["title"].lower())}</h2><p>{esc(n["line"])}</p><span class="more">read <span class="seed"></span></span></a>''' for i, n in enumerate(NEWS))
    page("news.html", "News — Silvertrees", "News and product launches from Silvertrees.",
         phead(R, [("home", "home.html")], "news", "news.", "Product launches and what the team is working on.") + f'<section class="band" style="padding-top:0"><div class="wrap"><div class="notes">{notes}</div></div></section>' + start(R), current="news")
    tools = {t["slug"]: t for t in TOOLS}
    for i, n in enumerate(NEWS):
        R = "../"
        t = tools[n["product"]]
        others = "".join(f'<a class="note" href="{m["slug"]}.html"><h3 class="d4">{esc(m["title"].lower())}</h3><p>{esc(m["line"])}</p></a>' for m in NEWS if m is not n)
        body = phead(R, [("home", "home.html"), ("news", "news.html")], n["title"], esc(n["title"].lower()) + ".", esc(n["line"])) + f'''
<section class="band" style="padding-top:0">
  <div class="wrap split">
    <div class="prose">{"".join(f"<p>{esc(p)}</p>" for p in n["body"])}<p style="margin-top:28px"><a class="btn" href="../products/{t["slug"]}.html">see {esc(t["title"])}</a></p></div>
    <div class="lead-shot notch sky" style="margin:0;--n:30px"><div class="notch-in frame photo">{shot(R, t["shots"][0], t["title"] + ": " + t["shots"][0]["caption"], lazy=False)}</div></div>
  </div>
</section>
<section class="band tight mist"><div class="wrap"><p class="tag" style="margin-bottom:12px">more news</p><div class="notes" style="grid-template-columns:repeat(2,minmax(0,1fr))">{others}</div></div></section>''' + start(R)
        page(f"news/{n['slug']}.html", f"{n['title']} — News — Silvertrees", n["line"], body, current="news")


# ---------- contact ----------
def contact():
    R = ""
    kinds = ["a new website", "an online store", "one of your products", "hosting or email", "not sure yet"]
    ch = "".join(f'<label><input type="radio" name="kind" value="{k}"{" checked" if i == 0 else ""}>{k}</label>' for i, k in enumerate(kinds))
    body = phead(R, [("home", "home.html")], "contact", "let's talk.", "Contact us today to discuss how we could achieve the results you want.") + f'''
<section class="band" style="padding-top:0" id="start">
  <div class="wrap split">
    <form class="form" id="enquiry" novalidate>
      <fieldset class="choices full"><legend>I'm after</legend>{ch}</fieldset>
      <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="f-co">Business</label><input id="f-co" name="company" autocomplete="organization"></div>
      <div class="field full"><label for="f-msg">What should it do?</label><textarea id="f-msg" name="message" required></textarea><span class="hint">A few lines is plenty. We'll call you back.</span></div>
      <label class="full" style="display:flex;gap:10px;align-items:center;font-size:15.5px"><input type="checkbox" name="news" style="inline-size:18px;block-size:18px;accent-color:var(--sky)"> Send me interesting information</label>
      <div class="full"><button class="btn hat" type="submit">send enquiry</button></div>
      <p class="done full" role="status"><span class="seed live" style="color:var(--sky)"></span><span>Prototype: nothing was sent. On the live site this goes to {COMPANY["email"]}.</span></p>
    </form>
    <div>
      <dl class="facts-tbl">
        <div><dt>phone</dt><dd><a href="tel:{COMPANY["tel"]}">{COMPANY["phone"]}</a></dd></div>
        <div><dt>enquiries</dt><dd><a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></dd></div>
        <div><dt>support</dt><dd><a href="mailto:{COMPANY["support"]}">{COMPANY["support"]}</a></dd></div>
        <div><dt>company</dt><dd>{COMPANY["name"]}</dd></div>
        <div><dt>servers</dt><dd>Alexandria, Sydney</dd></div>
      </dl>
      <p class="tag" style="margin:40px 0 14px">already a client</p>
      <p style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn line" href="{COMPANY["webmail"]}">webmail</a><a class="btn line" href="{COMPANY["mailadmin"]}">mail admin</a></p>
    </div>
  </div>
</section>'''
    page("contact.html", "Contact — Silvertrees", "Call +61 2 9063 8994 or send an enquiry to Silvertrees web development.", body, current="contact")


def not_found():
    R = BASE404
    body = f'''<section class="phead" style="min-height:60vh;display:grid;align-items:center">
  {rings(700, 400, RINGS, "rings", "0 0 1000 1000")}
  <div class="wrap" style="position:relative">
    <p class="tag" style="color:var(--hat-ink)"><span class="seed hat"></span> 404 · under construction</p>
    <h1 class="d1" style="margin-top:24px">this page is <em>still a seed.</em></h1>
    <p class="lede" style="margin-top:24px">Nothing has grown at this address yet. It may have moved when the site was rebuilt.</p>
    <p style="display:flex;gap:12px;flex-wrap:wrap;margin-top:32px"><a class="btn" href="{R}home.html">home</a><a class="btn line" href="{R}work.html">the work</a></p>
  </div>
</section>'''
    page("404.html", "Not found — Silvertrees", "This page does not exist.", body, R=R)


def main():
    photos()
    home()
    work_index()
    for i, w in enumerate(SITES):
        case(w, i, SITES, "work", "work", "Work")
    products_index()
    for i, t in enumerate(TOOLS):
        product_page(t, i)
    hosting()
    about()
    news_pages()
    contact()
    not_found()
    print(len(PAGES), "pages")


if __name__ == "__main__":
    main()
