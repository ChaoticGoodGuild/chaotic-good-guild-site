/* The Chaotic Good Spread: shuffle, stop, deal six cards into the Guild star, turn them over.
   Everything happens in the visitor's browser; nothing is sent or stored. */
(function () {
  const D = JSON.parse(document.getElementById("spread-data").textContent);
  const $ = id => document.getElementById(id);
  const stage = $("spStage"), deck = $("spDeck"), prompt = $("spPrompt"), list = $("spList");
  const btnAll = $("spAll"), btnAgain = $("spAgain"), light = $("spLight");
  const BACK = $("spBackTpl").innerHTML;
  const POS = D.positions, CW = D.card_width;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sleep = ms => new Promise(r => setTimeout(r, reduce ? 0 : ms));

  let state = "idle", order = D.cards.map((_, i) => i), shuffler = null, dealt = [];
  const svgCache = {};

  // ---- true randomness: the deck keeps reshuffling the whole time it's moving
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

  // ---- the deck: a small stack of card backs
  for (let i = 0; i < 7; i++) {
    const c = document.createElement("span");
    c.className = "sp-stackcard";
    c.style.setProperty("--i", i);
    c.innerHTML = BACK;
    deck.appendChild(c);
  }

  // ---- empty places on the table, so the star shows before any card is dealt
  POS.forEach((p, k) => {
    const s = document.createElement("span");
    s.className = "sp-slot";
    s.style.left = p.x + "%"; s.style.top = p.y + "%"; s.style.width = CW + "%";
    s.innerHTML = '<span class="sp-slotnum">' + (k + 1) + "</span>";
    stage.appendChild(s);
  });

  // ---- reading list
  function buildList() {
    list.innerHTML = "";
    POS.forEach((p, k) => {
      const li = document.createElement("li");
      li.className = "sp-entry";
      li.innerHTML = '<span class="sp-entrynum">' + (k + 1) + '</span><div><p class="sp-pos"></p><p class="sp-q"></p><div class="sp-what"><p class="sp-down">Face down</p></div></div>';
      li.querySelector(".sp-pos").textContent = p.title;
      li.querySelector(".sp-q").textContent = p.question;
      list.appendChild(li);
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
    deck.classList.remove("idle");
    deck.classList.add("shuffling");
    deck.setAttribute("aria-label", "The deck is shuffling. Touch to stop.");
    say("shuffling");
    shuffler = setInterval(shuffleOrder, 90);
  }

  function stopShuffle() {
    state = "settling";
    let done = false;
    const finish = () => {
      if (done) return; done = true;
      clearInterval(shuffler);
      shuffleOrder();
      deck.classList.remove("shuffling");
      deal();
    };
    if (reduce) return finish();
    deck.querySelector(".sp-stackcard").addEventListener("animationiteration", finish, { once: true });
    setTimeout(finish, 900);
  }

  // ---- deal into the star
  async function deal() {
    state = "dealing";
    say("dealing");
    deck.setAttribute("aria-label", "The deck");
    const picks = order.slice(0, POS.length).map(i => D.cards[i]);
    picks.forEach(c => loadCard(c.id));   // start fetching faces while the cards fly
    dealt = [];
    const lines = stage.querySelectorAll(".sp-seg");
    for (let k = 0; k < POS.length; k++) {
      const p = POS[k], card = picks[k];
      const el = document.createElement("button");
      el.type = "button";
      el.className = "sp-card";
      el.style.width = CW + "%";
      el.setAttribute("aria-label", p.title + ": face down. Turn it over.");
      el.innerHTML = '<span class="sp-inner"><span class="sp-face sp-back">' + BACK + '</span><span class="sp-face sp-front"></span></span><span class="sp-num">' + (k + 1) + "</span>";
      stage.appendChild(el);
      void el.offsetWidth;   // start at the deck, then glide to the point
      el.style.left = p.x + "%"; el.style.top = p.y + "%";
      el.addEventListener("click", () => onCard(k));
      dealt.push({ el, card, pos: p, turned: false });
      if (k === POS.length - 1) deck.classList.add("gone");
      await sleep(560);
      if (k >= 1 && k <= 4) lines[k - 1].classList.add("on");
      if (k === 4) { await sleep(200); lines[4].classList.add("on"); }
    }
    stage.querySelector(".sp-ring").classList.add("on");
    state = "dealt";
    say("dealt");
    btnAll.hidden = false; btnAgain.hidden = false;
  }

  // ---- turning cards over
  async function turn(k) {
    const d = dealt[k];
    if (d.turned) return;
    d.turned = true;
    const svg = await loadCard(d.card.id);
    const front = d.el.querySelector(".sp-front");
    front.innerHTML = svg || '<span class="sp-fallback"></span>';
    if (!svg) front.firstChild.textContent = d.card.name;
    d.el.classList.add("flipped");
    d.el.setAttribute("aria-label", d.pos.title + ": " + d.card.name + ". Open it larger.");
    const li = list.children[k];
    li.classList.add("turned");
    const what = li.querySelector(".sp-what");
    what.innerHTML = '<button type="button" class="sp-name"></button><p class="sp-scene"></p>';
    what.querySelector(".sp-name").textContent = d.card.name;
    what.querySelector(".sp-scene").textContent = d.card.scene;
    what.querySelector(".sp-name").addEventListener("click", () => openLight(k));
    if (dealt.every(x => x.turned)) { say("done"); btnAll.hidden = true; }
  }

  function onCard(k) {
    if (state !== "dealt") return;
    if (dealt[k].turned) openLight(k); else turn(k);
  }

  btnAll.addEventListener("click", async () => {
    for (let k = 0; k < dealt.length; k++) { if (!dealt[k].turned) { turn(k); await sleep(260); } }
  });

  // ---- start over
  btnAgain.addEventListener("click", () => {
    stage.querySelectorAll(".sp-card").forEach(c => c.remove());
    stage.querySelectorAll(".sp-seg, .sp-ring").forEach(l => l.classList.remove("on"));
    deck.classList.remove("gone");
    deck.classList.add("idle");
    deck.setAttribute("aria-label", "The deck. Touch to shuffle.");
    btnAll.hidden = true; btnAgain.hidden = true;
    dealt = []; state = "idle";
    buildList();
    say("idle");
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
    $("spLightScene").textContent = d.card.scene;
    light.hidden = false;
    $("spLightClose").focus();
  }
  function closeLight() { light.hidden = true; if (lastFocus) lastFocus.focus(); }
  $("spLightClose").addEventListener("click", closeLight);
  light.addEventListener("click", e => { if (e.target === light) closeLight(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !light.hidden) closeLight(); });
})();
