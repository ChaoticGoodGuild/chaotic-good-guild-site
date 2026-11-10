/* Chaotic Good Guild alignment test, Version 1.
   Everything happens in the visitor's browser. Nothing is sent anywhere.
   The only thing kept is the final result, in this browser's own storage,
   so the Guild Hall can offer to carry it into a profile later. */

// ---------- Scoring (pure functions) ----------
const CGGScore = {
  // answers: array of numbers (-2..2) or null, same order as items
  axisScore(items, answers, axis) {
    let sum = 0, n = 0;
    items.forEach((it, i) => {
      if (it.axis !== axis) return;
      n++;
      const a = answers[i];
      if (typeof a === "number") sum += a * it.key;
    });
    return n ? sum / (n * 2) : 0; // -1..1
  },
  // x: order axis (-1 Lawful .. +1 Chaotic); y: heart axis (-1 Evil .. +1 Good)
  label(x, y, band) {
    const ethic = x <= -band ? "lawful" : x >= band ? "chaotic" : "neutral";
    const moral = y >= band ? "good" : y <= -band ? "evil" : "neutral";
    if (ethic === "neutral" && moral === "neutral") return "true-neutral";
    return ethic + "-" + moral;
  },
  score(data, answers) {
    const x = CGGScore.axisScore(data.items, answers, "order");
    const y = CGGScore.axisScore(data.items, answers, "heart");
    return { x, y, slug: CGGScore.label(x, y, data.neutral_band) };
  },
  // Plain-language reading of one axis
  lean(v, neg, pos, band) {
    const pct = Math.round(Math.abs(v) * 100);
    if (Math.abs(v) < band) return "Balanced between " + neg + " and " + pos;
    return pct + "% toward " + (v < 0 ? neg : pos);
  }
};
if (typeof module !== "undefined") module.exports = CGGScore;

