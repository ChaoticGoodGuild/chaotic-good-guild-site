/* The Guild app, on every page: the journal (kept only on this device), the "Keep this in your journal" buttons,
   offline support (the service worker, /sw.js), and the "Bring the Guild home" install help in the footer. */
(function () {
  const W = (() => { try { return JSON.parse(document.getElementById("app-words").textContent); } catch (e) { return null; } })();
  const $ = id => document.getElementById(id);
  const standalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  if (standalone) document.documentElement.classList.add("in-app");

  // ---------- the journal: a list in this browser's storage, newest first. Never sent anywhere.
  const KEY = "cgg.journal";
  const J = window.CGGJournal = {
    all() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } },
    write(list) { localStorage.setItem(KEY, JSON.stringify(list)); },
    add(entry) {
      const list = J.all();
      const e = Object.assign({ note: "" }, entry, { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), at: new Date().toISOString() });
      list.unshift(e); J.write(list); return e.id;
    },
    update(id, patch) { const list = J.all(); const e = list.find(x => x.id === id); if (e) { Object.assign(e, patch); J.write(list); } },
    remove(id) { J.write(J.all().filter(x => x.id !== id)); },
    has(key) { return !!key && J.all().some(x => x.key === key); },
    // ask the browser to treat the journal as worth keeping, so it isn't cleared to save space
    protect() { try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e) {} },
    // merge a backup's entries in; returns how many were new
    restore(entries) {
      const list = J.all(), have = new Set(list.map(x => x.id));
      const fresh = entries.filter(x => x && x.id && x.at && Array.isArray(x.cards) && !have.has(x.id));
      if (fresh.length) J.write(list.concat(fresh).sort((a, b) => (a.at < b.at ? 1 : -1)));
      return fresh.length;
    }
  };

  // ---------- "Keep this in your journal": a page sets window.CGGKeep to its reading and fires "cgg:reading"
  function keptNote(btn, id) {
    const p = document.createElement("span"); p.className = "cj-kept";
    p.append(document.createTextNode(W.keep.kept + " "));
    const a = document.createElement("a"); a.href = "/journal/" + (id ? "#" + id : ""); a.textContent = W.keep.open; p.appendChild(a);
    btn.after(p);
  }
  function syncKeep() {
    document.querySelectorAll("[data-keep]").forEach(btn => {
      const r = window.CGGKeep;
      const old = btn.parentNode.querySelector(".cj-kept, .cj-keepfail"); if (old) old.remove();
      btn.hidden = !r; btn.disabled = false;
      if (r && J.has(r.key)) { btn.hidden = true; keptNote(btn, J.all().find(x => x.key === r.key).id); }
    });
  }
  document.addEventListener("cgg:reading", syncKeep);
  document.addEventListener("click", ev => {
    const btn = ev.target.closest("[data-keep]");
    if (!btn || !window.CGGKeep) return;
    try {
      const id = J.add(JSON.parse(JSON.stringify(window.CGGKeep)));
      btn.hidden = true; keptNote(btn, id);
      J.protect();
    } catch (e) {
      const p = document.createElement("span"); p.className = "cj-keepfail"; p.textContent = W.keep.full; btn.after(p);
    }
  });
  if (W) syncKeep();

  // ---------- offline: register the service worker; inside the installed app, ask it to save the whole village
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
    navigator.serviceWorker.register("/sw.js").then(() => navigator.serviceWorker.ready).then(reg => {
      if (standalone && reg.active) reg.active.postMessage({ type: "save-all" });
    }).catch(() => {});
  }

  // ---------- "Bring the Guild home"
  let deferred = null;
  window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); deferred = e; });
  const box = $("appBox");
  if (!box || !W) return;
  document.querySelectorAll("[data-install]").forEach(a => {
    if (standalone) { if (a.tagName === "A") a.hidden = true; return; }
    a.addEventListener("click", e => { e.preventDefault(); e.stopPropagation(); openBox(); });
    a.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && a.tagName !== "A") { e.preventDefault(); openBox(); } });
  });
  window.CGGInstall = { open: () => openBox() };
  function platform() {
    const ua = navigator.userAgent;
    if (/Instagram|FBAN|FBAV|musical_ly|TikTok|BytedanceWebview|Snapchat|Twitter|LinkedInApp/i.test(ua)) return "inapp";
    if (/iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1)) {
      if (/CriOS|EdgiOS/.test(ua)) return "ios_chrome";
      if (/FxiOS|OPiOS|DuckDuckGo/.test(ua)) return "ios_other";
      return "ios";
    }
    if (/Android/.test(ua)) return "android";
    if (/Firefox\//.test(ua)) return "firefox";
    if (/Macintosh/.test(ua) && /Safari\//.test(ua) && !/Chrome|Chromium|Edg\//.test(ua)) return "mac_safari";
    return "desktop";
  }
  function openBox() {
    const how = $("appHow"), go = $("appGo");
    go.hidden = !deferred;
    how.textContent = deferred ? "" : W.install[platform()];
    how.hidden = !!deferred;
    box.hidden = false; (deferred ? go : $("appClose")).focus();
  }
  const closeBox = () => { box.hidden = true; };
  $("appClose").addEventListener("click", closeBox);
  box.addEventListener("click", e => { if (e.target === box) closeBox(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !box.hidden) closeBox(); });
  $("appGo").addEventListener("click", async () => {
    if (!deferred) return;
    deferred.prompt();
    try { await deferred.userChoice; } catch (e) {}
    deferred = null; $("appGo").hidden = true;
  });
  window.addEventListener("appinstalled", () => {
    deferred = null;
    const how = $("appHow"); how.hidden = false; how.textContent = W.install.done; $("appGo").hidden = true;
  });
})();
