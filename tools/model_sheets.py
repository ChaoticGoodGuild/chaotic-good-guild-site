"""Builds the cast model sheets (sheets/index.html): the reference every card and page draws from.

Run:  python3 tools/model_sheets.py
Not part of the public site; it's a working reference for Ryan and anyone drawing the cast.
"""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene  # noqa: E402
import characters as C  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "sheets", "index.html")
e = html.escape
STAR = open(os.path.join(ROOT, "src", "star.b64")).read()

# Bounding boxes in each character's own units (measured), padded when drawn.
BOX = {"reynard": (-123, -218, 228, 218), "mira": (-77, -332, 154, 332), "badger": (-84, -204, 156, 204),
       "bull": (-56, -222, 147, 222), "lion": (-89, -272, 173, 272), "wolf": (-75, -314, 172, 318),
       "rat": (-72, -198, 133, 198), "frog": (-21, -31, 42, 34)}
HEAD = {"reynard": (-66, -232, 136, 136), "mira": (-72, -338, 150, 186), "badger": (-62, -206, 124, 124),
        "bull": (-62, -238, 132, 132), "lion": (-62, -290, 150, 150), "wolf": (-48, -312, 150, 150),
        "rat": (-30, -200, 100, 100), "frog": (-26, -36, 52, 42)}

CAST = [
    {"key": "reynard", "name": "Reynard", "role": "The fox. Narrator, mascot and troublemaker-turned-hero.",
     "suit": "Lutes (wands)", "align": "Chaotic Good",
     "draw": lambda x: C.reynard(x), "main": "grin",
     "exprs": ["grin", "laugh", "thinking", "determined", "worried", "sad"],
     "palette": [("Fur", "#f59545"), ("Fur shadow", "#bd4a17"), ("Ruff & tail tip", "#fffaf4"), ("Cowl", "#e0303c"),
                 ("Tunic", "#a07c5c"), ("Sleeves", "#ffffff"), ("Trousers", "#4a3a30"), ("Boots", "#2e1c10")],
     "always": ["Red cowl draped over the shoulders, brown sleeveless tunic, white long sleeves",
                "Dark trousers and matching boots, both feet fully in frame",
                "Swept orange tuft on his forehead, big white cheek ruff, white inner ears",
                "Dark eyes with the whites showing, heavy dark brows",
                "His lute, whenever he's playing or the suit of Lutes is in play"],
     "never": ["A cap, hat or different outfit", "A cropped leg or foot", "Fox banners, unless the card asks for one"]},
    {"key": "mira", "name": "Mira", "role": "The witchy cat. Mirrors, magic and reflection.",
     "suit": "Mirrors (cups)", "align": "True Neutral",
     "draw": lambda x: C.mira(x), "main": "happy",
     "exprs": ["happy", "laugh", "smug", "surprised", "sad", "angry"],
     "palette": [("Fur", "#aeabc0"), ("Fur shadow", "#63607a"), ("Stripes", "#4a4760"), ("Eyes", "#e4ff7a"),
                 ("Hat & scarf", "#7d1fd6"), ("Hat brim", "#2b0a52"), ("Hat band", "#0a0410"), ("Gold trim", "#e9d701")],
     "always": ["Shorter than Reynard, even with her hat on", "Gray fur with darker stripes, yellow-green eyes with slit pupils",
                "Purple witch hat with a black band and gold buckle",
                "Purple scarf with gold stripes", "Her frog familiar somewhere nearby",
                "A hand mirror with a gold frame and a violet jewel"],
     "never": ["A different hat or a scarf in another color", "Lawful Evil scenery in her enchanted forest"]},
    {"key": "badger", "name": "The Badger", "role": "Resilient builder of the village. Patient, steady, generous.",
     "suit": "Galleons (pentacles)", "align": "Lawful Good",
     "draw": lambda x: C.badger(x), "main": "happy",
     "exprs": ["happy", "laugh", "determined", "thinking", "sad", "crying"],
     "palette": [("Face", "#f4f1f7"), ("Stripes & paws", "#1b1b22"), ("Fur", "#8e8e9c"), ("Leather armor", "#9a6234"),
                 ("Studs & galleon", "#e9d701"), ("Herb pouch", "#3f8a4a"), ("Flower", "#ff7eb6"), ("Eyes", "#3a2408")],
     "always": ["She is female", "Pink flower behind her ear", "Leather armor with gold studs",
                "Green herb pouch on her belt and one galleon hanging from it",
                "Smiling unless the card calls for something else, with the whites of her eyes showing"],
     "never": ["Missing the flower, armor or herb pouch", "More galleons than the card's number"]},
    {"key": "bull", "name": "The Bull", "role": "The builder. Raises the village beam by beam.",
     "suit": "Galleons (and The President)", "align": "Lawful Neutral",
     "draw": lambda x: C.bull(x), "main": "determined",
     "exprs": ["determined", "happy", "laugh", "angry", "worried", "sad"],
     "palette": [("Hide", "#9a6040"), ("Hide shadow", "#5a301c"), ("Horns", "#fff6e6"), ("Muzzle", "#e0aa86"),
                 ("Apron", "#9a6234"), ("Nose ring", "#e9d701"), ("Trousers", "#4a3a30"), ("Hammer", "#7a7a86")],
     "always": ["Cream horns, brown hide, darker forelock", "Leather work apron with a tool pocket",
                "Gold nose ring", "A hammer or timber when he's working"],
     "never": ["Drawn as a minotaur or a statue"]},
    {"key": "lion", "name": "The LEO Lion", "role": "Lawful Evil Overlord. A petty tyrant who hoards galleons.",
     "suit": "Antagonist (The LEO, Five of Galleons)", "align": "Lawful Evil",
     "draw": lambda x: C.lion(x), "main": "smug",
     "exprs": ["smug", "laugh", "angry", "scared", "worried", "crying"],
     "palette": [("Fur", "#f2c062"), ("Mane", "#b8661c"), ("Muzzle", "#fbe2b0"), ("Robe", "#c8203a"),
                 ("Ermine", "#f6f1e6"), ("Crown & scepter", "#e9d701"), ("Jewels", "#c0182e"), ("Eyes", "#d9a400")],
     "always": ["A lion, never a human", "Wearing his gold crown (only one crown in any picture)",
                "Clothed in his red robe with an ermine collar", "Smug, petty and a little ridiculous, never majestic",
                "His banner is crimson with a black crown and black outline"],
     "never": ["A human body or human face", "Bare (no robe)", "A second crown elsewhere in the picture"]},
    {"key": "wolf", "name": "The Corporate Wolf", "role": "Greed in a suit. Counts coins, not friends.",
     "suit": "Antagonist (The LEO, Six of Galleons)", "align": "Neutral Evil",
     "draw": lambda x: C.wolf(x, arrows=(x == "worried")), "main": "greedy",
     "exprs": ["greedy", "laugh", "smug", "worried", "scared", "angry"],
     "palette": [("Fur", "#9a9aa8"), ("Fur shadow", "#55556a"), ("Muzzle", "#d8d8e2"), ("Suit", "#2c2c38"),
                 ("Shirt", "#f2f2f2"), ("Tie", "#c0182e"), ("Dollar eyes", "#e9d701"), ("Losing arrows", "#ff3b3b")],
     "always": ["Gray wolf in a black suit, white shirt and red tie", "Dollar signs for eyes",
                "When he's losing, red down-arrows float around his head"],
     "never": ["A crown", "Arrows floating off to the side, away from his head"]},
]

