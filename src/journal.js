/* Your Journal: the readings kept on this device, with your own notes. Nothing here leaves the device. */
(function () {
  const W = JSON.parse(document.getElementById("journal-data").textContent);
  const J = window.CGGJournal;
  const $ = id => document.getElementById(id);
  const el = (tag, cls, text) => { const x = document.createElement(tag); if (cls) x.className = cls; if (text != null) x.textContent = text; return x; };
  const KIND = { daily: "Today's card", spread: "The Chaotic Good Spread", priestess: "The Priestess by Moonlight" };
  const when = iso => new Date(iso).toLocaleString(undefined, { weekday: "short", month: "long", day: "numeric", year: "numeric", hour: "numeric", minute: "2-digit" });
  const list = $("jnList"), empty = $("jnEmpty"), tools = $("jnTools");

  function render() {
    const all = J.all();
    list.innerHTML = "";
    empty.hidden = all.length > 0; tools.hidden = all.length === 0;
    $("jnCount").textContent = all.length === 1 ? "One reading kept." : all.length + " readings kept.";
    all.forEach((e, i) => list.appendChild(entry(e, i)));
    if (location.hash) {
      const t = document.getElementById("e-" + location.hash.slice(1));
      if (t) { t.scrollIntoView({ block: "start" }); t.classList.add("jn-new"); const ta = t.querySelector("textarea"); if (ta) ta.focus({ preventScroll: true }); }
    }
  }

  function entry(e, i) {
    const art = el("article", "jn-entry"); art.id = "e-" + e.id;
    const head = el("header", "jn-head");
    head.append(el("p", "jn-kind", KIND[e.kind] || e.title || "A reading"), el("p", "jn-when", when(e.at)));
    art.appendChild(head);
    const cards = el("ul", "jn-cards");
    (e.cards || []).forEach(c => {
      const li = el("li");
      if (c.pos && e.kind !== "daily") li.appendChild(el("span", "jn-pos", c.pos + ": "));
      li.appendChild(el("b", null, c.name));
      if (c.reversed) li.appendChild(el("span", "jn-rev", " reversed"));
      cards.appendChild(li);
    });
    art.appendChild(cards);
    if (e.reading && e.reading.length) {
      const d = el("details", "jn-reading"); d.appendChild(el("summary", null, e.kind === "daily" ? "The card's meaning" : "Mira's reflection"));
      e.reading.forEach(p => d.appendChild(el("p", null, p)));
      art.appendChild(d);
    }
    const lab = el("label", "jn-notelab");
    lab.appendChild(el("span", null, e.prompt || W.prompts[i % W.prompts.length]));
    const ta = el("textarea", "jn-note"); ta.rows = 4; ta.value = e.note || ""; lab.appendChild(ta);
    const st = el("span", "jn-saved"); st.setAttribute("role", "status");
    let tm = null;
    ta.addEventListener("input", () => { clearTimeout(tm); tm = setTimeout(() => { J.update(e.id, { note: ta.value }); st.textContent = W.saved; setTimeout(() => { st.textContent = ""; }, 1500); }, 500); });
    art.append(lab, st);
    const del = el("button", "sp-ghost jn-del", W.let_go); del.type = "button";
    del.addEventListener("click", () => {
      if (!del.classList.contains("sure")) { del.classList.add("sure"); del.textContent = W.let_go_sure; setTimeout(() => { del.classList.remove("sure"); del.textContent = W.let_go; }, 4000); return; }
      J.remove(e.id); render();
    });
    art.appendChild(del);
    return art;
  }

  $("jnDownload").addEventListener("click", () => {
    const lines = ["Your Chaotic Good Guild journal", "Downloaded " + new Date().toLocaleString(), ""];
    J.all().forEach(e => {
      lines.push("=".repeat(40), (KIND[e.kind] || e.title) + " · " + when(e.at), "");
      (e.cards || []).forEach(c => lines.push("  " + (c.pos && e.kind !== "daily" ? c.pos + ": " : "") + c.name + (c.reversed ? " (reversed)" : "")));
      if (e.reading && e.reading.length) lines.push("", ...e.reading);
      if (e.note) lines.push("", "Your notes:", e.note);
      lines.push("");
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([lines.join("\n")], { type: "text/plain" }));
    a.download = "guild-journal-" + new Date().toISOString().slice(0, 10) + ".txt";
    document.body.appendChild(a); a.click(); a.remove();
  });
  window.addEventListener("hashchange", render);
  render();
})();
