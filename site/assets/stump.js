/* Reynard's Stump: filter the videos by segment, show them a page at a time, and play one in a lightbox.
   The TikTok or YouTube player loads only after a visitor presses play. */
(function () {
  const $ = id => document.getElementById(id);
  const grid = $("stGrid"), more = $("stMore"), box = $("stPlayer"), frame = $("stFrame");
  const items = Array.from(grid.children);
  const chips = Array.from(document.querySelectorAll(".st-chip"));
  const PAGE = 24;
  let seg = "all", shown = PAGE, lastFocus = null;

  function draw() {
    let list = items.filter(li => seg === "all" || li.dataset.seg === seg);
    if (seg === "tale") list.sort((a, b) => a.dataset.part - b.dataset.part);       // the tale reads in order
    else list.sort((a, b) => (b.dataset.date > a.dataset.date) - (b.dataset.date < a.dataset.date));
    items.forEach(li => { li.hidden = true; });
    list.forEach((li, i) => { li.hidden = i >= shown; grid.appendChild(li); });
    more.hidden = list.length <= shown;
    more.textContent = "Show more (" + (list.length - shown) + " left)";
    document.querySelectorAll(".st-segline").forEach(p => { p.hidden = p.dataset.seg !== seg; });
  }
  chips.forEach(c => c.addEventListener("click", () => {
    seg = c.dataset.seg; shown = PAGE;
    chips.forEach(x => x.setAttribute("aria-pressed", x === c ? "true" : "false"));
    draw();
  }));
  more.addEventListener("click", () => { shown += PAGE; draw(); });

  // ---- the player
  function open(a) {
    lastFocus = a;
    const tt = a.dataset.tt, yt = a.dataset.yt;
    const title = a.querySelector(".st-title").textContent;
    $("stPTitle").textContent = title;
    $("stPSeg").textContent = a.querySelector(".st-seg").textContent;
    const src = yt ? "https://www.youtube-nocookie.com/embed/" + yt + "?autoplay=1&playsinline=1&rel=0&modestbranding=1"
                   : "https://www.tiktok.com/player/v1/" + tt + "?autoplay=1&rel=0&description=0&music_info=0";
    frame.innerHTML = "";
    const f = document.createElement("iframe");
    f.src = src; f.title = title;
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    frame.appendChild(f);
    const links = $("stPLinks"); links.innerHTML = "";
    const link = (href, text) => { const l = document.createElement("a"); l.href = href; l.textContent = text; l.target = "_blank"; l.rel = "noopener"; links.appendChild(l); };
    if (yt) link("https://www.youtube.com/shorts/" + yt, "Watch on YouTube");
    link("https://www.tiktok.com/@chaotic_good_guild/video/" + tt, "Watch on TikTok");
    box.hidden = false;
    $("stClose").focus();
  }
  function close() {
    box.hidden = true; frame.innerHTML = "";          // removing the player stops the sound
    if (lastFocus) lastFocus.focus();
  }
  grid.addEventListener("click", e => {
    const a = e.target.closest(".st-vid");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;   // let people open TikTok in a new tab if they want
    e.preventDefault(); open(a);
  });
  $("stClose").addEventListener("click", close);
  box.addEventListener("click", e => { if (e.target === box) close(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !box.hidden) close(); });

  // a thumbnail that fails to load falls back to the Guild star
  function noThumb(img) { const v = img.closest(".st-vid"); if (v) v.classList.remove("has-thumb"); img.remove(); }
  grid.querySelectorAll(".st-thumb img").forEach(img => {
    if (img.complete && !img.naturalWidth) noThumb(img);
    else img.addEventListener("error", () => noThumb(img));
  });

  draw();
})();
