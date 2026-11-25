"""The secret full-moon reading (/tarot/priestess/): The High Priestess Spread, in an enchanted forest.

Not linked from the menus, the sitemap or llms.txt. The tarot page shows a small moon that leads here, but only on the day of the
full moon (src/moonwindow.js). Words in src/priestess.json; behavior in src/priestess.js.
Preview it outside a full moon at /tarot/priestess/?preview=fullmoon
"""
import json, os, random
import build as B

PATH = "/tarot/priestess/"


def pillar(x, dark, letter):
    """One of the Priestess's pillars, for the table behind cards 6 and 7 (x is the centre, in table units of 640 x 750)."""
    body, edge, ink = ("#0b1414", "#2c4a4a", "#d9f2ee") if dark else ("#dfeee9", "#9fc7c0", "#0b1414")
    return f"""<g class="hp-pillar" opacity=".62">
    <rect x="{x - 46}" y="196" width="92" height="300" rx="4" fill="{body}" stroke="{edge}" stroke-width="3"/>
    <rect x="{x - 58}" y="176" width="116" height="26" rx="6" fill="{body}" stroke="{edge}" stroke-width="3"/>
    <path d="M{x - 52} 176 q 52 -40 104 0" fill="{body}" stroke="{edge}" stroke-width="3"/>
    <rect x="{x - 58}" y="492" width="116" height="22" rx="5" fill="{body}" stroke="{edge}" stroke-width="3"/>
    <text x="{x}" y="160" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="30" fill="{ink}">{letter}</text>
  </g>"""


def pomegranate(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 -14 q10 -10 20 0" fill="none" stroke="#3f8f62" stroke-width="3"/>'
            f'<circle r="11" fill="#b2324a"/><path d="M-4 -11 l4 -6 l4 6" fill="#e3a33c"/><circle cx="-3" cy="-2" r="2.4" fill="#e7697d"/></g>')


def veil_pattern():
    return ('<pattern id="hpVeil" width="80" height="80" patternUnits="userSpaceOnUse">'
            '<rect width="80" height="80" fill="#0f2f33"/>'
            '<path d="M40 64 q-14 -20 0 -44 q14 24 0 44" fill="#1f5a4a"/><path d="M40 64 v-44" stroke="#2f7a5f" stroke-width="2"/>'
            + pomegranate(14, 18, .8) + pomegranate(66, 58, .8) + '</pattern>')


def table_art():
    """The Priestess, drawn under the cards: her veil, her pillars, three moons, the crescent at her feet."""
    moon = lambda x, y, kind: {
        "wax": f'<g transform="translate({x} {y})"><circle r="15" fill="#cfe8ef"/><circle cx="-8" r="15" fill="#0b1a20"/></g>',
        "full": f'<circle cx="{x}" cy="{y}" r="16" fill="#eef8fb"/>',
        "wane": f'<g transform="translate({x} {y})"><circle r="15" fill="#cfe8ef"/><circle cx="8" r="15" fill="#0b1a20"/></g>'}[kind]
    return f"""<svg class="hp-table" viewBox="0 0 640 750" preserveAspectRatio="none" aria-hidden="true">
  <defs>{veil_pattern()}
    <radialGradient id="hpGlow" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#bff3ff" stop-opacity=".22"/><stop offset="1" stop-color="#bff3ff" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="150" y="186" width="340" height="330" rx="10" fill="url(#hpVeil)" opacity=".42"/>
  <rect width="640" height="750" fill="url(#hpGlow)"/>
  {pillar(95, True, "B")}{pillar(545, False, "J")}
  {moon(66, 40, "wane")}{moon(320, 18, "full")}{moon(574, 40, "wax")}
  <path d="M250 742 q70 -36 140 0 q-70 -18 -140 0" fill="#e8f6f8" opacity=".55"/>
</svg>"""


