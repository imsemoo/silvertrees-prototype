"""The Silvertrees identity book -> index.html (built after build.py; reuses its page shell)."""
import build
from build import COMPANY, SITES, TOOLS, esc, glyph, mark_svg, page, rings

SWATCHES = [
    ("graphite", "#4D4C4A", "the business. Big disc, wordmark, body on dark grey.", "8.6:1 on white", "#fff"),
    ("sky", "#02A3FD", "the web. Blue disc, seeds, links, focus. Fills and shapes only.", "2.7:1 · shapes only", "#fff"),
    ("sky type", "#0098EC", "the logo blue nudged for large headlines.", "3.1:1 · large type", "#fff"),
    ("sky ink", "#006FB3", "blue for small text and labels.", "5.4:1 on white", "#fff"),
    ("ink", "#232220", "text. Warm, never pure black.", "15.9:1 on white", "#fff"),
    ("hat", "#FEB916", "the hard hat. Only for “start building”.", "9.2:1 with ink", "#232220"),
    ("mist", "#F2F3F4", "silver as a surface: alternate bands.", "panel", "#232220"),
    ("silver", "#C9CDD1", "silver as a line: rings, borders.", "lines only", "#232220"),
    ("night", "#1F1E1D", "dark bands and the footer.", "16.6:1 with white", "#fff"),
]


