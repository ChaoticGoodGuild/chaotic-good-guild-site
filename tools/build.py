"""Builds the Chaotic Good Guild website into the site/ folder.

Run from anywhere:  python3 tools/build.py

Where things live:
  src/places.json   every room: its address, title, popup text, scene marker and crop
  src/site.css      shared styles for every page
  src/logo.b64      the Guild logo (PNG, base64)
  src/star.b64      the Guild star from the logo (PNG, base64), used for the favicon and the sky
  tools/scene.py    the village artwork

site/ is generated. Don't edit it by hand: change src/ or tools/, then run this script.
"""
import base64, datetime, html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import scene  # noqa: E402

SITE = os.path.join(ROOT, "site")
SRC = os.path.join(ROOT, "src")
DOMAIN = "https://www.chaoticgoodguild.com"
NAME = "Chaotic Good Guild"
HOME_DESC = ("The Chaotic Good Guild: a village for dreamers, misfits and kind rebels. "
             "Tarot readings, the Guild calendar, fables, community and more.")
RAISING = "The Bull is still raising the beams of this room. Return when the lanterns are lit."

PLACES = json.load(open(os.path.join(SRC, "places.json")))
e = html.escape


def write(rel, text, binary=False):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w") as f:
        f.write(text)


def head(title, desc, path, image, extra=""):
    url = DOMAIN + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/assets/star.png">
<link rel="apple-touch-icon" href="/assets/star.png">
<meta name="theme-color" content="#0d0418">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/share/{image}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Alegreya:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
<body>
"""


def foot():
    links = "".join(f'<li><a href="/{p["slug"]}/">{e(p["title"])}</a></li>' for p in PLACES)
    return f"""<footer>
  <a href="/" aria-label="{NAME} home"><img class="foot-logo" src="/assets/logo.png" alt="{NAME}" width="345" height="360" loading="lazy"></a>
  <nav aria-label="Rooms of the village"><ul class="foot-nav">{links}</ul></nav>
  &copy; {datetime.date.today().year} {NAME}. Made by misfits, for misfits.
</footer>
"""


def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>\n'


def directory(exclude=None):
    items = []
    for p in PLACES:
        if p["slug"] == exclude:
            continue
        items.append(f'<li><a href="/{p["slug"]}/"><span class="t">{e(p["title"])}</span>'
                     f'<span class="w">{e(p["who"])}</span><span class="d">{e(p["desc"])}</span></a></li>')
    return '<ul class="places">' + "".join(items) + "</ul>"


HOME_JS = r"""
const PLACES = __PLACES__;
const byKey = Object.fromEntries(PLACES.map(p => [p.key, p]));
// Old links like /#tarot go to the room's own page now
(function () { const h = location.hash.slice(1); const p = PLACES.find(x => x.key === h || x.slug === h); if (p) location.replace("/" + p.slug + "/"); })();

const wrap = document.getElementById("sceneWrap");
const tip = document.getElementById("tip");
const touchMode = window.matchMedia("(hover: none)").matches;
let active = null;