RAT_OUTFITS = [
    ("plain", "The rat", "Base model"),
    ("hero", "The hero rat", "Robin Hood outfit. The Fool and the Neophytes"),
    ("lute", "Reynard's apprentice", "Court cards of Lutes. Red cowl, no fox tail"),
    ("wizard", "The journeyman", "Blue robes and mirror. Court cards of Mirrors"),
    ("master", "The master", "Purple robes. Master of Mirrors"),
    ("scribe", "The scribe", "Spectacles and quill. Suit of Quills"),
    ("merchant", "The merchant", "Trades galleons fairly. Suit of Galleons"),
    ("ragged", "The ragged rat", "Patched cloak. Beggars and newcomers"),
    ("suit", "The sellout", "Grey suit. The rat who sold out (The LEO)"),
]
RAT_RULES = {
    "always": ["Small: about two thirds of Reynard's height", "Round pink-lined ears, pink nose, pink tail",
               "Each rat in a different outfit so they're easy to tell apart",
               "Quills court cards grow with skill: crayon, pencil, pen, then quill"],
    "never": ["A fox tail", "Two rats in the same outfit in one picture (unless it's a uniform crowd)"],
}
GENERAL = ["Galleons in a card match the card's number", "No fox banners unless the card asks for one",
           "The Lawful Evil city sits under a red sky", "The enchanted forest never shows Lawful Evil things",
           "Characters keep these outfits on every card unless the card's text calls for a costume"]


