"""Builds the alignment test page (/alignment-test/) and one page per result (/alignment-test/<alignment>/).

Edit the statements, scale and result text in src/alignment.json.
Edit the test's behavior in src/alignment.js. Result portraits live in src/alignments/.
"""
import json, os, shutil
import build as B

DATA = json.load(open(os.path.join(B.SRC, "alignment.json")))
GRID = [["lawful-good", "neutral-good", "chaotic-good"],
        ["lawful-neutral", "true-neutral", "chaotic-neutral"],
        ["lawful-evil", "neutral-evil", "chaotic-evil"]]
e = B.e

# Lawful red, Chaotic gold, Good purple, Evil black, Neutral silver
ETHIC = {"lawful": "#e0283f", "neutral": "#cfc8dc", "chaotic": "#e9d701"}
MORAL = {"good": "#b06cff", "neutral": "#cfc8dc", "evil": "#000000"}


def tones(slug):
    if slug == "true-neutral":
        return "#cfc8dc", "#cfc8dc"
    a, b = slug.split("-")
    return ETHIC[a], MORAL[b]


def glow(slug):
    """Portrait aura: black for Evil, purple for Good, otherwise the law/chaos color."""
    if slug.endswith("-evil"):
        return "#000000f2"
    if slug.endswith("-good"):
        return "#c58bffbb"
    return tones(slug)[0] + "99"


def tone_style(slug):
    c1, c2 = tones(slug)
    return f'style="--c1:{c1};--c2:{c2}"'


NOTICE = ("For fun and self-reflection. This isn't a psychological assessment or a diagnosis. "
          "Your answers never leave your device: the Guild doesn't send, collect or store them.")


def grid_html():
    cells = "".join(f'<a class="at-cell" data-slug="{s}" href="/alignment-test/{s}/"><span>{e(DATA["results"][s]["name"])}</span></a>'
                    for row in GRID for s in row)
    return f"""<div class="at-gridwrap">
  <span class="at-axis at-axis-top">Good</span><span class="at-axis at-axis-bottom">Evil</span>
  <span class="at-axis at-axis-left">Lawful</span><span class="at-axis at-axis-right">Chaotic</span>
  <div class="at-grid">{cells}<span class="at-marker" id="atMarker" aria-hidden="true"></span></div>
</div>"""


def header():
    return f"""
<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>
"""


