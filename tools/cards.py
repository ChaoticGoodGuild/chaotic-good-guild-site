"""Guild tarot cards: one shared frame, and art built only from the cast in characters.py.

Run:  python3 tools/cards.py   -> sheets/cards.html (sample cards and the card back)
Card size 700 x 1200 (tarot proportions). The art window is 620 x 870 at (40, 112).
"""
import html, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene  # noqa: E402
import characters as C  # noqa: E402
from characters import O, O1, INK  # noqa: E402

ROOT = os.path.dirname(HERE)
STAR = open(os.path.join(ROOT, "src", "star.b64")).read()
LOGO = open(os.path.join(ROOT, "src", "logo.b64")).read()
e = html.escape

CARD_DEFS = """
<linearGradient id="kNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07021a"/><stop offset=".55" stop-color="#25094a"/><stop offset="1" stop-color="#4a1680"/></linearGradient>
<linearGradient id="kRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e0408"/><stop offset=".5" stop-color="#6e0f1e"/><stop offset="1" stop-color="#c8402a"/></linearGradient>
<linearGradient id="kDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14062e"/><stop offset=".55" stop-color="#4a1680"/><stop offset=".85" stop-color="#b8487a"/><stop offset="1" stop-color="#f2a65a"/></linearGradient>
<linearGradient id="kWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e0e2e"/><stop offset="1" stop-color="#3a1e3e"/></linearGradient>
<linearGradient id="kGroundPurple" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22103f"/><stop offset="1" stop-color="#0c0418"/></linearGradient>
<linearGradient id="kStreet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1418"/><stop offset="1" stop-color="#14060a"/></linearGradient>
<linearGradient id="kGrass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e2a52"/><stop offset="1" stop-color="#120a26"/></linearGradient>
<radialGradient id="kBrew" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#fff3a0"/><stop offset=".5" stop-color="#b06cff"/><stop offset="1" stop-color="#4b0f86"/></radialGradient>
<radialGradient id="kCandle"><stop offset="0" stop-color="#ffd75a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd75a" stop-opacity="0"/></radialGradient>
<radialGradient id="kBack" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#5a14a8"/><stop offset=".6" stop-color="#3d0872"/><stop offset="1" stop-color="#1c0638"/></radialGradient>
<pattern id="kLattice" patternUnits="userSpaceOnUse" width="40" height="40"><path d="M20,0 L40,20 L20,40 L0,20Z" fill="none" stroke="#e9d701" stroke-opacity=".16" stroke-width="1"/><circle cx="20" cy="20" r="1.6" fill="#e9d701" fill-opacity=".35"/></pattern>
"""


def place(svg, x, y, s=1.0, flip=False, rot=0):
    fx = -s if flip else s
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({fx},{s})">{svg}</g>'


def stars(n, seed, ymax, w=620):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y, rad = r.random() * w, r.random() * ymax, r.random() * 1.6 + .5
        col = "#e9d701" if r.random() < .2 else "#f3ecff"
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="{col}" opacity="{r.random()*.6+.35:.2f}"/>')
    return "".join(out)


def guild_star(cx, cy, size):
    return (f'<circle cx="{cx}" cy="{cy}" r="{size*0.75:.0f}" fill="url(#halo)"/>'
            f'<image href="data:image/png;base64,{STAR}" x="{cx-size/2:.0f}" y="{cy-size*0.48:.0f}" width="{size}" height="{size*0.96:.0f}"/>')


def note(x, y, size, ch="&#9834;"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="#e9d701" stroke="{INK}" stroke-width="1.2" font-family="Georgia, serif">{ch}</text>'


def stump(w=60):
    return f'''<path d="M-{w},0 L-{w+8},70 Q-{w+24},72 -{w+32},80 L-{w-6},78 L{w-6},78 L{w+32},80 Q{w+24},72 {w+8},70 L{w},0Z" fill="url(#gWoodV)" {O}/>
<g stroke="#2a1608" stroke-width="1.6" fill="none"><path d="M-{w*0.7:.0f},12 q-4,30 -8,56 M-{w*0.25:.0f},14 q2,30 -2,58 M{w*0.3:.0f},14 q4,28 2,58 M{w*0.7:.0f},12 q6,30 8,56"/></g>
<ellipse cx="0" cy="0" rx="{w}" ry="14" fill="#b08a5a" {O}/><ellipse cx="0" cy="0" rx="{w*0.68:.0f}" ry="9" fill="none" stroke="#7a5630" stroke-width="1.6"/><ellipse cx="0" cy="0" rx="{w*0.34:.0f}" ry="4.5" fill="none" stroke="#7a5630" stroke-width="1.6"/>'''


def broken_quill(x, y, rot, s=0.9):
    q = C.quill(s)
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<g clip-path="url(#qTop)"><g transform="translate(6,-8) rotate(16)">{q}</g></g>'
            f'<g clip-path="url(#qBot)">{q}</g>'
            f'<path d="M{18*s:.0f},{-30*s:.0f} l4,-3 l-2,5 l5,-2" stroke="{INK}" stroke-width="1.2" fill="none"/></g>')


