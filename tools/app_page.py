"""The Guild app: the website, installable on phones and computers.

- /today/      Mira's card for today (the app opens here)
- /journal/    readings kept on the visitor's own device, with their notes
- /offline/    shown when a page isn't saved on the device and there's no signal
- /manifest.webmanifest, /assets/icons/*  the app's name, colours, icons and shortcuts
- /sw.js       the service worker: keeps pages working offline. Every visitor gets the essentials saved as they
               browse; inside the installed app it saves the whole village, all 78 cards included.
Words in src/app.json. Behavior in src/app.js (every page), src/today.js, src/journal.js.
"""
import hashlib, json, os
import build as B
import priestess_page

_W = {}


def words():
    if not _W:
        _W.update(json.load(open(os.path.join(B.SRC, "app.json"), encoding="utf-8")))
    return _W


e = lambda s: B.e(s)


def top(back="/", label="The village"):
    return f"""<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="{back}">&larr; {label}</a>
</header>
"""


def tabs(here):
    """The installed app's own tab bar: just the daily card and the journal, plus a way out to the website."""
    cur = lambda k: ' aria-current="page"' if k == here else ""
    return f"""<nav class="app-tabs" aria-label="The Guild app">
  <a href="/today/"{cur("today")}><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="3" width="12" height="18" rx="2"/><path d="M12 8l1.2 2.6 2.8.3-2.1 1.9.6 2.8L12 14.2 9.5 15.6l.6-2.8L8 10.9l2.8-.3z"/></svg>Today</a>
  <a href="/journal/"{cur("journal")}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/></svg>Journal</a>
  <a href="https://www.chaoticgoodguild.com/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/></svg>The Guild</a>
</nav>"""


def build_pages(cards, back, defs):
    W = words()
    T = W["today"]
    PR = json.load(open(os.path.join(B.SRC, "priestess.json"), encoding="utf-8"))
    SP = json.load(open(os.path.join(B.SRC, "spread.json"), encoding="utf-8"))
    pos = {p["key"]: {"title": p["title"], "question": p["question"]} for p in PR["positions"]}
    data = json.dumps({"cards": cards, "words": T, "moon": W["moonday"], "secret": PR["secret"], "reflection": PR["reflection"],
                       "suits": SP["suits"], "priestess": {"dark": pos["dark"], "light": pos["light"], "secret": pos["secret"]}})
    mcard = lambda k, cls="": (f'<div class="td-mslot"><button type="button" class="td-mcard{cls}" aria-label="Face down">'
                               f'<span class="sp-inner"><span class="sp-face sp-back">{back}</span><span class="sp-face sp-front"></span></span></button>'
                               f'<p class="td-mlabel"><b></b><span></span></p></div>')
    page = B.head(f"{T['title']} · {B.NAME}", T["desc"], "/today/", "tarot")
    page += f"""<div class="hp-sky" id="tdSky" aria-hidden="true" hidden><div class="hp-flies">{priestess_page.fireflies(18)}</div></div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
{top()}
<main class="td">
  <section class="sp-intro">
    <p class="who"><span id="tdWho">{e(T['who'])}</span> · <span id="tdDate"></span></p>
    <h1 id="tdTitle">{e(T['title'])}</h1>
    <p class="desc" id="tdDesc">{e(T['desc'])}</p>
  </section>
  <p class="sp-prompt" id="tdPrompt" aria-live="polite">{e(T['idle'])}</p>
  <div class="td-moon" id="tdMoon" hidden>{mcard(0)}{mcard(1, " td-secret")}{mcard(2)}</div>
  <section class="td-moontext" aria-live="polite"><div id="tdMoonText" hidden></div>
    <p class="cj-keeprow" id="tdMoonKeep" hidden><button type="button" class="back-btn" data-keep hidden>{e(W['keep']['button'])}</button></p></section>
  <div class="td-table" id="tdTable">
    <button type="button" class="td-deck" id="tdDeck" aria-label="The deck. Touch to draw today's card.">
      {''.join(f'<span class="sp-stackcard" style="--i:{i}">{back}</span>' for i in range(6))}
    </button>
    <div class="td-card" id="tdCard" hidden><div class="sp-face sp-front" id="tdFront"></div></div>
  </div>
  <section class="td-text" id="tdText" hidden aria-live="polite">
    <h2 class="td-name" id="tdName"></h2>
    <p class="sp-rev" id="tdRev" hidden>Reversed</p>
    <div id="tdKw"></div>
    <p class="td-meaning" id="tdMeaning"></p>
    <p class="sp-revnote" id="tdRevNote" hidden></p>
    <p class="sp-counsel"><b>Reflect: </b><span id="tdAsk"></span></p>
    <p class="cj-keeprow"><button type="button" class="back-btn" data-keep hidden>{e(W['keep']['button'])}</button></p>
  </section>
  <nav class="td-more" aria-label="More from the Guild">
    <a class="back-btn" href="/tarot/">Ask Mira for a full reading</a>
    <a class="sp-ghost" href="/journal/">Your journal</a>
    <a class="sp-ghost" href="/calendar/">Tonight's sky</a>
  </nav>
  {priestess_page.rite()}
</main>
{tabs("today")}
{B.foot()}<script type="application/json" id="today-data">{data}</script>
<script src="/assets/sky.js"></script>
<script src="/assets/moonwindow.js"></script>
<script src="/assets/priestess-read.js"></script>
<script src="/assets/today.js"></script>
</body>
</html>
"""
    B.write("today/index.html", page)

    J = W["journal"]
    page = B.head(f"{J['title']} · {B.NAME}", J["desc"], "/journal/", "tarot", '<meta name="robots" content="noindex">\n')
    page += f"""{top()}
<main class="jn">
  <section class="sp-intro">
    <p class="who">{e(J['who'])}</p>
    <h1>{e(J['title'])}</h1>
    <p class="desc">{e(J['desc'])}</p>
  </section>
  <p class="jn-empty" id="jnEmpty" hidden>{e(J['empty'])}<br><a class="back-btn" href="/today/">Today's card</a> <a class="sp-ghost" href="/tarot/">Ask Mira for a reading</a></p>
  <div class="jn-tools" id="jnTools" hidden><p id="jnCount"></p><button type="button" class="sp-ghost" id="jnDownload">{e(J['download'])}</button></div>
  <div class="jn-list" id="jnList"></div>
  <section class="jn-safe">
    <p class="jn-fine">{e(J['fine'])}</p>
    <p class="jn-backup"><button type="button" class="back-btn" id="jnBackup">{e(J['backup'])}</button>
      <label class="sp-ghost jn-restore">{e(J['restore'])}<input type="file" id="jnRestore" accept=".json,application/json"></label></p>
    <p class="jn-msg" id="jnMsg" role="status"></p>
  </section>
</main>
{tabs("journal")}

{B.foot()}<script type="application/json" id="journal-data">{json.dumps(J)}</script>
<script src="/assets/journal.js"></script>
</body>
</html>
"""
    B.write("journal/index.html", page)

    O = W["offline"]
    page = B.head(f"{O['title']} · {B.NAME}", O["text"], "/offline/", "tarot", '<meta name="robots" content="noindex">\n')
    page += f"""{top()}
<main class="jn">
  <section class="sp-intro"><h1>{e(O['title'])}</h1><p class="desc">{e(O['text'])}</p></section>
  <p class="td-more"><a class="back-btn" href="/today/">Today's card</a> <a class="sp-ghost" href="/journal/">Your journal</a></p>
</main>
{tabs("")}
{B.foot()}</body>
</html>
"""
    B.write("offline/index.html", page)
    for f in ("today.js", "journal.js"):
        B.write("assets/" + f, open(os.path.join(B.SRC, f)).read())


