/* The Chaotic Good Spread: shuffle, stop, deal six cards into the Guild star, turn them over, read them.
   Everything happens in the visitor's browser; nothing is sent or stored. */

// ---------- The reading engine (pure functions, tested by tools/test_spread.js) ----------
// picks[k] is the card in positions[k]. Cards carry: id, name, suit, rank, keywords, meaning, question, tone,
// and reversed (true when it landed upside down: Mira reads that as too much of its energy, or not enough).
const CGGRead = {
  list(names) {
    if (names.length < 2) return names.join("");
    return names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
  },
  summarize(picks, positions, D) {
    const at = key => picks[positions.findIndex(p => p.key === key)];
    const heart = at("heart"), star = at("star");
    const paras = [], notes = [];
    const majors = picks.filter(c => c.suit === "major");
    const minors = picks.filter(c => c.suit !== "major");
    const courts = minors.filter(c => c.rank > 10);
    const kw = c => c.keywords;

    // 1. The heart anchors the reading
    paras.push(heart.reversed
      ? `At the heart of this reading sits ${heart.name}, reversed: ${CGGRead.list(kw(heart))}, out of balance. There may be too much of this in your life right now, or not enough. This is where you're standing, and every other card bends around it.`
      : `At the heart of this reading sits ${heart.name}: ${CGGRead.list(kw(heart))}. This is where you're standing, and every other card bends around it.`);
    notes.push("The Heart sits in the centre of the star, so Mira reads it first. Every other card is read in relation to it.");

    // 2. The five points
    // Read the points in the order they were dealt.
    const pts = positions.filter(p => p.key !== "heart").map(p => {
      const c = picks[positions.indexOf(p)];
      const q = p.question.replace(/[.?!]$/, "");
      return `${q.charAt(0).toLowerCase() + q.slice(1)} is ${c.name} (${kw(c)[0]}${c.reversed ? ", reversed" : ""})`;
    });
    paras.push(`Around it, the points of the star: ${pts.join("; ")}.`);

    // 3. Patterns
    const pat = [];
    if (majors.length === 0) {
      pat.push("No Major Arcana fell, so this reading lives in everyday choices. The day-to-day is yours to shape.");
      notes.push("No Major Arcana: the 22 Major Arcana are the deck's big life lessons. When none appear, the reading is about ordinary, changeable things.");
    } else if (majors.length <= 2) {
      pat.push(`${CGGRead.list(majors.map(c => c.name))} ${majors.length === 1 ? "marks" : "mark"} a bigger current running underneath the everyday.`);
      notes.push("Major Arcana are the deck's big life lessons. A card or two of them points to a deeper theme beneath the everyday ones.");
    } else {
      pat.push(`With ${majors.length} Major Arcana on the table, this is a season of big lessons. Some of this is larger than any one choice, so be patient with yourself.`);
      notes.push("Three or more Major Arcana means big forces are at work: life lessons more than daily decisions.");
    }

    const counts = {};
    minors.forEach(c => { counts[c.suit] = (counts[c.suit] || 0) + 1; });
    const ranked = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    if (ranked.length && ranked[0][1] >= 2 && (ranked.length === 1 || ranked[0][1] > ranked[1][1])) {
      const s = D.suits[ranked[0][0]];
      pat.push(`${ranked[0][1] === 2 ? "Two" : ranked[0][1] === 3 ? "Three" : "Several"} ${s.name} appear, so ${s.theme} color the whole reading.`);
      notes.push(`When a suit repeats, its element colors the reading. ${s.name} are ${s.element}: ${s.theme}.`);
    }
    if (minors.length >= 4) {
      const missing = Object.keys(D.suits).filter(k => !counts[k]);
      if (missing.length === 1) {
        pat.push(D.suits[missing[0]].absent);
        notes.push("A missing suit can say as much as a present one: notice what isn't on the table.");
      }
    }

    const home = positions.map((p, k) => [p, picks[k]]).filter(([p, c]) => p.suit !== "major" && p.suit === c.suit);
    if (home.length === 4) pat.push("Every suit found its own point of the star: a rare, balanced reading, with each message coming through doubly strong.");
    else if (home.length > 1) pat.push(`${CGGRead.list(home.map(([, c]) => c.name))} each landed on their own suit's point, so their messages come through doubly strong.`);
    else if (home.length === 1) pat.push(`${home[0][1].name} landed on its own point, ${home[0][0].title}, so its message comes through doubly strong.`);
    if (home.length) notes.push("Each point of the star belongs to a suit (the Lute to fire, the Quill to air, the Mirror to water, the Galleon to earth). A card that lands on its own suit's point speaks louder.");

    if (courts.length >= 2) {
      pat.push(`${CGGRead.list(courts.map(c => c.name))} bring the rats of the Guild into it. Other people have a hand in this, or skills you're still growing.`);
      notes.push("Court cards (Neophyte, Apprentice, Journeyman, Master) often stand for people in your life, or for a stage of learning you're in.");
    } else if (courts.length === 1) {
      pat.push(`${courts[0].name} may be a person in your life, or the part of you still learning this lesson.`);
      notes.push("A single court card often points to one person, or to the stage of learning you're in.");
    }

    const byRank = {};
    minors.filter(c => c.rank <= 10).forEach(c => { (byRank[c.rank] = byRank[c.rank] || []).push(c); });
    Object.entries(byRank).filter(([, cs]) => cs.length >= 2).forEach(([r, cs]) => {
      const [plural, theme] = D.numbers[r];
      pat.push(`${cs.length === 2 ? "Two" : "Several"} ${plural} (${CGGRead.list(cs.map(c => c.name))}) echo each other: ${theme}.`);
      notes.push(`Matching numbers echo. ${plural} speak of ${theme}.`);
    });

    const rev = picks.filter(c => c.reversed);
    const revPts = rev.filter(c => c !== heart);   // the Heart already spoke for itself
    if (rev.length >= 4) {
      pat.push(`${rev.length === 6 ? "Every card" : "Most of the star"} came reversed, so this reading is about balance: where something has grown too loud, and where something is missing.`);
    } else if (revPts.length) {
      pat.push(revPts.length === 1
        ? `${revPts[0].name} came reversed. Is there too much of its energy in your life right now, or not enough?`
        : `${CGGRead.list(revPts.map(c => c.name))} came reversed. For each, ask: is there too much of its energy in your life right now, or not enough?`);
    }
    if (rev.length) notes.push(D.reversed + " Only you can tell which.");

    const shadow = picks.filter(c => c.tone === "shadow").length;
    const light = picks.filter(c => c.tone === "light" && !c.reversed).length;
    if (shadow >= 3) {
      pat.push("The LEOs cast a long shadow over this spread. Name what's weighing on you before you try to fight it.");
      notes.push("Several heavy cards together show a hard season. That's information, not a sentence.");
    } else if (light >= 5) {
      pat.push("It's a bright star: the cards lean toward hope, warmth and things going right.");
      notes.push("When nearly every card is a bright one, the reading leans hopeful. Enjoy it, and act on it.");
    }
    if (pat.length) paras.push(pat.join(" "));

    // 4. Questions to carry, then the mirror
    const ask = c => c.question + (c.reversed ? ` And since it came reversed: is there too much of the energy of ${c.name} right now, or not enough?` : "");
    paras.push(`Questions to carry, from the Heart: ${ask(heart)} And from the Star above it: ${ask(star)}`);
    notes.push("Mira closes with questions, not answers. She takes them from the Heart and the Star; the answers are yours.");
    paras.push(D.reflection);
    return { paras, notes };
  }
};
if (typeof module !== "undefined") module.exports = CGGRead;