def paper_ball(x, y, r):
    rng = random.Random(x * 7 + y)
    pts = []
    for i in range(9):
        a = i * 2 * math.pi / 9
        rr = r * (0.8 + rng.random() * 0.35)
        pts.append(f"{x+math.cos(a)*rr:.1f},{y+math.sin(a)*rr:.1f}")
    lines = " ".join(f'M{x+rng.uniform(-r*.6,r*.6):.0f},{y+rng.uniform(-r*.6,r*.6):.0f} l{rng.uniform(-r*.5,r*.5):.0f},{rng.uniform(-r*.5,r*.5):.0f}' for _ in range(3))
    return f'<polygon points="{" ".join(pts)}" fill="#f6f0e2" {O1}/><path d="{lines}" stroke="#b8ab8e" stroke-width="1.2" fill="none"/>'


# ------------------------------------------------------------------ card art (620 x 870)
def art_temperance():
    """XIV Temperance: Mira pours into a swirling purple-and-gold cauldron; her frog is thrilled; the Guild star shines."""
    K = 2.4
    mx, my, ms = 160, 830, C.CANON_SCALE["mira"] * K
    sx, sy = mx + 76 * ms, my - 178 * ms
    pines_l = "".join(scene.pine(x, y, h, '#170a2e', '#2b1650') for x, y, h in ((10, 690, 360), (70, 700, 290)))
    pines_r = "".join(scene.pine(x, y, h, '#170a2e', '#2b1650') for x, y, h in ((560, 690, 330), (615, 700, 380)))
    shrooms = "".join(f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="-4" rx="18" ry="18" fill="{c}" opacity=".2"/><rect x="-3" y="-8" width="6" height="12" rx="2" fill="#e2d5b6"/><path d="M-13,-7 q13,-20 26,0Z" fill="{c}" {O1}/></g>'
                      for x, y, s, c in ((40, 800, 1.6, "#e9d701"), (585, 790, 1.4, "#b06cff"), (470, 850, 1.1, "#ff7eb6"), (250, 860, 1.0, "#b06cff")))
    return f'''
<rect width="620" height="870" fill="url(#kNight)"/>{stars(110, 14, 560)}
<g stroke="#e9d701" stroke-opacity=".3" stroke-width="1.4" fill="none"><path d="M70,120 L120,160 L170,140 L220,190 M500,300 L560,330 L590,280"/></g>
{guild_star(400, 170, 190)}
<path d="M0,620 Q160,560 330,600 Q480,630 620,580 L620,870 L0,870Z" fill="#1a0b32"/>
{pines_l}{pines_r}
<path d="M0,700 Q300,660 620,700 L620,870 L0,870Z" fill="url(#kGroundPurple)"/>
{shrooms}
<g opacity=".85"><path d="M330,600 C290,520 380,470 330,400 C300,350 360,300 340,240" stroke="#b06cff" stroke-width="22" fill="none" stroke-linecap="round" opacity=".55"/>
<path d="M410,600 C450,520 360,470 410,390 C440,340 390,300 420,250" stroke="#e9d701" stroke-width="18" fill="none" stroke-linecap="round" opacity=".55"/>
<path d="M370,610 C340,540 420,500 380,430" stroke="#fff3a0" stroke-width="6" fill="none" stroke-linecap="round" opacity=".6"/></g>
<g fill="#e9d701">{''.join(f'<use href="#sparkle" transform="translate({x} {y}) scale({s})"/>' for x, y, s in ((300, 480, .8), (450, 420, 1), (360, 330, .7), (420, 520, .6), (330, 380, .5)))}</g>
<g transform="translate(380,740)">
<g {O1}><rect x="-90" y="60" width="180" height="14" rx="6" fill="#5a3a22" transform="rotate(6)"/><rect x="-90" y="60" width="180" height="14" rx="6" fill="#6b4426" transform="rotate(-8)"/></g>
<path d="M-50,80 q-8,-26 10,-40 q2,16 14,20 q-4,-24 12,-36 q6,22 16,28 q8,-10 4,-20 q18,16 12,48Z" fill="#ff8a3c" {O1}/>
<path d="M-120,-30 Q-136,60 -60,72 L60,72 Q136,60 120,-30Z" fill="#15101c" {O}/>
<path d="M-104,-10 q-8,46 22,64" stroke="#3a3048" stroke-width="4" fill="none"/>
<ellipse cx="0" cy="-34" rx="128" ry="26" fill="#2a2434" {O}/>
<ellipse cx="0" cy="-34" rx="112" ry="19" fill="url(#kBrew)"/>
<path d="M-90,-34 C-60,-58 -10,-10 20,-34 C50,-56 80,-20 100,-36" stroke="#e9d701" stroke-width="5" fill="none"/>
<path d="M-70,-28 C-40,-12 0,-50 40,-26 C60,-16 80,-30 90,-28" stroke="#4b0f86" stroke-width="4" fill="none"/>
<circle cx="-134" cy="-4" r="11" fill="none" stroke="#3a3048" stroke-width="5"/><circle cx="134" cy="-4" r="11" fill="none" stroke="#3a3048" stroke-width="5"/>
<use href="#sparkle" fill="#e9d701" opacity=".55" transform="translate(0 20) scale(2.2)"/>
</g>
<path d="M{sx-10:.0f},{sy+8:.0f} Q{sx+60:.0f},{sy+40:.0f} 340,700" stroke="#ffd75a" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M{sx-10:.0f},{sy+8:.0f} Q{sx+60:.0f},{sy+40:.0f} 340,700" stroke="#b06cff" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="8 10"/>
{place(C.mira("happy", "pour"), mx, my, ms)}
{place(C.frog("laugh"), 548, 856, C.CANON_SCALE["frog"] * 1.9 * 1.6)}
'''


