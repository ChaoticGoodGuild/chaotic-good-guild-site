"""Builds The Raising (/about/): what the Guild is for, what Chaotic Good means, why a fox, the cast, and how to join.

Words live in src/about.json (drafts for Ryan to rewrite). The cast portraits are drawn from tools/characters.py,
the same code that draws the tarot deck, so everyone looks the same here as on the cards.
"""
import html, json, os
import build as B
import scene
import characters as C
import model_sheets as M

E = html.escape
ALIGN = [["lawful-good", "neutral-good", "chaotic-good"], ["lawful-neutral", "true-neutral", "chaotic-neutral"],
         ["lawful-evil", "neutral-evil", "chaotic-evil"]]
ETHIC = {"lawful": "#e0283f", "neutral": "#cfc8dc", "chaotic": "#e9d701", "true": "#cfc8dc"}
MORAL = {"good": "#b06cff", "neutral": "#cfc8dc", "evil": "#000000"}


def portrait(key):
    draw = {"reynard": lambda: C.reynard("grin", pose="lute"), "mira": lambda: C.mira("happy"), "badger": lambda: C.badger("happy"),
            "bull": lambda: C.bull("determined"), "rat": lambda: C.rat("happy", "hero"), "lion": lambda: C.lion("smug"),
            "wolf": lambda: C.wolf("greedy")}[key]
    return M.char_svg(key, draw(), M.BOX[key], pad=10, cls="ab-fig")


def red_city_rats():
    """Two rats of The Red City: one in the Wolf's suit and tie, one dressed for a break-in."""
    box = (-72, -198, 172, 198)
    return "".join(M.char_svg("rat", g, box, pad=8, cls="ab-fig") for g in (C.rat("smug", "suit"), C.rat("smug", "crook")))


def paras(ps):
    return "".join(f"<p>{E(p)}</p>" for p in ps)


def grid():
    cells = []
    for row in ALIGN:
        for slug in row:
            a, b = slug.split("-")
            name = "True Neutral" if slug == "true-neutral" else f"{a.title()} {b.title()}"
            cells.append(f'<a class="ab-cell{" home" if slug == "chaotic-good" else ""}" href="/alignment-test/{slug}/" '
                         f'style="--c1:{ETHIC[a]};--c2:{MORAL[b]}">{E(name)}</a>')
    return ('<div class="ab-grid" role="group" aria-label="The nine alignments">'
            '<span class="ab-axis x">Lawful &larr; &rarr; Chaotic</span><span class="ab-axis y">Good &uarr; &darr; Evil</span>'
            + "".join(cells) + "</div>")


