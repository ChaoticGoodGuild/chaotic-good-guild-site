/* The Guild's service worker: keeps the village working without a connection. Built by tools/app_page.py. */
const VERSION = "cf3b3f49ddfc";
const CORE = ["/today/", "/journal/", "/offline/", "/assets/site.css", "/assets/app.js", "/assets/join.js", "/assets/today.js", "/assets/journal.js", "/assets/logo.png", "/assets/star.png", "/assets/icons/icon-192.png", "/manifest.webmanifest"];                 // saved for every visitor: the app's own pages and the essentials
const PAGES = ["/", "/about/", "/alignment-test/", "/alignment-test/chaotic-evil/", "/alignment-test/chaotic-good/", "/alignment-test/chaotic-neutral/", "/alignment-test/lawful-evil/", "/alignment-test/lawful-good/", "/alignment-test/lawful-neutral/", "/alignment-test/neutral-evil/", "/alignment-test/neutral-good/", "/alignment-test/true-neutral/", "/calendar/", "/guild-hall/", "/join/", "/join/thanks/", "/journal/", "/market/", "/notice-board/", "/offline/", "/privacy/", "/stories/", "/tarot/", "/tarot/priestess/", "/today/"], CARDS = ["/tarot/cards/galleons-01.svg", "/tarot/cards/galleons-02.svg", "/tarot/cards/galleons-03.svg", "/tarot/cards/galleons-04.svg", "/tarot/cards/galleons-05.svg", "/tarot/cards/galleons-06.svg", "/tarot/cards/galleons-07.svg", "/tarot/cards/galleons-08.svg", "/tarot/cards/galleons-09.svg", "/tarot/cards/galleons-10.svg", "/tarot/cards/galleons-11.svg", "/tarot/cards/galleons-12.svg", "/tarot/cards/galleons-13.svg", "/tarot/cards/galleons-14.svg", "/tarot/cards/lutes-01.svg", "/tarot/cards/lutes-02.svg", "/tarot/cards/lutes-03.svg", "/tarot/cards/lutes-04.svg", "/tarot/cards/lutes-05.svg", "/tarot/cards/lutes-06.svg", "/tarot/cards/lutes-07.svg", "/tarot/cards/lutes-08.svg", "/tarot/cards/lutes-09.svg", "/tarot/cards/lutes-10.svg", "/tarot/cards/lutes-11.svg", "/tarot/cards/lutes-12.svg", "/tarot/cards/lutes-13.svg", "/tarot/cards/lutes-14.svg", "/tarot/cards/major-00.svg", "/tarot/cards/major-01.svg", "/tarot/cards/major-02.svg", "/tarot/cards/major-03.svg", "/tarot/cards/major-04.svg", "/tarot/cards/major-05.svg", "/tarot/cards/major-06.svg", "/tarot/cards/major-07.svg", "/tarot/cards/major-08.svg", "/tarot/cards/major-09.svg", "/tarot/cards/major-10.svg", "/tarot/cards/major-11.svg", "/tarot/cards/major-12.svg", "/tarot/cards/major-13.svg", "/tarot/cards/major-14.svg", "/tarot/cards/major-15.svg", "/tarot/cards/major-16.svg", "/tarot/cards/major-17.svg", "/tarot/cards/major-18.svg", "/tarot/cards/major-19.svg", "/tarot/cards/major-20.svg", "/tarot/cards/major-21.svg", "/tarot/cards/mirrors-01.svg", "/tarot/cards/mirrors-02.svg", "/tarot/cards/mirrors-03.svg", "/tarot/cards/mirrors-04.svg", "/tarot/cards/mirrors-05.svg", "/tarot/cards/mirrors-06.svg", "/tarot/cards/mirrors-07.svg", "/tarot/cards/mirrors-08.svg", "/tarot/cards/mirrors-09.svg", "/tarot/cards/mirrors-10.svg", "/tarot/cards/mirrors-11.svg", "/tarot/cards/mirrors-12.svg", "/tarot/cards/mirrors-13.svg", "/tarot/cards/mirrors-14.svg", "/tarot/cards/quills-01.svg", "/tarot/cards/quills-02.svg", "/tarot/cards/quills-03.svg", "/tarot/cards/quills-04.svg", "/tarot/cards/quills-05.svg", "/tarot/cards/quills-06.svg", "/tarot/cards/quills-07.svg", "/tarot/cards/quills-08.svg", "/tarot/cards/quills-09.svg", "/tarot/cards/quills-10.svg", "/tarot/cards/quills-11.svg", "/tarot/cards/quills-12.svg", "/tarot/cards/quills-13.svg", "/tarot/cards/quills-14.svg"], OTHER = ["/assets/alignment.js", "/assets/app.js", "/assets/calendar.js", "/assets/forest-night.webp", "/assets/forestsound.js", "/assets/icons/apple-touch-icon.png", "/assets/icons/icon-192.png", "/assets/icons/icon-512.png", "/assets/icons/icon-96.png", "/assets/icons/maskable-192.png", "/assets/icons/maskable-512.png", "/assets/join.js", "/assets/journal.js", "/assets/logo.png", "/assets/moonwindow.js", "/assets/priestess.js", "/assets/site.css", "/assets/sky.js", "/assets/spread.js", "/assets/star.png", "/assets/stump.js", "/assets/today.js", "/assets/village.svg"];   // saved inside the installed app ("save-all")
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
    return ev.respondWith(fresh(req, STATIC));
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
// everything else: the saved copy at once, refreshed in the background
async function fresh(req, box) {
  const c = await caches.open(box), hit = await c.match(req, { ignoreSearch: box === STATIC });
  const net = fetch(req).then(r => { if (r.ok || r.type === "opaque") c.put(req, r.clone()); return r; }).catch(() => null);
  return hit || (await net) || Response.error();
}