def char_svg(key, g, box, pad=10, cls="fig"):
    x, y, w, h = box
    return (f'<svg class="{cls}" viewBox="{x-pad} {y-pad} {w+2*pad} {h+2*pad}" role="img">'
            f'<ellipse cx="0" cy="2" rx="{w*0.36:.0f}" ry="7" fill="#000" opacity=".12"/>{g}</svg>')


def head_svg(g, box):
    x, y, w, h = box
    return f'<svg class="head" viewBox="{x} {y} {w} {h}">{g}</svg>'


def swatches(pal):
    return "".join(f'<li><span style="background:{c}"></span><b>{e(n)}</b><code>{c}</code></li>' for n, c in pal)


def rules(always, never):
    a = "".join(f"<li>{e(x)}</li>" for x in always)
    n = "".join(f"<li>{e(x)}</li>" for x in never)
    return f'<div class="rules"><div><h4>Always</h4><ul class="yes">{a}</ul></div><div><h4>Never</h4><ul class="no">{n}</ul></div></div>'


def lineup():
    order = ["rat", "badger", "reynard", "mira", "bull", "lion", "wolf"]
    funcs = {"reynard": C.reynard(pose="idle"), "mira": C.mira(), "badger": C.badger(), "bull": C.bull(),
             "lion": C.lion(), "wolf": C.wolf(), "rat": C.rat(outfit="hero")}
    names = {"rat": "A rat", "badger": "Badger", "reynard": "Reynard", "mira": "Mira", "bull": "Bull", "lion": "LEO Lion", "wolf": "Wolf"}
    x, parts, width = 70, [], 0
    for k in order:
        s = C.CANON_SCALE[k]
        bx = BOX[k]
        left = -bx[0] * s if k != "reynard" else 70 * s
        x += left
        parts.append(f'<g transform="translate({x:.0f},360) scale({s})">{funcs[k]}</g>'
                     f'<text x="{x:.0f}" y="388" class="ln">{names[k]}</text>')
        x += (bx[0] + bx[2]) * s + 46
    width = x + 20
    guides = "".join(f'<line x1="0" x2="{width:.0f}" y1="{360-h}" y2="{360-h}" class="guide"/>' for h in range(50, 351, 50))
    return (f'<svg class="lineup" viewBox="0 -20 {width:.0f} 420" role="img" aria-label="Height lineup">'
            f'<rect y="-20" width="{width:.0f}" height="420" fill="#f3e6c4"/>{guides}'
            f'<line x1="0" x2="{width:.0f}" y1="360" y2="360" stroke="#5a3a22" stroke-width="2"/>{"".join(parts)}</svg>')


def props():
    items = [
        (f'<svg viewBox="-60 -60 120 120">{C.galleon(54, text=True)}</svg>', "Galleon", "Gold coin with the Guild star, rim reads Kindness Calls · Chaos Clears"),
        (f'<svg viewBox="-40 -30 150 60"><g>{C.lute()}</g></svg>', "Reynard's lute", "Honey wood, dark sound hole with a gold ring, cream strings"),
        (f'<svg viewBox="-12 -80 64 94">{C.quill()}</svg>', "Quill", "White feather, ink-dark nib"),
        (f'<svg viewBox="-26 -30 52 72">{C.mirror()}</svg>', "Mira's mirror", "Gold frame, violet jewel; the glass shows only what the card needs"),
        (f'<svg viewBox="-60 -60 120 120"><image href="data:image/png;base64,{STAR}" x="-52" y="-50" width="104" height="100"/></svg>', "The Guild star", "From the Guild logo. Use it for stars, lanterns and the Hermit's light"),
        (f'<svg viewBox="-6 -6 42 74">{C.fox_banner()}</svg>', "Fox banner", "Purple with a gold fox. Only when the card asks"),
        (f'<svg viewBox="-6 -6 42 74">{C.leo_banner()}</svg>', "LEO banner", "Crimson with a black crown and black outline. Lawful Evil city"),
        (f'<svg viewBox="-14 -24 62 40">{C.down_arrows()}</svg>', "Losing arrows", "Red down-arrows around the Wolf's head"),
        (f'<svg viewBox="-30 -40 60 46">{C.frog()}</svg>', "Mira's frog", "Her familiar. Bright green, big round eyes"),
    ]
    return "".join(f'<figure class="prop">{s}<figcaption><b>{e(n)}</b><span>{e(d)}</span></figcaption></figure>' for s, n, d in items)