def build(p):
    A = json.load(open(os.path.join(B.SRC, "about.json"), encoding="utf-8"))
    V = json.load(open(os.path.join(B.SRC, "videos.json"), encoding="utf-8"))
    ch = V["channels"]
    path = "/about/"
    desc = ("The Chaotic Good Guild: rebellion through kindness. What Chaotic Good means, why Reynard the Fox, "
            "the Guild's creed and cast, and how to lend a hand.")
    ld = B.jsonld([
        {"@context": "https://schema.org", "@type": "AboutPage", "name": p["title"], "description": desc, "url": B.DOMAIN + path,
         "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"}},
        {"@context": "https://schema.org", "@type": "Organization", "name": B.NAME, "url": B.DOMAIN + "/",
         "logo": B.DOMAIN + "/assets/logo.png", "slogan": A["creed"]["motto"], "description": " ".join(A["raising"]["paras"][:2]),
         "sameAs": [ch["tiktok"], ch["youtube"]]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in A["faq"]]}])
    defs = scene.DEFS.replace("</defs>", C.EXTRA_DEFS + "</defs>")
    w, h = p["view"][2], p["view"][3]
    cr = A["creed"]
    tenets = "".join(f'<li><h3>{E(t["name"])}</h3><p>{E(t["text"])}</p></li>' for t in cr["tenets"])

    def card(c, foe=False):
        art = red_city_rats() if c["key"] == "rats" else portrait(c["key"])
        return (f'<li class="ab-card{" foe" if foe else ""}{" pair" if c["key"] == "rats" else ""}"><div class="ab-port">{art}</div>'
                f'<div><h3>{E(c["name"])}</h3><p class="ab-align">{E(c["align"])}</p><p>{E(c["text"])}</p></div></li>')
    cast = A["cast"]
    faq = "".join(f'<details class="ab-faq"><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in A["faq"])

    page = B.head(f"{p['title']} · {B.NAME}", desc, path, p["slug"], ld)
    page += f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>

<main class="ab">
  <section class="room-hero">
    <figure class="vignette">
      <img src="/assets/village.svg#v-{p['slug']}" alt="{E(p['who'])}" width="{w}" height="{h}">
    </figure>
    <div>
      <p class="who">{E(p['who'])}</p>
      <h1>{E(p['title'])}</h1>
      <p class="desc">{E(p['desc'])}</p>
      <p class="ab-lede">{E(A['lede'])}</p>
    </div>
  </section>

  <section class="ab-sec ab-raising">
    <div class="ab-text">
      <h2 class="places-h">{E(A['raising']['title'])}</h2>
      {paras(A['raising']['paras'])}
    </div>
    <div class="ab-bull">{portrait('bull')}</div>
  </section>

  <section class="ab-sec ab-creed" aria-labelledby="abCreed">
    <h2 class="places-h" id="abCreed">{E(cr['title'])}</h2>
    <p class="ab-lines">{"".join(f"<span>{E(l)}</span>" for l in cr['lines'])}</p>
    <p class="ab-motto">{E(cr['motto'])}</p>
    <ul class="ab-tenets">{tenets}</ul>
  </section>

  <section class="ab-sec ab-cg">
    <div class="ab-text">
      <h2 class="places-h">{E(A['chaotic_good']['title'])}</h2>
      {paras(A['chaotic_good']['paras'])}
    </div>
    <div>
      {grid()}
      <p class="ab-gridnote">{E(A['chaotic_good']['grid_note'])} <a href="/alignment-test/">Take the test.</a></p>
    </div>
  </section>

  <section class="ab-sec ab-fox">
    <figure class="ab-foxart ab-photo"><img src="/assets/reynard-market.jpg" alt="{E(A['why_fox']['image_alt'])}" width="475" height="570" loading="lazy"></figure>
    <div class="ab-text">
      <h2 class="places-h">{E(A['why_fox']['title'])}</h2>
      {paras(A['why_fox']['paras'])}
    </div>
  </section>

  <section class="ab-sec" aria-labelledby="abCast">
    <h2 class="places-h" id="abCast">{E(cast['title'])}</h2>
    <ul class="ab-cast">{"".join(card(c) for c in cast['folk'])}</ul>
    <h3 class="ab-foes-h">{E(cast['foes_title'])}</h3>
    <p class="ab-foes-note">{E(cast['foes_note'])}</p>
    <ul class="ab-cast foes">{"".join(card(c, True) for c in cast['foes'])}</ul>
  </section>

  <section class="ab-sec ab-vessel">
    <h2 class="places-h">{E(A['vessel']['title'])}</h2>
    {paras(A['vessel']['paras'])}
  </section>

  <section class="ab-sec" aria-labelledby="abFaq">
    <h2 class="places-h" id="abFaq">Questions at the raising</h2>
    {faq}
  </section>

  <h2 class="places-h">Other paths</h2>
  {B.directory(exclude=p['slug'])}
  <p class="ab-fine">{E(A['fine'])}</p>
</main>

{B.foot()}</body>
</html>
"""
    B.write("about/index.html", page)
    B.write("assets/reynard-market.jpg", open(os.path.join(B.SRC, "reynard-market.jpg"), "rb").read(), binary=True)