def build(p):
    w, h = p["view"][2], p["view"][3]
    n = len(DATA["items"])
    path = "/alignment-test/"
    desc = ("Are you Reynard or the Corporate Wolf? A free alignment test from the Chaotic Good Guild: "
            f"{n} statements place you between Lawful and Chaotic, Good and Evil.")
    ld = B.jsonld({"@context": "https://schema.org", "@type": "WebPage", "name": "The Chaotic Good Guild Alignment Test",
                   "description": desc, "url": B.DOMAIN + path,
                   "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"}})
    data = json.dumps({k: DATA[k] for k in ("version", "scale", "neutral_band", "items", "results")})
    page = B.head(f"The Alignment Test · {B.NAME}", desc, path, p["slug"], ld)
    page += header() + f"""
<main class="at">
  <section class="room-hero" id="atIntro">
    <figure class="vignette">
      <img src="/assets/village.svg#v-{p['slug']}" alt="{e(p['who'])}" width="{w}" height="{h}">
    </figure>
    <div>
      <p class="who">{e(p['who'])}</p>
      <h1>{e(p['title'])}</h1>
      <p class="desc">{e(p['desc'])}</p>
      <p class="at-facts"><span>{n} statements</span><span>About 5 minutes</span><span>Nothing leaves your device</span></p>
      <div class="at-actions">
        <button type="button" class="back-btn" id="atStart">Begin the test &rarr;</button>
      </div>
      <p class="at-prev" id="atPrev" hidden>Your last result: <b id="atPrevName"></b>. <button type="button" class="at-link" id="atPrevShow">See it again</button></p>
      <p class="at-notice">{e(NOTICE)}</p>
      <noscript><p class="raising">This test needs JavaScript turned on. You can still read about the nine alignments below.</p></noscript>
    </div>
  </section>

  <section class="at-quiz" id="atQuiz" hidden aria-live="polite"><div class="at-card">
    <div class="at-progress" id="atProgress" role="progressbar" aria-label="Progress" aria-valuemin="0" aria-valuemax="{n}" aria-valuenow="0"><span id="atBar"></span></div>
    <p class="at-count" id="atCount"></p>
    <p class="at-statement" id="atStatement"></p>
    <div class="at-scale" id="atScale" role="group" aria-label="How much do you agree?"></div>
    <div class="at-nav">
      <button type="button" class="at-link" id="atBack">&larr; Previous statement</button>
      <span class="at-tip">Tip: press 1 to 5 on your keyboard</span>
      <button type="button" class="at-link" id="atQuit">Leave the test</button>
    </div>
  </div></section>

  <section class="at-result" id="atResult" hidden>
    <figure class="at-portrait"><img id="atResImg" src="" alt="" width="600" height="800"></figure>
    <div class="at-res-body">
      <p class="who" id="atResEyebrow">Your alignment</p>
      <h1 id="atResTitle"></h1>
      <p class="at-host">In the Guild's tale, you walk with <b id="atResHost"></b></p>
      <p class="at-res-desc" id="atResDesc"></p>
      <dl class="at-axes">
        <div><dt>Law and chaos</dt><dd><span id="atOrder"></span><span class="at-meter" aria-hidden="true"><i id="atOrderFill"></i></span><span class="at-meter-ends" aria-hidden="true"><span style="color:var(--law)">Lawful</span><span style="color:var(--chaos)">Chaotic</span></span></dd></div>
        <div><dt>Good and evil</dt><dd><span id="atHeart"></span><span class="at-meter heart" aria-hidden="true"><i id="atHeartFill"></i></span><span class="at-meter-ends" aria-hidden="true"><span class="at-evil">Evil</span><span style="color:var(--good)">Good</span></span></dd></div>
      </dl>
      {grid_html()}
      <div class="at-actions">
        <button type="button" class="back-btn" id="atShare">Share my result</button>
        <button type="button" class="at-ghost" id="atAgain">Take it again</button>
        <a class="at-ghost" id="atReadMore" href="#">Read more</a>
      </div>
      <p class="at-sharenote" id="atShareNote" role="status"></p>
      <aside class="at-hall">
        <h2>The Guild Hall awaits</h2>
        <p>Soon you'll be able to carry this alignment into the Guild Hall, where it shapes the class you're sorted into.</p>
        <a class="at-link" href="/guild-hall/">Visit the Guild Hall &rarr;</a>
      </aside>
      <p class="at-notice">{e(NOTICE)} This browser remembers only your final result, so the Guild Hall can offer it to you later. <button type="button" class="at-link" id="atForget">Forget my result</button> <span id="atForgetNote" role="status"></span></p>
    </div>
  </section>

  <h2 class="places-h" style="margin-top:0">The nine alignments</h2>
  <ul class="places at-nine">{''.join(f'<li><a href="/alignment-test/{s}/" {tone_style(s)}><span class="t">{e(r["name"])}</span><span class="w">{e(r["host"])}</span></a></li>' for s, r in ((s, DATA["results"][s]) for row in GRID for s in row))}</ul>
</main>

{B.foot()}<script type="application/json" id="alignment-data">{data}</script>
<script src="/assets/alignment.js"></script>
</body>
</html>
"""
    B.write("alignment-test/index.html", page)
    B.write("assets/alignment.js", open(os.path.join(B.SRC, "alignment.js")).read())
    for row in GRID:
        for slug in row:
            build_result(slug)
    write_review_doc()