def panel(c):
    k = c["key"]
    main = char_svg(k, c["draw"](c["main"]), BOX[k])
    heads = "".join(f'<figure>{head_svg(c["draw"](x), HEAD[k])}<figcaption>{x}</figcaption></figure>' for x in c["exprs"])
    return f'''<section class="sheet" id="{k}">
  <div class="sheet-fig">{main}</div>
  <div class="sheet-body">
    <p class="kicker">{e(c["suit"])} · {e(c["align"])}</p>
    <h2>{e(c["name"])}</h2>
    <p class="role">{e(c["role"])}</p>
    <h3>Expressions</h3><div class="exprs">{heads}</div>
    <h3>Palette</h3><ul class="pal">{swatches(c["palette"])}</ul>
    {rules(c["always"], c["never"])}
  </div>
</section>'''


def rat_panel():
    outfits = "".join(f'<figure class="outfit">{char_svg("rat", C.rat("happy", o), BOX["rat"], pad=8)}<figcaption><b>{e(n)}</b><span>{e(d)}</span></figcaption></figure>' for o, n, d in RAT_OUTFITS)
    heads = "".join(f'<figure>{head_svg(C.rat(x), HEAD["rat"])}<figcaption>{x}</figcaption></figure>' for x in ["happy", "grin", "determined", "worried", "crying", "scared"])
    pal = [("Fur", "#b0a8c0"), ("Fur shadow", "#6e667e"), ("Belly", "#d4cde0"), ("Ears, nose, tail", "#e8a3b8")]
    return f'''<section class="sheet wide" id="rats">
  <div class="sheet-body">
    <p class="kicker">Quills (swords) and the court cards of every suit · Neutral Good</p>
    <h2>The Rats of the Guild</h2>
    <p class="role">The mischief of the Guild. All different, all busy, and far more alike than the LEOs want them to think.</p>
    <div class="outfits">{outfits}</div>
    <div class="split">
      <div><h3>Expressions</h3><div class="exprs">{heads}</div><h3>Palette</h3><ul class="pal">{swatches(pal)}</ul></div>
      <div>{rules(RAT_RULES["always"], RAT_RULES["never"])}</div>
    </div>
  </div>
</section>'''