def art_five_of_galleons():
    """V of Galleons: the Badger, downcast, beside her collapsed shanty. On the castle balcony the LEO Lion and the
    Corporate Wolf laugh over exactly five galleons. Red Lawful Evil sky."""
    K = 1.55
    rng = random.Random(5)
    rain = "".join(f'<path d="M{rng.random()*620:.0f},{rng.random()*860:.0f} l-6,22" stroke="#e8c9c9" stroke-opacity=".25" stroke-width="1.6"/>' for _ in range(90))
    coins = "".join(f'<g transform="translate({x},{y}) scale(1,{sy})">{C.galleon(12)}</g>' for x, y, sy in ((404, 352, .45), (430, 352, .45), (417, 346, .45), (410, 340, .45), (424, 334, .45)))
    castle = f'''<g fill="#2b0812">
<rect x="160" y="300" width="400" height="320"/>{''.join(f'<rect x="{x}" y="288" width="22" height="14"/>' for x in range(160, 560, 40))}
<rect x="120" y="180" width="80" height="440"/><polygon points="110,180 160,90 210,180"/>
<rect x="520" y="160" width="84" height="460"/><polygon points="510,160 562,70 614,160"/>
<rect x="300" y="120" width="120" height="200"/><polygon points="290,120 360,30 430,120"/>
</g>
<g fill="#ff6a3c" opacity=".9"><path d="M146,230 q8,-12 16,0 v26 h-16Z M548,220 q8,-12 16,0 v26 h-16Z M340,170 q10,-14 20,0 v30 h-20Z M146,320 q8,-12 16,0 v26 h-16Z M548,320 q8,-12 16,0 v26 h-16Z"/></g>
<g stroke="#2b0812" stroke-width="3"><path d="M160,90 v-26 M562,70 v-26 M360,30 v-24"/></g>
<g fill="#a3162c"><path d="M160,64 l24,7 l-24,8Z M562,44 l24,7 l-24,8Z M360,6 l26,8 l-26,8Z"/></g>'''
    shanty = f'''<g transform="translate(340,640)">
<path d="M-10,180 L60,40 L72,46 L6,186Z" fill="#6b4426" {O}/>
<path d="M40,184 L210,150 L214,166 L46,198Z" fill="#5a3a22" {O}/>
<path d="M120,180 L150,30 L166,34 L138,182Z" fill="#7a5630" {O}/>
<path d="M30,120 L230,70 L240,96 L44,150Z" fill="#8a6038" {O} transform="rotate(14 130 110)"/>
<path d="M60,140 L180,120 M80,118 L200,96" stroke="#3a2212" stroke-width="2" transform="rotate(14 130 110)"/>
<path d="M190,186 L250,110 L262,118 L206,190Z" fill="#5a3a22" {O}/>
<path d="M0,190 h260" stroke="#160a22" stroke-width="3"/>
<g fill="#4a2c16" {O1}><rect x="70" y="170" width="40" height="10" transform="rotate(-8 90 175)"/><rect x="150" y="176" width="34" height="8" transform="rotate(10 167 180)"/></g>
</g>'''
    return f'''
<rect width="620" height="870" fill="url(#kRed)"/>
<circle cx="360" cy="300" r="220" fill="#ff5a3c" opacity=".12"/>
{castle}
<rect x="250" y="240" width="250" height="110" fill="#14040a"/>
{place(C.lion("laugh"), 330, 400, C.CANON_SCALE["lion"] * 0.62)}
{place(C.wolf("laugh"), 456, 400, C.CANON_SCALE["wolf"] * 0.6)}
<path d="M240,350 h270 v12 h-270Z" fill="#4a1020" {O}/>{''.join(f'<rect x="{x}" y="362" width="8" height="34" fill="#3a0c18" {O1}/>' for x in range(250, 506, 22))}<path d="M240,396 h270 v10 h-270Z" fill="#4a1020" {O}/>
{coins}
<g transform="translate(262,406)">{C.leo_banner(38, 80)}</g><g transform="translate(450,406)">{C.leo_banner(38, 80)}</g>
<path d="M0,640 Q310,610 620,640 L620,870 L0,870Z" fill="url(#kStreet)"/>
<g stroke="#160a22" stroke-opacity=".5" stroke-width="2" fill="none">{''.join(f'<path d="M{x},{700+(x%3)*40} q20,-6 40,0"/>' for x in range(20, 600, 70))}</g>
{shanty}
{place(C.badger("sad", None, galleon_on_belt=False), 170, 840, C.CANON_SCALE["badger"] * K)}
{rain}
'''