def rite():
    """The dramatic pause before the secret: the Priestess's pillars and veil, and a moon that eclipses while she decides."""
    halves = "".join(pomegranate(x, y) for x in range(120, 300, 40) for y in range(250, 470, 44))
    return f"""<div class="hp-rite" id="hpRite" role="dialog" aria-modal="true" aria-labelledby="hpRiteMsg" hidden>
  <svg class="hp-rite-art" viewBox="0 0 400 480" aria-hidden="true">
    <defs>{veil_pattern()}
      <radialGradient id="hpMoonFill" cx="40%" cy="38%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#cfe9f0"/><stop offset="1" stop-color="#9cc4cf"/></radialGradient>
      <radialGradient id="hpHalo"><stop offset="0" stop-color="#d9fbff" stop-opacity=".9"/><stop offset="1" stop-color="#d9fbff" stop-opacity="0"/></radialGradient>
      <clipPath id="hpMoonClip"><circle cx="200" cy="120" r="62"/></clipPath>
    </defs>
    <circle class="hp-halo" cx="200" cy="120" r="150" fill="url(#hpHalo)"/>
    <circle cx="200" cy="120" r="62" fill="url(#hpMoonFill)"/>
    <g clip-path="url(#hpMoonClip)"><circle class="hp-shade" cx="200" cy="120" r="66" fill="#06121a"/>
      <circle class="hp-blood" cx="200" cy="120" r="62" fill="#7a1e2c"/></g>
    <g class="hp-veil-l"><rect x="96" y="214" width="104" height="250" fill="url(#hpVeil)"/></g>
    <g class="hp-veil-r"><rect x="200" y="214" width="104" height="250" fill="url(#hpVeil)"/></g>
    <rect x="40" y="200" width="58" height="270" fill="#0b1414" stroke="#2c4a4a" stroke-width="3"/>
    <rect x="32" y="186" width="74" height="20" rx="5" fill="#0b1414" stroke="#2c4a4a" stroke-width="3"/>
    <text x="69" y="252" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="34" fill="#d9f2ee">B</text>
    <rect x="302" y="200" width="58" height="270" fill="#dfeee9" stroke="#9fc7c0" stroke-width="3"/>
    <rect x="294" y="186" width="74" height="20" rx="5" fill="#dfeee9" stroke="#9fc7c0" stroke-width="3"/>
    <text x="331" y="252" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="34" fill="#0b1414">J</text>
  </svg>
  <p class="hp-rite-msg" id="hpRiteMsg" aria-live="assertive"></p>
  <p class="hp-rite-more" id="hpRiteMore" aria-live="polite"></p>
</div>"""


def fireflies(n=26):
    rnd = random.Random(9)
    return "".join(f'<i style="left:{rnd.uniform(2, 98):.1f}%;top:{rnd.uniform(30, 96):.1f}%;'
                   f'animation-delay:{rnd.uniform(0, 9):.1f}s;animation-duration:{rnd.uniform(7, 13):.1f}s"></i>' for _ in range(n))