function go(p) { location.href = "/" + p.slug + "/"; }
function showTip(spot) {
  const p = byKey[spot.dataset.key];
  tip.innerHTML = "";
  const h = document.createElement("h3"); h.textContent = p.title;
  const w = document.createElement("div"); w.className = "who"; w.textContent = p.who;
  const d = document.createElement("p"); d.textContent = p.desc;
  const c = document.createElement(touchMode ? "a" : "span"); c.className = "cta";
  c.textContent = "Step inside →";
  if (touchMode) c.href = "/" + p.slug + "/";
  tip.append(h, w, d, c);
  tip.classList.toggle("touch", touchMode);
  const hit = spot.querySelector(".hit").getBoundingClientRect();
  const box = wrap.getBoundingClientRect();
  const tw = tip.offsetWidth, th = tip.offsetHeight;
  let x = hit.left - box.left + hit.width / 2 - tw / 2;
  x = Math.max(8, Math.min(x, box.width - tw - 8));
  let y = hit.top - box.top - th - 10;
  if (y < 8) y = hit.bottom - box.top + 10;
  if (y + th > box.height - 8) y = Math.max(8, box.height - th - 8);
  tip.style.left = x + "px"; tip.style.top = y + "px";
  tip.classList.add("show"); tip.setAttribute("aria-hidden", "false");
  document.querySelectorAll(".spot.active").forEach(s => s.classList.remove("active"));
  spot.classList.add("active"); active = spot;
}
function hideTip() {
  tip.classList.remove("show"); tip.setAttribute("aria-hidden", "true");
  if (active) active.classList.remove("active");
  active = null;
}
document.querySelectorAll(".spot").forEach(spot => {
  const p = byKey[spot.dataset.key];
  spot.setAttribute("aria-label", p.title + ": " + p.who);
  spot.addEventListener("mouseenter", () => { if (!touchMode) showTip(spot); });
  spot.addEventListener("mouseleave", () => { if (!touchMode) hideTip(); });
  spot.addEventListener("focus", () => showTip(spot));
  spot.addEventListener("blur", () => { if (!touchMode) hideTip(); });
  spot.addEventListener("click", ev => {
    ev.stopPropagation();
    if (touchMode && active !== spot) { showTip(spot); return; }
    go(p);
  });
  spot.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); go(p); } });
});
tip.addEventListener("click", ev => ev.stopPropagation());
document.addEventListener("click", () => { if (touchMode) hideTip(); });
document.addEventListener("keydown", ev => { if (ev.key === "Escape") hideTip(); });
window.addEventListener("resize", hideTip);
"""

HOME_CSS = """<style>
#tip .cta { text-decoration: none; }
</style>
"""


def build_home():
    svg = scene.make_svg(PLACES)
    data = json.dumps([{k: p[k] for k in ("key", "slug", "title", "who", "desc")} for p in PLACES])
    ld = jsonld({"@context": "https://schema.org", "@type": "Organization", "name": NAME,
                 "url": DOMAIN + "/", "logo": DOMAIN + "/assets/logo.png",
                 "description": HOME_DESC})
    page = head(NAME, HOME_DESC, "/", "home", HOME_CSS + ld)
    page += f"""
<header class="top">
  <a class="brand" href="/" aria-label="{NAME} home"><img src="/assets/logo.png" alt="{NAME}" width="345" height="360"></a>
  <a class="join-btn" href="/guild-hall/">Enter the Hall</a>
</header>

<div class="scene-wrap" id="sceneWrap">
{svg}
<div id="tip" role="tooltip" aria-hidden="true"></div>
</div>

<main>
  <section class="intro">
    <div>
      <h1>Kindness calls. <em>Chaos clears.</em></h1>
      <p class="how">Wander the village. Linger over a friend to hear their whisper, then step through.</p>
    </div>
    <blockquote class="mission">
      <p>We're here for the dreamers, the misfits, and the rebels who want to make the world a better place, not by following the rules, but by rewriting them.</p>
      <p>Whether you're an artist, a wanderer, or a warrior for change, your spark of creativity matters. Join us in the chaos, and let's make a difference together, one story and one revolution at a time.</p>
      <cite>The Guild's creed</cite>
    </blockquote>
  </section>

  <h2 class="places-h">Paths through the village</h2>
  {directory()}
</main>