def art_four_of_lutes():
    """IV of Lutes: Reynard plays atop a stump; four notes float up; rats in different outfits dance."""
    K = 1.5
    dancers = [
        (78, 852, "hero", "laugh", -10, False, 0),
        (190, 820, "merchant", "grin", 8, False, -24),
        (445, 846, "scribe", "laugh", -8, True, 0),
        (552, 818, "ragged", "happy", 10, True, -20),
    ]
    rats = ""
    for x, y, outfit, ex, rot, flip, hop in dancers:
        rats += f'<ellipse cx="{x}" cy="{y+2}" rx="34" ry="6" fill="#000" opacity=".25"/>' if hop else ""
        rats += place(C.rat(ex, outfit), x, y + hop, C.CANON_SCALE["rat"] * K, flip, rot)
        if hop:
            rats += f'<path d="M{x-20},{y-4} q-8,6 -16,4 M{x+20},{y-4} q8,6 16,4" stroke="#f3ecff" stroke-opacity=".6" stroke-width="2" fill="none"/>'
    return f'''
<rect width="620" height="870" fill="url(#kDusk)"/>{stars(50, 4, 300)}
{scene.minihouse(70, 610, 1.0, '#7a1fb8')}{scene.minihouse(560, 600, 0.9, '#a3162c', '#ffe08a')}{scene.minihouse(470, 640, 0.6, '#6000AE')}
<path d="M0,640 Q310,600 620,640 L620,870 L0,870Z" fill="url(#kGrass)"/>
{scene.lstring(0, 250, 620, 230, 70, 10)}
{scene.tufts(30, 0, 620, lambda x: 700 + (x * 7) % 150, '#4a3a78', 10)}
<g transform="translate(310,705)">{stump(64)}</g>
{place(C.reynard("grin"), 300, 705, C.CANON_SCALE["reynard"] * K)}
{note(400, 330, 60)}{note(470, 260, 52, "&#9835;")}{note(150, 300, 54)}{note(90, 220, 46, "&#9835;")}
{rats}
'''