// ---------- Page ----------
(function () {
  if (typeof document === "undefined") return;
  const DATA = JSON.parse(document.getElementById("alignment-data").textContent);
  const ITEMS = DATA.items, N = ITEMS.length, BAND = DATA.neutral_band;
  const STORE = "cgg.alignment";
  const $ = id => document.getElementById(id);
  const intro = $("atIntro"), quiz = $("atQuiz"), result = $("atResult");
  let answers = new Array(N).fill(null), idx = 0;

  const store = {
    get() { try { return JSON.parse(localStorage.getItem(STORE)); } catch (e) { return null; } },
    set(v) { try { localStorage.setItem(STORE, JSON.stringify(v)); } catch (e) {} },
    clear() { try { localStorage.removeItem(STORE); } catch (e) {} }
  };

  function show(section) {
    [intro, quiz, result].forEach(s => { s.hidden = s !== section; });
    window.scrollTo({ top: Math.max(0, document.querySelector("main").offsetTop - 8), behavior: "smooth" });
  }

  // Previous result reminder on the intro
  const prev = store.get();
  if (prev && DATA.results[prev.slug]) {
    const box = $("atPrev");
    box.hidden = false;
    $("atPrevName").textContent = DATA.results[prev.slug].name;
    $("atPrevShow").addEventListener("click", () => renderResult(prev.x, prev.y, prev.slug, false));
  }

  // Quiz
  const scaleBox = $("atScale");
  DATA.scale.forEach((s, k) => {
    const b = document.createElement("button");
    b.type = "button"; b.className = "at-opt"; b.dataset.value = s.value;
    b.innerHTML = '<span class="at-key">' + (k + 1) + "</span><span></span>";
    b.lastChild.textContent = s.label;
    b.addEventListener("click", () => choose(s.value));
    scaleBox.appendChild(b);
  });

  function renderQ() {
    const it = ITEMS[idx];
    $("atCount").textContent = "Statement " + (idx + 1) + " of " + N;
    $("atBar").style.width = (idx / N * 100).toFixed(1) + "%";
    $("atProgress").setAttribute("aria-valuenow", idx);
    const q = $("atStatement");
    q.textContent = it.text;
    q.classList.remove("at-in"); void q.offsetWidth; q.classList.add("at-in");
    scaleBox.querySelectorAll(".at-opt").forEach(b => {
      b.setAttribute("aria-pressed", String(Number(b.dataset.value) === answers[idx]));
    });
    $("atBack").disabled = idx === 0;
  }
  function choose(v) {
    answers[idx] = v;
    if (idx < N - 1) { idx++; renderQ(); }
    else finish();
  }
  function finish() {
    $("atBar").style.width = "100%";
    const r = CGGScore.score(DATA, answers);
    store.set({ slug: r.slug, x: +r.x.toFixed(3), y: +r.y.toFixed(3), version: DATA.version, date: new Date().toISOString().slice(0, 10) });
    renderResult(r.x, r.y, r.slug, true);
  }
  function start() {
    answers = new Array(N).fill(null); idx = 0;
    show(quiz); renderQ();
    scaleBox.querySelector(".at-opt").focus({ preventScroll: true });
  }

  $("atStart").addEventListener("click", start);
  $("atBack").addEventListener("click", () => { if (idx > 0) { idx--; renderQ(); } });
  $("atQuit").addEventListener("click", () => show(intro));
  document.addEventListener("keydown", e => {
    if (quiz.hidden || e.altKey || e.ctrlKey || e.metaKey) return;
    const k = Number(e.key);
    if (k >= 1 && k <= DATA.scale.length) { e.preventDefault(); choose(DATA.scale[k - 1].value); }
    else if (e.key === "Backspace" || e.key === "ArrowLeft") { if (idx > 0) { e.preventDefault(); idx--; renderQ(); } }
  });

  // Result
  function renderResult(x, y, slug, fresh) {
    const res = DATA.results[slug];
    $("atResTitle").textContent = res.name;
    $("atResHost").textContent = res.host;
    $("atResDesc").textContent = res.desc;
    const img = $("atResImg");
    img.src = "/alignment-test/" + slug + "/portrait.jpg";
    img.alt = res.host + ", " + res.name;
    $("atResEyebrow").textContent = fresh ? "Your alignment" : "Your last alignment";
    $("atOrder").textContent = CGGScore.lean(x, "Lawful", "Chaotic", BAND);
    $("atHeart").textContent = CGGScore.lean(y, "Evil", "Good", BAND);
    meter($("atOrderFill"), x, "var(--law)", "var(--chaos)");
    meter($("atHeartFill"), y, "var(--evil)", "var(--good)");
    // Portrait aura: black for Evil, purple for Good, otherwise the law/chaos color
    const [eth, mor] = slug === "true-neutral" ? ["neutral", "neutral"] : slug.split("-");
    const tint = mor === "evil" ? "#000000f2" : mor === "good" ? "#c58bffbb"
      : ({ lawful: "#e0283f", chaotic: "#e9d701" }[eth] || "#cfc8dc") + "99";
    $("atResImg").parentNode.style.setProperty("--tint", tint);
    // grid marker: x -1..1 left->right, y +1..-1 top->bottom
    const m = $("atMarker");
    m.style.left = ((x + 1) / 2 * 100).toFixed(1) + "%";
    m.style.top = ((1 - y) / 2 * 100).toFixed(1) + "%";
    document.querySelectorAll(".at-cell").forEach(c => c.classList.toggle("is-you", c.dataset.slug === slug));
    $("atReadMore").href = "/alignment-test/" + slug + "/";
    result.dataset.slug = slug;
    show(result);
  }

  // Axis meter: fills outward from the center toward the side you lean
  function meter(el, v, negColor, posColor) {
    const w = Math.abs(v) * 50;
    el.style.left = (v < 0 ? 50 - w : 50) + "%";
    el.style.width = Math.max(w, 1.5) + "%";
    el.style.background = Math.abs(v) < BAND ? "var(--neu)" : (v < 0 ? negColor : posColor);
    el.style.color = el.style.background;
  }

  // Share
  $("atShare").addEventListener("click", async () => {
    const slug = result.dataset.slug, res = DATA.results[slug];
    const url = location.origin + "/alignment-test/" + slug + "/";
    const text = "I'm " + res.name + " on the Chaotic Good Guild alignment test. Where do you land?";
    const note = $("atShareNote");
    try {
      if (navigator.share) { await navigator.share({ title: "Chaotic Good Guild alignment test", text, url }); return; }
      await navigator.clipboard.writeText(text + " " + url);
      note.textContent = "Link copied. Paste it anywhere.";
    } catch (e) {
      if (e && e.name === "AbortError") return;
      note.textContent = "Copy this link: " + url;
    }
  });
  $("atAgain").addEventListener("click", start);
  $("atForget").addEventListener("click", () => {
    store.clear();
    $("atPrev").hidden = true;
    $("atForgetNote").textContent = "Forgotten. This browser no longer remembers your result.";
  });
})();