CSS = """
:root { --night:#0d0418; --dusk:#1b0b33; --violet:#6000AE; --gold:#e9d701; --ink:#f3ecff; --muted:#cbbde6; --paper:#f3e6c4; --paper-ink:#2a1810;
  --display:"Pirata One", Georgia, serif; --body:"Alegreya", Georgia, serif; color-scheme: dark; }
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--night); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.5; }
header.top { display: flex; align-items: center; gap: 18px; padding: 14px clamp(16px, 4vw, 48px); border-bottom: 1px solid rgba(233,215,1,.25); }
header.top img { height: 78px; }
header.top h1 { font-family: var(--display); font-weight: 400; font-size: clamp(30px, 4vw, 44px); margin: 0; line-height: 1; color: var(--gold); }
header.top p { margin: 2px 0 0; color: var(--muted); }
main { max-width: 1240px; margin: 0 auto; padding: 24px clamp(16px, 4vw, 48px) 60px; }
nav.toc { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 22px; }
nav.toc a { color: var(--ink); text-decoration: none; border: 1px solid rgba(233,215,1,.4); border-radius: 999px; padding: 3px 14px; font-size: 15px; }
nav.toc a:hover { border-color: var(--gold); color: var(--gold); }
h2.sec { font-family: var(--display); font-weight: 400; font-size: 34px; margin: 34px 0 12px; color: var(--gold); }
.lineup { display: block; width: 100%; height: auto; border-radius: 16px; border: 2px solid var(--gold); }
.lineup .guide { stroke: #c9b78e; stroke-dasharray: 4 6; }
.lineup .gl { font: 12px var(--body); fill: #8a7550; }
.lineup .ln { font: 700 15px var(--body); fill: var(--paper-ink); text-anchor: middle; }
.note { color: var(--muted); max-width: 70ch; }
.sheet { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 0; margin: 0 0 28px; border-radius: 18px; overflow: hidden; border: 2px solid var(--gold); background: var(--paper); color: var(--paper-ink); box-shadow: 0 0 0 5px rgba(96,0,174,.5); }
.sheet.wide { grid-template-columns: 1fr; }
.sheet-fig { display: flex; align-items: center; justify-content: center; padding: 24px; background: radial-gradient(circle at 50% 40%, #fff6dc, #ecd9ad); border-right: 2px dashed #c9b78e; }
.sheet-fig .fig { width: 100%; max-height: 540px; }
.sheet-body { padding: 22px 26px 24px; }
.kicker { margin: 0; font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #6000AE; }
.sheet h2 { font-family: var(--display); font-weight: 400; font-size: 46px; line-height: 1; margin: 4px 0 4px; color: #3d0872; }
.role { margin: 0 0 12px; font-style: italic; }
.sheet h3 { font-size: 13px; letter-spacing: .1em; text-transform: uppercase; margin: 14px 0 6px; color: #5a3a22; }
.exprs { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 8px; }
.exprs figure { margin: 0; text-align: center; }
.exprs .head { width: 100%; aspect-ratio: 1; background: #fffaf0; border: 1px solid #d8c69c; border-radius: 12px; }
.exprs figcaption { font-size: 13px; color: #5a3a22; }
.pal { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px 12px; }
.pal li { display: grid; grid-template-columns: 26px 1fr; grid-template-rows: auto auto; column-gap: 8px; align-items: center; font-size: 14px; line-height: 1.2; }
.pal span { grid-row: span 2; width: 26px; height: 26px; border-radius: 6px; border: 1.5px solid #160a22; }
.pal code { font-size: 12px; color: #6a5a40; }
.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
.rules h4 { margin: 0 0 4px; font-size: 13px; letter-spacing: .1em; text-transform: uppercase; }
.rules ul { margin: 0; padding-left: 18px; font-size: 15px; line-height: 1.4; }
.rules li { margin-bottom: 3px; }
.yes li::marker { content: "\\2713  "; color: #2f8a34; font-weight: 700; }
.no li::marker { content: "\\2715  "; color: #c0182e; font-weight: 700; }
.rules div:first-child h4 { color: #2f6b3a; } .rules div:last-child h4 { color: #a3162c; }
.outfits { display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); gap: 10px; margin: 8px 0 6px; }
.outfit { margin: 0; text-align: center; background: #fffaf0; border: 1px solid #d8c69c; border-radius: 12px; padding: 8px 6px; }
.outfit .fig { width: 100%; height: 150px; }
.outfit figcaption, .prop figcaption { display: flex; flex-direction: column; font-size: 13px; line-height: 1.25; }
.outfit figcaption b, .prop figcaption b { font-size: 15px; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.props { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 12px; }
.prop { margin: 0; background: var(--paper); color: var(--paper-ink); border: 2px solid var(--gold); border-radius: 14px; padding: 12px; text-align: center; }
.prop svg { width: 100%; height: 110px; }
.general { background: var(--dusk); border: 1px solid rgba(233,215,1,.35); border-radius: 14px; padding: 14px 20px; }
.general li { margin-bottom: 4px; }
@media (max-width: 860px) {
  .sheet { grid-template-columns: 1fr; } .sheet-fig { border-right: 0; border-bottom: 2px dashed #c9b78e; }
  .sheet-fig .fig { max-height: 380px; } .exprs { grid-template-columns: repeat(3, 1fr); }
  .pal { grid-template-columns: repeat(2, 1fr); } .rules, .split { grid-template-columns: 1fr; }
}
"""


def build():
    defs = scene.DEFS.replace("</defs>", C.EXTRA_DEFS + "</defs>")
    logo = open(os.path.join(ROOT, "src", "logo.b64")).read()
    toc = "".join(f'<a href="#{c["key"]}">{e(c["name"])}</a>' for c in CAST) + '<a href="#rats">The Rats</a><a href="#props">Props &amp; symbols</a><a href="#rules">House rules</a>'
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guild Cast Model Sheets</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Alegreya:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header class="top"><img src="data:image/png;base64,{logo}" alt="Chaotic Good Guild"><div><h1>The Guild Cast: Model Sheets</h1><p>Version 1. Every card, page and scene draws its characters from these.</p></div></header>
<main>
<nav class="toc">{toc}</nav>
<h2 class="sec">Height lineup</h2>
<p class="note">Everyone at their true size beside each other; the faint lines are a height grid. Rats stand about two thirds as tall as Reynard, Mira is shorter than him even with her hat, and the Bull and the Wolf tower over the village.</p>
{lineup()}
<h2 class="sec">The cast</h2>
{''.join(panel(c) for c in CAST)}
{rat_panel()}
<h2 class="sec" id="props">Props &amp; symbols</h2>
<div class="props">{props()}</div>
<h2 class="sec" id="rules">House rules for every card</h2>
<ul class="general">{''.join(f'<li>{e(x)}</li>' for x in GENERAL)}</ul>
</main></body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(page)
    print("Wrote", OUT, f"({len(page)//1024} KB)")


if __name__ == "__main__":
    build()