def art_eight_of_quills():
    """VIII of Quills: a spectacled scribe rat slumps at his desk, one quill in hand and seven broken on the floor,
    paper balled everywhere. Through the window, the Lawful Evil city under a red sky."""
    K = 2.0
    rs = C.CANON_SCALE["rat"] * K
    floor_q = [(70, 790, -30), (160, 840, 20), (250, 800, -70), (470, 830, 60), (540, 790, -20), (400, 860, -100), (590, 850, 40)]
    balls = "".join(paper_ball(x, y, r) for x, y, r in ((40, 700, 14), (62, 690, 13), (52, 676, 12), (150, 790, 12), (320, 850, 13), (500, 770, 11), (210, 860, 10), (600, 760, 12)))
    return f'''
<defs><clipPath id="qTop"><rect x="-10" y="-90" width="70" height="58"/></clipPath><clipPath id="qBot"><rect x="-10" y="-32" width="70" height="50"/></clipPath></defs>
<rect width="620" height="870" fill="url(#kWall)"/>
<g stroke="#120818" stroke-width="2" opacity=".6">{''.join(f'<path d="M{x},0 v720"/>' for x in range(40, 620, 62))}</g>
<g transform="translate(350,70)">
<rect width="230" height="290" rx="10" fill="url(#kRed)"/>
<g fill="#2b0812"><rect x="20" y="170" width="190" height="120"/><rect x="40" y="120" width="40" height="170"/><polygon points="34,120 60,70 86,120"/><rect x="140" y="110" width="44" height="180"/><polygon points="134,110 162,56 190,110"/>{''.join(f'<rect x="{x}" y="160" width="12" height="10"/>' for x in range(20, 210, 22))}</g>
<g fill="#ff6a3c"><rect x="56" y="140" width="8" height="12"/><rect x="156" y="130" width="8" height="12"/><rect x="100" y="200" width="10" height="14"/></g>
<g transform="translate(96,214)">{C.leo_banner(18, 36)}</g>
<path d="M115,0 v290 M0,145 h230" stroke="#4a2c18" stroke-width="10"/>
<rect width="230" height="290" rx="10" fill="none" stroke="#4a2c18" stroke-width="14"/><rect x="-4" y="286" width="238" height="14" rx="4" fill="#5a3a22" {O1}/>
</g>
<path d="M0,720 h620 v150 h-620Z" fill="#3a2416"/><g stroke="#2a1608" stroke-width="2">{''.join(f'<path d="M0,{y} h620"/>' for y in (760, 800, 840))}</g>
<circle cx="470" cy="548" r="150" fill="url(#kCandle)"/>
{place(C.rat("sad", "scribe"), 296, 704, rs)}
<path d="M90,600 h440 v22 h-440Z" fill="url(#gWood)" {O}/>
<path d="M110,622 h400 v120 h-400Z" fill="url(#gWoodV)" {O}/><rect x="250" y="650" width="120" height="40" rx="4" fill="#5a3a22" {O1}/><circle cx="310" cy="670" r="5" fill="url(#gGold)" {O1}/>
<path d="M300,590 l90,-14 l14,24 l-92,12Z" fill="#f6f0e2" {O1}/><g stroke="#8a7a6a" stroke-width="1.2"><path d="M312,596 l56,-8 M314,602 l40,-6"/></g><path d="M330,600 q14,-10 30,4" stroke="#3a2a6a" stroke-width="2" fill="none"/>
<path d="M352,566 Q372,580 382,594" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/><path d="M352,566 Q372,580 382,594" stroke="url(#gRat)" stroke-width="9.5" fill="none" stroke-linecap="round"/>
<g transform="translate(386,598) rotate(-20)">{C.quill(0.8)}</g><circle cx="386" cy="596" r="6.5" fill="#e8a3b8" {O1}/>
<g transform="translate(160,600)"><path d="M-14,0 v-18 h28 v18Z" fill="#1a1030" {O1}/><ellipse cx="0" cy="-18" rx="14" ry="4" fill="#2a2040" {O1}/></g>
<g transform="translate(470,600)"><rect x="-8" y="-46" width="16" height="46" fill="#f3e6c4" {O1}/><path d="M0,-46 q8,-14 0,-24 q-8,10 0,24Z" fill="#ffd75a" {O1}/><path d="M-16,0 h32 v6 h-32Z" fill="url(#gGold)" {O1}/></g>
<g transform="translate(60,760)"><path d="M-36,0 L-30,-80 L30,-80 L36,0Z" fill="#6a6a78" {O}/><path d="M-30,-60 h60 M-32,-36 h64 M-34,-14 h68" stroke="#4a4a58" stroke-width="2"/></g>
{balls}
{''.join(broken_quill(x, y, r) for x, y, r in floor_q)}
'''


