"""The full Guild tarot deck: 22 major arcana and four suits of 14 (Galleons, Lutes, Quills, Mirrors).

Run:  python3 tools/deck.py
  -> sheets/deck.html   gallery of all 78 cards and the card back
  -> src/tarot.json     each card's id, name, suit, rank and scene description
Art is composed only from the model-sheet cast (characters.py) and the settings/props in deck_lib.py.
"""
import html, json, math, os, sys, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene  # noqa: E402
import characters as C  # noqa: E402
import cards as K  # noqa: E402
from characters import O, O1, INK  # noqa: E402
from deck_lib import *  # noqa: E402,F401,F403
import deck_lib as L  # noqa: E402

ROOT = os.path.dirname(HERE)
e = html.escape


def lute_at(x, y, rot=0, s=1.0):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{C.lute()}</g>'


def stump_at(x, y, s=1.0, w=64):
    return f'<g transform="translate({x},{y}) scale({s})">{K.stump(w)}</g>'


def stick(x0, y0, x1, y1):
    return f'<path d="M{x0},{y0} L{x1},{y1}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M{x0},{y0} L{x1},{y1}" stroke="#8a6038" stroke-width="5" stroke-linecap="round"/>'


def candle(x, y, h=46):
    return (f'<circle cx="{x}" cy="{y-h-10}" r="80" fill="url(#kCandle)"/><rect x="{x-8}" y="{y-h}" width="16" height="{h}" fill="#f3e6c4" {O1}/>'
            f'<path d="M{x},{y-h} q8,-14 0,-24 q-8,10 0,24Z" fill="#ffd75a" {O1}/><path d="M{x-16},{y} h32 v6 h-32Z" fill="url(#gGold)" {O1}/>')


# ====================================================================== MAJOR ARCANA
def fool():
    return (sky("dawn", 2) + '<circle cx="470" cy="560" r="180" fill="#ffe9a8" opacity=".35"/>' + clouds(2, 100, 300, 3, "#ffd9c8", .45)
            + far_city(470, 590, .45, op=.75) + hills(610, "#4a2f6a", 20, 1) + ground("dusk", 680)
            + '<path d="M230,870 Q330,770 420,720 Q480,690 500,640 L530,640 Q520,700 470,750 Q410,810 400,870Z" fill="#d9b87a" opacity=".5"/>'
            + shack(110, 770, 1.7) + ch("rat", 156, 782, 1.3, expr="sad", outfit="ragged")
            + f'<path d="M352,708 L262,588" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M352,708 L262,588" stroke="#8a6038" stroke-width="6" stroke-linecap="round"/>'
            + f'<path d="M262,588 q-34,-6 -30,-40 q30,-20 54,6 q4,26 -24,34Z" fill="#a3162c" {O}/>' + sp(250, 560, .8)
            + ch("rat", 380, 832, 2.0, expr="determined", outfit="hero") + fg())


def magician():
    return (village("night", far=False) + gstar(310, 140, 150)
            + '<path d="M250,290 C250,260 300,260 310,290 C320,320 370,320 370,290 C370,260 320,260 310,290 C300,320 250,320 250,290Z" fill="none" stroke="#e9d701" stroke-width="7"/>'
            + ch("reynard", 310, 770, 1.7, expr="grin", pose="idle")
            + table(310, 650, 430, h=150, cloth="#6000AE")
            + gal(160, 618, 26) + lute_at(256, 620, -14, .9) + q(396, 636, 0, 1.2) + hmirror(476, 600, 1.3)
            + candle(80, 640, 50) + candle(545, 640, 50) + sp(200, 420, 1.2) + sp(430, 400, 1) + sp(120, 330, .8) + sp(500, 300, .9) + fg())


def priestess():
    pil = lambda x, c, cap: (f'<rect x="{x-32}" y="250" width="64" height="540" fill="{c}" {O}/><rect x="{x-44}" y="226" width="88" height="28" rx="6" fill="{cap}" {O}/><rect x="{x-44}" y="784" width="88" height="24" rx="6" fill="{cap}" {O}/>'
                             f'<g stroke="#000" stroke-opacity=".25" stroke-width="3"><path d="M{x-12},256 v526 M{x+12},256 v526"/></g>' + sp(x, 420, 1.4, cap) + sp(x, 600, 1.4, cap))
    return (forest("night", 2, moon_at=(310, 220, 120)) + '<rect x="132" y="300" width="356" height="360" fill="#3d0872" opacity=".6"/><rect x="132" y="300" width="356" height="360" fill="url(#kLattice)"/>'
            + pil(100, "#4b0f86", "#e9d701") + pil(520, "url(#gGold)", "#4b0f86")
            + '<path d="M250,846 a66,30 0 0,0 120,0 a80,20 0 0,1 -120,0Z" fill="url(#gGold)" stroke="#160a22" stroke-width="2"/>'
            + ch("mira", 310, 822, 2.5, expr="happy", prop="mirror") + ch("frog", 470, 846, 1.7) + tarot(160, 846, 3, 1.2) + fireflies(2, 8) + fg())


def empress():
    return (village("day", far=False, strings=False) + ch("badger", 310, 720, 1.45, expr="happy", prop="herb", galleon_on_belt=False)
            + garden(310, 790, 520, "veg", 1) + ch("rat", 548, 770, 1.2, flip=True, expr="happy", outfit="hero")
            + garden(300, 850, 590, "veg", 2)
            + "".join(f'<g transform="translate({x},{y})"><path d="M0,0 q-12,-14 -16,0 q4,12 16,0 q12,-14 16,0 q-4,12 -16,0Z" fill="{c}" {O1}/></g>' for x, y, c in ((120, 420, "#ff7eb6"), (470, 380, "#e9d701"), (230, 330, "#b06cff"))))


def president():
    crowd_ = (ch("rat", 70, 858, 1.25, expr="laugh", outfit="hero") + ch("rat", 175, 862, 1.2, expr="grin", outfit="ragged")
              + ch("rat", 360, 862, 1.2, flip=True, expr="laugh", outfit="plain") + ch("rat", 470, 860, 1.25, flip=True, expr="happy", outfit="master")
              + ch("rat", 570, 862, 1.2, flip=True, expr="laugh", outfit="wizard", prop="none"))
    return (sky("dusk", 3) + far_city(310, 624, 1.8) + le_houses(2) + street(640)
            + statue(470, 660, .8, rot=18) + f'<path d="M520,400 Q560,470 572,590" stroke="#c9a66a" stroke-width="5" fill="none"/>'
            + ch("reynard", 572, 700, .85, flip=True, expr="smug", pose="idle") + crowd(700, 9, 3, .9, 0, 420)
            + crate(250, 730, 1.4) + ch("rat", 250, 634, 2.0, expr="happy", outfit="hero")
            + '<path d="M222,500 L290,600" stroke="#160a22" stroke-width="18"/><path d="M222,500 L290,600" stroke="#6000AE" stroke-width="13"/><path d="M222,500 L290,600" stroke="#e9d701" stroke-width="3"/>'
            + confetti(3, 46, 560) + crowd_)


def hierophant():
    return (forest("day", 3) + rays(310, -40, 7, op=.12) + tree(40, 780, 2.3) + tree(590, 780, 2.3)
            + f'<ellipse cx="310" cy="660" rx="150" ry="62" fill="url(#kStone)" {O}/><path d="M170,650 Q310,590 450,650 Q310,628 170,650Z" fill="#5fae4a" {O1}/>'
            + cardinal(296, 612, 1.5) + ch("rat", 120, 852, 1.6, expr="happy", outfit="hero") + ch("rat", 505, 852, 1.6, flip=True, expr="surprised", outfit="ragged") + fg("#0c1a10"))


def partners():
    return (alley(2) + gstar(310, 110, 120) + crate(70, 790, 1.2) + barrel(575, 790, 1.1)
            + ch("rat", 215, 846, 1.7, expr="crying", outfit="ragged")
            + ch("badger", 425, 850, 1.5, flip=True, expr="happy", prop=None, galleon_on_belt=False) + lantern(326, 852, 1.35)
            + bread(250, 700, 1.1) + flower_crack(540, 856))


def chariot():
    s = '<rect width="620" height="870" fill="#12061f"/><polygon points="0,0 620,0 390,250 230,250" fill="#0c0416"/>'
    s += '<polygon points="0,0 230,250 230,480 0,870" fill="#241050"/><polygon points="620,0 390,250 390,480 620,870" fill="#3a1024"/>'
    s += '<g stroke="#000" stroke-opacity=".35" stroke-width="3"><path d="M0,290 L230,326 M0,580 L230,404 M620,290 L390,326 M620,580 L390,404 M115,125 V675 M505,125 V675"/></g>'
    s += '<rect x="230" y="250" width="160" height="230" fill="#1c0a30"/><circle cx="310" cy="390" r="170" fill="url(#halo)"/>'
    s += '<polygon points="0,870 230,480 390,480 620,870" fill="#2a1a3a"/><polygon points="190,870 282,480 338,480 430,870" fill="#6000AE"/><path d="M190,870 L282,480 M430,870 L338,480" stroke="#e9d701" stroke-width="4"/>'
    s += pedestal(310, 480, 56, 66) + lute_at(298, 392, -62, .75) + gal(334, 398, 14)
    s += arcade(206, 566, .62, "#ff82ff") + slot(414, 566, .62, True) + arcade(150, 660, 1.0, "#62ffa1") + slot(470, 660, 1.0, True) + arcade(62, 810, 1.5) + slot(558, 810, 1.5, True)
    return s + ch("reynard", 310, 856, 1.45, expr="determined", pose="idle")


def strength():
    return (village("day", far=False) + housefrm(440, 710, 1.7)
            + f'<rect x="30" y="486" width="380" height="28" rx="6" fill="url(#gWood)" {O} transform="rotate(-7 220 500)"/>'
            + ch("rat", 330, 478, 1.0, expr="laugh", outfit="plain", sh=False) + ch("bull", 200, 800, 1.35, expr="laugh")
            + ch("rat", 420, 810, 1.5, expr="grin", outfit="hero") + ch("rat", 545, 830, 1.4, flip=True, expr="happy", outfit="ragged")
            + ch("rat", 70, 858, 1.25, expr="laugh", outfit="scribe", prop="none") + fg("#0c1a10"))


def hermit():
    return (sky("night", 5, 150) + consts(5, 4) + hills(770, "#12082a", 14, 2) + far_city(520, 800, .3, op=.6)
            + '<polygon points="20,870 300,600 350,630 420,596 620,870" fill="url(#kSnow)" stroke="#160a22" stroke-width="2.4"/><polygon points="300,600 350,630 420,596 480,700 380,660 330,720 250,660" fill="#fff" opacity=".55"/>'
            + '<polygon points="350,630 420,596 620,870 480,870" fill="#000" opacity=".22"/>'
            + stick(244, 664, 236, 340) + sp(236, 330, 1.6) + ch("rat", 310, 648, 2.3, expr="thinking", outfit="master", prop="none") + lantern(372, 640, 1.45)
            + "".join(f'<circle cx="{(i*97)%620}" cy="{420+(i*53)%430}" r="2.4" fill="#fff" opacity=".7"/>' for i in range(40)))