{foot()}
<script>{HOME_JS.replace("__PLACES__", data)}</script>
</body>
</html>
"""
    write("index.html", page)


LANTERN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v3" stroke="#e9d701" stroke-width="2"/>'
           '<path d="M8 7h8l1 12H7z" fill="#e9d701" opacity=".9"/><path d="M6 7h12l-6-3z" fill="#b9a8d6"/>'
           '<path d="M7 19h10v2H7z" fill="#b9a8d6"/></svg>')


def build_room(p):
    path = f"/{p['slug']}/"
    title = f"{p['title']} · {NAME}"
    w, h = p["view"][2], p["view"][3]
    ld = jsonld({"@context": "https://schema.org", "@type": "WebPage", "name": p["title"],
                 "description": p["desc"], "url": DOMAIN + path,
                 "isPartOf": {"@type": "WebSite", "name": NAME, "url": DOMAIN + "/"}})
    page = head(title, p["desc"], path, p["slug"], ld)
    page += f"""
<header class="top">
  <a class="brand" href="/" aria-label="{NAME} home"><img src="/assets/logo.png" alt="{NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>

<main>
  <section class="room-hero">
    <figure class="vignette">
      <img src="/assets/village.svg#v-{p['slug']}" alt="{e(p['who'])}" width="{w}" height="{h}">
    </figure>
    <div>
      <p class="who">{e(p['who'])}</p>
      <h1>{e(p['title'])}</h1>
      <p class="desc">{e(p['desc'])}</p>
      <p class="raising">{LANTERN}<span>{e(RAISING)}</span></p>
      <a class="back-btn" href="/">&larr; Back to the village</a>
    </div>
  </section>

  <h2 class="places-h" style="margin-top:0">Other paths</h2>
  {directory(exclude=p['slug'])}
</main>

{foot()}</body>
</html>
"""
    write(f"{p['slug']}/index.html", page)


def build_404():
    page = head(f"Off the path · {NAME}", "This path leads nowhere. Head back to the village.", "/404", "home",
                '<meta name="robots" content="noindex">\n')
    page += f"""
<header class="top">
  <a class="brand" href="/" aria-label="{NAME} home"><img src="/assets/logo.png" alt="{NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>
<main class="lost">
  <h1>Off the path</h1>
  <p>The lanterns don't reach this far. Whatever was here has wandered off, or was never here at all.</p>
  <a class="back-btn" href="/">&larr; Back to the village</a>
</main>
{foot()}</body>
</html>
"""
    write("404.html", page)


def build_meta():
    today = datetime.date.today().isoformat()
    urls = ["/"] + [f"/{p['slug']}/" for p in PLACES]
    sm = "".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    rooms = "\n".join(f"- [{p['title']}]({DOMAIN}/{p['slug']}/): {p['desc']}" for p in PLACES)
    write("llms.txt", f"# {NAME}\n\n> {HOME_DESC}\n\n"
          "The Chaotic Good Guild is a creative universe about living Chaotic Good: kind, free-spirited "
          "and playfully rebellious, in contrast to the Lawful Evil Overlords (LEOs). Its characters include "
          "Reynard the fox, Mira the witchy cat, the Badger, the Bull, the rats of the Guild, the LEO Lion "
          "and the Corporate Wolf.\n\n## Rooms\n\n" + rooms + "\n")


def build_assets():
    write("assets/site.css", open(os.path.join(SRC, "site.css")).read())
    write("assets/logo.png", base64.b64decode(open(os.path.join(SRC, "logo.b64")).read()), binary=True)
    write("assets/star.png", base64.b64decode(open(os.path.join(SRC, "star.b64")).read()), binary=True)
    write("assets/village.svg", scene.make_svg(PLACES, standalone=True))
    # share images are rendered separately by tools/share_images.py and kept between builds


def main():
    share = os.path.join(SITE, "assets", "share")
    keep = None
    if os.path.isdir(share):
        keep = os.path.join(ROOT, ".share-tmp")
        shutil.rmtree(keep, ignore_errors=True)
        shutil.copytree(share, keep)
    shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(SITE)
    if keep:
        shutil.copytree(keep, share)
        shutil.rmtree(keep)
    build_assets()
    build_home()
    for p in PLACES:
        build_room(p)
    build_404()
    build_meta()
    print("Built", len(PLACES) + 2, "pages into", SITE)


if __name__ == "__main__":
    main()