ARTS = [
    ("XIV", "Temperance", "major", art_temperance,
     "Mira pours concoctions into a swirling purple-and-gold cauldron while her frog cheers; the Guild star shines above."),
    ("V", "Five of Galleons", "galleons", art_five_of_galleons,
     "The Badger stands downcast by her collapsed shanty while the LEO Lion and the Corporate Wolf laugh over their galleons."),
    ("IV", "Four of Lutes", "lutes", art_four_of_lutes,
     "Reynard plays atop a stump with four notes in the air, and rats in all different outfits dance to his music."),
    ("VIII", "Eight of Quills", "quills", art_eight_of_quills,
     "A scribe rat slumps at his desk: one quill in hand, seven broken on the floor, the Lawful Evil city through the window."),
]


def suit_icon(suit, x, y):
    if suit == "galleons":
        return f'<g transform="translate({x},{y})">{C.galleon(16)}</g>'
    if suit == "lutes":
        return f'<g transform="translate({x-24},{y+6}) rotate(-30) scale(.42)">{C.lute()}</g>'
    if suit == "quills":
        return f'<g transform="translate({x-10},{y+18}) scale(.5)">{C.quill()}</g>'
    if suit == "mirrors":
        return f'<g transform="translate({x},{y-4}) scale(.62)">{C.mirror()}</g>'
    return f'<use href="#sparkle" fill="url(#gGold)" transform="translate({x} {y}) scale(1.6)"/>'


def frame(i, numeral, title, suit, art):
    fs = 64 if len(title) < 13 else 54
    return f'''<svg class="card" viewBox="0 0 700 1200" role="img" aria-label="{e(title)}">
<defs><clipPath id="cardArt{i}"><rect x="40" y="112" width="620" height="870" rx="22"/></clipPath></defs>
<rect x="4" y="4" width="692" height="1192" rx="40" fill="#1c0638" stroke="#e9d701" stroke-width="6"/>
<rect x="18" y="18" width="664" height="1164" rx="30" fill="none" stroke="#e9d701" stroke-width="1.5" opacity=".55"/>
{suit_icon(suit, 190, 62)}{suit_icon(suit, 510, 62)}
<text x="350" y="84" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="58" fill="#e9d701">{numeral}</text>
<g clip-path="url(#cardArt{i})"><g transform="translate(40,112)">{art}</g></g>
<rect x="40" y="112" width="620" height="870" rx="22" fill="none" stroke="#e9d701" stroke-width="4"/>
<path d="M56,1010 H644 L620,1080 L644,1150 H56 L80,1080Z" fill="#f3e6c4" stroke="#e9d701" stroke-width="4"/>
<path d="M70,1022 H630 L610,1080 L630,1138 H70 L90,1080Z" fill="none" stroke="#3d0872" stroke-width="1.5" opacity=".5"/>
<text x="350" y="1100" text-anchor="middle" font-family="Pirata One, Georgia, serif" font-size="{fs}" fill="#3d0872">{e(title)}</text>
{''.join(f'<use href="#sparkle" fill="#e9d701" transform="translate({x} {y}) scale(1.1)"/>' for x, y in ((40, 44), (660, 44), (40, 1156), (660, 1156)))}
</svg>'''


