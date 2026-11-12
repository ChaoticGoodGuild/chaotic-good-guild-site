/* The Guild Calendar: moon phases, the wheel of the year, Guy Fox Day, and the sun, moon and Mercury
   through the zodiac. Sky math lives in sky.js; the words live in src/calendar.json. Nothing is sent anywhere. */
(function () {
  const C = JSON.parse(document.getElementById("calendar-data").textContent);
  const $ = id => document.getElementById(id);
  const el = (tag, cls, text) => { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; };
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const DAY = 86400000;
  const key = d => d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
  const midnight = d => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const time = d => d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  const longDate = d => d.toLocaleDateString([], { weekday: "long", month: "long", day: "numeric", year: "numeric" });
  const shortDate = d => d.toLocaleDateString([], { month: "short", day: "numeric" });
  const SIGN = i => C.signs[i];
  const signText = i => SIGN(i).glyph + "︎ " + SIGN(i).name;   // ︎ keeps the glyph as text, not an emoji

  // ---------- a little moon, drawn to its phase
  function moonSVG(fraction, waxing, size, cls) {
    const r = 10, f = Math.max(0, Math.min(1, fraction));
    const rx = (Math.abs(1 - 2 * f) * r).toFixed(2);
    const outer = waxing ? 1 : 0, inner = f < 0.5 ? (waxing ? 0 : 1) : (waxing ? 1 : 0);
    const lit = f < 0.005 ? "" : f > 0.995 ? `<circle cx="12" cy="12" r="${r}" class="m-lit"/>`
      : `<path class="m-lit" d="M12 2 A${r} ${r} 0 0 ${outer} 12 22 A${rx} ${r} 0 0 ${inner} 12 2Z"/>`;
    return `<svg class="${cls || "moon"}" viewBox="0 0 24 24" width="${size}" height="${size}" aria-hidden="true">` +
           `<circle cx="12" cy="12" r="${r}" class="m-dark"/>${lit}<circle cx="12" cy="12" r="${r}" class="m-rim"/></svg>`;
  }

  // ---------- everything the sky does in a year, worked out once and kept
  const years = {};
  function year(y) {
    if (years[y]) return years[y];
    const from = new Date(y - 1, 11, 1), to = new Date(y + 1, 1, 1);
    const phases = Sky.phasesBetween(from, to);
    const seasons = Sky.seasons(y);
    // full moon names: by month, with the Harvest Moon nearest the autumn equinox and the Hunter's Moon after it
    const fulls = phases.filter(p => p.phase === "full");
    fulls.forEach(p => { p.name = C.full_moons.names[p.date.getMonth()]; });
    let hi = 0;
    fulls.forEach((p, i) => { if (Math.abs(p.date - seasons.september) < Math.abs(fulls[hi].date - seasons.september)) hi = i; });
    if (fulls[hi]) fulls[hi].name = C.full_moons.harvest;
    if (fulls[hi + 1]) fulls[hi + 1].name = C.full_moons.hunters;
    fulls.forEach((p, i) => { if (i && fulls[i - 1].date.getMonth() === p.date.getMonth() && fulls[i - 1].date.getFullYear() === p.date.getFullYear()) { p.blue = true; p.name = C.full_moons.blue; } });
    const byDay = {};
    const add = (d, ev) => { (byDay[key(d)] = byDay[key(d)] || []).push(ev); };
    phases.forEach(p => add(p.date, { type: "phase", ...p }));
    const holidays = C.holidays.map(h => {
      const date = h.when.season ? seasons[h.when.season] : new Date(y, h.when.month - 1, h.when.day);
      const ev = { type: "holiday", h, date, exact: !!h.when.season };
      add(date, ev);
      return ev;
    });
    const stations = [y - 1, y, y + 1].flatMap(Sky.mercuryStations)
      .filter((s, i, a) => a.findIndex(t => Math.abs(t.date - s.date) < DAY) === i).sort((a, b) => a.date - b.date);
    stations.forEach(s => { if (s.date.getFullYear() === y) add(s.date, { type: "mercury", ...s }); });
    const retro = [];
    stations.forEach((s, i) => { if (s.kind === "retrograde" && stations[i + 1]) retro.push([s.date, stations[i + 1].date, s.lon]); });
    return (years[y] = { phases, seasons, holidays, byDay, retro });
  }
  const eventsOn = d => (year(d.getFullYear()).byDay[key(d)] || []).slice().sort((a, b) => a.date - b.date);
  const retroOn = d => { const y = year(d.getFullYear()); const noon = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12); return y.retro.find(([a, b]) => noon >= a && noon <= b); };
  function sunChange(d) { return Sky.signChange(Sky.sunLon, midnight(d), addDays(d, 1)); }
  function moonChange(d) { return Sky.signChange(Sky.moonLon, midnight(d), addDays(d, 1)); }

  function phaseOn(d) {
    const p = eventsOn(d).find(e => e.type === "phase");
    const noon = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12);
    const L = Sky.moonLight(Sky.jdOf(p ? p.date : noon));
    let i;
    if (p) i = { new: 0, first: 2, full: 4, last: 6 }[p.phase];
    else i = L.waxing ? (L.fraction < 0.5 ? 1 : 3) : (L.fraction < 0.5 ? 7 : 5);
    return { i, exact: p, fraction: L.fraction, waxing: L.waxing };
  }

  // ---------- tonight
  function tonight() {
    const now = new Date(), jd = Sky.jdOf(now), L = Sky.moonLight(jd), today = midnight(now);
    const ph = phaseOn(today);
    const box = $("calTonight"); box.innerHTML = "";
    const art = el("div", "ct-moon"); art.innerHTML = moonSVG(L.fraction, L.waxing, 132, "moon big"); box.appendChild(art);
    const t = el("div", "ct-text");
    t.appendChild(el("p", "ct-kicker", "Tonight above the village"));
    t.appendChild(el("h2", "ct-phase", C.phases[ph.i].name));
    t.appendChild(el("p", "ct-line", C.phases[ph.i].line));
    const facts = el("ul", "ct-facts");
    const li = (label, node) => { const x = el("li"); x.append(el("span", "ct-label", label), node); facts.appendChild(x); };
    li("Moon lit", el("span", null, Math.round(L.fraction * 100) + "%"));
    li("Moon in", signBtn(Sky.signOf(Sky.moonLon(jd))));
    li("Sun in", signBtn(Sky.signOf(Sky.sunLon(jd))));
    const y = year(now.getFullYear()), y2 = year(now.getFullYear() + 1);
    const nextFull = y.phases.concat(y2.phases).find(p => p.phase === "full" && p.date > now);
    if (nextFull) li("Next full moon", dateBtn(nextFull.date, nextFull.name + ", " + shortDate(nextFull.date)));
    const nextHol = y.holidays.concat(y2.holidays).filter(h => midnight(h.date) >= today).sort((a, b) => a.date - b.date)[0];
    if (nextHol) {
      const days = Math.round((midnight(nextHol.date) - today) / DAY);
      li("Next on the wheel", dateBtn(nextHol.date, nextHol.h.name + (days === 0 ? ", today!" : days === 1 ? ", tomorrow" : ", in " + days + " days")));
    }
    const r = retroOn(today);
    if (r) li("Mercury", dateBtn(r[1], "retrograde until " + shortDate(r[1])));
    box.appendChild(t); t.appendChild(facts);
  }

  function signBtn(i) {
    const b = el("button", "cal-sign", signText(i)); b.type = "button";
    b.addEventListener("click", () => openSign(i));
    return b;
  }
  function dateBtn(d, text) {
    const b = el("button", "cal-link", text); b.type = "button";
    b.addEventListener("click", () => { go(d); $("calMonth").scrollIntoView({ behavior: "smooth", block: "start" }); });
    return b;
  }

  // ---------- the month
  let viewY, viewM, selected;
  function go(d) { selected = midnight(d); viewY = d.getFullYear(); viewM = d.getMonth(); drawMonth(); drawDay(); }

  function drawMonth() {
    $("calTitle").textContent = MONTHS[viewM] + " " + viewY;
    const grid = $("calGrid"); grid.innerHTML = "";
    const first = new Date(viewY, viewM, 1), start = addDays(first, -first.getDay());
    const last = new Date(viewY, viewM + 1, 0), cells = Math.ceil((first.getDay() + last.getDate()) / 7) * 7;
    const today = key(new Date());
    for (let n = 0; n < cells; n++) {
      const d = addDays(start, n), inMonth = d.getMonth() === viewM;
      const b = el("button", "cal-day" + (inMonth ? "" : " out") + (key(d) === today ? " today" : "") + (selected && key(d) === key(selected) ? " sel" : ""));
      b.type = "button";
      const ph = phaseOn(d), evs = eventsOn(d), sc = sunChange(d), rt = retroOn(d);
      const top = el("span", "cd-top");
      top.appendChild(el("span", "cd-num", d.getDate()));
      const m = el("span", "cd-moon" + (ph.exact ? " exact" : "")); m.innerHTML = moonSVG(ph.fraction, ph.waxing, 22); top.appendChild(m);
      b.appendChild(top);
      const tags = el("span", "cd-tags"), labels = [];
      evs.forEach(e => {
        if (e.type === "holiday") { tags.appendChild(el("span", "cd-tag hol", e.h.name)); labels.push(e.h.name); }
        if (e.type === "phase" && (e.phase === "full" || e.phase === "new")) {
          const nm = e.phase === "full" ? (e.name || "Full Moon") : "New Moon";
          tags.appendChild(el("span", "cd-tag moon", nm)); labels.push(nm);
          if (e.eclipse) { tags.appendChild(el("span", "cd-tag ecl", "Eclipse")); labels.push(e.eclipse.kind + " " + e.eclipse.body + " eclipse"); }
        }
        if (e.type === "mercury") { tags.appendChild(el("span", "cd-tag merc", "☿︎ " + (e.kind === "retrograde" ? "℞" : "D"))); labels.push("Mercury stations " + e.kind); }
      });
      if (sc) { tags.appendChild(el("span", "cd-tag sun", "☉︎ " + SIGN(sc.to).glyph + "︎")); labels.push("the sun enters " + SIGN(sc.to).name); }
      if (rt) b.classList.add("retro");
      b.appendChild(tags);
      b.setAttribute("aria-label", longDate(d) + ". " + C.phases[ph.i].name + (labels.length ? ". " + labels.join(", ") : ""));
      if (selected && key(d) === key(selected)) b.setAttribute("aria-pressed", "true");
      b.addEventListener("click", () => { selected = d; if (!inMonth) { viewY = d.getFullYear(); viewM = d.getMonth(); } drawMonth(); drawDay(); });
      grid.appendChild(b);
    }
  }

  // ---------- one day, up close
  function drawDay() {
    const d = selected, box = $("calDay"); box.innerHTML = "";
    const ph = phaseOn(d), evs = eventsOn(d);
    box.appendChild(el("p", "cdy-date", longDate(d)));
    const moonRow = el("div", "cdy-moonrow");
    const art = el("div"); art.innerHTML = moonSVG(ph.fraction, ph.waxing, 72, "moon mid"); moonRow.appendChild(art);
    const mt = el("div");
    mt.appendChild(el("h3", "cdy-phase", C.phases[ph.i].name));
    mt.appendChild(el("p", "cdy-sub", ph.exact ? "Exactly at " + time(ph.exact.date) + ", " + Math.round(ph.fraction * 100) + "% lit"
                                               : Math.round(ph.fraction * 100) + "% lit at midday"));
    moonRow.appendChild(mt); box.appendChild(moonRow);
    box.appendChild(el("p", "cdy-line", C.phases[ph.i].line));

    const noon = Sky.jdOf(new Date(d.getFullYear(), d.getMonth(), d.getDate(), 12));
    const signs = el("ul", "cdy-signs");
    const row = (label, i, extra) => { const x = el("li"); x.append(el("span", "ct-label", label), signBtn(i)); if (extra) x.appendChild(el("span", "cdy-note", extra)); signs.appendChild(x); };
    const mc = moonChange(d), sc = sunChange(d);
    if (mc) row("Moon in", mc.from, "enters " + SIGN(mc.to).name + " at " + time(mc.date));
    else row("Moon in", Sky.signOf(Sky.moonLon(noon)));
    if (sc) row("Sun in", sc.from, "enters " + SIGN(sc.to).name + " at " + time(sc.date));
    else row("Sun in", Sky.signOf(Sky.sunLon(noon)));
    box.appendChild(signs);
    box.appendChild(el("p", "cdy-moonline", SIGN(Sky.signOf(Sky.moonLon(noon))).moon));

    const list = el("div", "cdy-events");
    evs.forEach(e => {
      if (e.type === "holiday") list.appendChild(holidayCard(e));
      if (e.type === "phase" && e.phase === "full") {
        const c = card("moon", e.name || "Full Moon", (e.blue ? C.full_moons.blue_line : C.phases[4].line));
        list.appendChild(c);
      }
      if (e.type === "phase" && e.eclipse) {
        const E = C.eclipses;
        list.appendChild(card("ecl", E[e.eclipse.body] + " (" + E.kinds[e.eclipse.kind] + ")", E[e.eclipse.body + "_line"], "At " + time(e.date)));
      }
      if (e.type === "mercury") {
        const M = C.mercury;
        list.appendChild(card("merc", e.kind === "retrograde" ? M.retrograde + " begins" : M.direct,
          e.kind === "retrograde" ? M.retrograde_line : M.direct_line, "At " + time(e.date) + ", in " + SIGN(Sky.signOf(e.lon)).name));
      }
    });
    if (sc) list.appendChild(card("sun", C.sun_enters + " " + SIGN(sc.to).name, SIGN(sc.to).text, "At " + time(sc.date), sc.to));
    const rt = retroOn(d);
    if (rt && !evs.some(e => e.type === "mercury")) list.appendChild(card("merc", C.mercury.retrograde, C.mercury.retrograde_line, "Until " + shortDate(rt[1])));
    if (list.children.length) box.appendChild(list);
  }

  function card(kind, title, text, meta, sign) {
    const c = el("article", "cdy-card " + kind);
    c.appendChild(el("h4", null, title));
    if (meta) c.appendChild(el("p", "cdy-meta", meta));
    c.appendChild(el("p", null, text));
    if (sign != null) { const p = el("p", "cdy-more"); p.appendChild(signBtn(sign)); c.appendChild(p); }
    return c;
  }
  function holidayCard(e) {
    const h = e.h, c = el("article", "cdy-card hol");
    c.appendChild(el("h4", null, h.name));
    c.appendChild(el("p", "cdy-meta", h.also + (e.exact ? " · the exact moment is " + time(e.date) : "")));
    c.appendChild(el("p", "cdy-holline", h.line));
    c.appendChild(el("p", null, h.text));
    c.appendChild(el("p", "cdy-small", "Ways to keep it"));
    const ul = el("ul", "cdy-ideas"); h.celebrate.forEach(t => ul.appendChild(el("li", null, t))); c.appendChild(ul);
    const sy = el("p", "cdy-symbols"); sy.append(el("b", null, "Symbols: "), document.createTextNode(h.symbols.join(", "))); c.appendChild(sy);
    const cd = el("p", "cdy-symbols"); cd.append(el("b", null, "Its card: ")); const a = el("a", null, h.card.name); a.href = "/tarot/"; cd.appendChild(a); c.appendChild(cd);
    return c;
  }

  // ---------- a sign, up close
  let lastFocus = null;
  function openSign(i) {
    const s = SIGN(i), box = $("calSignBody");
    lastFocus = document.activeElement; box.innerHTML = "";
    box.appendChild(el("p", "cs-glyph", s.glyph + "︎"));
    const h = el("h3", null, s.name); h.id = "calSignTitle"; box.appendChild(h);
    box.appendChild(el("p", "cs-title", s.title));
    // when the sun travels through this sign this year
    const y = new Date().getFullYear();
    const span = sunSpan(i, y);
    if (span) box.appendChild(el("p", "cs-dates", "The sun travels through " + s.name + " from " + shortDate(span[0]) + " to " + shortDate(addDays(span[1], -1)) + ", " + span[0].getFullYear() + "."));
    box.appendChild(el("p", null, s.text));
    const ul = el("ul", "sp-chips"); s.gifts.forEach(g => ul.appendChild(el("li", null, g))); box.appendChild(ul);
    const facts = el("dl", "cs-facts");
    const fact = (k, v) => { facts.append(el("dt", null, k), el("dd", null, v)); };
    const E = C.elements[s.element];
    fact("Element", s.element[0].toUpperCase() + s.element.slice(1) + ", the suit of " + E.suit + ": " + E.line);
    fact("Mode", C.modes[s.mode]);
    fact("Ruled by", s.ruler);
    const dd = el("dd"); const a = el("a", null, s.card.name); a.href = "/tarot/"; dd.appendChild(a);
    facts.append(el("dt", null, "Its card"), dd);
    fact("Growing edge", s.edge);
    box.appendChild(facts);
    box.appendChild(el("p", "cdy-moonline", s.moon));
    $("calSign").hidden = false; $("calSignClose").focus();
  }
  function sunSpan(i, y) {
    // find the days the sun enters sign i and the next sign, scanning the year
    let a = null, b = null;
    for (let d = new Date(y, 0, 1); d.getFullYear() === y || (a && !b && d.getFullYear() === y + 1); d = addDays(d, 1)) {
      const c = sunChange(d);
      if (c && c.to === i) a = midnight(c.date);
      if (c && c.from === i && a) { b = midnight(c.date); break; }
    }
    if (!a) { // Capricorn: entered last December
      for (let d = new Date(y - 1, 11, 15); d < new Date(y, 0, 1); d = addDays(d, 1)) { const c = sunChange(d); if (c && c.to === i) a = midnight(c.date); }
      for (let d = new Date(y, 0, 1); d < new Date(y, 1, 1); d = addDays(d, 1)) { const c = sunChange(d); if (c && c.from === i) b = midnight(c.date); }
    }
    return a && b ? [a, b] : null;
  }
  function closeSign() { $("calSign").hidden = true; if (lastFocus) lastFocus.focus(); }
  $("calSignClose").addEventListener("click", closeSign);
  $("calSign").addEventListener("click", e => { if (e.target === $("calSign")) closeSign(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("calSign").hidden) closeSign(); });

  // ---------- the wheel of the year, ringed by the zodiac
  function wheel() {
    const now = new Date(), y = year(now.getFullYear());
    const cx = 200, cy = 200;
    const pos = (lon, r) => { const a = (lon - 270) * Math.PI / 180; return [cx + r * Math.sin(a), cy - r * Math.cos(a)]; };
    const NS = "http://www.w3.org/2000/svg";
    const svg = $("calWheel"); svg.innerHTML = "";
    const mk = (tag, attrs, parent) => { const x = document.createElementNS(NS, tag); for (const k in attrs) x.setAttribute(k, attrs[k]); (parent || svg).appendChild(x); return x; };
    mk("circle", { cx, cy, r: 190, class: "w-ring" });
    mk("circle", { cx, cy, r: 152, class: "w-ring" });
    mk("circle", { cx, cy, r: 70, class: "w-hub" });
    for (let i = 0; i < 12; i++) {
      const [x1, y1] = pos(i * 30, 152), [x2, y2] = pos(i * 30, 190);
      mk("line", { x1, y1, x2, y2, class: "w-tick" });
      const [gx, gy] = pos(i * 30 + 15, 171);
      const g = mk("g", { class: "w-sign", tabindex: "0", role: "button", "aria-label": SIGN(i).name });
      mk("circle", { cx: gx, cy: gy, r: 15, class: "w-hit" }, g);
      const t = mk("text", { x: gx, y: gy + 6, "text-anchor": "middle", class: "w-glyph" }, g); t.textContent = SIGN(i).glyph + "︎";
      g.addEventListener("click", () => openSign(i));
      g.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openSign(i); } });
    }
    y.holidays.forEach(ev => {
      const lon = Sky.sunLon(Sky.jdOf(ev.date));
      const [sx, sy] = pos(lon, 70), [ex, ey] = pos(lon, 136);
      mk("line", { x1: sx, y1: sy, x2: ex, y2: ey, class: "w-spoke" + (ev.h.key === "guy-fox" ? " fox" : "") });
      const g = mk("g", { class: "w-hol" + (ev.h.key === "guy-fox" ? " fox" : ""), tabindex: "0", role: "button", "aria-label": ev.h.name + ", " + shortDate(ev.date) });
      mk("circle", { cx: ex, cy: ey, r: ev.h.key === "guy-fox" ? 6 : 9, class: "w-dot" }, g);
      // Guy Fox Day sits five days after Samhain, so its label stacks just under Samhain's
      const fox = ev.h.key === "guy-fox";
      const sam = fox && y.holidays.find(x => x.h.key === "samhain");
      const [lx, ly] = fox && sam ? pos(Sky.sunLon(Sky.jdOf(sam.date)), 110) : pos(lon, 110);
      const t = mk("text", { x: lx, y: ly + (fox ? 17 : 4), "text-anchor": "middle", class: "w-label" + (fox ? " small" : "") }, g);
      t.textContent = fox ? "Guy Fox Day" : ev.h.name;
      const open = () => { go(ev.date); $("calMonth").scrollIntoView({ behavior: "smooth", block: "start" }); };
      g.addEventListener("click", open);
      g.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    });
    // the sun, where it stands today
    const [sx, sy] = pos(Sky.sunLon(Sky.jdOf(now)), 152);
    mk("circle", { cx: sx, cy: sy, r: 9, class: "w-sun" });
    const L = Sky.moonLight(Sky.jdOf(now));
    const hub = mk("g", { transform: `translate(${cx - 34} ${cy - 34}) scale(2.833)` });
    hub.innerHTML = moonSVG(L.fraction, L.waxing, 24).replace(/^<svg[^>]*>|<\/svg>$/g, "");
    // the list beside it
    const ul = $("calWheelList"); ul.innerHTML = "";
    y.holidays.slice().sort((a, b) => a.date - b.date).forEach(ev => {
      const li = el("li"); const b = dateBtn(ev.date, ev.h.name);
      li.append(b, el("span", "wl-date", shortDate(ev.date)), el("span", "wl-line", ev.h.line));
      ul.appendChild(li);
    });
  }

  $("calPrev").addEventListener("click", () => { viewM--; if (viewM < 0) { viewM = 11; viewY--; } drawMonth(); });
  $("calNext").addEventListener("click", () => { viewM++; if (viewM > 11) { viewM = 0; viewY++; } drawMonth(); });
  $("calToday").addEventListener("click", () => go(new Date()));

  tonight();
  go(new Date());
  wheel();
})();
