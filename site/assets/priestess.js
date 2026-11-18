/* The Priestess by Moonlight: the secret full-moon reading (The High Priestess Spread).
   Nine cards laid like the High Priestess card. Card 9, the scroll, is the Priestess's secret: it is turned on its own,
   after a pause, and shown only when it is a Major Arcana card. Everything happens in the visitor's browser. */

// ---------- The reading engine (pure functions)
// picks[k] is the card in positions[k]; cards carry id, name, suit, rank, keywords, meaning, question, tone, reversed.
// shown: whether the Priestess revealed her secret (card 9 was a Major Arcana card).
const CGGPriestess = {
  list(xs) { return xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1]; },
  // a sentence ends at . ! or ? followed by a capital letter (so "Chaos! celebrates..." stays whole)
  firstSentence(t) { const m = String(t).match(/^.*?[.!?](?=\s+["“A-Z]|\s*$)/); return (m ? m[0] : t).trim(); },
  count(n) { return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"][n] || String(n); },
  isMajor(c) { return c.suit === "major"; },
  summarize(picks, positions, D, shown) {
    const L = CGGPriestess.list, at = key => picks[positions.findIndex(p => p.key === key)];
    const name = c => c.name + (c.reversed ? " (reversed)" : "");
    const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
    const kw0 = c => c.keywords[0];
    const self = at("self"), cross = at("crossing"), wax = at("waxing"), full = at("full"), wane = at("waning");
    const dark = at("dark"), lite = at("light"), sum = at("sum"), secret = at("secret");
    const paras = [], notes = [];

    // 1. The heart of it
    let p1 = `At the Priestess's heart sits ${name(self)}: ${L(self.keywords)}. This is where you are right now. `
      + `Across it lies ${cross.name}: ${L(cross.keywords)}. That's what surrounds you.`;
    if (self.suit === cross.suit && self.suit !== "major") p1 += ` Both are ${D.suits[self.suit].name}, so you and your surroundings are speaking the same language.`;
    paras.push(p1);
    notes.push(positions[0].how, positions[1].how);

    // 2. The three moons, in the order they were dealt
    const pk = c => `${c.name} (${kw0(c)}${c.reversed ? ", reversed" : ""})`;
    let p2 = `Above her, the three moons: the lenses you see it all through. The waning moon holds ${pk(wane)}, `
      + `the way you've seen what came before. The full moon holds ${pk(full)}, the lens you're looking through now. `
      + `The waxing moon holds ${pk(wax)}, the next step the path suggests.`;
    p2 += full.reversed
      ? ` The full moon came reversed, so ask whether this lens is magnifying things right now, or hiding them.`
      : ` The moon only reflects, so ask whether ${full.name} is showing things as they are, or larger than life.`;
    paras.push(p2);
    notes.push(positions[2].how, positions[3].how, positions[4].how);

    // 3. The pillars
    let p3 = `On either side stand her pillars. The dark pillar holds ${pk(dark)}: what moves you without your noticing. `
      + `The light pillar holds ${pk(lite)}: what you know drives you.`;
    if (dark.suit === lite.suit && dark.suit !== "major") p3 += ` Both pillars are ${D.suits[dark.suit].name}: what you know and what you don't are pulling the same way.`;
    else if ((dark.tone === "shadow") !== (lite.tone === "shadow") && (dark.tone === "shadow" || lite.tone === "shadow"))
      p3 += ` One pillar is heavy and one is not: the part of you that you can see and the part you can't may be pulling in different directions.`;
    paras.push(p3);
    notes.push(positions[5].how, positions[6].how);

    // 4. Patterns across the eight cards on the table (and the secret, if shown)
    const table = picks.filter((c, k) => positions[k].key !== "secret").concat(shown ? [secret] : []);
    const pat = [];
    const majors = table.filter(CGGPriestess.isMajor);
    if (majors.length === 0) pat.push("No Major Arcana sits on the table, so this reading lives in everyday choices you can shape.");
    else if (majors.length >= 3) pat.push(`With ${CGGPriestess.count(majors.length)} Major Arcana in the reading, this is a season of big lessons, larger than any one choice.`);
    else pat.push(`${L(majors.map(c => c.name))} ${majors.length === 1 ? "marks" : "mark"} a bigger current running beneath the everyday.`);
    const counts = {};
    table.filter(c => !CGGPriestess.isMajor(c)).forEach(c => { counts[c.suit] = (counts[c.suit] || 0) + 1; });
    const ranked = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    if (ranked.length && ranked[0][1] >= 3 && (ranked.length === 1 || ranked[0][1] > ranked[1][1])) {
      const s = D.suits[ranked[0][0]];
      pat.push(`${cap(CGGPriestess.count(ranked[0][1]))} ${s.name} appear, so ${s.theme} color the whole reading.`);
      notes.push(`When a suit repeats, its element colors the reading. ${s.name} are ${s.element}: ${s.theme}.`);
    }
    const rev = table.filter(c => c.reversed && c !== self);
    if (rev.length >= 4) pat.push("Many cards came reversed, so this reading is about balance: where something has grown too loud, and where something is missing.");
    else if (rev.length) pat.push(`${L(rev.map(c => c.name))} came reversed. For ${rev.length === 1 ? "it" : "each"}, ask: is there too much of that energy right now, or not enough?`);
    if (table.some(c => c.reversed)) notes.push(D.reversed + " Only you can tell which.");
    paras.push(pat.join(" "));

    // 5. The crescent: how it fits together
    paras.push(`At her feet, the crescent holds ${name(sum)}: ${L(sum.keywords)}. This is how the pieces fit together. ${CGGPriestess.firstSentence(sum.meaning)}`);
    notes.push(positions[7].how);

    // 6. The secret
    paras.push(shown
      ? `And the scroll. The Priestess showed you her secret, ${name(secret)}: ${L(secret.keywords)}. This is the deeper lesson in why you're here. ${CGGPriestess.firstSentence(secret.meaning)}`
      : `The scroll stayed sealed. The Priestess kept her secret tonight: the lesson beneath all this is still writing itself.`);
    notes.push(positions[8].how);

    // 7. Questions to carry, then the mirror
    const ask = c => c.question + (c.reversed ? ` And since it came reversed: is there too much of it right now, or not enough?` : "");
    let q = `Questions to carry, from the Self: ${ask(self)} And from the crescent: ${ask(sum)}`;
    if (shown) q += ` And from the scroll: ${secret.question}`;
    paras.push(q);
    notes.push("Mira closes with questions, not answers. The answers are yours.");
    paras.push(D.reflection);
    return { paras, notes };
  }
};
if (typeof module !== "undefined") module.exports = CGGPriestess;

(function () {
  if (typeof document === "undefined") return;
  const D = JSON.parse(document.getElementById("priestess-data").textContent);
  const $ = id => document.getElementById(id);
  const POS = D.positions, CW = D.card_width, SECRET = POS.findIndex(p => p.key === "secret");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sleep = ms => new Promise(r => setTimeout(r, reduce ? Math.min(ms, 60) : ms));
  const el = (tag, cls, text) => { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; };
  const chips = words => { const u = el("ul", "sp-chips"); words.forEach(w => u.appendChild(el("li", null, w))); return u; };

  // ---- is the moon full? (?preview=fullmoon opens it any time, for checking the page)
  const preview = /[?&]preview=fullmoon\b/.test(location.search);
  const w = CGGMoon.window(Sky, new Date());
  if (!w.open && !preview) {
    $("hpSealed").hidden = false;
    $("hpNext").textContent = `${D.sealed.next} ${w.full.toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" })}.`;
    return;
  }
  $("hpOpen").hidden = false;

  const stage = $("hpStage"), deck = $("hpDeck"), prompt = $("hpPrompt"), list = $("hpList");
  const btnAll = $("hpAll"), btnAgain = $("hpAgain"), btnRead = $("hpRead"), summary = $("hpSummary");
  const BACK = $("hpBackTpl").innerHTML;
  const say = k => { prompt.textContent = D.prompts[k]; };
  let state = "idle", order = D.cards.map((_, i) => i), shuffler = null, dealt = [], lastFocus = null;
  const svgCache = {};
  const rand = n => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; };
  const shuffleOrder = () => { for (let i = order.length - 1; i > 0; i--) { const j = rand(i + 1); [order[i], order[j]] = [order[j], order[i]]; } };
  const loadCard = id => svgCache[id] || (svgCache[id] = fetch("/tarot/cards/" + id + ".svg").then(r => r.ok ? r.text() : null).catch(() => null));
  const place = (node, p) => { node.style.left = p.x + "%"; node.style.top = p.y + "%"; node.style.transform = `translate(-50%, -50%) rotate(${p.rot}deg)`; };

  for (let i = 0; i < 7; i++) { const c = el("span", "sp-stackcard"); c.style.setProperty("--i", i); c.innerHTML = BACK; deck.appendChild(c); }
  POS.forEach((p, k) => {
    const s = el("span", "sp-slot hp-slot"); s.style.width = CW + "%"; place(s, p);
    s.appendChild(el("span", "sp-slotnum", String(k + 1))); stage.appendChild(s);
  });

  function buildList() {
    list.innerHTML = "";
    POS.forEach((p, k) => {
      const li = el("li", "sp-entry");
      li.appendChild(el("span", "sp-entrynum", String(k + 1)));
      const body = el("div");
      body.append(el("p", "sp-pos", p.title), el("p", "sp-q", p.question));
      const what = el("div", "sp-what"); what.appendChild(el("p", "sp-down", k === SECRET ? "Sealed" : "Face down"));
      body.appendChild(what); li.appendChild(body); list.appendChild(li);
    });
  }
  buildList();

  // ---- shuffle, stop, deal
  deck.addEventListener("click", () => {
    if (state === "idle") {
      state = "shuffling"; deck.classList.remove("idle"); deck.classList.add("shuffling");
      deck.setAttribute("aria-label", "The deck is shuffling. Touch to stop."); say("shuffling");
      shuffler = setInterval(shuffleOrder, 90);
    } else if (state === "shuffling") {
      state = "settling";
      setTimeout(() => { clearInterval(shuffler); shuffleOrder(); deck.classList.remove("shuffling"); deal(); }, reduce ? 0 : 500);
    }
  });

  async function deal() {
    state = "dealing"; say("dealing"); deck.setAttribute("aria-label", "The deck");
    const picks = order.slice(0, POS.length).map(i => Object.assign({}, D.cards[i], { reversed: rand(2) === 1 }));
    picks.forEach(c => loadCard(c.id));
    dealt = [];
    for (let k = 0; k < POS.length; k++) {
      const p = POS[k];
      const b = el("button", "sp-card hp-card" + (k === SECRET ? " hp-scroll" : ""));
      b.type = "button"; b.style.width = CW + "%";
      b.setAttribute("aria-label", `${k + 1}. ${p.title}: face down.` + (k === SECRET ? " The Priestess's secret." : " Turn it over."));
      b.innerHTML = '<span class="sp-inner"><span class="sp-face sp-back">' + BACK + '</span><span class="sp-face sp-front"></span></span><span class="sp-num">' + (k + 1) + "</span>";
      stage.appendChild(b); void b.offsetWidth;
      place(b, p);
      b.addEventListener("click", () => onCard(k));
      dealt.push({ el: b, card: picks[k], pos: p, turned: false });
      if (k === POS.length - 1) deck.classList.add("gone");
      await sleep(430);
    }
    state = "dealt"; say("dealt");
    btnAll.hidden = false; btnAgain.hidden = false;
  }

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
    d.el.setAttribute("aria-label", `${k + 1}. ${d.pos.title}: ${d.card.name}${d.card.reversed ? ", reversed" : ""}. Open it larger.`);
    fillEntry(k);
    if (dealt.every((x, i) => i === SECRET || x.turned) && state === "dealt") { state = "ready"; say("ready"); btnAll.hidden = true; d.el.blur(); dealt[SECRET].el.classList.add("beckon"); }
  }
  function fillEntry(k) {
    const d = dealt[k], li = list.children[k], what = li.querySelector(".sp-what");
    li.classList.add("turned"); what.innerHTML = "";
    const nm = el("button", "sp-name", d.card.name); nm.type = "button"; nm.addEventListener("click", () => openLight(k));
    what.appendChild(nm);
    if (d.card.reversed) what.appendChild(el("p", "sp-rev", "Reversed"));
    what.append(chips(d.card.keywords), el("p", "sp-meaning", d.card.meaning));
    if (d.card.reversed) what.appendChild(el("p", "sp-revnote", revNote(d.card)));
    const r = el("p", "sp-counsel"); r.append(el("b", null, "Reflect: "), document.createTextNode(d.card.question)); what.appendChild(r);
  }
  const revNote = c => "Reversed, so its energy is out of balance. Think of " + CGGPriestess.list(c.keywords) + ": is there too much of that in your life right now, or not enough?";

  function onCard(k) {
    const d = dealt[k];
    if (k === SECRET) {
      if (state === "dealt") { say("early"); d.el.classList.remove("nudge"); void d.el.offsetWidth; d.el.classList.add("nudge"); return; }
      if (state === "ready") return ceremony();
      if (d.turned && !d.kept) openLight(k);
      return;
    }
    if (state === "dealing" || state === "idle" || state === "shuffling" || state === "settling") return;
    if (!d.turned) turn(k); else openLight(k);
  }
  btnAll.addEventListener("click", async () => {
    for (let k = 0; k < dealt.length; k++) { if (k !== SECRET && !dealt[k].turned) { turn(k); await sleep(240); } }
  });

  // ---- the Priestess weighs her secret
  async function ceremony() {
    state = "weighing";
    const d = dealt[SECRET], shown = CGGPriestess.isMajor(d.card);
    d.el.classList.remove("beckon");
    const ov = $("hpRite"), msg = $("hpRiteMsg"), more = $("hpRiteMore");
    lastFocus = document.activeElement;
    msg.textContent = D.secret.weighing; more.textContent = "";
    ov.className = "hp-rite"; ov.hidden = false; void ov.offsetWidth;
    ov.classList.add("in");
    const cue = n => { if (window.CGGSound) window.CGGSound.cue(n); };
    await sleep(500); ov.classList.add("weigh"); cue("weigh");
    await sleep(3000);
    if (shown) {
      ov.classList.add("reveal"); msg.textContent = D.secret.revealed; cue("reveal");
      await sleep(1700);
      ov.classList.remove("in"); await sleep(600); ov.hidden = true;
      await turn(SECRET); d.el.classList.add("revealed");
    } else {
      ov.classList.add("keep"); msg.textContent = D.secret.kept; more.textContent = D.secret.kept_more; cue("keep");
      await sleep(3600);
      ov.classList.remove("in"); await sleep(600); ov.hidden = true;
      d.turned = true; d.kept = true; d.el.classList.add("kept");
      d.el.setAttribute("aria-label", `9. ${d.pos.title}: ${D.secret.kept_card}`);
      const li = list.children[SECRET]; li.classList.add("turned");
      li.querySelector(".sp-what").innerHTML = ""; li.querySelector(".sp-what").appendChild(el("p", "sp-down", D.secret.kept_card));
    }
    if (lastFocus) lastFocus.focus();
    finish(shown);
  }

  function finish(shown) {
    state = "done"; say("done");
    btnRead.hidden = false;
    const r = CGGPriestess.summarize(dealt.map(x => x.card), POS, D, shown);
    const box = $("hpSummaryText"); box.innerHTML = "";
    r.paras.forEach(t => box.appendChild(el("p", null, t)));
    const notes = $("hpNotes"); notes.innerHTML = "";
    r.notes.forEach(t => notes.appendChild(el("li", null, t)));
    summary.hidden = false;
  }
  btnRead.addEventListener("click", () => summary.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }));

  btnAgain.addEventListener("click", () => {
    stage.querySelectorAll(".sp-card").forEach(c => c.remove());
    dealt = []; state = "idle"; say("idle");
    deck.className = "sp-deck idle"; deck.setAttribute("aria-label", "The deck. Touch to shuffle.");
    btnAll.hidden = true; btnRead.hidden = true; btnAgain.hidden = true; summary.hidden = true;
    buildList();
  });

  // ---- a closer look
  const light = $("hpLight");
  function openLight(k) {
    const d = dealt[k];
    lastFocus = document.activeElement;
    $("hpLightCard").innerHTML = d.el.querySelector(".sp-front").innerHTML;
    $("hpLightCard").classList.toggle("reversed", !!d.card.reversed);
    $("hpLightPos").textContent = (k + 1) + ". " + d.pos.title + ": " + d.pos.question;
    $("hpLightTitle").textContent = d.card.name;
    $("hpLightTag").hidden = !d.card.reversed;
    const rv = $("hpLightRev"); rv.hidden = !d.card.reversed; rv.textContent = d.card.reversed ? revNote(d.card) : "";
    const kw = $("hpLightKw"); kw.innerHTML = ""; kw.appendChild(chips(d.card.keywords));
    $("hpLightScene").textContent = d.card.scene;
    $("hpLightMeaning").textContent = d.card.meaning;
    $("hpLightCounsel").textContent = d.card.question;
    light.hidden = false; $("hpLightClose").focus();
  }
  const closeLight = () => { light.hidden = true; if (lastFocus) lastFocus.focus(); };
  $("hpLightClose").addEventListener("click", closeLight);
  light.addEventListener("click", e => { if (e.target === light) closeLight(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !light.hidden) closeLight(); });
})();
