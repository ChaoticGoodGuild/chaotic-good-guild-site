/* Mira's card for today: one card per day, drawn once and kept on this device until tomorrow. */
(function () {
  const D = JSON.parse(document.getElementById("today-data").textContent);
  const $ = id => document.getElementById(id);
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const el = (tag, cls, text) => { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; };
  const dayKey = d => d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
  const today = dayKey(new Date());
  const rand = n => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; };
  const deck = $("tdDeck"), card = $("tdCard"), prompt = $("tdPrompt");
  $("tdDate").textContent = new Date().toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" });

  let saved = null;
  try { saved = JSON.parse(localStorage.getItem("cgg.today")); } catch (e) {}
  if (saved && saved.day === today && D.cards.some(c => c.id === saved.id)) show(saved, false);
  else deck.addEventListener("click", draw, { once: true });

  async function draw() {
    const pick = { day: today, id: D.cards[rand(D.cards.length)].id, reversed: rand(2) === 1 };
    try { localStorage.setItem("cgg.today", JSON.stringify(pick)); } catch (e) {}
    prompt.textContent = D.words.drawing;
    deck.classList.add("shuffling");
    await new Promise(r => setTimeout(r, reduce ? 0 : 1300));
    show(pick, true);
  }

  async function show(pick, fresh) {
    const c = D.cards.find(x => x.id === pick.id);
    let svg = null;
    try { const r = await fetch("/tarot/cards/" + c.id + ".svg"); if (r.ok) svg = await r.text(); } catch (e) {}
    deck.hidden = true; card.hidden = false;
    const front = $("tdFront");
    front.innerHTML = svg || ""; if (!svg) front.appendChild(el("span", "sp-fallback", c.name));
    card.classList.toggle("reversed", !!pick.reversed);
    if (fresh && !reduce) { card.classList.add("arrive"); }
    prompt.textContent = D.words.drawn;
    const t = $("tdText"); t.hidden = false;
    $("tdName").textContent = c.name;
    $("tdRev").hidden = !pick.reversed;
    const kw = $("tdKw"); kw.innerHTML = ""; const u = el("ul", "sp-chips"); c.keywords.forEach(k => u.appendChild(el("li", null, k))); kw.appendChild(u);
    $("tdMeaning").textContent = c.meaning;
    const rv = $("tdRevNote"); rv.hidden = !pick.reversed;
    rv.textContent = "Reversed, so its energy is out of balance. Think of " + list(c.keywords) + ": is there too much of that in your life right now, or not enough?";
    $("tdAsk").textContent = c.question;
    window.CGGKeep = { kind: "daily", key: "daily-" + today, title: "Today's card", day: today,
                       cards: [{ id: c.id, name: c.name, reversed: !!pick.reversed, pos: "Today's card" }],
                       reading: [c.meaning, (pick.reversed ? "Reversed. " : "") + "Reflect: " + c.question], prompt: D.words.note_prompt };
    document.dispatchEvent(new Event("cgg:reading"));
  }
  function list(xs) { return xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1]; }
})();