def chaos():
    return (cosmos(4) + wheel(310, 480, 200) + ch("reynard", 310, 282, 1.0, expr="laugh", sh=False)
            + ch("rat", 126, 452, 1.0, rot=-62, expr="laugh", outfit="hero") + ch("lion", 506, 500, .62, rot=74, expr="scared")
            + ch("wolf", 170, 650, .68, rot=158, expr="scared", arrows=True)
            + "".join(sp(x, y, s_) for x, y, s_ in ((80, 120, 1.6), (540, 140, 1.3), (560, 760, 1.5), (60, 790, 1.2), (310, 80, 1), (470, 820, .9))))


def justice():
    fl = f'<g fill="#ff7eb6" {O1}>' + "".join(f'<circle cx="{11*math.cos(a):.0f}" cy="{-16+11*math.sin(a):.0f}" r="8"/>' for a in [k * math.pi / 3 for k in range(6)]) + f'</g><circle cy="-16" r="7" fill="#ffe27a" {O1}/>'
    return (sky("dusk", 6) + far_city(310, 624, 1.8) + le_houses(4) + street(640)
            + scales(310, 240, 1.25, 13, left=fl, right=heap(0, 2, 84, 30, seed=3))
            + ch("rat", 100, 856, 1.4, expr="happy", outfit="hero") + ch("rat", 525, 856, 1.4, flip=True, expr="happy", outfit="ragged")
            + ch("badger", 310, 850, 1.6, expr="determined", prop=None, galleon_on_belt=False))


def hanged():
    return (forest("dusk", 5) + tree(80, 800, 2.7)
            + f'<path d="M100,340 Q260,250 450,276" stroke="{INK}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M100,340 Q260,250 450,276" stroke="url(#gWood)" stroke-width="24" fill="none" stroke-linecap="round"/>'
            + f'<g fill="#2f6b3a" {O1}><circle cx="450" cy="262" r="30"/><circle cx="486" cy="282" r="26"/><circle cx="420" cy="240" r="24"/></g>'
            + '<path d="M340,266 V340" stroke="#c9a66a" stroke-width="6"/>' + ch("reynard", 340, 336, 1.3, rot=180, expr="smug", pose="idle", sh=False)
            + f'<g transform="rotate(-70 170 850)">{sack(170, 850, 1.3)}</g>' + heap(250, 856, 130, 36, seed=5) + lute_at(430, 846, 8, 1.0)
            + ch("rat", 535, 852, 1.5, flip=True, expr="happy", outfit="hero", prop="quill") + fg())


def death():
    c1, c2 = uid("dp"), uid("dp")
    wall = lambda x: (f'<g fill="#2b0812"><rect x="{x}" y="170" width="300" height="260"/>' + "".join(f'<rect x="{x+i*30}" y="156" width="16" height="16"/>' for i in range(10))
                      + f'<rect x="{x+16}" y="80" width="74" height="350"/><polygon points="{x+6},80 {x+53},10 {x+100},80"/></g><path d="M{x+150},424 v-110 q50,-66 100,0 v110Z" fill="#0c0206"/>'
                      + f'<g stroke="#3a0c18" stroke-width="4"><path d="M{x+170},424 v-124 M{x+200},424 v-140 M{x+230},424 v-124 M{x+150},360 h100"/></g><rect x="{x+44}" y="130" width="14" height="22" fill="#ff6a3c"/>'
                      + f'<g transform="translate({x+104},210)">{C.leo_banner(32, 66)}</g>')
    woods = lambda xs, c1_, c2_: "".join(scene.pine(x, 424, h, c1_, c2_) for x, h in xs)
    top = (sky("red", 6) + wall(0) + woods(((400, 280), (470, 340), (540, 300), (610, 360), (360, 200)), "#241446", "#3a2266")
           + '<path d="M0,404 h260 Q400,396 620,404 v30 h-620Z" fill="#2a1438"/><path d="M150,424 L250,424 L330,406 L250,404Z" fill="#3a1418"/>'
           + '<path d="M290,330 h-50 M300,360 h-66 M290,390 h-44" stroke="#f3ecff" stroke-opacity=".5" stroke-width="4" stroke-linecap="round"/>'
           + ch("reynard", 400, 418, .95, expr="worried", pose="idle"))
    bot = (sky("dusk", 7) + wall(320) + woods(((20, 330), (90, 280), (160, 350), (230, 260)), "#2a1648", "#3d2466")
           + '<path d="M0,404 Q200,396 620,404 v30 h-620Z" fill="#241438"/>'
           + ch("rat", 60, 418, .85, expr="laugh", outfit="hero") + ch("rat", 132, 420, .85, expr="grin", outfit="ragged") + ch("rat", 204, 418, .85, expr="happy", outfit="plain")
           + ch("badger", 340, 420, 1.1, expr="determined", prop=None, galleon_on_belt=False))
    return (f'<clipPath id="{c1}"><rect width="620" height="424"/></clipPath><clipPath id="{c2}"><rect width="620" height="424"/></clipPath>'
            f'<g clip-path="url(#{c1})">{top}</g><g transform="translate(0,446)"><g clip-path="url(#{c2})">{bot}</g></g>'
            f'<rect y="424" width="620" height="22" fill="url(#gGold)" stroke="#160a22" stroke-width="2"/>' + sp(310, 435, 1.3, "#3d0872") + sp(110, 435, .9, "#3d0872") + sp(510, 435, .9, "#3d0872"))


def temperance():
    return K.art_temperance() + fireflies(14, 8, 420, 700) + fg()


def the_leo():
    return (sky("red", 7) + far_city(310, 624, 1.8) + le_houses(7) + street(640) + pole_banner(40, 660, 300, "leo", 1.7)
            + heap(450, 668, 340, 110, seed=2) + ch("lion", 410, 644, .95, expr="laugh") + ch("wolf", 545, 654, .8, flip=True, expr="laugh")
            + ch("rat", 280, 672, 1.2, expr="smug", outfit="suit")
            + ch("reynard", 160, 856, 1.3, expr="sad", pose="idle") + stocks(160, 668, 200, 856)
            + ch("rat", 445, 858, 1.7, expr="worried", outfit="scribe", prop="none") + stocks(450, 716, 160, 858))


def tower():
    s = sky("red", 9) + '<path d="M600,0 L520,90 L560,96 L450,190 L500,196 L400,280" stroke="#fff3a0" stroke-width="10" fill="none" stroke-linejoin="round"/><path d="M600,0 L520,90 L560,96 L450,190 L500,196 L400,280" stroke="#e9d701" stroke-width="4" fill="none"/>'
    s += far_city(110, 700, .5) + street(690)
    s += f'<rect x="232" y="250" width="156" height="540" fill="url(#kStone)" {O}/><g stroke="#2a2434" stroke-width="2">' + "".join(f'<path d="M232,{y} h156"/>' for y in range(290, 790, 40)) + "".join(f'<path d="M{x},{y} v40"/>' for y in range(290, 780, 80) for x in (270, 350)) + "".join(f'<path d="M{x},{y} v40"/>' for y in range(330, 780, 80) for x in (310,)) + '</g>'
    s += f'<path d="M300,250 l14,60 l-20,50 l26,70 l-16,60 l20,80" stroke="{INK}" stroke-width="6" fill="none"/><g fill="#ff8a4c" {O1}><path d="M292,470 q18,-24 36,0 v40 h-36Z"/><path d="M292,620 q18,-24 36,0 v40 h-36Z"/></g>'
    s += f'<path d="M270,790 v-70 q40,-50 80,0 v70Z" fill="#0c0206" {O1}/>'
    s += f'<g transform="rotate(-20 310 250) translate(-10,-46)"><rect x="216" y="150" width="188" height="90" fill="url(#kStone)" {O}/>' + "".join(f'<rect x="{x}" y="124" width="26" height="28" fill="url(#kStone)" {O}/>' for x in range(216, 400, 40)) + f'<g transform="translate(290,160)">{C.leo_banner(40, 76)}</g></g>'
    s += '<path d="M236,250 l20,-30 l16,22 l24,-36 l20,30 l22,-26 l18,34 l28,-20 v26Z" fill="#ff8a3c" stroke="#160a22" stroke-width="2"/>'
    s += gstar(150, 200, 70) + gstar(470, 330, 56) + gstar(110, 400, 44) + gstar(520, 150, 40, False) + gstar(200, 90, 46, False) + sp(420, 120, 1.4) + sp(80, 290, 1.2) + sp(540, 460, 1.1)
    s += ch("wolf", 500, 400, .5, rot=150, sh=False, expr="scared")
    s += f'<g fill="url(#kStone)" {O1}><path d="M190,790 l20,-26 l30,10 l8,16Z M380,792 l14,-20 l30,4 l10,16Z M420,800 l10,-12 l18,12Z"/></g>'
    return s + ch("reynard", 110, 856, 1.3, expr="smug", pose="idle") + ch("rat", 510, 858, 1.7, flip=True, expr="grin", outfit="scribe")


def star():
    pts = [(90, 330), (150, 180), (250, 90), (400, 80), (500, 170), (550, 320), (470, 420)]
    return (sky("night", 8, 150) + f'<path d="M{" L".join(f"{x},{y}" for x, y in pts)}" stroke="#fff3a0" stroke-opacity=".35" stroke-width="1.6" fill="none"/>'
            + "".join(sp(x, y, 1.5) for x, y in pts) + gstar(310, 250, 280) + hills(650, "#1a0b32", 18, 3) + ground("night", 690)
            + pond(380, 790, 200, 48) + '<g opacity=".55">' + gstar(380, 786, 64, False) + '</g>'
            + ch("rat", 120, 800, 1.6, expr="happy", outfit="hero") + ch("rat", 215, 818, 1.15, expr="surprised", outfit="ragged") + fireflies(8, 12) + fg())


def moon_card():
    tw = lambda x: f'<g fill="#1a0b32" stroke="#160a22" stroke-width="2"><rect x="{x-36}" y="340" width="72" height="330"/><polygon points="{x-44},340 {x},260 {x+44},340"/></g><rect x="{x-8}" y="400" width="16" height="26" fill="#ff6a3c"/><rect x="{x-8}" y="500" width="16" height="26" fill="#ff6a3c"/>'
    return (sky("night", 9) + moon(310, 205, 105) + "".join(f'<path d="M{x},{y} q5,10 0,16 q-5,-6 0,-16Z" fill="#fff3a0"/>' for x, y in ((240, 360), (310, 390), (380, 360), (275, 430), (345, 430)))
            + hills(650, "#1a0b32", 16, 1) + tw(96) + tw(524) + ground("night", 660)
            + '<path d="M262,800 Q340,730 300,670 Q292,650 306,634 L326,634 Q326,656 350,680 Q400,740 356,800Z" fill="#c9b78e" opacity=".5"/>'
            + ch("wolf", 140, 770, .9, expr="laugh") + ch("mira", 482, 780, 1.6, flip=True, expr="thinking", prop="mirror")
            + pond(310, 836, 230, 34) + ch("frog", 310, 846, 1.8, sh=False) + fg())


