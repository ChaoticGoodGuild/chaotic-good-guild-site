/* Mira's card for today: one card per day, drawn at random for each person and kept on their own device until tomorrow.
   On the day of the full moon it becomes three cards, the way the High Priestess sits: the dark pillar (what moves you
   unnoticed), the light pillar (what you know drives you), and her secret between them, shown only if it is a Major
   Arcana card (and then always upright). Preview the full-moon pull any day with ?preview=fullmoon (nothing is saved). */
(function () {
  const D = JSON.parse(document.getElementById("today-data").textContent);
  const $ = id => document.getElementById(id);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sleep = ms => new Promise(r => setTimeout(r, reduce ? Math.min(ms, 60) : ms));
  const el = (tag, cls, text) => { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; };
  const list = xs => xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1];
  const chips = words => { const u = el("ul", "sp-chips"); words.forEach(w => u.appendChild(el("li", null, w))); return u; };
  const dayKey = d => d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
  const today = dayKey(new Date());
  const rand = n => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; };
  const card = id => D.cards.find(c => c.id === id);
  const svgs = {};
  const loadSvg = id => svgs[id] || (svgs[id] = fetch("/tarot/cards/" + id + ".svg").then(r => r.ok ? r.text() : null).catch(() => null));
  const load = key => { try { return JSON.parse(localStorage.getItem(key)); } catch (e) { return null; } };
  const store = (key, v) => { try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} };
  const deck = $("tdDeck"), prompt = $("tdPrompt");
  $("tdDate").textContent = new Date().toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" });

  const preview = /[?&]preview=fullmoon(&|$)/.test(location.search);
  let moon = preview;
  try { moon = moon || CGGMoon.window(Sky, new Date()).open; } catch (e) {}
  if (moon) return moonDay();

  // ---------------- an ordinary day: one card
  const saved = load("cgg.today");
  if (saved && saved.day === today && card(saved.id)) show(saved, false);
  else deck.addEventListener("click", draw, { once: true });

  async function draw() {
    const pick = { day: today, id: D.cards[rand(D.cards.length)].id, reversed: rand(2) === 1 };
    store("cgg.today", pick);
    prompt.textContent = D.words.drawing;
    deck.classList.add("shuffling");
    await sleep(1300);
    show(pick, true);
  }

  async function show(pick, fresh) {
    const c = card(pick.id), svg = await loadSvg(c.id), box = $("tdCard");
    deck.hidden = true; box.hidden = false;
    const front = $("tdFront");
    front.innerHTML = svg || ""; if (!svg) front.appendChild(el("span", "sp-fallback", c.name));
    box.classList.toggle("reversed", !!pick.reversed);
    if (fresh && !reduce) box.classList.add("arrive");
    prompt.textContent = D.words.drawn;
    $("tdText").hidden = false;
    $("tdName").textContent = c.name;
    $("tdRev").hidden = !pick.reversed;
    const kw = $("tdKw"); kw.innerHTML = ""; kw.appendChild(chips(c.keywords));
    $("tdMeaning").textContent = c.meaning;
    const rv = $("tdRevNote"); rv.hidden = !pick.reversed; rv.textContent = revNote(c);
    $("tdAsk").textContent = c.question;
    window.CGGKeep = { kind: "daily", key: "daily-" + today, title: "Today's card", day: today,
                       cards: [{ id: c.id, name: c.name, reversed: !!pick.reversed, pos: "Today's card" }],
                       reading: [c.meaning, (pick.reversed ? "Reversed. " : "") + "Reflect: " + c.question], prompt: D.words.note_prompt };
    document.dispatchEvent(new Event("cgg:reading"));
  }
  function revNote(c) { return "Reversed, so its energy is out of balance. Think of " + list(c.keywords) + ": is there too much of that in your life right now, or not enough?"; }

  // ---------------- the full moon: three cards
  function moonDay() {
    const M = D.moon, P = D.priestess, POS = [P.dark, P.secret, P.light];   // left, middle, right
    const SECRET = 1;
    document.documentElement.classList.add("moonday");
    $("tdSky").hidden = false;
    $("tdWho").textContent = M.who; $("tdTitle").textContent = M.title; $("tdDesc").textContent = M.desc;
    prompt.textContent = M.idle;
    const row = $("tdMoon"), slots = Array.from(row.querySelectorAll(".td-mcard"));
    POS.forEach((p, k) => { const lab = row.querySelectorAll(".td-mlabel")[k]; lab.querySelector("b").textContent = p.title; lab.querySelector("span").textContent = p.question; });
    let state = load("cgg.moonday");
    if (preview || !state || state.day !== today) state = null;
    if (state) { lay(state); } else deck.addEventListener("click", deal, { once: true });

    async function deal() {
      const ids = []; while (ids.length < 3) { const id = D.cards[rand(D.cards.length)].id; if (!ids.includes(id)) ids.push(id); }
      // [dark, secret, light]; a secret the Priestess will reveal is always upright
      const picks = ids.map((id, k) => ({ id, reversed: rand(2) === 1 && !(k === SECRET && card(id).suit === "major") }));
      state = { day: today, picks, turned: [false, false, false], done: false };
      save();
      deck.classList.add("shuffling"); prompt.textContent = D.words.drawing;
      await sleep(1300);
      lay(state, true);
    }
    function save() { if (!preview) store("cgg.moonday", state); }

    async function lay(s, fresh) {
      $("tdTable").hidden = true; row.hidden = false;
      if (fresh && !reduce) row.classList.add("arrive");
      for (let k = 0; k < 3; k++) {
        const b = slots[k];
        b.onclick = () => onCard(k);
        if (s.turned[k] && !(k === SECRET && !isShown())) await flip(k, false);
        if (k === SECRET && s.done && !isShown()) seal();
      }
      if (s.done) return finish();
      nextPrompt();
    }
    const isShown = () => card(state.picks[SECRET].id).suit === "major";
    function nextPrompt() {
      if (state.turned[0] && state.turned[2]) { prompt.textContent = M.ready; slots[SECRET].classList.add("beckon"); }
      else prompt.textContent = M.dealt;
    }
    async function flip(k, anim) {
      const pick = state.picks[k], c = card(pick.id), b = slots[k];
      const svg = await loadSvg(c.id);
      const front = b.querySelector(".sp-front"); front.innerHTML = svg || ""; if (!svg) front.appendChild(el("span", "sp-fallback", c.name));
      b.classList.toggle("reversed", !!pick.reversed);
      if (!anim) b.classList.add("instant");
      b.classList.add("flipped");
      b.setAttribute("aria-label", `${POS[k].title}: ${c.name}${pick.reversed ? ", reversed" : ""}`);
    }
    async function onCard(k) {
      if (state.done) return;
      if (k === SECRET) {
        if (!(state.turned[0] && state.turned[2])) { prompt.textContent = M.early; slots[k].classList.remove("nudge"); void slots[k].offsetWidth; slots[k].classList.add("nudge"); return; }
        return ceremony();
      }
      if (state.turned[k]) return;
      state.turned[k] = true; save();
      await flip(k, true);
      nextPrompt();
    }
    function seal() { slots[SECRET].classList.add("kept"); slots[SECRET].setAttribute("aria-label", `${P.secret.title}: ${D.secret.kept_card}`); }
    async function ceremony() {
      if (state.busy) return; state.busy = true;
      const shown = isShown(), ov = $("hpRite"), msg = $("hpRiteMsg"), more = $("hpRiteMore");
      slots[SECRET].classList.remove("beckon");
      msg.textContent = D.secret.weighing; more.textContent = "";
      ov.className = "hp-rite"; ov.hidden = false; void ov.offsetWidth; ov.classList.add("in");
      await sleep(500); ov.classList.add("weigh");
      await sleep(3000);
      if (shown) { ov.classList.add("reveal"); msg.textContent = D.secret.revealed; await sleep(1700); }
      else { ov.classList.add("keep"); msg.textContent = D.secret.kept; more.textContent = D.secret.kept_more; await sleep(3600); }
      ov.classList.remove("in"); await sleep(600); ov.hidden = true;
      state.turned[SECRET] = true; state.done = true; delete state.busy; save();
      if (shown) { await flip(SECRET, true); slots[SECRET].classList.add("revealed"); } else seal();
      finish();
    }
    function finish() {
      prompt.textContent = M.done;
      const shown = isShown();
      const picks = state.picks.map(p => Object.assign({}, card(p.id), { reversed: !!p.reversed }));
      const paras = CGGPriestess.moonDay([picks[0], picks[2], picks[1]], P, D, shown);
      const box = $("tdMoonText"); box.innerHTML = ""; box.hidden = false;
      paras.forEach(t => box.appendChild(el("p", null, t)));
      const keep = $("tdMoonKeep"); keep.hidden = false;
      window.CGGKeep = { kind: "moonday", key: "moon-" + today + (preview ? "-preview-" + Date.now() : ""), title: M.title, day: today, reading: paras, prompt: M.note_prompt,
        cards: state.picks.map((p, k) => k === SECRET && !shown
          ? { id: "", name: "Sealed (the Priestess kept her secret)", reversed: false, pos: POS[k].title }
          : { id: p.id, name: card(p.id).name, reversed: !!p.reversed, pos: POS[k].title }) };
      document.dispatchEvent(new Event("cgg:reading"));
    }
  }
})();
