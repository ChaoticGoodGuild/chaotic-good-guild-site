/* The Chaotic Good Spread: shuffle, stop, deal six cards into the Guild star, turn them over, read them.
   Everything happens in the visitor's browser; nothing is sent or stored. */

// ---------- The reading engine (pure functions, tested by tools/test_spread.js) ----------
// picks[k] is the card in positions[k]. Cards carry: id, name, suit, rank, keywords, meaning, counsel, tone.
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
    paras.push(`At the heart of this reading sits ${heart.name}: ${CGGRead.list(kw(heart))}. This is where you're standing, and every other card bends around it.`);
    notes.push("The Heart sits in the centre of the star, so Mira reads it first. Every other card is read in relation to it.");

    // 2. The five points
    const pts = positions.filter(p => p.key !== "heart").map(p => {
      const c = picks[positions.indexOf(p)];
      const q = p.question.replace(/[.?!]$/, "");
      return `${q.charAt(0).toLowerCase() + q.slice(1)} is ${c.name} (${kw(c)[0]})`;
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

    const shadow = picks.filter(c => c.tone === "shadow").length;
    const light = picks.filter(c => c.tone === "light").length;
    if (shadow >= 3) {
      pat.push("The LEOs cast a long shadow over this spread. Name what's weighing on you before you try to fight it.");
      notes.push("Several heavy cards together show a hard season. That's information, not a sentence.");
    } else if (light >= 5) {
      pat.push("It's a bright star: the cards lean toward hope, warmth and things going right.");
      notes.push("When nearly every card is a bright one, the reading leans hopeful. Enjoy it, and act on it.");
    }
    if (pat.length) paras.push(pat.join(" "));

    // 4. Counsel
    paras.push(star === heart ? `Mira's counsel: ${heart.counsel}` :
      `Mira's counsel, from the heart: ${heart.counsel} And from the Star above it: ${star.counsel}`);
    notes.push("Close with counsel: something to carry into the days ahead. Mira takes it from the Heart and the Star.");
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
    const picks = order.slice(0, POS.length).map(i => D.cards[i]);
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
    d.el.setAttribute("aria-label", d.pos.title + ": " + d.card.name + ". Open it larger.");
    const li = list.children[k];
    li.classList.add("turned");
    const what = li.querySelector(".sp-what");
    what.innerHTML = "";
    const nm = el("button", "sp-name", d.card.name); nm.type = "button";
    nm.addEventListener("click", () => openLight(k));
    what.append(nm, chips(d.card.keywords), el("p", "sp-meaning", d.card.meaning));
    const cn = el("p", "sp-counsel"); cn.append(el("b", null, "Counsel: "), document.createTextNode(d.card.counsel));
    what.appendChild(cn);
    if (dealt.every(x => x.turned)) finishReading();
  }

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
    dealt = []; state = "idle";
    buildList(); say("idle");
    stage.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
  });

  // ---- a closer look
  let lastFocus = null;
  function openLight(k) {
    const d = dealt[k];
    lastFocus = document.activeElement;
    $("spLightCard").innerHTML = d.el.querySelector(".sp-front").innerHTML;
    $("spLightPos").textContent = (k + 1) + ". " + d.pos.title + ": " + d.pos.question;
    $("spLightTitle").textContent = d.card.name;
    const kw = $("spLightKw"); kw.innerHTML = ""; kw.appendChild(chips(d.card.keywords));
    $("spLightScene").textContent = d.card.scene;
    $("spLightMeaning").textContent = d.card.meaning;
    $("spLightCounsel").textContent = d.card.counsel;
    light.hidden = false;
    $("spLightClose").focus();
  }
  function closeLight() { light.hidden = true; if (lastFocus) lastFocus.focus(); }
  $("spLightClose").addEventListener("click", closeLight);
  light.addEventListener("click", e => { if (e.target === light) closeLight(); });
  document.addEventListener("keydown", e => {
    if (e.key !== "Escape") return;
    if (!light.hidden) closeLight(); else hideTip();
  });
})();