def sun_card():
    cas = castle(balcony=K.place(C.lion("angry"), 380, 400, .66))
    return (sky("day", 10) + sunface(310, 180, 100) + f'<g transform="translate(310,646) scale(.5) translate(-360,-630)">{cas}</g>'
            + le_houses(9) + street(640, "#a88a6e") + scene.lstring(0, 430, 620, 410, 40, 9)
            + stall(125, 750, 190) + stall(470, 740, 190, "#a3162c", "#f6e9a8")
            + ch("rat", 70, 856, 1.3, expr="grin", outfit="ragged") + bread(108, 800, .9)
            + ch("rat", 225, 842, 1.4, expr="happy", outfit="hero") + ch("rat", 335, 850, 1.4, flip=True, expr="laugh", outfit="merchant")
            + ch("rat", 432, 858, 1.25, flip=True, expr="happy", outfit="plain")
            + ch("wolf", 560, 800, .78, flip=True, expr="worried") + cart(545, 852, .85))


def judgement():
    rats = (ch("rat", 62, 858, 1.25, expr="laugh", outfit="hero") + ch("rat", 185, 862, 1.2, expr="happy", outfit="ragged")
            + ch("rat", 300, 864, 1.25, expr="laugh", outfit="scribe", prop="none") + ch("rat", 425, 862, 1.2, flip=True, expr="grin", outfit="plain")
            + ch("rat", 548, 858, 1.25, flip=True, expr="happy", outfit="master"))
    return (sky("red", 10) + rays(310, 250, 11, 760, "#e9d701", .13, 15, 165) + far_city(310, 624, 1.8) + le_houses(10) + street(640)
            + '<g fill="#fff6d8" stroke="#160a22" stroke-width="2"><ellipse cx="310" cy="356" rx="150" ry="30"/><ellipse cx="230" cy="344" rx="60" ry="26"/><ellipse cx="390" cy="342" rx="70" ry="28"/></g>'
            + pole_banner(450, 350, 250, "fox", 1.9) + ch("reynard", 300, 346, 1.2, expr="laugh", sh=False)
            + notes([(150, 250, 56), (90, 170, 48), (190, 130, 44), (520, 330, 50)])
            + '<g stroke="#e9d701" stroke-width="5" fill="none" opacity=".6"><path d="M150,420 Q310,500 470,420"/><path d="M110,470 Q310,570 510,470"/></g>'
            + ch("wolf", 105, 730, .72, expr="scared", arrows=True) + ch("lion", 510, 730, .75, flip=True, expr="scared", crown=False) + crown(408, 732, 1.3, 24) + rats)


def world():
    lv = "".join(f'<ellipse cx="{310+150*math.cos(a):.0f}" cy="{440+195*math.sin(a):.0f}" rx="20" ry="9" fill="{"#4c9a4a" if i % 2 else "#2f6b3a"}" {O1} transform="rotate({math.degrees(a)+90:.0f} {310+150*math.cos(a):.0f} {440+195*math.sin(a):.0f})"/>' for i, a in enumerate([k * math.pi / 18 for k in range(36)]))
    cl = lambda x, y: f'<g fill="#fff" stroke="#160a22" stroke-width="2"><ellipse cx="{x}" cy="{y}" rx="110" ry="24"/><ellipse cx="{x-50}" cy="{y-8}" rx="50" ry="22"/><ellipse cx="{x+46}" cy="{y-10}" rx="56" ry="24"/></g>'
    return (sky("world", 11) + K.stars(70, 11, 420) + consts(11, 5, "#ffffff") + far_city(310, 872, 1.25)
            + lv + gstar(310, 440, 230) + cl(120, 300) + cl(500, 300)
            + ch("badger", 120, 296, .95, expr="happy", prop="herb", sh=False) + ch("reynard", 505, 296, .95, flip=True, expr="grin", sh=False)
            + ch("mira", 112, 800, 1.45, expr="happy", prop="mirror") + ch("rat", 512, 800, 1.5, flip=True, expr="happy", outfit="hero", prop="quill"))


# ====================================================================== GALLEONS
def g_ace():
    return (sky("dawn", 12) + '<circle cx="310" cy="560" r="250" fill="url(#halo)"/>' + far_city(500, 592, .4, op=.7) + hills(612, "#4a2f6a", 20, 2) + ground("dusk", 660)
            + f'<g transform="translate(310,590) rotate(-14)">{C.galleon(150, text=True)}<circle r="150" fill="#5a3a1a" opacity=".2"/><path d="M-110,40 q30,-30 70,-6 M20,-90 q40,-10 70,20" stroke="#5a3a1a" stroke-width="10" opacity=".3" fill="none" stroke-linecap="round"/></g>'
            + f'<path d="M70,712 Q190,640 310,668 Q430,640 550,712 L570,780 L50,780Z" fill="#3a2416" {O}/><g fill="#22130c"><ellipse cx="150" cy="720" rx="22" ry="9"/><ellipse cx="460" cy="730" rx="26" ry="10"/><ellipse cx="320" cy="750" rx="30" ry="9"/></g>'
            + f'<path d="M480,712 v-40" stroke="#3f8a4a" stroke-width="5"/><path d="M480,676 q-20,-16 -26,4 q14,8 26,-4 q20,-16 26,4 q-14,8 -26,-4Z" fill="#8fd06a" {O1}/>'
            + ch("rat", 110, 858, 1.4, expr="surprised", outfit="hero") + sp(150, 420, 1.3) + sp(480, 400, 1.1) + fg())


def g2():
    return city("red", 1.9, 2) + ch("badger", 185, 848, 1.6, expr="happy", prop="herb") + ch("rat", 445, 852, 2.0, flip=True, expr="happy", outfit="merchant")


def g3():
    return (city("red", 1.9, 3) + housefrm(505, 668, 1.5) + ch("bull", 395, 724, 1.15, expr="happy")
            + gals([(300, 800, 17, .5), (336, 802, 17, .5), (318, 786, 17, .5)])
            + ch("badger", 115, 856, 1.4, expr="happy", prop=None, galleon_on_belt=False) + ch("rat", 232, 860, 1.4, expr="happy", outfit="hero")
            + ch("rat", 560, 860, 1.4, flip=True, expr="grin", outfit="ragged"))


def g4():
    return (city("red", 1.9, 4, houses=False) + shack(80, 706, 1.4) + shack(215, 696, 1.15)
            + ch("rat", 72, 856, 1.3, expr="scared", outfit="plain") + gals([(50, 800, 13), (108, 796, 13)])
            + ch("rat", 172, 864, 1.2, expr="scared", outfit="ragged") + gals([(150, 812, 13), (204, 810, 13)])
            + ch("badger", 335, 856, 1.6, expr="angry", prop=None, galleon_on_belt=False) + ch("wolf", 535, 864, 1.1, flip=True, expr="angry"))


def g5():
    return K.art_five_of_galleons()


def g6():
    return (city("red", 1.9, 6) + heap(490, 610, 270, 120, seed=6) + ch("wolf", 490, 506, .75, flip=True, expr="smug", sh=False)
            + ch("rat", 240, 646, .9, expr="worried", outfit="ragged") + ch("rat", 300, 654, .9, expr="sad", outfit="plain") + ch("rat", 352, 644, .85, expr="worried", outfit="ragged")
            + '<path d="M440,330 Q400,290 372,380" stroke="#fff3a0" stroke-width="3" stroke-dasharray="6 8" fill="none"/>' + gal(372, 392, 15)
            + gals([(376, 622, 14, .5), (414, 630, 14, .5), (566, 624, 14, .5), (600, 616, 14, .5), (490, 634, 14, .5)])
            + ch("badger", 165, 860, 1.55, expr="happy", prop=None, galleon_on_belt=False) + ch("rat", 405, 862, 1.9, flip=True, expr="happy", outfit="ragged") + bread(282, 762, 1.5))


def g7():
    s = city("red", 1.9, 7, houses=False)
    outfits = ["plain", "hero", "lute", "scribe", "ragged", "wizard", "master"]
    spots = [(250, 650, .85), (385, 650, .85), (520, 650, .85), (120, 660, .85), (290, 780, 1.05), (430, 780, 1.05), (565, 780, 1.05)]
    for i, (x, y, sc) in enumerate(spots):
        s += shack(x, y, sc) + gal(round(x - 8 * sc), round(y - 150 * sc), round(13 * sc)) + ch("rat", round(x + 46 * sc), y + 8, .75 * sc, expr=["happy", "grin", "laugh"][i % 3], outfit=outfits[i], prop="none")
    return s + ch("badger", 100, 862, 1.5, expr="thinking", prop=None, galleon_on_belt=False)


def g8():
    return (village("day", strings=False, houses=[(575, 640, .5, '#6000AE', '#ffd75a')]) + bunting(8)
            + housefrm(150, 700, 1.35) + housefrm(430, 690, 1.55) + ladder(520, 690, 210) + ch("rat", 520, 560, 1.0, flip=True, expr="grin", outfit="hero", sh=False)
            + f'<rect x="240" y="640" width="150" height="16" rx="4" fill="url(#gWood)" {O} transform="rotate(-10 310 650)"/>' + ch("rat", 310, 750, 1.3, expr="happy", outfit="ragged")
            + ch("rat", 70, 750, 1.25, expr="laugh", outfit="plain") + garden(410, 846, 380, "weeds")
            + ch("badger", 150, 858, 1.45, expr="happy", prop="herb", galleon_on_belt=False))


def g9():
    food = (bread(140, 632, 1.3) + f'<g {O1}><ellipse cx="310" cy="622" rx="56" ry="18" fill="#d9a05a"/><path d="M270,616 l80,10 M270,628 l80,-12 M300,606 v30 M326,606 v30" stroke="#8a5a2a" fill="none"/>'
            f'<circle cx="420" cy="618" r="13" fill="#d23a4a"/><circle cx="444" cy="620" r="13" fill="#e85a5a"/><circle cx="432" cy="604" r="12" fill="#8fd06a"/>'
            f'<rect x="210" y="596" width="26" height="36" rx="4" fill="#8a6038"/><rect x="208" y="590" width="30" height="10" rx="5" fill="#fff"/><rect x="510" y="596" width="26" height="36" rx="4" fill="#8a6038"/><rect x="508" y="590" width="30" height="10" rx="5" fill="#fff"/></g>')
    return (village("dusk") + bunting(9, 34)
            + ch("badger", 135, 730, 1.2, expr="laugh", prop=None, galleon_on_belt=False) + ch("reynard", 318, 730, 1.2, expr="laugh", pose="idle") + ch("mira", 490, 730, 1.5, expr="happy", prop=None)
            + table(310, 640, 570, h=130, cloth="#6000AE") + food + candle(70, 632, 40) + candle(560, 632, 40)
            + ch("rat", 90, 864, 1.25, expr="laugh", outfit="hero") + ch("rat", 245, 866, 1.2, expr="grin", outfit="ragged")
            + ch("rat", 400, 866, 1.2, flip=True, expr="laugh", outfit="plain") + ch("rat", 545, 864, 1.25, flip=True, expr="happy", outfit="scribe", prop="none"))


def g10():
    return (sky("day", 20) + sun(110, 110, 46) + clouds(20, 60, 220, 3) + far_city(250, 560, .32, op=.22, glow=False) + hills(590, "#5a9a5a", 16, 2)
            + scene.minihouse(80, 620, .8, '#7a1fb8') + scene.minihouse(300, 610, .6, '#a3162c', '#ffe08a') + scene.minihouse(190, 630, .5, '#b8860b')
            + ground("day", 640) + stall(120, 800, 150) + garden(250, 850, 240, "veg")
            + stump_at(250, 690, .6) + ch("reynard", 250, 690, .8, expr="grin") + ch("rat", 150, 716, .7, expr="happy", outfit="plain") + ch("rat", 340, 724, .7, flip=True, expr="laugh", outfit="ragged")
            + f'<path d="M330,870 Q390,650 520,580 Q590,556 620,574 L620,870Z" fill="url(#kGrassDay)" {O}/>'
            + gals([(410, 760, 14, .6), (446, 690, 14, .6), (470, 800, 14, .6), (520, 730, 14, .6), (560, 660, 14, .6), (590, 780, 14, .6), (430, 840, 14, .6), (520, 846, 14, .6), (585, 850, 14, .6), (600, 620, 14, .6)])
            + ch("badger", 505, 600, 1.25, flip=True, expr="happy", prop=None, galleon_on_belt=False))