(function () {
  if (typeof document === "undefined") return;
  const D = JSON.parse(document.getElementById("spread-data").textContent);
  const $ = id => document.getElementById(id);
  const stage = $("spStage"), deck = $("spDeck"), prompt = $("spPrompt"), list = $("spList");
  const btnAll = $("spAll"), btnAgain = $("spAgain"), btnRead = $("spRead"), light = $("spLight"), tip = $("spTip");
  const summary = $("spSummary");
  const BACK = $("spBackTpl").innerHTML;
  const POS = D.positions, CW = D.card_width;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const touch = window.matchMedia("(hover: none)").matches;
  const sleep = ms => new Promise(r => setTimeout(r, reduce ? 0 : ms));

  let state = "idle", order = D.cards.map((_, i) => i), shuffler = null, dealt = [], tipFor = -1;
  const svgCache = {};

  function rand(n) { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; }
  function shuffleOrder() {
    for (let i = order.length - 1; i > 0; i--) { const j = rand(i + 1); [order[i], order[j]] = [order[j], order[i]]; }
  }
  function loadCard(id) {
    if (!svgCache[id]) {
      svgCache[id] = fetch("/tarot/cards/" + id + ".svg")
        .then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })
        .catch(() => null);
    }
    return svgCache[id];
  }
  function say(key) { prompt.textContent = D.prompts[key]; }
  function el(tag, cls, text) { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; }
  function chips(words) { const u = el("ul", "sp-chips"); words.forEach(w => u.appendChild(el("li", null, w))); return u; }

  // ---- the deck
  for (let i = 0; i < 7; i++) {
    const c = el("span", "sp-stackcard");
    c.style.setProperty("--i", i);
    c.innerHTML = BACK;
    deck.appendChild(c);
  }
  // ---- empty places on the table
  POS.forEach((p, k) => {
    const s = el("span", "sp-slot");
    s.style.left = p.x + "%"; s.style.top = p.y + "%"; s.style.width = CW + "%";
    s.appendChild(el("span", "sp-slotnum", String(k + 1)));
    stage.appendChild(s);
  });

  // ---- card by card
  function buildList() {
    list.innerHTML = "";
    POS.forEach((p, k) => {
      const li = el("li", "sp-entry");
      li.appendChild(el("span", "sp-entrynum", String(k + 1)));
      const body = el("div");
      body.append(el("p", "sp-pos", p.title), el("p", "sp-q", p.question));
      const what = el("div", "sp-what"); what.appendChild(el("p", "sp-down", "Face down"));
      body.appendChild(what); li.appendChild(body); list.appendChild(li);
    });
  }
  buildList();

  // ---- shuffle / stop
  deck.addEventListener("click", () => {
    if (state === "idle") startShuffle();
    else if (state === "shuffling") stopShuffle();
  });
  function startShuffle() {
    state = "shuffling";
    deck.classList.remove("idle"); deck.classList.add("shuffling");
    deck.setAttribute("aria-label", "The deck is shuffling. Touch to stop.");
    say("shuffling");
    shuffler = setInterval(shuffleOrder, 90);
  }
  function stopShuffle() {
    state = "settling";
    let done = false;
    const finish = () => {
      if (done) return; done = true;
      clearInterval(shuffler); shuffleOrder();
      deck.classList.remove("shuffling");
      deal();
    };
    if (reduce) return finish();
    deck.querySelector(".sp-stackcard").addEventListener("animationiteration", finish, { once: true });
    setTimeout(finish, 900);
  }

  // ---- deal into the star
  async function deal() {
    state = "dealing"; say("dealing");
    deck.setAttribute("aria-label", "The deck");
    const picks = order.slice(0, POS.length).map(i => Object.assign({}, D.cards[i], { reversed: rand(2) === 1 }));
    picks.forEach(c => loadCard(c.id));
    dealt = [];
    const lines = stage.querySelectorAll(".sp-seg");
    for (let k = 0; k < POS.length; k++) {
      const p = POS[k], card = picks[k];
      const b = el("button", "sp-card");
      b.type = "button";
      b.style.width = CW + "%";
      b.setAttribute("aria-label", p.title + ": face down. Turn it over.");
      b.innerHTML = '<span class="sp-inner"><span class="sp-face sp-back">' + BACK + '</span><span class="sp-face sp-front"></span></span><span class="sp-num">' + (k + 1) + "</span>";
      stage.appendChild(b);
      void b.offsetWidth;
      b.style.left = p.x + "%"; b.style.top = p.y + "%";
      b.addEventListener("click", e => { e.stopPropagation(); onCard(k); });
      b.addEventListener("mouseenter", () => { if (!touch && state === "dealt") showTip(k); });
      b.addEventListener("mouseleave", () => { if (!touch) hideTip(); });
      b.addEventListener("focus", () => { if (state === "dealt") showTip(k); });
      b.addEventListener("blur", () => { if (!touch) hideTip(); });
      dealt.push({ el: b, card, pos: p, turned: false });
      if (k === POS.length - 1) deck.classList.add("gone");
      await sleep(560);
      if (k >= 1 && k <= 4) lines[k - 1].classList.add("on");
      if (k === 4) { await sleep(200); lines[4].classList.add("on"); }
    }
    stage.querySelector(".sp-ring").classList.add("on");
    state = "dealt"; say("dealt");
    btnAll.hidden = false; btnAgain.hidden = false;
  }

  // ---- the little summary that appears on hover (or on tap)
  function showTip(k) {
    const d = dealt[k];
    tip.innerHTML = "";
    tip.appendChild(el("p", "sp-tippos", (k + 1) + ". " + d.pos.title + ": " + d.pos.question));
    if (d.turned) {
      tip.appendChild(el("p", "sp-tipname", d.card.name));
      if (d.card.reversed) tip.appendChild(el("p", "sp-rev", "Reversed"));
      tip.appendChild(chips(d.card.keywords));
      tip.appendChild(el("p", "sp-tipscene", d.card.scene));
      tip.appendChild(el("p", "sp-tiphint", touch ? "Tap again to look closer." : "Click to look closer."));
    } else {
      tip.appendChild(el("p", "sp-tiphint", touch ? "Tap to turn it over." : "Click to turn it over."));
    }
    const wrap = stage.getBoundingClientRect(), r = d.el.getBoundingClientRect();
    tip.hidden = false;
    tip.classList.toggle("sheet", touch || wrap.width < 520);
    if (!tip.classList.contains("sheet")) {
      const tw = tip.offsetWidth, th = tip.offsetHeight;
      const right = r.left - wrap.left + r.width / 2 >= wrap.width / 2 - 2;   // centre and top cards open to the right
      const roomy = wrap.left >= tw + 24 && window.innerWidth - wrap.right >= tw + 24;
      let x = roomy ? (right ? wrap.width + 16 : -tw - 16)                  // beside the table, clear of every card
                    : (right ? r.right - wrap.left + 12 : r.left - wrap.left - tw - 12);
      let y = r.top - wrap.top + r.height / 2 - th / 2;
      y = Math.max(-20, Math.min(y, wrap.height - th + 20));
      tip.style.left = x + "px"; tip.style.top = y + "px";
    } else { tip.style.left = ""; tip.style.top = ""; }
    tipFor = k;
  }
  function hideTip() { tip.hidden = true; tipFor = -1; }
  document.addEventListener("click", e => { if (!tip.hidden && !tip.contains(e.target)) hideTip(); });

  // ---- turning cards over
  async function turn(k) {
    const d = dealt[k];
    if (d.turned) return;
    d.turned = true;
    const svg = await loadCard(d.card.id);
    const front = d.el.querySelector(".sp-front");
    front.innerHTML = svg || "";
    if (!svg) front.appendChild(el("span", "sp-fallback", d.card.name));
    d.el.classList.add("flipped");
    d.el.classList.toggle("reversed", !!d.card.reversed);
    d.el.setAttribute("aria-label", d.pos.title + ": " + d.card.name + (d.card.reversed ? ", reversed" : "") + ". Open it larger.");
    const li = list.children[k];
    li.classList.add("turned");
    const what = li.querySelector(".sp-what");
    what.innerHTML = "";
    const nm = el("button", "sp-name", d.card.name); nm.type = "button";
    nm.addEventListener("click", () => openLight(k));
    what.appendChild(nm);
    if (d.card.reversed) what.appendChild(el("p", "sp-rev", "Reversed"));
    what.append(chips(d.card.keywords), el("p", "sp-meaning", d.card.meaning));
    if (d.card.reversed) what.appendChild(el("p", "sp-revnote", revNote(d.card)));
    what.appendChild(reflect(d.card.question));
    if (dealt.every(x => x.turned)) finishReading();
  }

  function revNote(c) { return "Reversed, so its energy is out of balance. Think of " + CGGRead.list(c.keywords) + ": is there too much of that in your life right now, or not enough?"; }
  function reflect(q) { const p = el("p", "sp-counsel"); p.append(el("b", null, "Reflect: "), document.createTextNode(q)); return p; }

  function onCard(k) {
    if (state !== "dealt") return;
    const d = dealt[k];
    if (!d.turned) { turn(k).then(() => { if (touch || d.el.matches(":hover") || document.activeElement === d.el) showTip(k); }); return; }
    if (touch && tipFor !== k) { showTip(k); return; }
    hideTip(); openLight(k);
  }

  btnAll.addEventListener("click", async () => {
    for (let k = 0; k < dealt.length; k++) { if (!dealt[k].turned) { turn(k); await sleep(260); } }
  });

  // ---- Mira's reading
  function finishReading() {
    say("done");
    btnAll.hidden = true; btnRead.hidden = false;
    document.querySelectorAll("[data-share]").forEach(b => { b.hidden = false; });
    const r = CGGRead.summarize(dealt.map(d => d.card), POS, D);
    const box = $("spSummaryText"); box.innerHTML = "";
    r.paras.forEach(t => box.appendChild(el("p", null, t)));
    const notes = $("spNotes"); notes.innerHTML = "";
    r.notes.forEach(t => notes.appendChild(el("li", null, t)));
    summary.hidden = false;
  }
  btnRead.addEventListener("click", () => summary.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }));

  // ---- start over
  btnAgain.addEventListener("click", () => {
    hideTip();
    stage.querySelectorAll(".sp-card").forEach(c => c.remove());
    stage.querySelectorAll(".sp-seg, .sp-ring").forEach(l => l.classList.remove("on"));
    deck.classList.remove("gone"); deck.classList.add("idle");
    deck.setAttribute("aria-label", "The deck. Touch to shuffle.");
    btnAll.hidden = true; btnAgain.hidden = true; btnRead.hidden = true; summary.hidden = true;
    document.querySelectorAll("[data-share]").forEach(b => { b.hidden = true; });
    dealt = []; state = "idle";
    buildList(); say("idle");
    stage.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
  });


  // ---- share the reading as a picture. It is painted right here in the browser; nothing is uploaded.
  const shareBox = $("spShareBox"), shareImg = $("spShareImg"), shareGo = $("spShareGo"), shareDl = $("spShareDl"), shareMsg = $("spShareMsg");
  let fontCSS = null, logoURL = null, shareFile = null, shareURL = null;
  const xml = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  function b64(buf) {
    const bytes = new Uint8Array(buf); let s = "";
    for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(s);
  }
  async function fonts() {           // the page's own fonts, tucked inside the picture so the lettering matches
    if (fontCSS !== null) return fontCSS;
    try {
      const css = await (await fetch("https://fonts.googleapis.com/css2?family=Pirata+One&family=Alegreya:ital,wght@0,400;1,400&display=swap")).text();
      const out = [];
      for (const block of css.split("@font-face").slice(1)) {
        if (!/U\+0000-00FF/.test(block)) continue;              // the Latin letters are all the picture needs
        const url = (block.match(/url\((https:[^)]+)\)/) || [])[1];
        if (!url) continue;
        const buf = await (await fetch(url)).arrayBuffer();
        out.push("@font-face" + block.replace(url, "data:font/woff2;base64," + b64(buf)));
      }
      fontCSS = out.join("\n");
    } catch (e) { fontCSS = ""; }
    return fontCSS;
  }
  async function logo() {
    if (logoURL !== null) return logoURL;
    try { logoURL = "data:image/png;base64," + b64(await (await fetch("/assets/logo.png")).arrayBuffer()); } catch (e) { logoURL = ""; }
    return logoURL;
  }

  async function paintReading() {
    const W = 1080, H = 1350, S = 860, X0 = (W - S) / 2, Y0 = 178;
    const px = v => X0 + v / 100 * S, py = v => Y0 + v / 100 * S;
    const [fcss, lg] = await Promise.all([fonts(), logo()]);
    const defs = $("spDefs").innerHTML;
    const when = new Date().toLocaleDateString([], { month: "long", day: "numeric", year: "numeric" });
    let s = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">` +
      `<style>${fcss}
        .d{font-family:"Pirata One",Georgia,serif;fill:#e9d701}
        .b{font-family:"Alegreya",Georgia,serif;fill:#f3ecff}
        .m{font-family:"Alegreya",Georgia,serif;fill:#c9b8ee;font-style:italic}</style>` + defs +
      `<defs><radialGradient id="shBg" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#4a1590"/><stop offset=".55" stop-color="#22093f"/><stop offset="1" stop-color="#0d0418"/></radialGradient>
        <filter id="shGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter></defs>` +
      `<rect width="${W}" height="${H}" fill="url(#shBg)"/>` +
      `<rect x="16" y="16" width="${W - 32}" height="${H - 32}" rx="34" fill="none" stroke="#e9d701" stroke-width="4"/>` +
      `<rect x="28" y="28" width="${W - 56}" height="${H - 56}" rx="26" fill="none" stroke="#e9d701" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="6 6"/>`;
    if (lg) s += `<image href="${lg}" x="52" y="44" width="104" height="108"/>`;
    s += `<text class="d" x="${W / 2 + 40}" y="112" text-anchor="middle" font-size="74">The Chaotic Good Spread</text>` +
         `<text class="m" x="${W / 2 + 40}" y="154" text-anchor="middle" font-size="28">Read in Mira's tent · ${xml(when)}</text>`;
    // the star: the ring, then the lines in the order the cards were dealt
    const outer = POS.filter(p => p.key !== "heart"), heart = POS.find(p => p.key === "heart");
    s += `<circle cx="${px(heart.x)}" cy="${py(heart.y)}" r="${39 / 100 * S}" fill="none" stroke="#e9d701" stroke-opacity=".75" stroke-width="3"/>`;
    outer.forEach((a, i) => { const b = outer[(i + 1) % outer.length];
      s += `<line x1="${px(a.x)}" y1="${py(a.y)}" x2="${px(b.x)}" y2="${py(b.y)}" stroke="#e9d701" stroke-opacity=".75" stroke-width="3"/>`; });
    // the six cards, reversed ones upside down
    const cw = CW / 100 * S, ch = cw * 1200 / 700;
    dealt.forEach(d => {
      const svg = d.el.querySelector(".sp-front svg");
      const x = px(d.pos.x) - cw / 2, y = py(d.pos.y) - ch / 2;
      s += `<rect x="${x - 4}" y="${y - 4}" width="${cw + 8}" height="${ch + 8}" rx="12" fill="#e9d701" opacity=".45" filter="url(#shGlow)"/>`;
      if (!svg) { s += `<rect x="${x}" y="${y}" width="${cw}" height="${ch}" rx="10" fill="#1c0638" stroke="#e9d701" stroke-width="3"/>`; return; }
      const inner = svg.outerHTML.replace(/^<svg\b/, `<svg x="${x}" y="${y}" width="${cw}" height="${ch}"`);
      s += d.card.reversed ? `<g transform="rotate(180 ${x + cw / 2} ${y + ch / 2})">${inner}</g>` : inner;
    });
    // what was drawn, in the order it was dealt
    const top = 1066, colW = 470;
    dealt.forEach((d, i) => {
      const x = W / 2 - colW + (i % 2) * colW + 24, y = top + Math.floor(i / 2) * 72;
      s += `<text class="m" x="${x}" y="${y}" font-size="23">${i + 1} · ${xml(d.pos.title)}</text>` +
           `<text class="d" x="${x}" y="${y + 33}" font-size="34">${xml(d.card.name)}${d.card.reversed ? ' <tspan class="m" font-size="24">reversed</tspan>' : ""}</text>`;
    });
    s += `<text class="m" x="${W / 2}" y="${H - 50}" text-anchor="middle" font-size="25">Mira's mirror reflects; it doesn't predict. · chaoticgoodguild.com/tarot</text></svg>`;

    const url = URL.createObjectURL(new Blob([s], { type: "image/svg+xml" }));
    try {
      const img = new Image();
      img.src = url;
      await img.decode();
      await sleep(120);                 // give the tucked-in fonts a breath before painting
      const c = document.createElement("canvas"); c.width = W; c.height = H;
      const g = c.getContext("2d");
      g.drawImage(img, 0, 0);
      await sleep(60); g.drawImage(img, 0, 0);
      return await new Promise((ok, no) => c.toBlob(b => b ? ok(b) : no(new Error("no picture")), "image/png"));
    } finally { URL.revokeObjectURL(url); }
  }

  async function openShare() {
    if (state !== "dealt" || !dealt.every(d => d.turned)) return;
    lastFocus = document.activeElement;
    shareBox.hidden = false; shareMsg.textContent = "Mira is painting your reading…";
    shareImg.hidden = true; shareGo.hidden = true; shareDl.hidden = true;
    $("spShareClose").focus();
    try {
      const blob = await paintReading();
      const name = "chaotic-good-spread-" + new Date().toISOString().slice(0, 10) + ".png";
      shareFile = new File([blob], name, { type: "image/png" });
      if (shareURL) URL.revokeObjectURL(shareURL);
      shareURL = URL.createObjectURL(blob);
      shareImg.src = shareURL; shareImg.hidden = false;
      shareDl.href = shareURL; shareDl.download = name; shareDl.hidden = false;
      shareGo.hidden = !(navigator.canShare && navigator.canShare({ files: [shareFile] }));
      shareMsg.textContent = "Painted here on your device. Nothing is sent anywhere unless you share it.";
    } catch (e) {
      shareMsg.textContent = "The mirror fogged over and the picture wouldn't paint on this device. Try another browser?";
    }
  }
  shareGo.addEventListener("click", async () => {
    try { await navigator.share({ files: [shareFile], title: "My Chaotic Good Spread", text: "Mira read my star at chaoticgoodguild.com/tarot" }); }
    catch (e) { /* closed the share sheet; nothing to do */ }
  });
  function closeShare() { shareBox.hidden = true; if (lastFocus) lastFocus.focus(); }
  $("spShareClose").addEventListener("click", closeShare);
  shareBox.addEventListener("click", e => { if (e.target === shareBox) closeShare(); });
  document.querySelectorAll("[data-share]").forEach(b => b.addEventListener("click", openShare));

  // ---- a closer look
  let lastFocus = null;
  function openLight(k) {
    const d = dealt[k];
    lastFocus = document.activeElement;
    $("spLightCard").innerHTML = d.el.querySelector(".sp-front").innerHTML;
    $("spLightCard").classList.toggle("reversed", !!d.card.reversed);
    const rv = $("spLightRev"); rv.hidden = !d.card.reversed; rv.textContent = d.card.reversed ? revNote(d.card) : "";
    $("spLightPos").textContent = (k + 1) + ". " + d.pos.title + ": " + d.pos.question;
    $("spLightTitle").textContent = d.card.name;
    $("spLightTag").hidden = !d.card.reversed;
    const kw = $("spLightKw"); kw.innerHTML = ""; kw.appendChild(chips(d.card.keywords));
    $("spLightScene").textContent = d.card.scene;
    $("spLightMeaning").textContent = d.card.meaning;
    $("spLightCounsel").textContent = d.card.question;
    light.hidden = false;
    $("spLightClose").focus();
  }
  function closeLight() { light.hidden = true; if (lastFocus) lastFocus.focus(); }
  $("spLightClose").addEventListener("click", closeLight);
  light.addEventListener("click", e => { if (e.target === light) closeLight(); });
  document.addEventListener("keydown", e => {
    if (e.key !== "Escape") return;
    if (!shareBox.hidden) closeShare(); else if (!light.hidden) closeLight(); else hideTip();
  });
})();