def card_back():
    ring = "".join(scene.phase(350 + 205 * math.sin(k * math.pi / 4), 600 - 205 * math.cos(k * math.pi / 4), 20, k / 8) for k in range(8))
    ticks = "".join(f'<line x1="{350+236*math.sin(a):.1f}" y1="{600-236*math.cos(a):.1f}" x2="{350+250*math.sin(a):.1f}" y2="{600-250*math.cos(a):.1f}"/>' for a in [k * math.pi / 12 for k in range(24)])
    corners = "".join(f'<g transform="translate({x} {y}) scale(1,{sy})"><path d="M0,0 q40,10 60,60 q-30,-14 -60,-10 q4,-30 0,-50Z" fill="none" stroke="#e9d701" stroke-width="2"/><use href="#sparkle" fill="#e9d701" transform="translate(22 22) scale(1.2)"/></g>'
                      for x, y, sy in ((54, 54, 1), (646, 54, 1), (54, 1146, -1), (646, 1146, -1)))
    corners = corners.replace('translate(646 54) scale(1,1)', 'translate(646 54) scale(-1,1)').replace('translate(646 1146) scale(1,-1)', 'translate(646 1146) scale(-1,-1)')
    return f'''<svg class="card" viewBox="0 0 700 1200" role="img" aria-label="Card back">
<rect x="4" y="4" width="692" height="1192" rx="40" fill="url(#kBack)" stroke="#e9d701" stroke-width="6"/>
<rect x="30" y="30" width="640" height="1140" rx="26" fill="url(#kLattice)" stroke="#e9d701" stroke-width="2"/>
<rect x="44" y="44" width="612" height="1112" rx="20" fill="none" stroke="#e9d701" stroke-width="1" opacity=".6"/>
{corners}
<circle cx="350" cy="600" r="262" fill="#1c0638" stroke="#e9d701" stroke-width="3"/>
<circle cx="350" cy="600" r="232" fill="none" stroke="#e9d701" stroke-width="1" opacity=".6"/>
<g stroke="#e9d701" stroke-width="2">{ticks}</g>
{ring}
{guild_star(350, 600, 250)}
<g fill="#e9d701">{''.join(f'<use href="#sparkle" transform="translate({x} {y}) scale({s})"/>' for x, y, s in ((350, 210, 2), (350, 990, 2), (66, 600, 1.4), (634, 600, 1.4)))}</g>
<path d="M300,150 Q350,120 400,150 M300,1050 Q350,1080 400,1050" stroke="#e9d701" stroke-width="2.5" fill="none"/>
</svg>'''


CSS = """
:root { --night:#0d0418; --gold:#e9d701; --ink:#f3ecff; --muted:#cbbde6; color-scheme: dark; }
html, body { margin: 0; background: radial-gradient(1200px 700px at 50% -10%, #3d1777, #0d0418 70%); background-color: #0d0418; color: var(--ink); font-family: "Alegreya", Georgia, serif; }
header { display: flex; align-items: center; gap: 18px; padding: 14px clamp(16px, 4vw, 48px); }
header img { height: 76px; } header h1 { font-family: "Pirata One", Georgia, serif; font-weight: 400; font-size: clamp(30px, 4vw, 46px); margin: 0; color: var(--gold); line-height: 1; }
header p { margin: 4px 0 0; color: var(--muted); }
main { max-width: 1280px; margin: 0 auto; padding: 10px clamp(16px, 4vw, 48px) 60px; }
.deck { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 28px; }
figure { margin: 0; }
.card { display: block; width: 100%; height: auto; filter: drop-shadow(0 18px 30px rgba(0,0,0,.6)); }
figcaption { margin-top: 10px; font-size: 16px; line-height: 1.4; color: var(--muted); }
figcaption b { display: block; color: var(--gold); font-family: "Pirata One", Georgia, serif; font-weight: 400; font-size: 24px; }
"""


def build():
    defs = scene.DEFS.replace("</defs>", C.EXTRA_DEFS + CARD_DEFS + "</defs>")
    figs = "".join(f'<figure>{frame(i, n, t, s, f())}<figcaption><b>{e(t)}</b>{e(d)}</figcaption></figure>' for i, (n, t, s, f, d) in enumerate(ARTS))
    figs += f'<figure>{card_back()}<figcaption><b>The card back</b>Purple and gold, with the Guild star inside a ring of moon phases.</figcaption></figure>'
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guild Tarot Sample Cards</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Alegreya:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{defs}</svg>
<header><img src="data:image/png;base64,{LOGO}" alt="Chaotic Good Guild"><div><h1>The Guild Tarot: Sample Cards</h1><p>Four cards drawn from Ryan's own card prompts, using only the model-sheet cast.</p></div></header>
<main><div class="deck">{figs}</div></main>
</body></html>"""
    out = os.path.join(ROOT, "sheets", "cards.html")
    open(out, "w").write(page)
    print("Wrote", out, f"({len(page)//1024} KB)")


if __name__ == "__main__":
    build()