def build_result(slug):
    r = DATA["results"][slug]
    path = f"/alignment-test/{slug}/"
    first = r["desc"].split(". ")[0].rstrip(".") + "."
    desc = f"{r['name']} in the Chaotic Good Guild: {first}"
    os.makedirs(os.path.join(B.SITE, "alignment-test", slug), exist_ok=True)
    shutil.copy(os.path.join(B.SRC, "alignments", slug + ".jpg"),
                os.path.join(B.SITE, "alignment-test", slug, "portrait.jpg"))
    ld = B.jsonld({"@context": "https://schema.org", "@type": "WebPage", "name": f"{r['name']} · Alignment",
                   "description": desc, "url": B.DOMAIN + path,
                   "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"}})
    page = B.head(f"{r['name']} · The Alignment Test · {B.NAME}", desc, path, "alignment-test", ld)
    page = page.replace(f"{B.DOMAIN}/assets/share/alignment-test.jpg", f"{B.DOMAIN}{path}portrait.jpg")
    others = "".join(f'<li><a href="/alignment-test/{s}/" {tone_style(s)}><span class="t">{e(DATA["results"][s]["name"])}</span>'
                     f'<span class="w">{e(DATA["results"][s]["host"])}</span></a></li>'
                     for row in GRID for s in row if s != slug)
    page += header() + f"""
<main class="at">
  <section class="at-result">
    <figure class="at-portrait" style="--tint:{glow(slug)}"><img src="portrait.jpg" alt="{e(r['host'])}, {e(r['name'])}" width="600" height="800"></figure>
    <div class="at-res-body">
      <p class="who">An alignment of the Guild</p>
      <h1>{e(r['name'])}</h1>
      <p class="at-host">In the Guild's tale, {e(r['name'])} walks with <b>{e(r['host'])}</b></p>
      <p class="at-res-desc">{e(r['desc'])}</p>
      {grid_html().replace(f'data-slug="{slug}"', f'data-slug="{slug}" aria-current="page"').replace('class="at-cell" data-slug="' + slug + '"', 'class="at-cell is-you" data-slug="' + slug + '"').replace('<span class="at-marker" id="atMarker" aria-hidden="true"></span>', '')}
      <div class="at-actions">
        <a class="back-btn" href="/alignment-test/">Find your own alignment &rarr;</a>
      </div>
    </div>
  </section>
  <h2 class="places-h" style="margin-top:0">The other eight</h2>
  <ul class="places at-nine">{others}</ul>
</main>

{B.foot()}</body>
</html>
"""
    B.write(f"alignment-test/{slug}/index.html", page)


def write_review_doc():
    """docs/alignment-items.md: a readable list of every statement for review and rewriting."""
    lines = ["# Alignment test statements (Version 1, draft)", "",
             "Drafted by Claude for Ryan to review and rewrite in his own words. Edit them in `src/alignment.json`.",
             "", "Scale: " + " / ".join(f"{s['label']} ({s['value']:+d})" for s in DATA["scale"]), "",
             "**Direction** says which way *agreeing* pushes the score.", ""]
    for axis, title, pos, neg in (("order", "Law and chaos", "Chaotic", "Lawful"), ("heart", "Good and evil", "Good", "Evil")):
        lines += [f"## {title}", "", "| ID | Statement | Direction |", "|---|---|---|"]
        for it in DATA["items"]:
            if it["axis"] == axis:
                lines.append(f"| {it['id']} | {it['text']} | {pos if it['key'] > 0 else neg} |")
        lines.append("")
    lines += ["## Scoring", "",
              "Each axis score is the sum of (answer x direction) divided by the maximum possible, giving -1 to +1.",
              f"Scores within {DATA['neutral_band']} of zero count as Neutral on that axis. Both axes Neutral = True Neutral.",
              "Agreeing with every statement lands exactly at True Neutral, because each axis has 8 statements keyed each way.", ""]
    path = os.path.join(B.ROOT, "docs", "alignment-items.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(lines))