def book():
    R = ""
    sw = "".join(f'''<div class="sw"><div class="chip" style="background:{h};color:{fg}"><span class="num" style="color:inherit">{h}</span></div><h3 class="d4">{n}</h3><p>{r}</p><p class="num">{c}</p></div>''' for n, h, r, c, fg in SWATCHES)
    body = f'''
<section class="bk-cover">
  {rings(500, 500, [150, 190, 236, 270, 320, 352, 400, 440, 470], "rings", "0 0 1000 1000")}
  <div class="wrap">
    <div class="bk-mark">{mark_svg("replay", "cv")}</div>
    <div class="copy">
      <p class="tag">identity · {build.YEAR}</p>
      <h1 class="d1">small<br>beginnings.</h1>
      <p class="lede">A visual identity for Silvertrees, built so that if the logo came off the page you would still know whose page it is.</p>
      <p class="acts"><button class="btn line" type="button" data-replay>replay the mark</button><a class="btn hat" href="home.html">open the site</a></p>
    </div>
  </div>
</section>

<section class="band" id="idea">
  <div class="wrap split">
    <div>
      <p class="tag">01 · the idea</p>
      <h2 class="d2" style="margin-top:20px">from small beginnings, <em>super heroes grow.</em></h2>
      <p class="lede" style="margin-top:24px">That line has sat on silvertrees.net for years. The logo already draws it: two discs, each carrying a small seed on its rim. We kept the logo exactly as it is and read it as a system.</p>
    </div>
    <figure class="anatomy">
      {mark_svg("", "an")}
      <figcaption>
        <span style="--x:84%;--y:0%"><b>seed</b> something starting</span>
        <span style="--x:72%;--y:46%"><b>disc</b> something launched</span>
        <span style="--x:0%;--y:22%"><b>moat</b> the white gap where two things meet</span>
        <span style="--x:2%;--y:92%"><b>diagonal</b> graphite above, sky below</span>
      </figcaption>
    </figure>
  </div>
</section>

<section class="band mist" id="fingerprints">
  <div class="wrap">
    <div class="head"><p class="tag">02 · six fingerprints</p><h2 class="d2">recognisable <em>without the logo.</em></h2><p class="lede">Each one is lifted straight from the mark. Any two of them on a page are enough to say “Silvertrees”.</p></div>
    <div class="fp">
      <div class="fp-t"><div class="fp-v"><span class="st"><span class="seed" style="color:var(--graphite)"></span> planned</span><span class="st"><span class="seed hat"></span> building</span><span class="st"><span class="seed live" style="color:var(--sky)"></span> live</span></div><h3 class="d4">seed and disc</h3><p>A ring means starting, a dot in its moat means launched. Bullets, statuses, links and the menu button all speak it.</p></div>
      <div class="fp-t"><div class="fp-v"><svg viewBox="0 0 200 120" aria-hidden="true"><circle cx="120" cy="56" r="46" fill="#4D4C4A"/><circle cx="80" cy="70" r="40" fill="#02A3FD" stroke="#fff" stroke-width="8"/></svg></div><h3 class="d4">the moat</h3><p>Where two shapes meet there is always a white gap, never an overlap. It is what makes the logo feel clean, so the whole site inherits it.</p></div>
      <div class="fp-t"><div class="fp-v"><div class="notch sky" style="--n:18px;inline-size:min(56%,180px)"><div class="notch-in" style="background:var(--graphite);aspect-ratio:4/3"></div></div></div><h3 class="d4">the notch</h3><p>Panels and screenshots carry a seed bitten into one corner: graphite at the top, sky at the bottom, as in the mark.</p></div>
      <div class="fp-t"><div class="fp-v"><p class="tag" style="font-size:15px">web development</p></div><h3 class="d4">tracked lowercase</h3><p>The logo's second line, widely spaced and lowercase, becomes every label. Headlines go lowercase like the wordmark.</p></div>
      <div class="fp-t"><div class="fp-v" style="overflow:hidden">{rings(100, 60, [14, 22, 32, 40, 52, 60, 74, 86, 100], "rings", "0 0 200 120", "position:static;color:var(--silver);width:100%;height:100%")}</div><h3 class="d4">growth rings</h3><p>Silver trees, read in section: thin silver rings spread from the discs, never evenly, like a trunk. They replace gradients and texture.</p></div>
      <div class="fp-t"><div class="fp-v" style="background:var(--hat)"><span class="btn" style="pointer-events:none">start a project</span></div><h3 class="d4">hard hat yellow</h3><p>From the “under construction” version of the logo. One meaning only: start building. The CTA, the enquiry slab, the 404.</p></div>
    </div>
  </div>
</section>

<section class="band" id="colour">
  <div class="wrap">
    <div class="head"><p class="tag">03 · colour</p><h2 class="d2">two logo colours, <em>one rule each.</em></h2><p class="lede">Graphite and sky are sampled from the logo file. Everything else is silver, ink or the hat. Contrast is measured, not guessed.</p></div>
    <div class="swatches">{sw}</div>
  </div>
</section>

<section class="band dark" id="type">
  <div class="wrap">
    <div class="head"><p class="tag on-dark">04 · type</p><h2 class="d2">figtree. <em style="color:var(--sky-night)">silver, trees, figs.</em></h2><p class="lede">A friendly geometric sans with the open, round counters of the wordmark. One family, set three ways, plus a mono for numbers.</p></div>
    <div class="spec">
      <div><p class="num" style="color:#8d8b86">display · 700 · lowercase · −0.045em</p><p class="d1" style="margin-top:12px">making online business simpler.</p></div>
      <div class="spec-row">
        <div><p class="num" style="color:#8d8b86">label · 600 · 12.5px · +0.34em</p><p class="tag on-dark" style="margin-top:14px">web development · sydney</p></div>
        <div><p class="num" style="color:#8d8b86">text · 400 · 17/1.6</p><p style="margin:14px 0 0;color:#cfcdc8;max-width:40ch">We create systems that talk to the public, and also save time and automate office processes, in a way that is easily understood and operated.</p></div>
        <div><p class="num" style="color:#8d8b86">numbers · JetBrains Mono</p><p style="margin:14px 0 0;font:500 34px/1 var(--mono);color:#fff">+61 2 9063 8994</p></div>
      </div>
    </div>
  </div>
</section>

<section class="band" id="mark">
  <div class="wrap">
    <div class="head"><p class="tag">05 · the mark</p><h2 class="d2">kept, <em>tightened.</em></h2><p class="lede">The same mark, redrawn as clean geometry so it scales from a favicon to a building wrap. Discs on a 45° diagonal, seeds sitting on the rims, a moat around everything that touches.</p></div>
    <div class="versions">
      <div class="v" style="background:#fff;outline:1px solid var(--silver-2)"><img src="assets/brand/mark.svg" alt="" width="120" height="120"><div class="lock"><b>silvertrees</b><small>web development</small></div></div>
      <div class="v" style="background:var(--night)"><img src="assets/brand/mark-night.svg" alt="" width="120" height="120"><div class="lock" style="--c:#fff"><b>silvertrees</b><small>web development</small></div></div>
      <div class="v" style="background:var(--sky)">{mark_svg("mono-w", "mw")}<div class="lock" style="--c:#fff;--t:#fff"><b>silvertrees</b><small>web development</small></div></div>
      <div class="v" style="background:var(--hat)">{mark_svg("mono-k", "mk")}<div class="lock" style="--c:var(--ink);--t:var(--ink)"><b>silvertrees</b><small>web development</small></div></div>
    </div>
    <div class="rules">
      <div><h3 class="d4">construction</h3><p>Graphite disc r 80, sky disc r 66, seeds r 17 and 15, moats 8 units. Centres share one diagonal.</p></div>
      <div><h3 class="d4">clear space</h3><p>One seed diameter on every side. Nothing enters the moat.</p></div>
      <div><h3 class="d4">smallest size</h3><p>Mark 20 px. Lockup 120 px wide; below that, drop the “web development” line.</p></div>
      <div><h3 class="d4">never</h3><p>Recolour the discs, fill the moat, rotate the diagonal, or add the hat to the everyday logo.</p></div>
    </div>
  </div>
</section>

<section class="band mist" id="hat">
  <div class="wrap split" style="align-items:center">
    <figure style="margin:0"><img src="assets/brand/hardhat.webp" alt="The Silvertrees logo wearing a yellow hard hat" width="1000" height="333" style="width:100%;height:auto;background:#fff"></figure>
    <div>
      <p class="tag">06 · the hat</p>
      <h2 class="d2" style="margin-top:20px">the hat means <em>we're building.</em></h2>
      <p class="lede" style="margin-top:24px">Silvertrees already had a hard-hat version of the logo. Instead of a second logo, it became a colour with one job: every “start a project” is hat yellow, the enquiry slab is hat yellow, and a missing page is “under construction”.</p>
      <p style="margin-top:28px"><a class="more" href="404.html">see the 404 <span class="seed"></span></a></p>
    </div>
  </div>
</section>

<section class="band" id="motion">
  <div class="wrap">
    <div class="head"><p class="tag">07 · motion</p><h2 class="d2">things <em>grow,</em> they don't slide.</h2><p class="lede">One verb for all motion: a seed grows into a disc. Springy, short, and switched off for anyone who asks their device for less motion.</p></div>
    <div class="motion">
      <div><div class="mo-v"><button class="btn" type="button">hover me</button></div><h3 class="d4">buttons</h3><p>The seed inside the button grows until it fills it.</p></div>
      <div><div class="mo-v">{mark_svg("replay small", "mo")}<button class="btn line" type="button" data-replay style="position:absolute;bottom:14px;inset-inline-end:14px;min-block-size:40px;font-size:14px">replay</button></div><h3 class="d4">loader</h3><p>First visit only: the sky seed, the sky disc, the graphite disc, then its seed. 1.7 seconds.</p></div>
      <div><div class="mo-v"><ol class="grow in" style="grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;inline-size:100%"><li><div class="stage" style="block-size:90px"><i></i></div></li><li><div class="stage" style="block-size:90px"><i></i></div></li><li><div class="stage" style="block-size:90px"><i style="inline-size:40px;block-size:40px"></i></div></li><li><div class="stage" style="block-size:90px"><i style="inline-size:58px;block-size:58px"></i></div></li><li><div class="stage" style="block-size:90px"><i style="inline-size:80px;block-size:80px"></i></div></li></ol></div><h3 class="d4">process</h3><p>The five steps of a project are drawn as one seed growing.</p></div>
    </div>
  </div>
</section>

<section class="band mist" id="apply">
  <div class="wrap">
    <div class="head"><p class="tag">08 · in use</p><h2 class="d2">off the screen, <em>still them.</em></h2></div>
    <div class="apps">
      <div class="card-biz front"><img src="assets/brand/mark.svg" alt="" width="56" height="56"><div><b>Gerard</b><span>Silvertrees Web Development</span></div><p class="num">{COMPANY["phone"]}<br>{COMPANY["email"]}</p></div>
      <div class="card-biz back">{rings(300, 60, [30, 52, 70, 96, 120, 150, 176, 210], "rings", "0 0 350 200", "inset:0;width:100%;height:100%;color:#ffffff22")}<p class="tag on-dark" style="position:relative">making online business simpler</p></div>
      <div class="sig"><p style="margin:0 0 4px"><b>Gerard</b></p><p style="margin:0;color:var(--ink-2);font-size:14px">Silvertrees Web Development</p><p class="num" style="margin:12px 0 0">{COMPANY["phone"]} · silvertrees.net</p><p class="tag" style="margin-top:14px;display:flex;gap:8px;align-items:center"><span class="seed live" style="color:var(--sky)"></span>web development</p></div>
      <div class="avatar"><div><img src="assets/brand/mark.svg" alt="" width="120" height="120"></div><p class="num">social avatar · favicon</p></div>
    </div>
  </div>
</section>

<section class="band" id="pages">
  <div class="wrap">
    <div class="head"><p class="tag">09 · the site</p><h2 class="d2">every page, <em>built.</em></h2><p class="lede">{len(SITES)} case studies and {len(TOOLS)} product pages from the real material on silvertrees.net, plus hosting, about, news, contact and a 404.</p></div>
    <ul class="feat sitemap" style="columns:3 240px;column-gap:40px;display:block">
      <li><span class="seed live"></span><a href="home.html">Home</a></li>
      <li><span class="seed live"></span><a href="work.html">Work, filtered by sector</a></li>
      {"".join(f'<li><span class="seed"></span><a href="work/{w["slug"]}.html">{esc(w["title"])}</a></li>' for w in SITES)}
      <li><span class="seed live"></span><a href="products.html">Products</a></li>
      {"".join(f'<li><span class="seed"></span><a href="products/{t["slug"]}.html">{esc(t["title"])}</a></li>' for t in TOOLS)}
      <li><span class="seed live"></span><a href="hosting.html">Hosting</a></li>
      <li><span class="seed live"></span><a href="about.html">About</a></li>
      <li><span class="seed live"></span><a href="news.html">News</a> (3 stories)</li>
      <li><span class="seed live"></span><a href="contact.html">Contact</a></li>
      <li><span class="seed hat"></span><a href="404.html">404</a></li>
    </ul>
  </div>
</section>'''
    page("index.html", "Silvertrees — identity", "The Silvertrees visual identity: small beginnings. Disc, seed, moat, notch, tracked lowercase, growth rings and hard-hat yellow.", body, current="")


if __name__ == "__main__":
    book()