def build(cards, back, defs):
    P = json.load(open(os.path.join(B.SRC, "priestess.json")))
    S = json.load(open(os.path.join(B.SRC, "spread.json")))
    e = B.e
    data = json.dumps({k: P[k] for k in ("positions", "card_width", "prompts", "secret", "sealed", "reflection", "reversed")}
                      | {"suits": S["suits"], "cards": cards})
    first = P["positions"][0]
    page = B.head(f"{P['title']} · {B.NAME}", P["desc"], PATH, "tarot", '<meta name="robots" content="noindex">\n')
    page += f"""<div class="hp-sky" aria-hidden="true"><div class="hp-flies">{fireflies()}</div></div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/tarot/">&larr; Back to Mira's tent</a>
</header>

<main class="sp hp-page">
  <section class="sp-intro hp-intro">
    <p class="who">{e(P['who'])}</p>
    <h1>{e(P['title'])}</h1>
    <p class="desc">{e(P['desc'])}</p>
  </section>

  <section class="hp-sealed" id="hpSealed" hidden>
    <h2 class="sp-h">{e(P['sealed']['title'])}</h2>
    <p>{e(P['sealed']['text'])}</p>
    <p><a class="back-btn" href="/tarot/">Back to Mira's tent</a></p>
  </section>
  <noscript><p class="raising">This reading needs JavaScript turned on.</p></noscript>

  <div id="hpOpen" hidden>
    <p class="sp-prompt hp-prompt" id="hpPrompt" aria-live="polite">{e(P['prompts']['idle'])}</p>
    <div class="hp-stage" id="hpStage">
      {table_art()}
      <button type="button" class="sp-deck idle" id="hpDeck" style="left:{first['x']}%;top:{first['y']}%;width:{P['card_width']}%" aria-label="The deck. Touch to shuffle."></button>
    </div>
    <div class="sp-actions">
      <button type="button" class="back-btn" id="hpAll" hidden>Turn the eight</button>
      <button type="button" class="back-btn" id="hpRead" hidden>Read Mira's reflection &darr;</button>
      <button type="button" class="sp-ghost" id="hpAgain" hidden>Shuffle again</button>
    </div>

    <section class="sp-summary hp-summary" id="hpSummary" hidden aria-labelledby="hpSumTitle">
      <h2 class="sp-h" id="hpSumTitle">Mira's reflection, by moonlight</h2>
      <p class="sp-sumlede">A story for reflection, not a fortune.</p>
      <div class="sp-sumtext" id="hpSummaryText"></div>
      <details class="sp-how"><summary>How Mira read this</summary><ul id="hpNotes"></ul></details>
      <p class="sp-sharerow"><button type="button" class="back-btn" data-keep hidden>Keep this in your journal</button></p>
    </section>

    <h2 class="sp-h">Card by card</h2>
    <ol class="sp-list" id="hpList"></ol>
  </div>

  <div class="sp-light" id="hpLight" role="dialog" aria-modal="true" aria-labelledby="hpLightTitle" hidden>
    <div class="sp-lightbox">
      <div class="sp-lightcard" id="hpLightCard"></div>
      <div class="sp-lighttext">
        <p class="sp-pos" id="hpLightPos"></p>
        <h3 id="hpLightTitle"></h3>
        <p class="sp-rev" id="hpLightTag" hidden>Reversed</p>
        <div id="hpLightKw"></div>
        <p class="sp-scene" id="hpLightScene"></p>
        <p id="hpLightMeaning"></p>
        <p class="sp-revnote" id="hpLightRev" hidden></p>
        <p class="sp-counsel"><b>Reflect: </b><span id="hpLightCounsel"></span></p>
        <button type="button" class="sp-ghost" id="hpLightClose">Close</button>
      </div>
    </div>
  </div>
  {rite()}
  <template id="hpBackTpl">{back}</template>
</main>
<button type="button" class="hp-sound" id="hpSound" aria-pressed="false" title="The forest at night: soft sound, made right here in your browser">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path class="hp-waves" d="M16 8.5a4.5 4.5 0 0 1 0 7M18.5 6a8 8 0 0 1 0 12"/></svg>
  <span class="hp-sound-label">Sound off</span>
</button>

{B.foot()}<script type="application/json" id="priestess-data">{data}</script>
<script src="/assets/sky.js"></script>
<script src="/assets/moonwindow.js"></script>
<script src="/assets/priestess.js"></script>
<script src="/assets/forestsound.js"></script>
</body>
</html>
"""
    B.write("tarot/priestess/index.html", page)
    for f in ("priestess.js", "moonwindow.js", "forestsound.js"):
        B.write("assets/" + f, open(os.path.join(B.SRC, f)).read())
    os.makedirs(os.path.join(B.SITE, "assets"), exist_ok=True)
    with open(os.path.join(B.SRC, "forest-night.webp"), "rb") as fi, open(os.path.join(B.SITE, "assets", "forest-night.webp"), "wb") as fo:
        fo.write(fi.read())