def foot_bits():
    """The install help and the app words, appended to every page's footer."""
    W = words()
    I = W["install"]
    payload = json.dumps({"keep": W["keep"], "install": I})
    return f"""<div class="sp-light app-box" id="appBox" role="dialog" aria-modal="true" aria-labelledby="appTitle" hidden>
  <div class="app-card">
    <img src="/assets/icons/icon-192.png" alt="" width="96" height="96">
    <h2 id="appTitle">{e(I['title'])}</h2>
    <p>{e(I['lede'])}</p>
    <p class="app-how" id="appHow"></p>
    <p class="app-go"><button type="button" class="back-btn" id="appGo" hidden>{e(I['button'])}</button>
      <button type="button" class="sp-ghost" id="appClose">{e(I['close'])}</button></p>
  </div>
</div>
<script type="application/json" id="app-words">{payload}</script>
<script src="/assets/app.js"></script>
"""


def build_app():
    """Manifest, icons and the service worker. Runs last, once every page is built."""
    W = words()
    os.makedirs(os.path.join(B.SITE, "assets", "icons"), exist_ok=True)
    for f in os.listdir(os.path.join(B.SRC, "icons")):
        if f.endswith(".png"):
            with open(os.path.join(B.SRC, "icons", f), "rb") as fi, open(os.path.join(B.SITE, "assets", "icons", f), "wb") as fo:
                fo.write(fi.read())
    B.write("assets/app.js", open(os.path.join(B.SRC, "app.js")).read())
    def icon(n, purpose):
        s = n.rsplit("-", 1)[1][:-4]
        return {"src": f"/assets/icons/{n}", "sizes": f"{s}x{s}", "type": "image/png", "purpose": purpose}
    manifest = {
        "id": "/", "name": W["name"], "short_name": W["short_name"], "description": W["app_description"],
        "start_url": "/today/", "scope": "/", "display": "standalone", "orientation": "any",
        "background_color": "#0d0418", "theme_color": "#0d0418", "categories": ["lifestyle", "entertainment"],
        "icons": [icon("icon-192.png", "any"), icon("icon-512.png", "any"), icon("maskable-192.png", "maskable"), icon("maskable-512.png", "maskable")],
        "shortcuts": [
            {"name": "Draw today's card", "short_name": "Today's card", "url": "/today/", "icons": [{"src": "/assets/icons/icon-96.png", "sizes": "96x96"}]},
            {"name": "Your journal", "short_name": "Journal", "url": "/journal/", "icons": [{"src": "/assets/icons/icon-96.png", "sizes": "96x96"}]},
        ],
    }
    B.write("manifest.webmanifest", json.dumps(manifest, indent=2))

    # what to keep on the device
    pages, cards, other, h = [], [], [], hashlib.sha256()
    for root, _, files in os.walk(B.SITE):
        for f in sorted(files):
            full = os.path.join(root, f)
            rel = "/" + os.path.relpath(full, B.SITE).replace(os.sep, "/")
            if rel in ("/sw.js",):
                continue
            with open(full, "rb") as fh:
                h.update(rel.encode()); h.update(fh.read())
            if rel.startswith("/tarot/cards/"):
                cards.append(rel)
    version = h.hexdigest()[:12]
    pages = ["/today/", "/journal/", "/offline/"]
    other = ["/assets/sky.js", "/assets/moonwindow.js", "/assets/priestess-read.js", "/assets/forest-night.webp",
             "/assets/icons/icon-512.png", "/assets/icons/maskable-192.png"]
    core = ["/today/", "/journal/", "/offline/", "/assets/site.css", "/assets/app.js", "/assets/join.js", "/assets/today.js",
            "/assets/journal.js", "/assets/logo.png", "/assets/star.png", "/assets/icons/icon-192.png", "/manifest.webmanifest"]
    sw = SW.replace("__VERSION__", version).replace("__CORE__", json.dumps(core)) \
           .replace("__PAGES__", json.dumps(sorted(pages))).replace("__CARDS__", json.dumps(sorted(cards))) \
           .replace("__OTHER__", json.dumps(sorted(other)))
    B.write("sw.js", sw)
    return version


