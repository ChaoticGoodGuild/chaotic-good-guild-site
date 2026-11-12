"""Builds the tarot room (/tarot/): The Chaotic Good Spread, plus every card as an SVG at /tarot/cards/<id>.svg.

Edit the spread's positions, questions and prompts in src/spread.json; its behavior in src/spread.js.
Card art comes from tools/deck.py.
"""
import json, os
import build as B
import deck
import cards as K



def build(p):
    SPREAD = json.load(open(os.path.join(B.SRC, "spread.json")))
    e = B.e
    meta, defs = deck.export(os.path.join(B.SITE, "tarot", "cards"))
    back = K.card_back()
    path = "/tarot/"
    desc = ("The Chaotic Good Spread: shuffle the Guild's own tarot deck and lay six cards in the shape of the Guild star. "
            "Galleons, Lutes, Quills and Mirrors, with Reynard, Mira and the rats of the Guild.")
    ld = B.jsonld({"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": desc,
                   "url": B.DOMAIN + path, "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"}})
    MEAN = json.load(open(os.path.join(B.SRC, "meanings.json")))
    cards = []
    for c in meta:
        m = MEAN[c["id"]]
        cards.append({"id": c["id"], "name": c["name"], "suit": c["suit"], "rank": c["rank"], "scene": c["scene"],
                      "keywords": m["keywords"], "meaning": m["meaning"], "question": m["question"], "tone": m["tone"]})
    data = json.dumps({k: SPREAD[k] for k in ("positions", "card_width", "prompts", "suits", "numbers", "reflection", "reversed")} | {"cards": cards})
    pos = SPREAD["positions"]
    outer = pos[:5]
    segs = "".join(f'<line class="sp-seg" pathLength="1" x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}"/>'
                   for a, b in zip(outer, outer[1:] + outer[:1]))
    cx, cy = pos[5]["x"], pos[5]["y"]
    page = B.head(f"{p['title']} · {B.NAME}", desc, path, p["slug"], ld)
    page += f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>

<main class="sp">
  <section class="sp-intro">
    <p class="who">{e(p['who'])}</p>
    <h1>{e(p['title'])}</h1>
    <p class="desc">{e(p['desc'])}</p>
  </section>

  <p class="sp-prompt" id="spPrompt" aria-live="polite">{e(SPREAD['prompts']['idle'])}</p>
  <div class="sp-stage" id="spStage">
    <svg class="sp-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <circle class="sp-ring" pathLength="1" cx="{cx}" cy="{cy}" r="39"/>{segs}
    </svg>
    <div class="sp-tip" id="spTip" role="tooltip" hidden></div>
    <button type="button" class="sp-deck idle" id="spDeck" style="left:{cx}%;top:{cy}%;width:{SPREAD['card_width']}%" aria-label="The deck. Touch to shuffle."></button>
  </div>
  <div class="sp-actions">
    <button type="button" class="back-btn" id="spAll" hidden>Turn them all</button>
    <button type="button" class="back-btn" id="spRead" hidden>Read Mira's reading &darr;</button>
    <button type="button" class="sp-ghost" id="spAgain" hidden>Shuffle again</button>
  </div>
  <noscript><p class="raising">The spread needs JavaScript turned on.</p></noscript>

  <section class="sp-summary" id="spSummary" hidden aria-labelledby="spSumTitle">
    <h2 class="sp-h" id="spSumTitle">Mira's reading</h2>
    <p class="sp-sumlede">A story for reflection, not a fortune.</p>
    <div class="sp-sumtext" id="spSummaryText"></div>
    <details class="sp-how"><summary>How Mira read this</summary><ul id="spNotes"></ul>
      <p class="sp-howend">These are the threads Mira pulled this time. With practice you'll find your own.</p></details>
  </section>

  <h2 class="sp-h">Card by card</h2>
  <ol class="sp-list" id="spList"></ol>

  <div class="sp-light" id="spLight" role="dialog" aria-modal="true" aria-labelledby="spLightTitle" hidden>
    <div class="sp-lightbox">
      <div class="sp-lightcard" id="spLightCard"></div>
      <div class="sp-lighttext">
        <p class="sp-pos" id="spLightPos"></p>
        <h3 id="spLightTitle"></h3>
        <p class="sp-rev" id="spLightTag" hidden>Reversed</p>
        <div id="spLightKw"></div>
        <p class="sp-scene" id="spLightScene"></p>
        <p id="spLightMeaning"></p>
        <p class="sp-revnote" id="spLightRev" hidden></p>
        <p class="sp-counsel"><b>Reflect: </b><span id="spLightCounsel"></span></p>
        <button type="button" class="sp-ghost" id="spLightClose">Close</button>
      </div>
    </div>
  </div>
  <template id="spBackTpl">{back}</template>

  <h2 class="places-h">Other paths</h2>
  {B.directory(exclude=p['slug'])}
</main>

{B.foot()}<script type="application/json" id="spread-data">{data}</script>
<script src="/assets/spread.js"></script>
</body>
</html>
"""
    B.write("tarot/index.html", page)
    B.write("assets/spread.js", open(os.path.join(B.SRC, "spread.js")).read())
    write_review_doc()


def write_review_doc():
    """docs/card-meanings.md: every card's meaning in one readable list, marked by who wrote it."""
    T = json.load(open(os.path.join(B.SRC, "tarot.json")))
    M = json.load(open(os.path.join(B.SRC, "meanings.json")))
    heads = {"major": "Major Arcana", "galleons": "Galleons", "lutes": "Lutes", "quills": "Quills", "mirrors": "Mirrors"}
    mine = sum(1 for c in T if M[c["id"]]["source"] == "ryan")
    out = ["# Card meanings", "",
           f"{mine} meanings come from Ryan's Tarot Deck Notes (marked **Ryan**); the other {len(T) - mine} are drafts by Claude "
           "(marked **Draft**) to rewrite in Ryan's own words. The reflection questions are Claude's drafts from Ryan's counsel.",
           "", "Edit them in `src/meanings.json`. `tone` (light, mixed, shadow) helps the reading summary.", ""]
    cur = None
    for c in T:
        if c["suit"] != cur:
            cur = c["suit"]; out += [f"## {heads[cur]}", ""]
        m = M[c["id"]]
        out += [f"### {c['name']} ({'Ryan' if m['source'] == 'ryan' else 'Draft'}, {m['tone']})", "",
                f"*Scene:* {c['scene']}", "", f"*Keywords:* {', '.join(m['keywords'])}", "",
                f"*Meaning:* {m['meaning']}", "", f"*Counsel:* {m['counsel']}", "", f"*Reflect:* {m['question']}", ""]
    open(os.path.join(B.ROOT, "docs", "card-meanings.md"), "w").write("\n".join(out))
