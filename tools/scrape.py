"""Pull Silvertrees' real projects, products, hosting and news from silvertrees.net.

Writes research/catalog.json and research/shots/<slug>-<n>.jpg (full-size originals).
"""
import base64, html, json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research"
SHOTS = OUT / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)
BASE = "https://www.silvertrees.net"

GROUPS = {
    "web": [
        "sold-expo", "psychmatters", "brydens-compensation-lawyers", "myflowermarket",
        "global-knives", "capstar", "trade-publishing-pty-ltd", "online-curtains",
        "classic-building", "sesmo", "portfolio-reel", "doors-plus", "viewmag",
        "penthouse-on-bright-point", "mwt-foods", "jayspjs", "hardware-glass", "scanpan",
        "nepean-motor-group", "bhf-couriers", "di-lorenzo",
    ],
    "product": [
        "online-expos", "online-newsletters", "online-organiser", "help-desk-ticket-support-system",
        "surveys-in-seconds", "filexchange", "online-doc-store", "e-therapy-com-au",
    ],
    "hosting": ["silvertrees-hosting"],
}
NEWS = ["online-newsletters", "the-silvertrees-organiser", "the-business-expo"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def text(fragment):
    fragment = re.sub(r"<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"[ \t\xa0]+", " ", html.unescape(fragment)).strip()


def original(src):
    """resize_image.php?image=<base64 filename> -> /img/uploads/<filename>"""
    q = urllib.parse.parse_qs(urllib.parse.urlparse(html.unescape(src)).query)
    name = base64.b64decode(q["image"][0]).decode()
    return f"{BASE}/img/uploads/{name}", name


def project(slug, group):
    page = get(f"{BASE}/projects/view/{slug}").decode("utf-8", "replace")
    block = re.search(r'class="ProjectAbs">(.*?)</td>', page, re.S)
    body = block.group(1) if block else ""
    title = text(re.search(r"<h4>(.*?)</h4>", body, re.S).group(1)) if "<h4>" in body else slug
    paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
    paras = [p for p in paras if p]
    heads = [text(h) for h in re.findall(r"<h4>(.*?)</h4>", body, re.S)][1:]
    feats = [text(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S)]
    links = re.findall(r'<li><a target="_blank" title="([^"]*)" href="([^"]*)"', page)
    shots = []
    seen = set()
    for alt, src in re.findall(r'<img alt="([^"]*)" src="(/resize_image\.php[^"]*&w=160[^"]*)"', page):
        url, name = original(src)
        if name in seen:
            continue
        seen.add(name)
        dest = SHOTS / f"{slug}-{len(shots) + 1}.jpg"
        if not dest.exists():
            try:
                dest.write_bytes(get(url))
            except Exception as e:  # missing originals are skipped, not faked
                print("  miss", url, e)
                continue
        shots.append({"file": dest.name, "caption": alt.replace("-", " ").replace("_", " ")})
    if not shots:  # fall back to the main thumb
        m = re.search(r'class="MaskedThumbs">.*?src="(/resize_image\.php[^"]*)"', page, re.S)
        if m:
            url, name = original(m.group(1))
            dest = SHOTS / f"{slug}-1.jpg"
            if not dest.exists():
                dest.write_bytes(get(url))
            shots.append({"file": dest.name, "caption": "Home"})
    return {
        "slug": slug, "group": group, "title": title, "paras": paras, "subheads": heads,
        "features": feats, "links": [{"label": l, "href": h} for l, h in links], "shots": shots,
    }


def news(slug):
    page = get(f"{BASE}/news/view/{slug}").decode("utf-8", "replace")
    m = re.search(r'<div class="(?:NewsContent|news-content|content)[^"]*">(.*?)</div>', page, re.S)
    main = m.group(1) if m else page
    title = text(re.search(r"<h[1-4][^>]*>(.*?)</h[1-4]>", main, re.S).group(1))
    paras = [text(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", main, re.S)]
    return {"slug": slug, "title": title, "paras": [p for p in paras if p][:12]}


def main():
    catalog = {"projects": [], "news": []}
    for group, slugs in GROUPS.items():
        for slug in slugs:
            print(group, slug)
            catalog["projects"].append(project(slug, group))
            time.sleep(0.3)
    for slug in NEWS:
        print("news", slug)
        (OUT / f"news-{slug}.html").write_bytes(get(f"{BASE}/news/view/{slug}"))
        catalog["news"].append(news(slug))
    (OUT / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