def g_neo():
    return (village("day", far=False) + garden(350, 846, 320, "sprouts") + gal(350, 796, 24)
            + f'<path d="M300,812 q50,-22 100,0 l6,22 h-112Z" fill="#3a2416" {O}/>' + ch("rat", 190, 852, 1.9, expr="happy", outfit="ragged")
            + ch("badger", 500, 856, 1.4, flip=True, expr="happy", prop="herb", galleon_on_belt=False))


def g_app():
    can = (f'<g transform="translate(318,726)"><path d="M0,0 h46 v44 h-46Z" fill="#7a8a9a" {O}/><path d="M46,14 l34,-18 l6,8 l-34,26Z" fill="#7a8a9a" {O}/><path d="M6,0 q16,-26 34,0" fill="none" {O}/>'
           f'<g fill="#7de3ff"><circle cx="92" cy="14" r="4"/><circle cx="100" cy="30" r="4"/><circle cx="88" cy="40" r="3.5"/><circle cx="104" cy="52" r="3.5"/></g></g>')
    return (village("day", far=False) + stick(530, 800, 530, 640) + f'<rect x="490" y="610" width="80" height="70" rx="8" fill="url(#gWoodV)" {O}/>' + gal(530, 645, 24)
            + garden(330, 852, 480, "sprouts") + ch("rat", 250, 826, 2.2, expr="determined", outfit="plain") + can)


def g_jour():
    return (village("dusk")
            + f'<g transform="translate(310,800) scale(1.7) translate(-310,-800)">{stall(310, 800, 230, inside=K.place(C.rat("happy", "merchant"), 310, 776, .8))}</g>'
            + ch("rat", 100, 864, 1.5, expr="happy", outfit="hero") + ch("rat", 540, 864, 1.3, flip=True, expr="grin", outfit="ragged"))


def g_master():
    return (village("day") + garden(480, 856, 250, "veg") + ch("badger", 548, 700, .8, flip=True, expr="happy", prop=None, galleon_on_belt=False)
            + ch("rat", 230, 848, 2.1, expr="happy", outfit="merchant") + ch("rat", 430, 856, 1.3, flip=True, expr="surprised", outfit="ragged") + sp(340, 640, 1.2))


# ====================================================================== LUTES
def l_ace():
    return (forest("day", 21) + rays(310, -60, 7, op=.13) + '<circle cx="310" cy="560" r="230" fill="url(#halo)"/>' + stump_at(310, 730, 1.2)
            + lute_at(300, 664, -62, 2.4) + notes([(440, 330, 76)]) + sp(160, 420, 1.3) + sp(470, 520, 1.1) + sp(120, 600, .9) + fg("#0c1a10"))


def l2():
    return (sky("red", 22) + far_city(400, 660, 1.7) + far_city(150, 700, .5, glow=False) + hills(710, "#3a0f1e", 18, 2) + hills(780, "#2a0a16", 14, 4)
            + f'<path d="M0,870 V610 Q120,592 250,606 Q334,618 312,706 Q300,790 356,870Z" fill="#2a1438" {O}/>' + scene.tufts(16, 0, 250, lambda x: 612, "#4a3a78", 12)
            + reynard_back(170, 612, 1.45) + notes([(330, 390, 64), (410, 310, 54)]))


def l3():
    return (forest("day", 23) + '<path d="M210,870 Q300,760 290,690 L340,690 Q360,770 430,870Z" fill="#c9a66a" opacity=".55"/>'
            + ch("reynard", 300, 846, 1.75, expr="thinking", pose="idle") + lute_at(384, 828, -100, 1.25)
            + notes([(110, 330, 60), (180, 240, 54), (100, 170, 48)]) + fg("#0c1a10"))


def l4():
    return K.art_four_of_lutes() + fg()


def l5():
    return (city("red", 1.9, 25) + ch("lion", 505, 650, .6, flip=True, expr="angry") + crate(310, 706, 1.5) + ch("reynard", 310, 600, 1.1, expr="grin", sh=False)
            + ch("wolf", 80, 800, .8, expr="angry") + ch("wolf", 560, 810, .8, flip=True, expr="angry")
            + notes([(190, 330, 56), (430, 300, 52), (120, 450, 48), (500, 440, 50), (300, 250, 46)])
            + ch("rat", 190, 864, 1.3, expr="determined", outfit="scribe") + stick(318, 760, 350, 650) + ch("rat", 300, 866, 1.3, expr="angry", outfit="hero")
            + stick(392, 760, 360, 652) + ch("rat", 410, 864, 1.3, flip=True, expr="determined", outfit="ragged") + ch("rat", 505, 866, 1.2, flip=True, expr="angry", outfit="plain", prop="quill")
            + '<g fill="#f3ecff" opacity=".35"><ellipse cx="250" cy="850" rx="40" ry="12"/><ellipse cx="460" cy="856" rx="46" ry="12"/></g>')


def l6():
    return (sky("dusk", 26) + far_city(310, 624, 1.8) + le_houses(26) + street(640) + confetti(26, 46, 520)
            + ch("reynard", 286, 596, 1.15, expr="laugh", sh=False) + horse(280, 836, 1.45) + wreath(291, 398, 1.2)
            + notes([(430, 250, 56), (500, 170, 48), (110, 270, 52), (180, 180, 46), (60, 380, 44), (540, 330, 44)])
            + ch("rat", 80, 864, 1.2, expr="laugh", outfit="hero") + ch("rat", 190, 868, 1.15, expr="grin", outfit="plain") + ch("rat", 565, 866, 1.2, flip=True, expr="laugh", outfit="ragged"))


def l7():
    return (sky("red", 27) + far_city(310, 624, 1.8) + le_houses(27) + street(640)
            + barrel(190, 730, 1.3) + crate(250, 730, 1.4) + crate(372, 730, 1.4) + crate(310, 632, 1.4) + ch("bull", 105, 770, 1.05, expr="angry")
            + ch("reynard", 310, 534, 1.15, expr="determined", sh=False)
            + notes([(180, 300, 54), (440, 290, 54), (110, 400, 46), (510, 400, 46), (250, 200, 46), (380, 190, 44), (310, 120, 50)])
            + ch("wolf", 440, 866, .9, flip=True, expr="angry") + ch("lion", 565, 866, .78, flip=True, expr="angry"))


def l8():
    return (meadow("dusk", seed=28) + ch("lion", 530, 650, .5, flip=True, expr="angry")
            + arrow(520, 300, 186) + arrow(600, 430, 174) + arrow(470, 540, 183) + arrow(560, 190, 192)
            + ch("reynard", 290, 826, 1.7, rot=-8, expr="laugh")
            + notes([(120, 300, 54), (200, 210, 50), (90, 190, 44), (420, 220, 50), (330, 150, 46), (480, 120, 42), (60, 420, 44), (250, 100, 42)])
            + arrow(250, 440, 186, 180) + arrow(190, 760, 176, 180) + fg())


def l9():
    dim = notes([(196 + i * 30, 560 - (i % 2) * 26, 44) for i in range(8)], "#9a8ab8")
    return (alley(29) + dim + ch("reynard", 300, 856, 1.7, expr="determined", pose="idle")
            + f'<path d="M250,556 Q304,538 360,560" stroke="{INK}" stroke-width="19" fill="none" stroke-linecap="round"/><path d="M250,556 Q304,538 360,560" stroke="#f6f0e2" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M252,556 l-22,-12 l4,22Z" fill="#f6f0e2" {O1}/>'
            + lute_at(448, 846, -82, 1.35) + notes([(470, 480, 58)]))


def l10():
    necks = "".join(f'<g transform="translate({x},{y}) rotate({r})"><rect x="-6" y="-70" width="12" height="70" fill="#6b4426" {O1}/><rect x="-10" y="-88" width="20" height="20" rx="3" fill="#3a2212" {O1}/></g>' for x, y, r in ((186, 486, -24), (214, 474, -6), (242, 480, 14)))
    fall = notes([(60, 200, 44), (150, 120, 40), (260, 220, 42), (360, 110, 40), (430, 260, 44), (540, 180, 40), (100, 380, 40), (470, 560, 40), (560, 700, 42), (60, 620, 40)], "#9a8ab8")
    return (sky("red", 30) + far_city(500, 430, .6) + f'<path d="M0,870 V770 Q300,710 620,470 V870Z" fill="#2a0a16" {O}/><path d="M0,870 V820 Q300,780 620,600 V870Z" fill="#1c060e"/>'
            + fall + necks + sack(214, 650, 2.5, "#6a4c34") + ch("reynard", 280, 800, 1.45, rot=-8, expr="determined", pose="idle") + rain(30, 110))


def l_neo():
    return alley(31) + ch("reynard", 185, 856, 1.5, expr="happy") + ch("rat", 445, 860, 1.9, flip=True, expr="surprised", outfit="ragged") + sp(330, 600, 1.4) + sp(360, 660, .9)


def l_app():
    zz = "".join(f'<path d="M{x},{y} l10,-14 l8,14 l10,-14 l8,14" stroke="#ff6a6a" stroke-width="4" fill="none"/>' for x, y in ((290, 610), (60, 600), (220, 500)))
    return (sky("red", 32) + far_city(310, 624, 1.7) + le_houses(32) + street(640) + statue(400, 790, 1.2, ped=90)
            + ch("rat", 180, 864, 2.0, expr="determined", outfit="lute") + notes([(300, 580, 50), (80, 570, 46), (240, 470, 44)], "#ff6a6a") + zz)


def l_jour():
    arc = lambda x0, y0, x1, y1: f'<path d="M{x0},{y0} Q{(x0+x1)/2:.0f},{min(y0, y1)-90} {x1},{y1}" stroke="#fff3a0" stroke-width="3" stroke-dasharray="5 8" fill="none"/>'
    return (tavern() + ch("rat", 310, 564, 1.9, expr="laugh", outfit="lute") + notes([(450, 330, 54), (160, 340, 50), (500, 440, 44)])
            + arc(200, 760, 180, 620) + gal(180, 612, 15) + arc(420, 770, 440, 610) + gal(440, 602, 15) + gal(360, 588, 14, .5)
            + ch("rat", 90, 864, 1.3, expr="laugh", outfit="hero") + ch("rat", 215, 868, 1.3, expr="grin", outfit="merchant")
            + ch("rat", 405, 868, 1.3, flip=True, expr="laugh", outfit="ragged") + ch("rat", 535, 864, 1.3, flip=True, expr="happy", outfit="plain"))