SW = r"""/* The Guild's service worker: keeps the village working without a connection. Built by tools/app_page.py. */
const VERSION = "__VERSION__";
const CORE = __CORE__;                 // saved for every visitor: the app's own pages and the essentials
const PAGES = __PAGES__, CARDS = __CARDS__, OTHER = __OTHER__;   // saved inside the installed app ("save-all"): its two pages and all 78 cards
const STATIC = "cgg-static-" + VERSION, HTML = "cgg-pages-" + VERSION, CARDBOX = "cgg-cards", FONTS = "cgg-fonts";

self.addEventListener("install", ev => {
  ev.waitUntil(caches.open(STATIC).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", ev => {
  const keep = [STATIC, HTML, CARDBOX, FONTS];
  ev.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("cgg-") && !keep.includes(k)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// inside the installed app: save the whole village once per version, the cards once ever
let saving = null;
self.addEventListener("message", ev => {
  if (!ev.data || ev.data.type !== "save-all" || saving) return;
  saving = (async () => {
    const done = await caches.open(STATIC).then(c => c.match("/__saved-all"));
    if (done) return;
    const fill = async (box, urls) => {
      const c = await caches.open(box);
      for (const u of urls) { try { if (!(await c.match(u))) { const r = await fetch(u); if (r.ok) await c.put(u, r); } } catch (e) {} }
    };
    await fill(HTML, PAGES); await fill(STATIC, OTHER); await fill(CARDBOX, CARDS);
    await caches.open(STATIC).then(c => c.put("/__saved-all", new Response("1")));
  })().finally(() => { saving = null; });
  ev.waitUntil(saving);
});

self.addEventListener("fetch", ev => {
  const req = ev.request, url = new URL(req.url);
  if (req.method !== "GET") return;
  if (url.origin === location.origin) {
    if (url.pathname.startsWith("/.netlify/")) return;
    if (req.mode === "navigate") return ev.respondWith(page(req, url));
    if (url.pathname.startsWith("/tarot/cards/")) return ev.respondWith(cacheFirst(req, CARDBOX));
    return ev.respondWith(networkFirst(req, STATIC));
  }
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") return ev.respondWith(fresh(req, FONTS));
});

// pages: the newest from the network; the saved copy when offline
async function page(req, url) {
  const c = await caches.open(HTML);
  try {
    const r = await fetch(req);
    if (r.ok && r.type === "basic") c.put(url.pathname, r.clone());
    return r;
  } catch (e) {
    return (await c.match(url.pathname)) || (await caches.match(url.pathname)) || (await caches.match("/offline/")) || Response.error();
  }
}
async function cacheFirst(req, box) {
  const c = await caches.open(box), hit = await c.match(req);
  if (hit) return hit;
  const r = await fetch(req); if (r.ok) c.put(req, r.clone()); return r;
}
// the site's own styles, scripts and pictures: the newest from the network (so an update shows at once); the saved copy offline
async function networkFirst(req, box) {
  const c = await caches.open(box);
  try {
    const r = await fetch(req);
    if (r.ok) c.put(req, r.clone());
    return r;
  } catch (e) {
    return (await c.match(req, { ignoreSearch: true })) || Response.error();
  }
}
// fonts from Google: the saved copy at once, refreshed in the background
async function fresh(req, box) {
  const c = await caches.open(box), hit = await c.match(req, { ignoreSearch: box === STATIC });
  const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => null);
  return hit || (await net) || Response.error();
}
"""