def l_master():
    front = "".join(ch("rat", x, 868, 1.05, flip=x > 310, expr=ex, outfit=o, prop="none") for x, o, ex in
                    ((50, "hero", "determined"), (150, "ragged", "laugh"), (250, "plain", "determined"), (370, "scribe", "laugh"), (470, "master", "determined"), (570, "wizard", "laugh")))
    return (sky("red", 33) + castle(balcony=duo("worried", "worried", arrows=True)) + street(630) + le_houses(33, right=False)
            + f'<g transform="translate(14,420)">{C.leo_banner(46, 96)}</g><g transform="translate(34,400) rotate(10)">{C.fox_banner(46, 96)}</g>' + ladder(92, 640, 190)
            + ch("rat", 92, 500, .75, flip=True, expr="grin", outfit="hero", sh=False)
            + crowd(680, 16, 1, .8) + crowd(716, 14, 2, .95) + statue(310, 740, .6, ped=60)
            + ch("rat", 318, 500, 1.15, expr="determined", outfit="lute", sh=False) + notes([(400, 400, 44), (220, 410, 40)])
            + pole_banner(130, 790, 200, "fox", 1.2) + pole_banner(470, 790, 200, "fox", 1.2) + crowd(772, 12, 3, 1.1)
            + pole_banner(240, 840, 190, "fox", 1.3) + pole_banner(560, 840, 190, "fox", 1.3) + front)


# ====================================================================== QUILLS
def q_ace():
    return (sky("red", 41) + far_city(130, 790, .9) + hills(800, "#1c060e", 10, 1)
            + '<rect x="300" width="320" height="870" fill="url(#kBrick)"/><rect x="300" width="320" height="870" fill="#000" opacity=".28"/><path d="M300,0 V870" stroke="#160a22" stroke-width="5"/>'
            + f'<circle cx="430" cy="230" r="150" fill="url(#kCandle)"/><path d="M372,310 v-120 q58,-80 116,0 v120Z" fill="#ff9a4c" {O}/><path d="M430,150 v160 M372,240 h116" stroke="#4a1020" stroke-width="7"/><rect x="356" y="306" width="148" height="18" rx="4" fill="#4a1020" {O}/>'
            + f'<g transform="translate(476,390)">{C.leo_banner(110, 240)}</g>'
            + '<g stroke="#f3ecff" stroke-opacity=".5" stroke-width="4" stroke-linecap="round"><path d="M300,220 l-34,-40 M330,300 l-30,-36 M250,250 l-26,-32"/></g>'
            + q(150, 560, 22, 3.5) + f'<g transform="translate(120,330) rotate(-20)"><rect x="-22" y="-28" width="44" height="56" fill="#f6f0e2" {O1}/></g><g transform="translate(250,700) rotate(30)"><rect x="-18" y="-24" width="36" height="48" fill="#f6f0e2" {O1}/></g>')


def q2():
    return (room("city", 42) + ch("rat", 310, 650, 2.0, expr="thinking", outfit="scribe", prop="none") + desk(310, 650, 460)
            + paper(190, 634, 78, 92, -8, "crown") + paper(430, 634, 78, 92, 8, "star") + candle(310, 630, 34)
            + q(236, 330, 6, 2.3) + f'<g transform="translate(384,330) scale(-1,1) rotate(6)">{C.quill(2.3)}</g>')


def q3():
    heart = (f'<g transform="translate(180,330) scale(1.5)"><path d="M0,70 L-64,0 C-116,-62 -42,-116 0,-62 C42,-116 116,-62 64,0Z" fill="#f6f0e2" {O}/>'
             f'<g stroke="#8a7a6a" stroke-width="1.5"><path d="M-50,-40 h100 M-56,-24 h112 M-50,-8 h100 M-36,8 h72 M-22,24 h44"/></g><path d="M-4,-58 l10,26 l-14,20 l12,30 l-8,26" stroke="#a3162c" stroke-width="3" fill="none"/></g>')
    return (room("rain", 43) + '<rect width="620" height="870" fill="#0a0414" opacity=".25"/>' + heart
            + q(120, 330, -26, 2.2) + q(176, 356, 0, 2.2) + q(226, 320, 22, 2.2) + ch("rat", 310, 856, 1.9, expr="crying", outfit="ragged") + candle(520, 850, 40))


def q4():
    doodle = (f'<g transform="translate(236,690) rotate(-6)"><rect x="-36" y="-84" width="72" height="84" fill="#f6f0e2" {O1}/><g fill="#ff7eb6">' + "".join(f'<circle cx="{10*math.cos(a):.0f}" cy="{-52+10*math.sin(a):.0f}" r="7"/>' for a in [k * math.pi / 3 for k in range(6)])
              + '</g><circle cy="-52" r="6" fill="#ffe27a"/><path d="M0,-40 v30 M0,-22 q-12,-4 -14,-14" stroke="#3f8a4a" stroke-width="3" fill="none"/></g>')
    cup = f'<path d="M436,690 v-34 h36 v34Z" fill="#3f7fd8" {O1}/>' + q(446, 660, -34, .9) + q(454, 658, -22, .9) + q(462, 660, -8, .9)
    plant = f'<path d="M150,690 l4,-30 h30 l4,30Z" fill="#a3562c" {O1}/><path d="M169,660 q-20,-20 -16,-40 q14,10 16,40 q4,-34 20,-44 q4,24 -20,44" fill="#5fae4a" {O1}/>'
    return office() + ch("rat", 340, 706, 1.9, expr="happy", outfit="scribe") + desk(320, 706, 400) + doodle + cup + plant


def q5():
    return (office() + q(390, 852, 70, 1.3) + q(300, 836, 110, 1.3) + ch("rat", 450, 790, 1.3, expr="sad", outfit="plain") + ch("rat", 560, 750, 1.1, expr="crying", outfit="ragged")
            + ch("wolf", 180, 860, 1.15, expr="smug") + q(196, 706, -44, 1.6) + q(214, 704, -24, 1.6) + q(232, 706, -4, 1.6))


def q6():
    rip = "".join(f'<path d="M{(i*83)%560+10},{480+(i*47)%370} q20,-8 40,0" />' for i in range(26))
    return (sky("dusk", 46) + gstar(480, 150, 160) + far_city(120, 452, .62) + '<path d="M370,452 Q500,410 620,440 V470 H370Z" fill="#2a1648"/>' + scene.minihouse(540, 446, .36, '#7a1fb8') + scene.minihouse(470, 450, .26, '#a3162c')
            + f'<rect y="450" width="620" height="420" fill="url(#kWater)"/><polygon points="440,450 520,450 420,870 240,870" fill="#fff3a0" opacity=".14"/><g stroke="#bcd0ff" stroke-opacity=".45" stroke-width="2.5" fill="none">{rip}</g>'
            + ch("rat", 140, 700, 1.1, flip=True, expr="sad", outfit="plain", sh=False) + ch("rat", 250, 700, 1.25, expr="determined", outfit="hero", sh=False) + ch("rat", 340, 704, 1.0, expr="happy", outfit="ragged", sh=False)
            + "".join(q(404 + i * 17, 690, -30, 1.35) for i in range(6)) + boat(310, 740, 1.6) + stick(262, 650, 150, 810) + f'<ellipse cx="146" cy="816" rx="16" ry="30" fill="#8a6038" {O1} transform="rotate(34 146 816)"/>')


def q7():
    outfits = ["plain", "hero", "lute", "wizard", "master", "ragged", "merchant"]
    line = "".join(ch("rat", 160 + i * 64, 656, .75, expr=["happy", "grin"][i % 2], outfit=o, prop="quill") for i, o in enumerate(outfits))
    can = f'<rect x="46" y="760" width="26" height="46" rx="4" fill="#e9d701" {O1}/><rect x="52" y="748" width="14" height="14" fill="#2a2e36" {O1}/><g fill="#e9d701" opacity=".7"><circle cx="90" cy="748" r="4"/><circle cx="104" cy="756" r="3"/><circle cx="98" cy="740" r="3"/></g>'
    return (office(door=True) + line + ch("reynard", 110, 864, 1.4, expr="smug", pose="idle") + can
            + heap(300, 864, 240, 104, fake=True, seed=7) + ch("wolf", 500, 866, 1.15, flip=True, expr="greedy"))


def q8():
    return K.art_eight_of_quills()


def q9():
    return (room("city", 49) + '<rect width="620" height="870" fill="#0a0414" opacity=".3"/>' + "".join(q(40, 150 + i * 30, 60, 2.3) for i in range(9))
            + ch("rat", 250, 744, 1.9, expr="scared", outfit="plain", sh=False) + bed(330, 856, 1.7))


def q10():
    return (room("dawn", 50) + ch("rat", 300, 660, 1.9, expr="crying", outfit="plain") + desk(310, 660, 480)
            + papers(170, 640, 9, 84) + papers(440, 640, 12, 84) + papers(530, 856, 8, 96) + papers(90, 856, 6, 96)
            + q(148, 588, -42, 1.25) + q(172, 588, -24, 1.25) + q(194, 588, -4, 1.25) + q(416, 570, -46, 1.25) + q(440, 570, -28, 1.25) + q(462, 570, -8, 1.25)
            + q(512, 810, -34, 1.25) + q(542, 810, -6, 1.25) + q(76, 822, -34, 1.25) + q(104, 822, -6, 1.25))


def q_neo():
    doodles = (f'<g transform="translate(455,330) skewY(8)" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M40,0 L64,74 L2,28 H78 L16,74Z" stroke="#ffd75a" stroke-width="7"/>'
               f'<path d="M20,130 l14,26 l14,-10 l14,10 l14,-26 l-6,44 l-22,18 l-22,-18Z" stroke="#f59545" stroke-width="6"/><path d="M60,230 c-30,-30 10,-50 20,-22 c10,-28 50,-8 20,22 l-20,20Z" stroke="#ff7eb6" stroke-width="6"/></g>')
    return (alley(51) + doodles + crate(90, 800, 1.2) + ch("rat", 350, 858, 2.0, expr="happy", outfit="ragged")
            + f'<rect x="398" y="734" width="14" height="42" rx="4" fill="#d23a4a" {O1} transform="rotate(24 405 756)"/>')


def q_app():
    plan = (f'<path d="M90,640 L150,400 M270,640 L210,400 M180,400 V660" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M90,640 L150,400 M270,640 L210,400 M180,400 V660" stroke="#8a6038" stroke-width="5" stroke-linecap="round"/>'
            f'<rect x="60" y="390" width="240" height="190" fill="#2a5ab8" {O}/><g stroke="#fff" stroke-width="3" fill="none"><path d="M110,540 V470 H250 V540 Z M100,470 Q180,380 260,470 M165,540 v-36 h30 v36"/><circle cx="215" cy="500" r="12"/><path d="M80,560 h200" stroke-dasharray="6 6"/></g>')
    return (village("day", far=False) + housefrm(490, 700, 1.4) + plan + ch("rat", 370, 856, 2.1, expr="determined", outfit="hero")
            + f'<rect x="418" y="716" width="11" height="58" rx="3" fill="#ffd75a" {O1} transform="rotate(24 423 745)"/>')


def q_jour():
    board = (stick(70, 660, 70, 340) + stick(250, 660, 250, 340) + f'<rect x="40" y="350" width="240" height="220" fill="#8a5a32" {O}/><rect x="52" y="362" width="216" height="196" fill="#b08a5a"/>'
             + paper(110, 460, 70, 84, -5, "star") + paper(200, 450, 70, 84, 4, "star") + paper(150, 548, 80, 70, 2, "star"))
    return (city("red", 1.9, 53) + board + paper(470, 420, 54, 66, 20, "star") + paper(545, 560, 54, 66, -16, "star") + paper(400, 300, 48, 58, -30, "star")
            + ch("rat", 380, 862, 2.0, expr="grin", outfit="scribe"))


def q_master():
    scroll = (f'<path d="M196,560 q-12,130 14,240 l84,8 q-22,-120 -10,-246Z" fill="#f6f0e2" {O}/><g stroke="#8a7a6a" stroke-width="2">' + "".join(f'<path d="M{212+i},{590+i*26} h56"/>' for i in range(7))
              + f'</g><circle cx="262" cy="784" r="14" fill="#6000AE" {O1}/>' + sp(262, 784, .8) + f'<rect x="186" y="548" width="104" height="18" rx="9" fill="#e8dfc8" {O1}/>')
    return (sky("dusk", 54) + far_city(310, 624, 1.7) + le_houses(54) + street(640) + crowd(716, 12, 5, 1.0) + crate(330, 740, 1.5)
            + ch("rat", 330, 636, 2.0, expr="determined", outfit="master", prop="quill") + scroll
            + ch("rat", 70, 866, 1.2, expr="happy", outfit="hero") + ch("rat", 440, 868, 1.2, flip=True, expr="grin", outfit="plain") + ch("rat", 555, 866, 1.2, flip=True, expr="happy", outfit="ragged"))


# ====================================================================== MIRRORS
def m_ace():
    inner = '<rect x="-130" y="-170" width="260" height="340" fill="#1c0a40"/>' + gstar(0, 0, 170)
    return (forest("night", 61, moon_at=(500, 140, 56)) + '<circle cx="310" cy="480" r="260" fill="url(#halo)"/>'
            + f'<rect x="296" y="640" width="28" height="150" fill="url(#gGold)" {O}/>' + bigmirror(310, 480, 122, 166, inner) + pond(310, 806, 250, 54)
            + ch("frog", 500, 820, 1.7, sh=False) + sp(120, 380, 1.4) + sp(500, 420, 1.2) + sp(150, 620, 1) + fireflies(61, 8) + fg())


def m2():
    cap = f'<rect x="-70" y="-100" width="140" height="200" fill="#d8f0d0"/><path d="M-40,20 Q0,-50 46,-4 L60,8 Q0,2 -40,30Z" fill="url(#gGreen)" {O}/><path d="M0,-18 Q-22,-58 -40,-62 Q-28,-36 -8,-10Z" fill="#d23a4a" {O1}/>'
    hat = f'<rect x="-70" y="-100" width="140" height="200" fill="#eadcff"/><path d="M-50,40 Q0,22 50,40 Q0,50 -50,40Z" fill="#2b0a52" {O}/><path d="M-26,34 Q-10,-20 20,-50 Q14,-10 28,34Z" fill="url(#gPurple)" {O}/>'
    return (forest("dusk", 62) + bigmirror(232, 570, 64, 98, cap, stand=True) + bigmirror(388, 570, 64, 98, hat, stand=True)
            + ch("mira", 92, 856, 2.0, expr="happy", prop=None) + ch("rat", 538, 860, 1.9, flip=True, expr="happy", outfit="hero") + sp(310, 400, 1.4) + fg())


def m3():
    inner = '<rect x="-90" y="-130" width="180" height="260" fill="#eadcff"/><path d="M0,40 c-60,-60 20,-100 0,-44 c-20,-56 60,-16 0,44Z" fill="#ff7eb6" transform="translate(0,-10) scale(1.2)"/>' + sp(-40, -70, 1.4) + sp(46, -50, 1) + sp(30, 70, 1.2)
    wisps = "".join(f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" opacity=".22"/><circle cx="{x}" cy="{y}" r="7" fill="#fff" opacity=".8"/>' for x, y, c in ((200, 300, "#7de3ff"), (360, 250, "#b06cff"), (290, 420, "#62ffa1")))
    return (forest("night", 63, moon_at=(130, 120, 54)) + wisps + '<path d="M70,0 V270 M545,0 V240" stroke="#c9a66a" stroke-width="3"/>' + hmirror(70, 300, 1.8) + hmirror(545, 270, 1.8)
            + ch("rat", 60, 760, .9, expr="laugh", outfit="hero") + ch("rat", 150, 780, .85, expr="happy", outfit="ragged")
            + bigmirror(460, 600, 86, 126, inner, stand=True) + ch("mira", 250, 856, 2.3, expr="laugh", prop=None) + ch("frog", 570, 856, 1.5) + fg())


def m4():
    old = (f'<rect x="-80" y="-110" width="160" height="220" fill="#cfd6dc"/><path d="M-40,-10 L-50,-60 L-16,-40Z M40,-10 L50,-60 L16,-40Z" fill="#7a7786" {O1}/><ellipse cx="0" cy="14" rx="52" ry="46" fill="#8a8794" {O}/>'
           f'<path d="M-32,2 q10,8 20,0 M12,2 q10,8 20,0 M-20,40 q20,-14 40,0 M-36,-16 l16,6 M36,-16 l-16,6 M-44,22 l-20,6 M44,22 l20,6" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    return (meadow("day", far=False, seed=64) + tree(450, 770, 2.5) + bigmirror(128, 640, 76, 106, old, crack=True, stand=True)
            + ch("mira", 320, 856, 2.1, expr="sad", prop=None) + hmirror(470, 850, 1.7, 80) + hmirror(548, 826, 1.7, 100) + hmirror(590, 862, 1.5, 76) + fg("#0c1a10"))


def m5():
    broken = ""
    for x, y in ((430, 810), (520, 850), (585, 790)):
        broken += (f'<g transform="translate({x},{y})"><ellipse rx="50" ry="24" fill="url(#gGold)" {O}/><ellipse rx="38" ry="17" fill="#1c0638" {O1}/>'
                   f'<g fill="#bfe6ff" {O1}><path d="M-30,-4 l16,-10 l6,14Z M4,6 l18,-12 l4,14Z M-44,24 l14,-8 l6,14Z M40,22 l12,-12 l8,16Z M-6,-30 l10,-12 l8,14Z"/></g></g>')
    return (sky("dusk", 65) + scene.minihouse(500, 500, .42, '#7a1fb8') + scene.minihouse(570, 506, .32, '#a3162c') + hills(520, "#3a2a5a", 14, 2)
            + '<path d="M0,540 Q310,500 620,560 V620 Q310,560 0,600Z" fill="url(#kWater)"/>'
            + f'<path d="M360,560 Q440,480 520,566 L520,590 Q440,520 360,584Z" fill="url(#kStone)" {O}/>' + ground("dusk", 640)
            + bigmirror(70, 650, 40, 60, stand=True) + bigmirror(165, 630, 40, 60, stand=True) + ch("mira", 280, 856, 2.0, expr="sad", prop=None) + broken + fg())


def m6():
    hang = [(40, 430), (100, 480), (165, 440), (215, 500), (70, 540)]
    return (village("day", far=False, strings=False) + tree(110, 760, 2.2)
            + "".join(f'<path d="M{x},{y-60} V{y-22}" stroke="#c9a66a" stroke-width="2.5"/>' + hmirror(x, y, 1.15) for x, y in hang)
            + ch("mira", 330, 856, 1.9, expr="happy", prop="mirror") + ch("rat", 505, 860, 1.3, flip=True, expr="happy", outfit="ragged") + sp(420, 640, 1.2))


def m7():
    r, ry = 56, 74
    bg = lambda c: f'<rect x="-{r+24}" y="-{ry+28}" width="{2*r+48}" height="{2*ry+56}" fill="{c}"/>'
    starc = bg("#2a1a5a") + gstar(0, -10, 120) + '<g fill="#f3ecff"><ellipse cx="-30" cy="36" rx="60" ry="24"/><ellipse cx="-56" cy="20" rx="30" ry="20"/><ellipse cx="6" cy="20" rx="34" ry="24"/></g>'
    coins = bg("#3a2a10") + heap(0, 66, 110, 80, seed=9)
    mansion = bg("url(#kDay)") + f'<g {O1}><rect x="-44" y="-10" width="88" height="70" fill="#f6f0e2"/><path d="M-54,-10 L0,-50 L54,-10Z" fill="#a3162c"/><rect x="-10" y="24" width="20" height="36" fill="#5a3a22"/><rect x="-34" y="4" width="16" height="18" fill="#7de3ff"/><rect x="18" y="4" width="16" height="18" fill="#7de3ff"/></g><rect x="-80" y="60" width="160" height="40" fill="url(#kGrassDay)"/>'
    rey = bg("#2a1648") + K.place(C.reynard("grin"), 0, 70, .44)
    laurel = bg("#eadcff") + K.place(C.mira("happy", None), 0, 100, .5) + wreath(0, -6, .8)
    suit = bg("#cfd6dc") + K.place(C.mira("smug", None), 0, 100, .5) + f'<path d="M-22,22 h44 v60 h-44Z" fill="url(#gSuit)" {O1}/><path d="M-6,22 l6,16 l6,-16Z" fill="#f2f2f2"/><path d="M-3,26 h6 l2,22 l-5,6 l-5,-6Z" fill="#c0182e"/>'
    thr = bg("#5a0f1e") + f'<path d="M-36,70 V-30 Q0,-64 36,-30 V70Z" fill="url(#gRobe)" {O}/>' + crown(0, 10, 1.5)
    spots = [(310, 180, 78, 100, starc), (105, 300, r, ry, coins), (515, 300, r, ry, mansion), (80, 540, r, ry, rey), (540, 540, r, ry, laurel), (150, 760, r, ry, suit), (470, 760, r, ry, thr)]
    return (cosmos(67) + "".join(bigmirror(x, y, a, b, inner) for x, y, a, b, inner in spots)
            + ch("mira", 310, 730, 1.7, expr="surprised", prop=None, sh=False) + "".join(sp(x, y, s_) for x, y, s_ in ((230, 330, 1.2), (400, 340, 1), (250, 790, 1.1), (380, 800, .9))))


def m8():
    mts = ('<polygon points="-20,640 130,360 230,520 330,300 450,540 540,400 640,640" fill="#1c1446" stroke="#160a22" stroke-width="2"/>'
           '<polygon points="130,360 156,410 136,404 112,424 104,408Z M330,300 362,366 338,356 312,380 300,360Z M540,400 562,440 540,434 522,450Z" fill="#f3f0ff" opacity=".8"/>')
    row = lambda xs, y: "".join(bigmirror(x, y, 40, 56, stand=True) for x in xs)
    return (sky("night", 68) + moon(450, 160, 76) + mts + ground("night", 640)
            + '<path d="M250,870 Q330,760 390,700 Q430,664 420,640 L444,640 Q460,680 420,730 Q380,790 370,870Z" fill="#c9b78e" opacity=".45"/>'
            + stick(452, 640, 446, 500) + ch("mira", 420, 640, 1.1, expr="thinking", prop=None) + ch("frog", 350, 668, 1.0)
            + row((150, 262, 486), 700) + row((90, 200, 310, 420, 530), 800))


def m9():
    xs = [122, 160, 198, 236, 274, 398, 436, 474, 512]
    hang = "".join(f'<path d="M{x},352 V{372}" stroke="#c9a66a" stroke-width="2"/>' + hmirror(x, 392, .85) for x in xs)
    n = 14
    awn = "".join(f'<path d="M{96+i*30.6:.0f},300 h30.6 v44 q-15,22 -30.6,0Z" fill="{"#4b0f86" if i % 2 == 0 else "#e9d701"}" {O1}/>' for i in range(n))
    graf = (f'<g transform="translate(8,500) skewY(-9)" font-family="Pirata One, Georgia, serif" font-size="40" font-weight="700" fill="#ffe94a" stroke="#3d0872" stroke-width="2" paint-order="stroke"><text x="0" y="0">Chaotic</text><text x="14" y="36">Good</text><text x="26" y="70">Guild</text></g>'
            + gstar(60, 400, 60, False))
    ball = f'<circle cx="310" cy="676" r="60" fill="url(#halo)"/><path d="M286,722 q24,-14 48,0 l4,8 h-56Z" fill="url(#gGold)" {O1}/><circle cx="310" cy="682" r="32" fill="url(#ballGlow)" {O}/>' + sp(312, 680, .9, "#fff")
    lamp = f'<g transform="translate(420,716)" {O1}><path d="M-22,10 q-4,-18 22,-18 q26,0 30,10 q14,-10 18,-4 q-8,4 -14,14Z" fill="url(#gGold)"/><path d="M-22,2 q-14,-4 -10,8 q4,6 10,0" fill="none" stroke="url(#gGold)" stroke-width="3"/><circle cx="4" cy="-12" r="3.5" fill="url(#gGold)"/></g>'
    return (alley(69) + graf + stick(100, 860, 100, 300) + stick(522, 860, 522, 300) + '<rect x="110" y="310" width="404" height="420" fill="#1c0638" opacity=".5"/>' + awn + hang
            + ch("mira", 310, 770, 1.7, expr="smug", prop=None, sh=False) + table(310, 730, 420, h=130, cloth="#6000AE")
            + ball + tarot(205, 724, 3, 1.1) + lamp + crystals(486, 722, 1.3) + ch("frog", 140, 728, 1.3, sh=False) + cauldron(566, 846, .32) + candle(60, 856, 36))


def m10():
    arc = ""
    for i in range(9):
        a = math.pi * (1 - i / 8)
        x, y = 330 + 262 * math.cos(a), 440 - 300 * math.sin(a)
        arc += hmirror(round(x), round(y), 1.0, round(math.degrees(math.pi / 2 - a))) + sp(round(x), round(y) + 54, .7)
    return (city("red", 1.9, 70) + '<circle cx="330" cy="500" r="290" fill="url(#halo)"/>' + bigmirror(330, 520, 150, 200, mini_village(150, 200), stand=True) + arc
            + ch("mira", 110, 864, 1.6, expr="happy", prop=None) + ch("frog", 222, 866, 1.5) + flower_crack(560, 860, 1.2))


def m_neo():
    pile = (f'<path d="M270,790 h130 l8,40 h-146Z" fill="url(#gBlue)" {O}/><path d="M276,770 h118 l6,22 h-130Z" fill="#5a9ae8" {O}/><path d="M290,772 Q330,740 336,690 Q352,740 380,772Z" fill="url(#gBlue)" {O}/>'
            + sp(334, 740, .8, "#bfe6ff") + hmirror(392, 742, 1.0, 20))
    return (forest("night", 71, moon_at=(310, 170, 100)) + ch("mira", 170, 856, 2.1, expr="happy", prop=None) + pile
            + ch("rat", 500, 860, 1.9, flip=True, expr="surprised", outfit="hero") + ch("frog", 60, 858, 1.5) + fireflies(71, 8) + fg())


def m_app():
    return (meadow("dusk", seed=72) + gstar(150, 150, 150) + '<g fill="#3a2a5a"><ellipse cx="130" cy="196" rx="110" ry="34"/><ellipse cx="80" cy="176" rx="50" ry="30"/><ellipse cx="190" cy="174" rx="60" ry="34"/></g>'
            + tree(570, 730, 1.8, "#2a4a3a", "#3f6a4a")
            + '<path d="M250,690 C320,640 300,560 380,520 C440,490 400,420 420,380" stroke="#b06cff" stroke-width="6" stroke-dasharray="4 12" fill="none" stroke-linecap="round"/>'
            + ch("reynard", 410, 300, 1.25, rot=180, expr="laugh", pose="idle", sh=False) + ch("rat", 190, 856, 1.9, expr="worried", outfit="wizard")
            + "".join(sp(x, y, s_, "#b06cff") for x, y, s_ in ((300, 600, 1.2), (360, 500, 1), (460, 420, 1.3), (330, 330, .9), (500, 560, .8))) + fg())


def m_jour():
    return (forest("night", 73, moon_at=(130, 140, 72)) + pond(460, 816, 150, 36) + '<circle cx="400" cy="430" r="200" fill="url(#halo)"/>'
            + '<path d="M250,700 Q300,640 330,540" stroke="#b06cff" stroke-width="5" stroke-dasharray="4 12" fill="none" stroke-linecap="round"/>'
            + bigmirror(400, 430, 96, 126, mini_city(96, 126)) + sp(290, 330, 1.3) + sp(520, 350, 1.1) + sp(500, 560, 1) + sp(300, 560, .9)
            + ch("rat", 170, 856, 1.9, expr="determined", outfit="wizard", prop="none") + tarot(340, 860, 5, 1.2) + fg())


def m_master():
    return (alley(74) + bigmirror(535, 530, 60, 88, mini_village(60, 88), stand=True) + ch("rat", 215, 750, 2.0, expr="happy", outfit="master")
            + table(290, 750, 310, h=116, cloth="#6000AE") + tarot(290, 744, 4, 1.1) + candle(160, 742, 30)
            + ch("rat", 470, 864, 1.35, flip=True, expr="crying", outfit="ragged") + flower_crack(90, 858, 1.3)
            + '<path d="M392,560 c-22,-22 8,-38 16,-16 c8,-22 38,-6 16,16 l-16,16Z" fill="#ff7eb6" stroke="#160a22" stroke-width="2"/>')


# ====================================================================== the deck
MAJORS = [
    ("0", "The Fool", fool, "A brave young rat in a Robin Hood outfit strides out of his shelter at dawn while his mother watches, proud and sad."),
    ("I", "The Magician", magician, "Reynard stands at a table set with a galleon, a lute, a quill and a mirror, the Guild star above him."),
    ("II", "The High Priestess", priestess, "Mira sits between a purple pillar and a gold one beneath a great moon, mirror in paw, her frog beside her."),
    ("III", "The Empress", empress, "The Badger tends a garden where every vegetable has its own space, so everybody can eat."),
    ("IV", "The President", president, "A rat presides from a soapbox to a cheering crowd while Reynard, in the background, pulls down the LEO's statue."),
    ("V", "The Hierophant", hierophant, "A cardinal with a vine-wrapped staff topped by the Guild star teaches two rats in a sunlit forest."),
    ("VI", "The Partners", partners, "In a dark alley the Badger brings a lantern and bread to a weeping rat; the Guild star shines between the rooftops."),
    ("VII", "The Chariot", chariot, "Reynard walks a hallway of arcade games and slot machines without a glance, toward a lute and a galleon on a pedestal."),
    ("VIII", "Strength", strength, "The Bull laughs as he shoulders a great beam and the rats raise a house together."),
    ("IX", "The Hermit", hermit, "A robed rat stands on a snowy peak beneath the constellations, holding a lantern lit by the Guild star."),
    ("X", "Chaos!", chaos, "The great wheel spins: Reynard laughs on top while the LEO Lion clings on and the Corporate Wolf tumbles off."),
    ("XI", "Justice", justice, "The Badger stands beneath golden scales where a single flower outweighs a heap of gold."),
    ("XII", "The Hanged Man", hanged, "Reynard hangs by one ankle from a snare, loot spilled below him, as a friend arrives with a quill to cut the rope."),
    ("XIII", "Death", death, "Above, Reynard flees the Lawful Evil city for the woods. Below, the Badger walks toward it as the rats cheer her on."),
    ("XIV", "Temperance", temperance, "Mira pours a potion into a swirling purple-and-gold cauldron while her frog cheers and the Guild star shines."),
    ("XV", "The LEO", the_leo, "Reynard and a scribe sit in the stocks while the rat who sold them out holds one coin beside the laughing Lion and Wolf."),
    ("XVI", "The Tower", tower, "Lightning splits the LEO's tower; Guild stars fly where stones should, and Reynard and a scribe look on, pleased."),
    ("XVII", "The Star", star, "Two rats sit by a pond beneath the great Guild star and its seven companions."),
    ("XVIII", "The Moon", moon_card, "Under a heavy moon, the Wolf howls and Mira studies her mirror on either side of a winding path; her frog rises from the pond."),
    ("XIX", "The Sun", sun_card, "A fox-faced sun winks over a rat bazaar in the LEO's own square; the Lion rages on his balcony and the Wolf is ignored."),
    ("XX", "Judgement", judgement, "Reynard plays from the clouds beside the fox banner; the rats rise, the Lion cowers with his crown on the ground, the Wolf panics."),
    ("XXI", "The World", world, "The Guild star in a laurel wreath, with the Badger, Reynard, Mira and a rat at the four corners, above the red city."),
]
NUM = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
NAMES = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Neophyte", "Apprentice", "Journeyman", "Master"]
SUITS = {
    "galleons": ("Galleons", [
        (g_ace, "One dingy galleon lies half-buried at dawn, a sprout beside it, waiting for somebody to find it."),
        (g2, "The Badger trades an herb to a merchant rat for a galleon; both walk away winners."),
        (g3, "The Badger and two rats add their galleons to a pile while the Bull builds them houses."),
        (g4, "The Badger stands between the Corporate Wolf and two frightened rats clutching their galleons."),
        (g5, "The Badger stands downcast by her collapsed shanty while the Lion and the Wolf laugh over their galleons."),
        (g6, "The Badger shares her bread with a ragged rat; behind her the Wolf flips a single coin from his hoard to beggars."),
        (g7, "The Badger looks over seven small shanties and the rats who live in them, thinking about what comes next."),
        (g8, "The rats raise unfinished mushroom houses while the Badger pulls weeds; hard work, done together."),
        (g9, "A feast in the mushroom village: the Badger, Reynard, Mira and the rats celebrate what they built."),
        (g10, "The Badger looks down from her hill on a bustling village; Reynard plays on a stump and ten galleons shine in the grass."),
        (g_neo, "A ragged rat plants a first galleon like a seed while the Badger shows the way."),
        (g_app, "A rat waters rows of new sprouts, patient and careful."),
        (g_jour, "A merchant rat keeps an honest stall, trading fair with everyone who comes."),
        (g_master, "A prosperous rat hands a galleon to a young one, passing on what was given."),
    ]),
    "lutes": ("Lutes", [
        (l_ace, "A lute rests on a stump in a sunlit clearing, one note hanging in the air."),
        (l2, "Reynard stands at a cliff's edge, lute in hand, looking out over the kingdom of the Lawful Evil overlords."),
        (l3, "Reynard walks through the woods with his lute, thinking hard."),
        (l4, "Reynard plays atop a stump and rats in every sort of outfit dance."),
        (l5, "Chaos in the street: Reynard plays an inspiring tune as rats with quills and sticks face shouting wolves and a LEO."),
        (l6, "Reynard rides in triumph, crowned with laurel, playing as cheering rats walk beside his horse."),
        (l7, "Reynard holds the high ground on a barricade, the Bull beside him, as the Wolf and the Lion rage below."),
        (l8, "Reynard dances between flying arrows, still playing, still laughing."),
        (l9, "Bandaged and weary in an alley, Reynard stands his ground with his lute close by."),
        (l10, "Reynard trudges uphill in the rain under a heavy bundle of lutes, and does not stop."),
        (l_neo, "In an alley of the red city, Reynard offers his lute to a young rat in beggar's clothes."),
        (l_app, "A rat dressed like Reynard sits beneath the LEO's golden statue, tuning his lute; the notes come out sour."),
        (l_jour, "The rat plays gleefully on the Guild Hall stage while the audience dances and tosses galleons."),
        (l_master, "The rat plays from atop the LEO's statue to a vast crowd under fox banners; on the balcony the Lion and the Wolf worry."),
    ]),
    "quills": ("Quills", [
        (q_ace, "A single quill falls from a window of the Lawful Evil castle."),
        (q2, "A scribe sits between two documents, one sealed with a crown and one with a star, two quills crossed above him."),
        (q3, "Three quills pierce a heart-shaped letter while a rat weeps and rain streaks the window."),
        (q4, "In a corporate cubicle, a scribe uses a quiet moment to draw a flower."),
        (q5, "The Wolf smirks over the quills he has taken as two rats walk away."),
        (q6, "Three rats row away from the red city toward the Guild star, six quills standing in the bow."),
        (q7, "Reynard distracts the Wolf with a heap of spray-painted coins while seven rats each carry a quill out the door."),
        (q8, "A scribe slumps at his desk with one quill in hand and seven broken on the floor."),
        (q9, "A rat sits bolt upright in bed beneath nine quills, the red city in the window."),
        (q10, "A rat weeps at a desk buried in paperwork stuck with ten quills; in the window, dawn and the Guild star."),
        (q_neo, "A ragged rat draws on an alley wall with a crayon."),
        (q_app, "A rat with a pencil sketches plans for a mushroom house."),
        (q_jour, "A scribe posts pamphlets on a notice board and sends more flying."),
        (q_master, "A robed rat with a great quill reads a charter to the crowd."),
    ]),
    "mirrors": ("Mirrors", [
        (m_ace, "A great mirror rises from a moonlit pond, the Guild star shining in its glass."),
        (m2, "Mira and a rat each look into a mirror and see the other's hat: what we admire in others is in us too."),
        (m3, "Mira laughs at her reflection, delighted with herself, among the creatures of the enchanted forest."),
        (m4, "Mira pouts beneath a tree before a cracked mirror that shows her older and sadder; three other mirrors lie ignored."),
        (m5, "Mira grieves over three broken mirrors while two still stand whole behind her."),
        (m6, "Mira gives a mirror to a young rat beneath a tree hung with five more."),
        (m7, "Mira floats in a galaxy among seven mirrors of tempting things; in the centre one, the Guild star peeks from a cloud."),
        (m8, "Mira walks away from eight mirrors toward the moonlit mountains, her frog hopping after."),
        (m9, "Mira reads tarot at her alley booth in the red city, with her frog, her cauldron and a genie lamp."),
        (m10, "In the red city, Mira looks into a great mirror and sees a happy hamlet beneath an arc of nine more."),
        (m_neo, "Under a bright moon, Mira hands blue robes, a hat and a mirror to a rat in a Robin Hood outfit."),
        (m_app, "A rat in oversized robes accidentally levitates Reynard upside down; Reynard thinks it's hilarious."),
        (m_jour, "By a forest pool, a robed rat levitates a mirror that shows the red city; tarot cards lie at his feet."),
        (m_master, "In an alley, a rat in purple robes comforts a crying young rat; a mirror shows the village, and a flower grows from a crack."),
    ]),
}


def suit_icon(suit, x, y):
    return K.suit_icon(suit, x, y)


def frame(i, numeral, title, suit, art):
    n = len(title)
    fs = 64 if n <= 10 else 54 if n <= 14 else 46 if n <= 18 else 40
    corner = lambda x, y, sx, sy: (f'<g transform="translate({x},{y}) scale({sx},{sy})"><path d="M0,54 V18 Q0,0 18,0 H54" fill="none" stroke="#e9d701" stroke-width="5"/>'
                                   f'<path d="M10,44 Q10,10 44,10" fill="none" stroke="#e9d701" stroke-width="2"/><circle cx="18" cy="18" r="5" fill="#e9d701"/></g>')
    return f'''<svg class="card" viewBox="0 0 700 1200" role="img" aria-label="{e(title)}">
<defs><clipPath id="cardArt{i}"><rect x="40" y="112" width="620" height="870" rx="22"/></clipPath></defs>
<rect x="4" y="4" width="692" height="1192" rx="40" fill="#1c0638" stroke="#e9d701" stroke-width="6"/>
<rect x="14" y="14" width="672" height="1172" rx="32" fill="url(#kLattice)"/>
<rect x="20" y="20" width="660" height="1160" rx="28" fill="none" stroke="#e9d701" stroke-width="1.5" opacity=".6"/>
<path d="M250,34 H450 Q470,34 476,62 Q470,92 450,92 H250 Q230,92 224,62 Q230,34 250,34Z" fill="#1c0638" stroke="#e9d701" stroke-width="3"/>
{suit_icon(suit, 150, 62)}{suit_icon(suit, 550, 62)}
<text x="350" y="82" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="52" fill="#e9d701">{numeral}</text>
<g clip-path="url(#cardArt{i})"><g transform="translate(40,112)">{art}
<rect width="620" height="870" fill="url(#kHatch)" opacity=".05"/><rect width="620" height="870" fill="url(#kVig)"/></g></g>
<rect x="40" y="112" width="620" height="870" rx="22" fill="none" stroke="#e9d701" stroke-width="4"/>
<rect x="48" y="120" width="604" height="854" rx="16" fill="none" stroke="#160a22" stroke-width="2" opacity=".7"/>
{corner(30, 102, 1, 1)}{corner(670, 102, -1, 1)}{corner(30, 992, 1, -1)}{corner(670, 992, -1, -1)}
<path d="M56,1010 H644 L620,1080 L644,1150 H56 L80,1080Z" fill="#f3e6c4" stroke="#e9d701" stroke-width="4"/>
<path d="M56,1010 H644 L636,1034 H64Z" fill="#fff" opacity=".35"/><path d="M64,1126 H636 L644,1150 H56Z" fill="#000" opacity=".12"/>
<path d="M70,1022 H630 L610,1080 L630,1138 H70 L90,1080Z" fill="none" stroke="#3d0872" stroke-width="1.5" opacity=".5"/>
<text x="350" y="{1080 + fs * .32:.0f}" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="{fs}" fill="#3d0872">{e(title)}</text>
</svg>'''


def all_cards():
    out = []
    for k, (num, title, fn, desc) in enumerate(MAJORS):
        out.append({"id": f"major-{k:02d}", "name": title, "arcana": "major", "suit": "major", "rank": k, "numeral": num, "scene": desc, "fn": fn})
    for suit, (sname, lst) in SUITS.items():
        for r, (fn, desc) in enumerate(lst):
            numeral = NUM[r] if r < 10 else NAMES[r][0]
            out.append({"id": f"{suit}-{r+1:02d}", "name": f"{NAMES[r]} of {sname}", "arcana": "minor", "suit": suit, "rank": r + 1, "numeral": numeral, "scene": desc, "fn": fn})
    return out


CSS = K.CSS + """
h2 { font-family: "Pirata One", Georgia, serif; font-weight: 400; font-size: 38px; color: var(--gold); margin: 44px 0 14px; }
figure { content-visibility: auto; contain-intrinsic-size: 260px 560px; }
nav { display: flex; flex-wrap: wrap; gap: 8px; margin: 6px 0 0; } nav a { color: var(--ink); text-decoration: none; border: 1px solid rgba(233,215,1,.45); border-radius: 999px; padding: 3px 14px; }
nav a:hover { color: var(--gold); border-color: var(--gold); }
"""


def build(only=None):
    cards = all_cards()
    defs = scene.DEFS.replace("</defs>", C.EXTRA_DEFS + K.CARD_DEFS + L.DEFS + "</defs>")
    sections, figs, cur = [], "", None
    titles = {"major": "The Major Arcana", "galleons": "Galleons", "lutes": "Lutes", "quills": "Quills", "mirrors": "Mirrors"}
    fails = 0
    for i, c in enumerate(cards):
        if only and c["id"] not in only:
            continue
        if c["suit"] != cur:
            if cur:
                sections.append((cur, figs))
            cur, figs = c["suit"], ""
        try:
            art = c["fn"]()
        except Exception:
            fails += 1
            print("FAILED", c["id"], c["name"])
            traceback.print_exc()
            art = '<rect width="620" height="870" fill="#400"/>'
        figs += f'<figure id="{c["id"]}">{frame(i, c["numeral"], c["name"], c["suit"], art)}<figcaption><b>{e(c["name"])}</b>{e(c["scene"])}</figcaption></figure>'
    sections.append((cur, figs))
    body = "".join(f'<h2 id="{s}">{titles[s]}</h2><div class="deck">{f}</div>' for s, f in sections)
    body += f'<h2 id="back">The card back</h2><div class="deck"><figure>{K.card_back()}<figcaption><b>The card back</b>Purple and gold, with the Guild star inside a ring of moon phases.</figcaption></figure></div>'
    nav = "".join(f'<a href="#{s}">{titles[s]}</a>' for s, _ in sections) + '<a href="#back">Card back</a>'
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Guild Tarot Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Alegreya:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header><img src="data:image/png;base64,{K.LOGO}" alt="Chaotic Good Guild"><div><h1>The Guild Tarot: All 78 Cards</h1><p>Version 1. Every character comes from the model sheets.</p><nav>{nav}</nav></div></header>
<main>{body}</main>
</body></html>"""
    out = os.path.join(ROOT, "sheets", "deck.html" if not only else "deck_test.html")
    open(out, "w").write(page)
    if not only:
        meta = [{k: v for k, v in c.items() if k != "fn"} for c in cards]
        json.dump(meta, open(os.path.join(ROOT, "src", "tarot.json"), "w"), indent=1)
    print("Wrote", out, f"({len(page)/1e6:.1f} MB), {len(cards)} cards, {fails} failed")


if __name__ == "__main__":
    build(set(sys.argv[1:]) or None)


def export(outdir):
    """Write each card as an SVG fragment (outdir/<id>.svg) for the reading page. The page supplies the shared defs.
    Returns (card metadata list, shared defs string)."""
    import random
    random.seed(78)   # stable output, so rebuilding doesn't change every file
    os.makedirs(outdir, exist_ok=True)
    meta = []
    for i, c in enumerate(all_cards()):
        svg = frame(i, c["numeral"], c["name"], c["suit"], c["fn"]())
        svg = svg.replace('<svg class="card"', '<svg xmlns="http://www.w3.org/2000/svg" class="card"', 1)
        open(os.path.join(outdir, c["id"] + ".svg"), "w").write(svg)
        meta.append({k: c[k] for k in ("id", "name", "suit", "rank", "numeral", "scene")})
    defs = scene.DEFS.replace("</defs>", C.EXTRA_DEFS + K.CARD_DEFS + L.DEFS + "</defs>")
    return meta, defs
