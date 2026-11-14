"""The Chaotic Good Guild cast, drawn once and reused everywhere (scene, cards, pages).

Every function returns an SVG <g> in the character's own coordinates:
  * feet on y = 0, the figure extends upward (negative y)
  * facing right, three-quarter view; flip with transform="scale(-1,1)"
  * expr picks a facial expression from EXPRESSIONS

Gradients and symbols come from scene.DEFS plus EXTRA_DEFS below.
"""
import math

INK = "#160a22"
O = f'stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"'
O1 = f'stroke="{INK}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"'

EXTRA_DEFS = """
<linearGradient id="gRobe" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c8203a"/><stop offset="1" stop-color="#6e0c1c"/></linearGradient>
<linearGradient id="gLion" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2c062"/><stop offset="1" stop-color="#c88a2e"/></linearGradient>
<linearGradient id="gMane" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8661c"/><stop offset="1" stop-color="#6e3410"/></linearGradient>
<linearGradient id="gWolf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a9aa8"/><stop offset="1" stop-color="#55556a"/></linearGradient>
<linearGradient id="gSuit" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2c2c38"/><stop offset="1" stop-color="#101016"/></linearGradient>
<linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f7fd8"/><stop offset="1" stop-color="#1c3f86"/></linearGradient>
<linearGradient id="gFrog" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7fd06a"/><stop offset="1" stop-color="#2f8a34"/></linearGradient>
<linearGradient id="gSleeve" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d9d3e6"/></linearGradient>
<linearGradient id="gTunic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a07c5c"/><stop offset="1" stop-color="#6a4c34"/></linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0303c"/><stop offset="1" stop-color="#9c1420"/></linearGradient>
"""

# ---------------------------------------------------------------- expressions
# name: (eyes, brows, mouth)
#   eyes:  open | wide | lidded | closed (happy arcs) | shut (sad arcs) | squint
#   brows: neutral | up (worried) | down (angry/determined) | raised | smug
#   mouth: smile | grin | laugh | frown | flat | smirk | o | wavy | teeth
EXPRESSIONS = {
    "happy":      ("open",   "neutral", "smile"),
    "grin":       ("open",   "neutral", "grin"),
    "laugh":      ("closed", "raised",  "laugh"),
    "sad":        ("open",   "up",      "frown"),
    "crying":     ("shut",   "up",      "wavy"),
    "worried":    ("wide",   "up",      "wavy"),
    "scared":     ("wide",   "raised",  "o"),
    "angry":      ("squint", "down",    "teeth"),
    "determined": ("open",   "down",    "flat"),
    "thinking":   ("lidded", "smug",    "flat"),
    "smug":       ("lidded", "smug",    "smirk"),
    "surprised":  ("wide",   "raised",  "o"),
}


def eyes(kind, L, R, rx, ry, pupil="#160a22", iris=None, slit=False, lid="#000", look=(1.2, 0.4),
         white="#fff", far=0.92, arc=INK):
    """Two eyes. L is the far (left) eye, drawn a touch smaller for the three-quarter view."""
    out = []
    for (cx, cy), s in ((L, far), (R, 1.0)):
        ex, ey = rx * s, ry * s
        if kind == "closed":
            out.append(f'<path d="M{cx-ex:.1f},{cy+ey*0.25:.1f} Q{cx:.1f},{cy-ey*1.1:.1f} {cx+ex:.1f},{cy+ey*0.25:.1f}" '
                       f'fill="none" stroke="{arc}" stroke-width="2.8" stroke-linecap="round"/>')
            continue
        if kind == "shut":
            out.append(f'<path d="M{cx-ex:.1f},{cy-ey*0.1:.1f} Q{cx:.1f},{cy+ey*0.8:.1f} {cx+ex:.1f},{cy-ey*0.1:.1f}" '
                       f'fill="none" stroke="{arc}" stroke-width="2.8" stroke-linecap="round"/>'
                       f'<path d="M{cx+ex*0.6:.1f},{cy+ey*0.7:.1f} q-2,7 1,12 q4,-3 -1,-12Z" fill="#8fd3ff" {O1}/>')
            continue
        w = 1.22 if kind == "wide" else 1.0
        h = 0.62 if kind == "squint" else 1.0
        out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{ex*w:.1f}" ry="{ey*w*h:.1f}" fill="{white}" {O1}/>')
        px, py = cx + look[0] * s, cy + look[1] * s
        if iris:
            out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{ex*0.82:.1f}" ry="{ey*0.86*h:.1f}" fill="{iris}"/>')
        if slit:
            out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{ex*(0.42 if kind=="wide" else 0.26):.1f}" ry="{ey*0.8*h:.1f}" fill="{pupil}"/>')
        else:
            pr = min(ex, ey) * (0.42 if kind == "wide" else 0.64)
            out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{pr:.1f}" ry="{pr*1.12*h:.1f}" fill="{pupil}"/>')
        out.append(f'<circle cx="{px-ex*0.25:.1f}" cy="{py-ey*0.28*h:.1f}" r="{max(1.1, ex*0.2):.1f}" fill="#fff"/>')
        if kind in ("lidded",):
            out.append(f'<path d="M{cx-ex-1.5:.1f},{cy-ey*0.05:.1f} Q{cx:.1f},{cy-ey*0.3:.1f} {cx+ex+1.5:.1f},{cy-ey*0.05:.1f} '
                       f'L{cx+ex+1.5:.1f},{cy-ey-2.5:.1f} Q{cx:.1f},{cy-ey*1.7:.1f} {cx-ex-1.5:.1f},{cy-ey-2.5:.1f}Z" fill="{lid}"/>'
                       f'<path d="M{cx-ex-1:.1f},{cy-ey*0.05:.1f} Q{cx:.1f},{cy-ey*0.3:.1f} {cx+ex+1:.1f},{cy-ey*0.05:.1f}" '
                       f'fill="none" stroke="{arc}" stroke-width="2.2" stroke-linecap="round"/>')
    return "".join(out)


def brows(kind, L, R, w, gap, color=INK, sw=3.2):
    out = []
    for i, (cx, cy) in enumerate((L, R)):
        by = cy - gap
        inner = 1 if i == 0 else -1   # direction toward the face's center
        a, b = cx - w, cx + w           # left and right ends
        ia, ib = (b, a) if inner == 1 else (a, b)
        if kind == "neutral":
            d = f"M{a:.1f},{by:.1f} Q{cx:.1f},{by-4:.1f} {b:.1f},{by:.1f}"
        elif kind == "raised":
            d = f"M{a:.1f},{by-4:.1f} Q{cx:.1f},{by-11:.1f} {b:.1f},{by-4:.1f}"
        elif kind == "up":
            d = f"M{ib:.1f},{by+1:.1f} Q{cx:.1f},{by-3:.1f} {ia:.1f},{by-7:.1f}"
        elif kind == "down":
            d = f"M{ib:.1f},{by-5:.1f} Q{cx:.1f},{by-3:.1f} {ia:.1f},{by+3:.1f}"
        elif kind == "smug":
            d = (f"M{a:.1f},{by+1:.1f} L{b:.1f},{by+1:.1f}" if i == 0
                 else f"M{a:.1f},{by-3:.1f} Q{cx:.1f},{by-10:.1f} {b:.1f},{by-5:.1f}")
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "".join(out)


def mouth(kind, cx, cy, w, inside="#5a0f1a", tongue="#f08a9a", line=INK):
    if kind == "smile":
        return f'<path d="M{cx-w:.1f},{cy:.1f} Q{cx:.1f},{cy+w*0.75:.1f} {cx+w:.1f},{cy:.1f}" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
    if kind in ("grin", "laugh", "teeth"):
        h = {"grin": 0.95, "laugh": 1.35, "teeth": 0.7}[kind]
        d = f"M{cx-w:.1f},{cy:.1f} Q{cx:.1f},{cy+w*0.25:.1f} {cx+w:.1f},{cy:.1f} Q{cx+w*0.75:.1f},{cy+w*h:.1f} {cx:.1f},{cy+w*h:.1f} Q{cx-w*0.75:.1f},{cy+w*h:.1f} {cx-w:.1f},{cy:.1f}Z"
        s = f'<path d="{d}" fill="{inside}" {O1}/>'
        s += f'<path d="M{cx-w*0.9:.1f},{cy+1:.1f} Q{cx:.1f},{cy+w*0.3:.1f} {cx+w*0.9:.1f},{cy+1:.1f} L{cx+w*0.8:.1f},{cy+w*0.2+2:.1f} Q{cx:.1f},{cy+w*0.45:.1f} {cx-w*0.8:.1f},{cy+w*0.2+2:.1f}Z" fill="#fff"/>'
        if kind == "teeth":
            s += f'<path d="M{cx-w*0.75:.1f},{cy+w*0.62:.1f} L{cx+w*0.75:.1f},{cy+w*0.62:.1f}" stroke="#fff" stroke-width="3"/>'
        else:
            s += f'<path d="M{cx-w*0.45:.1f},{cy+w*h*0.95:.1f} Q{cx:.1f},{cy+w*h*0.45:.1f} {cx+w*0.45:.1f},{cy+w*h*0.95:.1f}Z" fill="{tongue}"/>'
        return s
    if kind == "frown":
        return f'<path d="M{cx-w*0.8:.1f},{cy+w*0.45:.1f} Q{cx:.1f},{cy-w*0.2:.1f} {cx+w*0.8:.1f},{cy+w*0.45:.1f}" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
    if kind == "flat":
        return f'<path d="M{cx-w*0.7:.1f},{cy+w*0.2:.1f} Q{cx:.1f},{cy+w*0.3:.1f} {cx+w*0.7:.1f},{cy+w*0.15:.1f}" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
    if kind == "smirk":
        return f'<path d="M{cx-w*0.7:.1f},{cy+w*0.15:.1f} Q{cx+w*0.1:.1f},{cy+w*0.45:.1f} {cx+w:.1f},{cy-w*0.3:.1f}" fill="none" stroke="{line}" stroke-width="2.4" stroke-linecap="round"/>'
    if kind == "o":
        return f'<ellipse cx="{cx:.1f}" cy="{cy+w*0.4:.1f}" rx="{w*0.36:.1f}" ry="{w*0.48:.1f}" fill="{inside}" {O1}/>'
    if kind == "wavy":
        x0 = cx - w * 0.8
        st = w * 1.6 / 4
        return (f'<path d="M{x0:.1f},{cy+w*0.3:.1f} q{st/2:.1f},-4 {st:.1f},0 t{st:.1f},0 t{st:.1f},0 t{st:.1f},0" '
                f'fill="none" stroke="{line}" stroke-width="2.2" stroke-linecap="round"/>')
    return ""


def face(expr, L, R, rx, ry, gap, bw, mc, mw, **kw):
    e, b, m = EXPRESSIONS[expr]
    eye_kw = {k: v for k, v in kw.items() if k in ("pupil", "iris", "slit", "lid", "look", "white", "far", "arc")}
    s = eyes(e, L, R, rx, ry, **eye_kw)
    s += brows(b, L, R, bw, gap, color=kw.get("brow", INK), sw=kw.get("brow_w", 3.2))
    s += mouth(m, mc[0], mc[1], mw, **{k: v for k, v in kw.items() if k in ("inside", "tongue")})
    return s


# ---------------------------------------------------------------- props
def lute(scale=1.0):
    return f'''<g transform="scale({scale})">
<rect x="20" y="-5" width="60" height="10" fill="#6b4426" {O1}/><g stroke="#e9d701" stroke-width="1">{''.join(f'<path d="M{x},-5 v10"/>' for x in range(30, 78, 9))}</g>
<path d="M78,-8 l20,-6 l3,12 l-20,6Z" fill="#3a2212" {O1}/><g fill="url(#gGold)" {O1}><circle cx="84" cy="-12" r="2.4"/><circle cx="93" cy="-14" r="2.4"/><circle cx="87" cy="8" r="2.4"/><circle cx="96" cy="5" r="2.4"/></g>
<path d="M22,-8 Q10,-24 -10,-24 Q-32,-22 -32,0 Q-32,22 -10,24 Q10,24 22,8Z" fill="#c98a3c" {O}/>
<path d="M-28,-10 Q-10,-18 14,-10 M-30,4 Q-8,-2 18,4 M-26,16 Q-8,10 12,16" stroke="#9a5e22" stroke-width="1.2" fill="none"/>
<circle cx="-2" cy="0" r="8.5" fill="#2a1408" {O1}/><circle cx="-2" cy="0" r="8.5" fill="none" stroke="url(#gGold)" stroke-width="1.6"/>
<path d="M-22,-3 L80,-3 M-22,0 L80,0 M-22,3 L80,3" stroke="#f3e6c4" stroke-width=".8" opacity=".9"/>
<rect x="-25" y="-7" width="5" height="14" fill="#3a2212" {O1}/></g>'''


def pentagram(r, color="#7a6200", sw=1.6):
    pts = [(r * math.sin(i * 4 * math.pi / 5), -r * math.cos(i * 4 * math.pi / 5)) for i in range(5)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>'


def galleon(r=13, text=False):
    s = f'<circle r="{r}" fill="url(#gGold)" stroke="#7a6200" stroke-width="{max(1.2, r/9):.1f}"/>'
    s += f'<circle r="{r*0.74:.1f}" fill="none" stroke="#7a6200" stroke-width="{max(.8, r/16):.1f}"/>'
    s += pentagram(r * 0.55, sw=max(1, r / 10))
    s += "".join(f'<path d="M0,{-r*0.62:.1f} l0,-{r*0.08:.1f}" transform="rotate({a})" stroke="#7a6200" stroke-width="{max(.8, r/14):.1f}"/>' for a in range(0, 360, 30))
    if text:
        s += (f'<path id="coinArc{r}" d="M{-r*0.86:.1f},0 A{r*0.86:.1f},{r*0.86:.1f} 0 1,1 {r*0.86:.1f},0 A{r*0.86:.1f},{r*0.86:.1f} 0 1,1 {-r*0.86:.1f},0" fill="none"/>'
              f'<text font-family="Georgia, serif" font-size="{r*0.13:.1f}" font-weight="700" fill="#5a4600" letter-spacing="1">'
              f'<textPath href="#coinArc{r}" startOffset="2%">KINDNESS CALLS · CHAOS CLEARS · KINDNESS CALLS · CHAOS CLEARS ·</textPath></text>')
    return s


def quill(scale=1.0):
    return f'''<g transform="scale({scale})"><path d="M0,0 C6,-20 22,-52 44,-74 C40,-56 34,-40 28,-30 C36,-36 40,-40 46,-50 C40,-30 26,-14 6,-4Z" fill="#f6f2ff" {O1}/>
<path d="M2,-2 C14,-26 28,-50 42,-70" stroke="#b9a8d6" stroke-width="1.4" fill="none"/>
<path d="M14,-22 l-6,-4 M20,-32 l-6,-5 M26,-42 l-5,-5 M18,-26 l7,0 M25,-37 l7,-1" stroke="#c9bde0" stroke-width="1"/>
<path d="M0,0 L-5,10" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/></g>'''


def mirror(scale=1.0, glass="#bfe6ff", inner=""):
    return f'''<g transform="scale({scale})"><rect x="-3.5" y="16" width="7" height="22" rx="2" fill="url(#gGold)" {O1}/>
<ellipse rx="16" ry="20" fill="url(#gGold)" {O}/><ellipse rx="11.5" ry="15.5" fill="{glass}" {O1}/>{inner}
<path d="M-6,-7 l8,-6 M-4,1 l10,-8" stroke="#fff" stroke-width="2" opacity=".85"/><circle cy="-20" r="3.2" fill="#b06cff" {O1}/></g>'''


def down_arrows():
    return (f'<g fill="#ff3b3b" {O1}>' + "".join(
        f'<path transform="translate({x},{y})" d="M-3,-12 h6 v8 h5 l-8,10 l-8,-10 h5Z"/>' for x, y in ((0, 0), (16, -10), (32, 6))) + '</g>')


def fox_banner(w=30, h=62):
    """The Guild's banner: purple with a gold fox."""
    return f'''<path d="M0,0 h{w} v{h} l-{w/2},-{h*0.18:.1f} l-{w/2},{h*0.18:.1f}Z" fill="#6000AE" {O}/>
<path d="M3,3 h{w-6} v{h*0.75:.0f} l-{(w-6)/2},-{h*0.13:.1f} l-{(w-6)/2},{h*0.13:.1f}Z" fill="none" stroke="#e9d701" stroke-width="1.2"/>
<g transform="translate({w/2} {h*0.4:.1f}) scale({w/30:.2f})"><path d="M-9,-9 L-4,0 L0,-3 L4,0 L9,-9 L7,6 L0,12 L-7,6Z" fill="#e9d701"/><circle cx="-3" cy="3" r="1.2" fill="#3d0872"/><circle cx="3" cy="3" r="1.2" fill="#3d0872"/></g>'''


def leo_banner(w=30, h=62):
    """The LEO banner: crimson with a black crown and a black outline."""
    return f'''<path d="M0,0 h{w} v{h} l-{w/2},-{h*0.18:.1f} l-{w/2},{h*0.18:.1f}Z" fill="#a3162c" {O}/>
<path d="M3,3 h{w-6} v{h*0.75:.0f} l-{(w-6)/2},-{h*0.13:.1f} l-{(w-6)/2},{h*0.13:.1f}Z" fill="none" stroke="#0a0406" stroke-width="2"/>
<g transform="translate({w/2} {h*0.4:.1f}) scale({w/30:.2f})"><path d="M-10,4 L-11,-8 L-5,-2 L0,-11 L5,-2 L11,-8 L10,4Z" fill="#0a0406"/></g>'''


def frog(expr="happy"):
    f = face(expr, (-6.5, -21), (7, -21.5), 4.2, 4.4, 7, 3.5, (0.5, -10.5), 6, look=(0.6, 0.4), brow_w=2, lid="url(#gFrog)")
    return f'''<g>
<ellipse cx="0" cy="0" rx="17" ry="3.5" fill="#000" opacity=".2"/>
<path d="M-15,0 Q-20,-6 -14,-12 Q-6,-20 0,-18 Q6,-20 14,-12 Q20,-6 15,0Z" fill="url(#gFrog)" {O}/>
<circle cx="-7" cy="-21" r="7" fill="url(#gFrog)" {O}/><circle cx="7" cy="-21.5" r="7.5" fill="url(#gFrog)" {O}/>
<path d="M-10,-2 q10,4 20,0" stroke="#9fe08a" stroke-width="3" fill="none"/>
<path d="M-15,0 q-4,-1 -6,1 M15,0 q4,-1 6,1" stroke="#2f8a34" stroke-width="3" stroke-linecap="round"/>
<circle cx="-11" cy="-9" r="1.4" fill="#2f6b2a"/><circle cx="10" cy="-8" r="1.2" fill="#2f6b2a"/>
{f}</g>'''


# ---------------------------------------------------------------- Reynard
def reynard(expr="grin", pose="lute"):
    """Reynard the fox. Red cowl, brown sleeveless tunic, white sleeves, dark trousers and boots."""
    if pose == "lute":
        arms = f'''<path d="M-22,-64 Q4,-46 30,-28" stroke="#3a2414" stroke-width="4" fill="none"/>
<g transform="translate(6,-36) rotate(-30)">{lute()}</g>
<path d="M-28,-64 Q-34,-42 -6,-34" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M-28,-64 Q-34,-42 -6,-34" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M-26,-56 q2,10 10,16" stroke="#c9c2d6" stroke-width="2" fill="none"/>
<path d="M-4,-40 q10,0 10,8 q-2,7 -10,5Z" fill="#e8742e" {O1}/>
<path d="M26,-66 Q44,-76 60,-68" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M26,-66 Q44,-76 60,-68" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M56,-76 q12,2 10,11 q-4,6 -12,2Z" fill="#e8742e" {O1}/>'''
    else:
        arms = f'''<path d="M-28,-64 Q-40,-40 -34,-16" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M-28,-64 Q-40,-40 -34,-16" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M-40,-18 q6,-6 12,0 q2,10 -6,12 q-8,-2 -6,-12Z" fill="#e8742e" {O1}/>
<path d="M27,-66 Q42,-42 36,-18" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M27,-66 Q42,-42 36,-18" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M30,-20 q6,-6 12,0 q2,10 -6,12 q-8,-2 -6,-12Z" fill="#e8742e" {O1}/>'''
    f = face(expr, (-9, -114), (17, -114), 7, 8, 11, 9, (4, -91), 15, lid="url(#gFox)", look=(1.5, 0.6))
    body = f'''
<g transform="translate(4,-30) rotate(8 -30 0)"><path d="M-26,-12 C-70,-34 -122,-10 -116,38 C-112,72 -72,78 -44,58 C-68,42 -64,16 -28,8Z" fill="url(#gFox)" {O}/>
<path d="M-117,30 l12,6 l-2,-12 l12,10 l0,-12 l12,14 l4,-10 l8,16 l8,-4 l4,16 l8,2 l7,14 C-72,78 -112,72 -117,30Z" fill="#fffaf4" {O}/>
<g stroke="#9a3a12" stroke-width="1.6" fill="none" opacity=".7"><path d="M-60,-14 q-20,2 -32,14 M-70,-2 q-16,6 -22,20 M-52,4 q-12,8 -12,22"/></g></g>
<path d="M-26,-6 L-30,38 L-10,38 L-8,-6Z M8,-6 L10,38 L30,38 L26,-6Z" fill="#4a3a30" {O}/>
<path d="M-34,30 L-8,30 L-6,54 L-40,54 Q-42,46 -34,44Z M8,30 L33,30 L34,44 Q44,46 42,54 L6,54Z" fill="#2e1c10" {O}/>
<path d="M-36,28 h30 v9 h-30Z M6,28 h30 v9 h-30Z" fill="url(#gLeather)" {O}/>
<path d="M-35,4 Q-42,-50 -24,-74 L24,-74 Q42,-50 35,4 Q0,12 -35,4Z" fill="url(#gTunic)" {O}/>
<path d="M24,-74 Q42,-50 35,4 Q30,6 24,7 Q30,-40 16,-72Z" fill="#000" opacity=".2"/>
<g stroke="#4a3424" stroke-width="1.4" fill="none" opacity=".8"><path d="M-22,-10 q-2,10 -4,16 M6,-12 q2,10 0,18 M24,-14 q4,10 4,18"/></g>
<path d="M-36,-26 h72 v8 h-72Z" fill="#3a2414" {O}/><rect x="-6" y="-27" width="12" height="10" rx="1.5" fill="none" stroke="url(#gGold)" stroke-width="2"/>
<path d="M-34,-18 h14 v16 q-7,5 -14,0Z" fill="url(#gLeather)" {O1}/><circle cx="-27" cy="-10" r="1.6" fill="url(#gGold)"/>
<path d="M-36,-70 Q-30,-92 0,-94 Q30,-92 36,-70 Q42,-56 30,-50 Q18,-46 8,-52 Q0,-46 -8,-52 Q-18,-46 -30,-50 Q-42,-56 -36,-70Z" fill="url(#gRed)" {O}/>
<g stroke="#7a0f18" stroke-width="1.8" fill="none" stroke-linecap="round"><path d="M-26,-74 q4,12 -2,22 M-12,-80 q6,14 2,28 M10,-80 q-4,14 0,28 M24,-74 q-4,12 2,22"/></g>
<path d="M-30,-82 Q0,-74 30,-82" stroke="#ff6a6a" stroke-width="2" fill="none" opacity=".5"/>
{arms}
<g transform="translate(2,4)">
<path d="M-24,-116 L-34,-168 L-2,-134Z" fill="url(#gFox)" {O}/><path d="M8,-134 L32,-168 L34,-114Z" fill="url(#gFox)" {O}/>
<path d="M-22,-122 L-30,-158 L-8,-134Z M12,-134 L29,-158 L30,-120Z" fill="#3a1208"/>
<path d="M-22,-124 q2,-12 -2,-20 q6,8 6,16 q2,-10 0,-16 q6,8 4,22Z M28,-122 q-2,-12 2,-20 q-6,8 -6,16 q-2,-10 0,-16 q-6,8 -4,22Z" fill="#fffaf4"/>
<path d="M-32,-104 C-34,-130 -14,-142 4,-142 C24,-142 40,-130 38,-104 Q36,-86 4,-82 Q-30,-86 -32,-104Z" fill="url(#gFox)" {O}/>
<path d="M-24,-110 L-50,-107 L-38,-101 L-54,-96 L-37,-93 L-42,-86 L-24,-88 Q-10,-77 4,-77 Q18,-77 30,-88 L48,-86 L43,-93 L60,-96 L44,-101 L56,-107 L30,-110 Q24,-98 4,-98 Q-16,-98 -24,-110Z" fill="#fffaf4" {O}/>
<path d="M-12,-108 Q4,-118 20,-108 Q14,-98 4,-98 Q-6,-98 -12,-108Z" fill="#fffaf4"/>
<path d="M-14,-136 Q-8,-156 10,-152 Q2,-148 2,-140 Q10,-154 26,-146 Q14,-142 14,-134 Q6,-138 -14,-136Z" fill="#e0611f" {O1}/>
<path d="M-4,-138 q4,-8 12,-10 M8,-136 q6,-6 12,-6" stroke="#b8461a" stroke-width="1.2" fill="none"/>
<path d="M0,-102 Q4,-106 8,-102 Q4,-97 0,-102Z" fill="{INK}"/><ellipse cx="3" cy="-103" rx="1.4" ry=".8" fill="#fff" opacity=".7"/>
{f}
</g>'''
    return f'<g transform="translate(0,-54)">{body}</g>'


# ---------------------------------------------------------------- Mira
def mira(expr="happy", prop="mirror"):
    """prop: "mirror" (left paw raised with her mirror), "pour" (right paw pouring a vial; stream starts at (76,-178)), or None."""
    """Mira, the witchy cat. Gray, purple witch hat with a black band and gold buckle, purple-and-gold scarf."""
    f = face(expr, (71, 142), (105, 142), 10.5, 11.5, 12, 9, (88, 158), 9, iris="#e4ff7a", slit=True,
             lid="url(#gCat)", look=(1, 0.5), far=1.0, brow="#3a3650", brow_w=2.6)
    head = f'''<g transform="translate(-88,-330)">
<path d="M46,130 L40,84 L76,110Z" fill="url(#gCat)" {O}/><path d="M130,130 L136,84 L100,110Z" fill="url(#gCat)" {O}/>
<path d="M51,121 L48,96 L67,112Z M125,121 L128,96 L109,112Z" fill="#e8a3b8"/>
<path d="M88,98 C124,98 132,122 130,142 L140,150 L130,154 L138,164 L124,166 Q106,182 88,182 Q70,182 52,166 L38,164 L46,154 L36,150 L46,142 C44,122 52,98 88,98Z" fill="url(#gCat)" {O}/>
<g stroke="#4a4760" stroke-width="2.6" fill="none"><path d="M80,112 q-2,8 2,14 M88,110 v16 M96,112 q2,8 -2,14 M50,146 l10,2 M52,156 l9,-1 M126,146 l-10,2 M124,156 l-9,-1"/></g>
<ellipse cx="88" cy="164" rx="17" ry="11" fill="#d6d3e2"/>
<path d="M83,153 h10 l-5,6Z" fill="#e8a3b8" {O1}/>
<path d="M70,160 L40,154 M70,164 L42,168 M106,160 L136,154 M106,164 L134,168" stroke="#f3ecff" stroke-opacity=".8" stroke-width="1.2"/>
{f}
<path d="M22,108 Q88,84 154,108 Q150,120 88,116 Q26,120 22,108Z" fill="#2b0a52" {O}/>
<path d="M56,104 Q68,66 78,44 Q88,14 124,-2 Q130,6 138,4 Q118,22 112,50 Q112,80 122,104 Q88,96 56,104Z" fill="url(#gPurple)" {O}/>
<path d="M78,44 q14,6 30,2 M70,66 q20,8 42,2" stroke="#2b0a52" stroke-width="2" fill="none"/>
<path d="M58,96 Q88,86 120,96 L122,105 Q88,95 56,105Z" fill="#0a0410" {O1}/><rect x="80" y="88" width="16" height="13" rx="2" fill="none" stroke="url(#gGold)" stroke-width="3"/>
<path d="M138,4 v14" stroke="#e9d701" stroke-width="1"/><use href="#sparkle" fill="url(#gGold)" transform="translate(138 24) scale(.7)"/>
<g fill="#e9d701" opacity=".8"><use href="#sparkle" transform="translate(96 60) scale(.35)"/><use href="#sparkle" transform="translate(104 30) scale(.3)"/><use href="#sparkle" transform="translate(84 76) scale(.28)"/></g>
</g>'''
    held = ""
    right_arm = f'''<path d="M26,-138 Q46,-112 40,-84" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M26,-138 Q46,-112 40,-84" stroke="url(#gCat)" stroke-width="11.5" fill="none" stroke-linecap="round"/>
<circle cx="40" cy="-82" r="7.5" fill="url(#gCat)" {O1}/>'''
    if prop == "mirror":
        held = f'<g transform="translate(-52,-132) rotate(-14)">{mirror(1.15)}</g>'
    elif prop == "pour":
        right_arm = ""
        held = f'''<path d="M24,-140 Q56,-150 72,-174" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M24,-140 Q56,-150 72,-174" stroke="url(#gCat)" stroke-width="11.5" fill="none" stroke-linecap="round"/>
<g transform="translate(76,-178) rotate(118)"><path d="M-4,0 h8 v6 q7,4 7,13 q0,11 -11,11 q-11,0 -11,-11 q0,-9 7,-13Z" fill="#ffd75a" {O1}/><path d="M-9,18 q9,-5 18,0 v3 q-9,8 -18,0Z" fill="#b06cff" opacity=".8"/><rect x="-4" y="-3" width="8" height="4" fill="#8a6038" {O1}/></g>
<circle cx="72" cy="-174" r="7.5" fill="url(#gCat)" {O1}/>'''
    body = f'''
<path d="M24,-30 C74,-28 92,-92 64,-122 C54,-132 42,-122 50,-114 C70,-92 58,-54 22,-52Z" fill="url(#gCat)" {O}/>
<g stroke="#4a4760" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M58,-50 l8,-6 M68,-74 l8,-2 M66,-100 l8,2"/></g>
<path d="M-30,-148 Q-44,-104 -38,-56 Q-34,-14 -18,-8 L18,-8 Q34,-14 38,-56 Q44,-104 30,-148Z" fill="url(#gCat)" {O}/>
<path d="M-14,-140 Q-22,-104 -14,-62 Q0,-50 14,-62 Q22,-104 14,-140Z" fill="#d6d3e2"/>
<g stroke="#4a4760" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M-36,-96 l8,2 M-38,-80 l9,1 M36,-96 l-8,2 M38,-80 l-9,1"/></g>
<path d="M-36,-70 Q0,-60 36,-70 L37,-62 Q0,-52 -37,-62Z" fill="#3a2414" {O1}/><rect x="-5" y="-69" width="10" height="9" rx="1.5" fill="none" stroke="url(#gGold)" stroke-width="2"/>
<g transform="translate(22,-58)"><path d="M-4,0 h8 v4 q6,4 6,12 q0,10 -10,10 q-10,0 -10,-10 q0,-8 6,-12Z" fill="#ffb54a" {O1}/><path d="M-6,12 q6,-4 12,0 v4 q-6,6 -12,0Z" fill="#ff8a3c" opacity=".7"/><rect x="-3.5" y="-5" width="7" height="6" fill="#8a6038" {O1}/></g>
<g transform="translate(-24,-60)"><path d="M-3,0 h6 v6 q5,3 5,9 q0,8 -8,8 q-8,0 -8,-8 q0,-6 5,-9Z" fill="#b06cff" {O1}/><rect x="-2.6" y="-4" width="5.2" height="5" fill="#8a6038" {O1}/></g>
<path d="M-30,-14 Q-34,0 -18,0 Q-6,0 -6,-10Z M6,-10 Q6,0 18,0 Q34,0 30,-14Z" fill="url(#gCat)" {O}/>
<path d="M-24,-4 v-4 M-18,-3 v-4 M18,-3 v-4 M24,-4 v-4" stroke="{INK}" stroke-width="1.2"/>
{right_arm}
{head}
<g transform="translate(-88,-330)">
<path d="M46,170 Q88,194 130,170 L134,190 Q88,214 42,190Z" fill="url(#gPurple)" {O}/>
<g stroke="#e9d701" stroke-width="3" fill="none"><path d="M45,177 Q88,201 131,177"/><path d="M43,185 Q88,209 133,185"/></g>
<path d="M108,194 L128,244 L106,240 L98,198Z" fill="url(#gPurple)" {O}/><path d="M104,214 l20,6 M106,226 l21,6" stroke="#e9d701" stroke-width="3"/>
</g>
{held}
<path d="M-26,-138 Q-46,-124 -50,-108" stroke="{INK}" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M-26,-138 Q-46,-124 -50,-108" stroke="url(#gCat)" stroke-width="11.5" fill="none" stroke-linecap="round"/>
<circle cx="-50" cy="-106" r="7.5" fill="url(#gCat)" {O1}/>'''
    return f"<g>{body}</g>"


# ---------------------------------------------------------------- Badger
def badger(expr="happy", prop="herb", galleon_on_belt=True):
    """The Badger. Leather armor with gold studs, herb pouch, a galleon on her belt, pink flower behind her ear."""
    f = face(expr, (1318, 640), (1352, 640), 6.4, 7.4, 13, 7, (1335, 680), 12, pupil="#3a2408", lid="#1b1b22",
             look=(1.4, 0.8), far=1.0, brow="#f4f1f7", brow_w=2.6, arc="#f4f1f7")
    flower = "".join(f'<ellipse cx="{1380+9*math.cos(a):.1f}" cy="{613+9*math.sin(a):.1f}" rx="7" ry="5" transform="rotate({math.degrees(a):.0f} {1380+9*math.cos(a):.1f} {613+9*math.sin(a):.1f})"/>' for a in [k * 2 * math.pi / 6 for k in range(6)])
    head = f'''<g transform="translate(-1335,-800)">
<circle cx="1302" cy="616" r="11" fill="#1b1b22" {O}/><circle cx="1368" cy="616" r="11" fill="#1b1b22" {O}/><circle cx="1302" cy="616" r="5" fill="#8e8e9c"/><circle cx="1368" cy="616" r="5" fill="#8e8e9c"/>
<path d="M1335,610 C1372,610 1378,634 1376,650 L1384,658 L1374,662 Q1362,686 1335,688 Q1308,686 1296,662 L1286,658 L1294,650 C1292,634 1298,610 1335,610Z" fill="#f4f1f7" {O}/>
<path d="M1304,618 Q1318,608 1328,618 L1331,664 Q1322,676 1314,666 Q1300,642 1304,618Z" fill="#1b1b22" {O1}/><path d="M1366,618 Q1352,608 1342,618 L1339,664 Q1348,676 1356,666 Q1370,642 1366,618Z" fill="#1b1b22" {O1}/>
<ellipse cx="1335" cy="669" rx="8.5" ry="6" fill="#1b1b22"/><ellipse cx="1333" cy="667" rx="3" ry="1.6" fill="#fff" opacity=".5"/>
{f}
<g {O1}><g fill="#ff7eb6">{flower}</g><circle cx="1380" cy="613" r="5" fill="url(#gGold)"/></g><path d="M1370,622 q-8,6 -6,14 q8,-4 6,-14Z" fill="#5fae4a" {O1}/>
</g>'''
    held = ""
    if prop == "herb":
        held = f'<g transform="translate(58,-62)"><path d="M0,0 q-4,-16 2,-30 M0,-8 q-12,-6 -14,-16 q10,0 14,12 M2,-18 q10,-6 12,-16 q-10,2 -12,12" stroke="#2f6b3a" stroke-width="2" fill="#5fae4a"/></g>'
    belt_coin = f'<path d="M30,-51 v10" stroke="#3a2414" stroke-width="2"/><g transform="translate(30,-30)">{galleon(9)}</g>' if galleon_on_belt else ""
    body = f'''
<path d="M-56,-40 Q-80,-34 -84,-12 Q-70,-18 -58,-26Z" fill="#1b1b22" {O}/>
<path d="M-44,-46 L-46,-8 L-16,-8 L-14,-46Z M14,-46 L16,-8 L46,-8 L44,-46Z" fill="#2a2a32" {O}/>
<path d="M-52,0 Q-52,-14 -30,-14 Q-10,-14 -10,0Z M10,0 Q10,-14 30,-14 Q52,-14 52,0Z" fill="#1b1b22" {O}/>
<path d="M-46,0 v-4 M-38,0 v-5 M-30,0 v-5 M30,0 v-5 M38,0 v-5 M46,0 v-4" stroke="#f4f1f7" stroke-width="1.6"/>
<path d="M-64,-40 Q-74,-110 -36,-122 L36,-122 Q74,-110 64,-40 Q0,-26 -64,-40Z" fill="url(#gBadger)" {O}/>
<path d="M-54,-92 Q0,-124 54,-92 L52,-42 Q0,-30 -52,-42Z" fill="url(#gLeather)" {O}/>
<g stroke="#e9d701" stroke-width="1" stroke-dasharray="3 3" fill="none"><path d="M-48,-86 Q0,-114 48,-86 M-48,-48 Q0,-38 48,-48"/></g>
<path d="M-34,-104 L-22,-42 M34,-104 L22,-42" stroke="#4a2c18" stroke-width="5"/>
<g fill="url(#gGold)" {O1}><circle cx="-31" cy="-88" r="3"/><circle cx="-27" cy="-66" r="3"/><circle cx="31" cy="-88" r="3"/><circle cx="27" cy="-66" r="3"/></g>
<path d="M-56,-60 h112 v9 h-112Z" fill="#3a2414" {O}/><rect x="-7" y="-61" width="14" height="11" rx="2" fill="none" stroke="url(#gGold)" stroke-width="2.2"/>
<path d="M-40,-52 h28 v24 q-14,8 -28,0Z" fill="url(#gGreen)" {O}/><path d="M-40,-52 h28 l-14,10Z" fill="#2f6b3a" {O1}/><path d="M-26,-32 Q-34,-40 -30,-48 Q-20,-44 -26,-32Z" fill="#b8e88a"/>
<g {O1}><path d="M-34,-52 q-4,-12 2,-16 q4,6 2,16 M-22,-52 q0,-14 6,-16 q2,8 -2,16" fill="#5fae4a"/></g>
{belt_coin}
<path d="M-66,-104 q-4,-22 22,-24 q10,10 0,26 q-12,6 -22,-2Z M66,-104 q4,-22 -22,-24 q-10,10 0,26 q12,6 22,-2Z" fill="url(#gLeather)" {O}/>
<path d="M-60,-100 Q-76,-72 -66,-48" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-60,-100 Q-76,-72 -66,-48" stroke="url(#gBadger)" stroke-width="16" fill="none" stroke-linecap="round"/>
<path d="M-74,-50 q8,-8 16,0 q2,12 -8,14 q-10,-2 -8,-14Z" fill="#1b1b22" {O1}/>
<path d="M60,-100 Q72,-82 62,-62" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M60,-100 Q72,-82 62,-62" stroke="url(#gBadger)" stroke-width="16" fill="none" stroke-linecap="round"/>
{held}
<path d="M54,-66 q8,-8 16,0 q2,12 -8,14 q-10,-2 -8,-14Z" fill="#1b1b22" {O1}/>
{head}'''
    return f"<g>{body}</g>"


# ---------------------------------------------------------------- Bull
def bull(expr="determined"):
    """The Bull, the builder. Leather work apron with tools, gold nose ring, hammer."""
    f = face(expr, (999, 540), (1024, 540), 6.5, 7, 11, 7, (1013, 584), 8, pupil="#2a1408", lid="url(#gBull)",
             look=(1.6, 0.8), far=1.0, brow="#2a1408", brow_w=3.4)
    return f'''<g transform="translate(-998,-702)">
<path d="M966,640 q-14,10 -8,30 q2,8 -4,10" stroke="#5a301c" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M950,676 q4,8 10,4 q-2,-6 -6,-8Z" fill="#2a1810"/>
<path d="M972,640 h20 v54 h-20Z M1004,640 h20 v54 h-20Z" fill="#4a3a30" {O}/>
<path d="M968,690 h26 v12 h-28Z M1000,690 h26 l2,12 h-28Z" fill="#1a1010" {O}/>
<path d="M952,612 Q950,566 998,562 Q1046,566 1044,612 Q1044,660 998,662 Q952,660 952,612Z" fill="url(#gBull)" {O}/>
<path d="M962,596 L1034,596 L1032,660 Q998,676 964,660Z" fill="url(#gLeather)" {O}/>
<path d="M970,596 L980,570 M1026,596 L1016,570" stroke="#5e3618" stroke-width="6"/>
<g stroke="#e9d701" stroke-width="1" stroke-dasharray="3 3" fill="none"><path d="M966,602 h64 M968,656 q30,12 60,0"/></g>
<rect x="984" y="614" width="28" height="18" rx="2" fill="#5e3618" {O1}/><path d="M990,614 v-8 M998,614 v-10 M1006,614 v-7" stroke="#b9b9c4" stroke-width="2"/>
<use href="#sparkle" fill="#e9d701" transform="translate(998 646) scale(.6)"/>
<path d="M960,588 Q944,612 952,640" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M960,588 Q944,612 952,640" stroke="url(#gBull)" stroke-width="18" fill="none" stroke-linecap="round"/>
<circle cx="952" cy="642" r="10" fill="#5a301c" {O1}/>
<path d="M1034,584 Q1054,572 1062,552" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M1034,584 Q1054,572 1062,552" stroke="url(#gBull)" stroke-width="18" fill="none" stroke-linecap="round"/>
<line x1="1064" y1="560" x2="1072" y2="508" stroke="url(#gWood)" stroke-width="7" stroke-linecap="round"/>
<path d="M1054,494 h34 v16 h-34Z" fill="#7a7a86" {O} transform="rotate(-8 1071 502)"/><path d="M1056,497 h30" stroke="#b9b9c4" stroke-width="2" transform="rotate(-8 1071 502)"/>
<circle cx="1063" cy="556" r="10" fill="#5a301c" {O1}/>
<path d="M984,532 Q956,512 962,486 Q966,478 972,486 Q974,508 998,520Z" fill="url(#gCream)" {O}/><path d="M1038,530 Q1066,510 1060,484 Q1056,476 1050,484 Q1048,506 1024,518Z" fill="url(#gCream)" {O}/>
<path d="M966,492 q4,12 16,22 M1056,490 q-4,12 -16,22" stroke="#c9b08a" stroke-width="1.5" fill="none"/>
<ellipse cx="974" cy="542" rx="12" ry="7" fill="url(#gBull)" {O} transform="rotate(-24 974 542)"/><ellipse cx="1048" cy="540" rx="12" ry="7" fill="url(#gBull)" {O} transform="rotate(24 1048 540)"/>
<path d="M980,546 Q980,516 1011,514 Q1042,516 1042,546 Q1042,566 1011,578 Q980,566 980,546Z" fill="url(#gBull)" {O}/>
<path d="M996,522 q4,-12 10,-2 q4,-12 10,0 q6,-8 8,4 q-16,6 -28,-2Z" fill="#3a1c0e" {O1}/>
<path d="M988,568 Q988,550 1012,550 Q1038,550 1038,568 Q1038,592 1012,592 Q988,592 988,568Z" fill="#e0aa86" {O}/>
<ellipse cx="1003" cy="563" rx="3.4" ry="4.4" fill="#5a3420"/><ellipse cx="1022" cy="563" rx="3.4" ry="4.4" fill="#5a3420"/>
{f}
<path d="M1005,569 a7.5,7.5 0 1,0 15,0" stroke="url(#gGold)" stroke-width="3.4" fill="none" stroke-linecap="round"/>
</g>'''


# ---------------------------------------------------------------- Rat
RAT_OUTFITS = ("plain", "hero", "lute", "wizard", "master", "scribe", "merchant", "ragged", "suit")


def rat(expr="happy", outfit="plain", prop=None):
    """A rat of the Guild. Small, round ears, pink tail and nose. Outfits tell rats apart; NEVER a fox tail."""
    f = face(expr, (12, -138), (30, -137), 5, 6, 9, 5, (40, -117), 7, lid="url(#gRat)", look=(1.4, 0.4), brow_w=2.4)
    tail = f'<path d="M-14,-30 C-46,-30 -62,-14 -52,-6 C-44,0 -58,-2 -72,-8" stroke="{INK}" stroke-width="6.5" fill="none" stroke-linecap="round"/><path d="M-14,-30 C-46,-30 -62,-14 -52,-6 C-44,0 -58,-2 -72,-8" stroke="#e8a3b8" stroke-width="4" fill="none" stroke-linecap="round"/>'
    feet = f'<ellipse cx="-8" cy="-3" rx="12" ry="5" fill="#e8a3b8" {O1}/><ellipse cx="18" cy="-3" rx="12" ry="5" fill="#e8a3b8" {O1}/>'
    legs = f'<path d="M-16,-30 L-14,-6 L-2,-6 L0,-30Z M10,-30 L12,-6 L24,-6 L26,-30Z" fill="url(#gRat)" {O1}/>'
    body = f'<path d="M-26,-44 Q-30,-98 4,-102 Q36,-98 32,-44 Q30,-14 2,-12 Q-24,-14 -26,-44Z" fill="url(#gRat)" {O}/><ellipse cx="9" cy="-52" rx="15" ry="25" fill="#d4cde0"/>'
    arm_l = f'<path d="M-18,-90 Q-30,-72 -26,-56" stroke="{INK}" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M-18,-90 Q-30,-72 -26,-56" stroke="url(#gRat)" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="-26" cy="-54" r="5" fill="#e8a3b8" {O1}/>'
    arm_r = f'<path d="M26,-90 Q40,-74 36,-58" stroke="{INK}" stroke-width="11" fill="none" stroke-linecap="round"/><path d="M26,-90 Q40,-74 36,-58" stroke="url(#gRat)" stroke-width="8" fill="none" stroke-linecap="round"/><circle cx="36" cy="-56" r="5" fill="#e8a3b8" {O1}/>'
    head = f'''<circle cx="-4" cy="-160" r="17" fill="url(#gRat)" {O}/><circle cx="-4" cy="-160" r="10" fill="#e8a3b8"/>
<path d="M-16,-130 C-18,-152 0,-162 16,-160 C32,-158 42,-148 52,-136 Q58,-130 52,-125 C42,-114 24,-108 6,-110 C-10,-112 -16,-118 -16,-130Z" fill="url(#gRat)" {O}/>
<circle cx="24" cy="-164" r="18" fill="url(#gRat)" {O}/><circle cx="24" cy="-164" r="11" fill="#e8a3b8"/>
<path d="M28,-122 Q40,-116 50,-124" fill="#d4cde0"/>
<circle cx="54" cy="-131" r="4.5" fill="#e8a3b8" {O1}/>
<path d="M46,-126 l14,-5 M46,-124 l15,0 M46,-122 l13,5" stroke="#f3ecff" stroke-width="1" opacity=".85"/>
{f}'''
    over_body = over_head = back = held = ""
    if outfit == "hero":   # Robin Hood: green tunic, belt, feathered cap
        over_body = f'''<path d="M-27,-48 Q-30,-96 4,-100 Q34,-96 31,-48 L34,-26 L22,-30 L12,-22 L2,-30 L-8,-22 L-18,-30 L-30,-26Z" fill="url(#gGreen)" {O}/>
<path d="M-28,-52 h58 v7 h-58Z" fill="#5a3a22" {O1}/><rect x="-1" y="-53" width="8" height="9" fill="none" stroke="url(#gGold)" stroke-width="1.8"/>
<path d="M-10,-99 l12,14 l12,-14" fill="none" stroke="#2a5a30" stroke-width="2.4"/>'''
        over_head = f'''<path d="M-18,-142 Q6,-176 40,-152 L50,-146 Q10,-150 -18,-136Z" fill="url(#gGreen)" {O}/><path d="M6,-162 Q-10,-186 -22,-188 Q-14,-172 0,-158Z" fill="#d23a4a" {O1}/>'''
    elif outfit == "lute":   # Reynard's apprentice: red cowl, brown tunic, white sleeves
        over_body = f'''<path d="M-27,-48 Q-30,-96 4,-100 Q34,-96 31,-48 Q4,-38 -27,-48Z" fill="url(#gTunic)" {O}/>
<path d="M-28,-102 Q4,-118 36,-102 Q40,-90 30,-86 Q4,-80 -24,-86 Q-34,-92 -28,-102Z" fill="url(#gRed)" {O}/>'''
        arm_l = arm_l.replace('url(#gRat)" stroke-width="8"', 'url(#gSleeve)" stroke-width="8"')
        arm_r = arm_r.replace('url(#gRat)" stroke-width="8"', 'url(#gSleeve)" stroke-width="8"')
        held = f'<g transform="translate(10,-64) rotate(-28) scale(.6)">{lute()}</g>'
    elif outfit in ("wizard", "master"):   # blue robes (journeyman) / purple robes (master)
        g = "url(#gBlue)" if outfit == "wizard" else "url(#gPurple)"
        trim = "#e9d701" if outfit == "master" else "#bfe6ff"
        over_body = f'''<path d="M-30,-6 Q-34,-60 -24,-98 Q4,-108 32,-98 Q42,-60 38,-6Z" fill="{g}" {O}/>
<path d="M-30,-8 L38,-8" stroke="{trim}" stroke-width="3"/><path d="M4,-100 L4,-8" stroke="{trim}" stroke-width="2" opacity=".8"/>
<use href="#sparkle" fill="{trim}" transform="translate(-12 -40) scale(.5)"/><use href="#sparkle" fill="{trim}" transform="translate(20 -64) scale(.4)"/>'''
        over_head = f'''<path d="M-20,-140 Q12,-150 46,-140 Q42,-134 12,-136 Q-16,-134 -20,-140Z" fill="{g}" {O}/>
<path d="M-8,-142 Q6,-174 16,-198 Q24,-188 32,-186 Q24,-168 30,-142Z" fill="{g}" {O}/>
<use href="#sparkle" fill="{trim}" transform="translate(14 -160) scale(.45)"/>'''
        feet = ""
        if outfit == "wizard":
            held = f'<g transform="translate(46,-78) rotate(10) scale(.75)">{mirror()}</g>'
    elif outfit == "scribe":   # quills: spectacles, ink-stained vest, quill
        over_body = f'''<path d="M-26,-50 Q-28,-94 -6,-100 L2,-60 L12,-100 Q34,-94 30,-50 Q4,-40 -26,-50Z" fill="#4b0f86" {O}/>
<g fill="url(#gGold)"><circle cx="-6" cy="-76" r="2"/><circle cx="-4" cy="-64" r="2"/></g><path d="M18,-70 q4,4 2,10" stroke="#1a1030" stroke-width="3" stroke-linecap="round"/>'''
        over_head = f'<g fill="none" stroke="#3a2414" stroke-width="2"><circle cx="13" cy="-138" r="7"/><circle cx="31" cy="-137" r="8"/><path d="M20,-138 h3 M-6,-142 l12,2"/></g>'
        held = f'<g transform="translate(38,-56) rotate(-6)">{quill(.75)}</g>'
    elif outfit == "merchant":
        over_body = f'''<path d="M-26,-50 Q-28,-94 -6,-100 L4,-56 L12,-100 Q34,-94 30,-50 Q4,-40 -26,-50Z" fill="#a3162c" {O}/>
<g fill="url(#gGold)" {O1}><circle cx="-6" cy="-80" r="2.4"/><circle cx="-4" cy="-66" r="2.4"/></g>
<path d="M14,-48 q-2,14 8,18 q10,-4 8,-18Z" fill="url(#gLeather)" {O1}/>'''
        over_head = f'<path d="M-14,-146 Q10,-166 34,-150 L36,-144 Q10,-150 -14,-140Z" fill="#a3162c" {O1}/>'
        held = f'<g transform="translate(40,-62)">{galleon(8)}</g>'
    elif outfit == "ragged":
        over_body = f'''<path d="M-32,-24 L-30,-60 Q-28,-100 4,-104 Q36,-100 36,-60 L38,-24 L28,-30 L22,-20 L12,-28 L4,-18 L-6,-28 L-14,-20 L-22,-30Z" fill="#7a5a3a" {O}/>
<rect x="-14" y="-70" width="12" height="11" fill="#a3162c" stroke="{INK}" stroke-width="1" stroke-dasharray="2 1.5"/><rect x="14" y="-48" width="10" height="9" fill="#5a6a8a" stroke="{INK}" stroke-width="1" stroke-dasharray="2 1.5"/>'''
    elif outfit == "suit":   # the rat who sold out
        over_body = f'''<path d="M-27,-48 Q-30,-96 4,-100 Q34,-96 31,-48 Q4,-38 -27,-48Z" fill="url(#gSuit)" {O}/>
<path d="M-6,-100 L4,-74 L14,-100Z" fill="#f2f2f2"/><path d="M2,-96 h4 l1.6,16 l-3.6,5 l-3.6,-5Z" fill="#c0182e"/>'''
        arm_l = arm_l.replace('url(#gRat)" stroke-width="8"', 'url(#gSuit)" stroke-width="8"')
        arm_r = arm_r.replace('url(#gRat)" stroke-width="8"', 'url(#gSuit)" stroke-width="8"')
        held = f'<g transform="translate(40,-62)">{galleon(7)}</g>'
    elif outfit == "crook":   # a Red City rat gone bad: striped sweater, flat cap, burglar's mask, crowbar
        over_body = f'''<path d="M-27,-48 Q-30,-96 4,-100 Q34,-96 31,-48 Q4,-38 -27,-48Z" fill="#1d1a26" {O}/>
<g stroke="#c9c2d6" stroke-width="4.5" opacity=".9"><path d="M-28,-88 Q4,-80 34,-88"/><path d="M-29,-74 Q4,-66 33,-74"/><path d="M-29,-60 Q4,-52 32,-60"/></g>
<path d="M-27,-48 Q-30,-96 4,-100 Q34,-96 31,-48 Q4,-38 -27,-48Z" fill="none" {O}/>'''
        arm_l = arm_l.replace('url(#gRat)" stroke-width="8"', '#1d1a26" stroke-width="8"')
        arm_r = arm_r.replace('url(#gRat)" stroke-width="8"', '#1d1a26" stroke-width="8"')
        over_head = f'''<path d="M2,-147 Q22,-154 44,-146 Q48,-138 44,-131 Q22,-126 2,-131 Q-2,-139 2,-147Z M12,-138 m-6.5,0 a6.5,7.5 0 1,0 13,0 a6.5,7.5 0 1,0 -13,0 M30,-137 m-6.5,0 a6.5,7.5 0 1,0 13,0 a6.5,7.5 0 1,0 -13,0" fill="#0d0a14" fill-rule="evenodd" {O1}/>
<path d="M-4,-140 L-12,-134 M-4,-142 L-14,-142" stroke="#0d0a14" stroke-width="3" stroke-linecap="round"/>
<path d="M-18,-150 Q8,-176 42,-160 L56,-152 Q50,-148 40,-150 Q10,-160 -18,-144Z" fill="#3a3448" {O}/><path d="M-6,-160 Q12,-170 30,-162" stroke="#2a2436" stroke-width="2" fill="none"/>'''
        held = f'<g transform="translate(37,-52) rotate(34)"><path d="M0,0 L0,-62 Q0,-72 8,-74 L14,-72" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M0,0 L0,-62 Q0,-72 8,-74 L14,-72" fill="none" stroke="#7a7f8c" stroke-width="4" stroke-linecap="round"/><path d="M0,0 l-5,7" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
    if prop == "quill":
        held = f'<g transform="translate(38,-56) rotate(-6)">{quill(.75)}</g>'
    elif prop == "none":
        held = ""
    return f'<g>{tail}{legs}{feet}{body}{over_body}{arm_l}{held}{arm_r}{head}{over_head}</g>'


# ---------------------------------------------------------------- LEO Lion
def lion(expr="smug", crown=True):
    """The LEO Lion, Lawful Evil Overlord. Always a lion, always crowned, always robed. A petty tyrant, not majestic."""
    f = face(expr, (-4, -214), (18, -214), 6, 6.5, 11, 6.5, (14, -184), 10, pupil="#2a1408", iris="#d9a400",
             lid="url(#gLion)", look=(1.2, 0.6), far=1.0, brow="#5a2a0e", brow_w=3.2)
    crown_svg = f'''<path d="M-18,-236 L-20,-262 L-8,-250 L6,-272 L16,-252 L30,-262 L28,-236 Q6,-242 -18,-236Z" fill="url(#gGold)" {O}/>
<circle cx="6" cy="-252" r="3.6" fill="#c0182e" {O1}/><circle cx="-12" cy="-246" r="2.4" fill="#3f7fd8"/><circle cx="22" cy="-246" r="2.4" fill="#3f7fd8"/>''' if crown else ""
    mane = []
    for i in range(18):
        a = i * 2 * math.pi / 18
        r1, r2 = (62, 44) if i % 2 == 0 else (54, 44)
        mane.append(f"{6+math.cos(a)*r1:.1f},{-206+math.sin(a)*r1*0.95:.1f}")
        b = a + math.pi / 18
        mane.append(f"{6+math.cos(b)*r2:.1f},{-206+math.sin(b)*r2*0.95:.1f}")
    mane_pts = " ".join(mane)
    return f'''<g>
<path d="M-40,-30 C-80,-24 -96,-60 -84,-80" stroke="url(#gLion)" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-84,-80 q-8,-10 -2,-18 q10,0 8,14Z" fill="url(#gMane)" {O1}/>
<path d="M-26,0 q0,-12 14,-12 q14,0 14,12Z M8,0 q0,-12 14,-12 q14,0 14,12Z" fill="url(#gLion)" {O}/>
<path d="M-50,-6 Q-62,-90 -36,-150 Q6,-166 46,-150 Q72,-90 60,-6Z" fill="url(#gRobe)" {O}/>
<path d="M-50,-6 Q4,6 60,-6" stroke="url(#gGold)" stroke-width="6" fill="none"/><path d="M4,-150 L6,-6" stroke="url(#gGold)" stroke-width="5"/>
<g stroke="#4a0610" stroke-width="1.6" fill="none" opacity=".7"><path d="M-30,-120 q-8,50 -12,110 M36,-120 q10,50 12,110"/></g>
<path d="M-40,-150 Q6,-178 52,-150 Q56,-132 40,-128 Q6,-124 -28,-128 Q-46,-134 -40,-150Z" fill="#f6f1e6" {O}/>
<g fill="{INK}">{''.join(f'<path d="M{x},{y} l-2,5 l4,0Z"/>' for x, y in ((-28, -144), (-12, -138), (4, -136), (20, -138), (36, -144), (-20, -150), (28, -150)))}</g>
<path d="M50,-130 Q68,-110 60,-92" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M50,-130 Q68,-110 60,-92" stroke="url(#gRobe)" stroke-width="18" fill="none" stroke-linecap="round"/>
<path d="M66,-96 L76,-232" stroke="url(#gGold)" stroke-width="5" stroke-linecap="round"/><circle cx="76" cy="-238" r="8" fill="url(#gGold)" {O1}/><circle cx="76" cy="-238" r="3.6" fill="#c0182e"/>
<path d="M52,-98 q10,-10 18,0 q2,12 -8,14 q-12,-2 -10,-14Z" fill="url(#gLion)" {O1}/>
<path d="M-34,-128 Q-48,-100 -28,-84" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M-34,-128 Q-48,-100 -28,-84" stroke="url(#gRobe)" stroke-width="18" fill="none" stroke-linecap="round"/>
<path d="M-30,-92 q10,-8 18,2 q0,10 -10,12 q-10,-2 -8,-14Z" fill="url(#gLion)" {O1}/>
<polygon points="{mane_pts}" fill="url(#gMane)" {O}/>
<circle cx="-20" cy="-244" r="9" fill="url(#gLion)" {O}/><circle cx="34" cy="-244" r="9" fill="url(#gLion)" {O}/><circle cx="-20" cy="-244" r="4.5" fill="#a0601a"/><circle cx="34" cy="-244" r="4.5" fill="#a0601a"/>
<path d="M-22,-204 C-22,-234 -2,-242 8,-242 C26,-242 36,-232 38,-210 Q40,-188 30,-176 Q12,-164 -6,-172 Q-22,-182 -22,-204Z" fill="url(#gLion)" {O}/>
<path d="M-2,-194 Q14,-204 32,-194 Q36,-180 26,-172 Q12,-166 0,-172 Q-8,-182 -2,-194Z" fill="#fbe2b0"/>
<path d="M8,-198 h12 l-6,7Z" fill="#5a2a12" {O1}/>
{f}
{crown_svg}
</g>'''


# ---------------------------------------------------------------- Corporate Wolf
def wolf(expr="greedy", arrows=False):
    """The Corporate Wolf. Gray wolf, black suit, red tie, dollar-sign eyes. NEVER a crown."""
    e, b, m = EXPRESSIONS.get(expr, ("open", "down", "teeth")) if expr != "greedy" else ("open", "down", "teeth")
    # Dollar-sign eyes: always. Expression changes brows, lids and mouth.
    def dollar_eye(cx, cy, s):
        if e == "closed":
            return f'<path d="M{cx-7*s:.1f},{cy+2:.1f} Q{cx:.1f},{cy-8*s:.1f} {cx+7*s:.1f},{cy+2:.1f}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'
        k = 1.2 if e == "wide" else 1.0
        h = 0.65 if e == "squint" else 1.0
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{8*s*k:.1f}" ry="{9*s*k*h:.1f}" fill="#0c0a08" {O1}/>'
                f'<text x="{cx}" y="{cy+5*s*k*h:.1f}" font-size="{15*s*k*h:.1f}" font-weight="700" text-anchor="middle" fill="#e9d701" font-family="Georgia, serif">$</text>'
                + (f'<path d="M{cx-9*s:.1f},{cy-1:.1f} Q{cx:.1f},{cy-4:.1f} {cx+9*s:.1f},{cy-1:.1f} L{cx+9*s:.1f},{cy-11*s:.1f} L{cx-9*s:.1f},{cy-11*s:.1f}Z" fill="url(#gWolf)"/><path d="M{cx-9*s:.1f},{cy-1:.1f} Q{cx:.1f},{cy-4:.1f} {cx+9*s:.1f},{cy-1:.1f}" stroke="{INK}" stroke-width="2" fill="none"/>' if e == "lidded" else ""))
    mouth_svg = {
        "teeth": f'''<path d="M32,-210 Q58,-196 86,-214 Q74,-196 56,-192 Q40,-192 32,-210Z" fill="#5a0f1a" {O1}/>
<path d="M36,-208 L40,-202 L44,-207 L48,-200 L52,-205 L56,-198 L60,-204 L64,-198 L68,-205 L72,-200 L76,-207 L80,-202 L84,-212 Q58,-200 36,-208Z" fill="#fff" stroke="{INK}" stroke-width="1"/>''',
        "laugh": f'''<path d="M32,-210 Q58,-200 86,-214 Q78,-184 56,-182 Q38,-184 32,-210Z" fill="#5a0f1a" {O1}/><path d="M36,-208 L42,-201 L48,-206 L54,-200 L60,-205 L66,-199 L72,-205 L78,-200 L84,-212 Q58,-202 36,-208Z" fill="#fff"/><path d="M46,-186 q10,-8 22,0Z" fill="#f08a9a"/>''',
        "wavy": f'<path d="M38,-204 q6,-4 12,0 t12,0 t12,0 t10,-2" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>',
        "o": f'<ellipse cx="60" cy="-200" rx="7" ry="9" fill="#5a0f1a" {O1}/>',
        "frown": f'<path d="M38,-198 Q58,-212 82,-202" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>',
        "smirk": f'<path d="M38,-204 Q60,-198 84,-214" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>',
        "flat": f'<path d="M38,-204 L82,-208" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>',
        "smile": f'<path d="M38,-208 Q60,-196 84,-212" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>',
        "grin": None,
    }
    if m == "grin":
        m = "teeth"
    arrows_svg = f'<g transform="translate(-34,-298)">{down_arrows()}</g>' if arrows else ""
    return f'''<g>
<path d="M-30,-60 C-70,-50 -88,-10 -64,4 C-74,-20 -60,-40 -30,-44Z" fill="url(#gWolf)" {O}/>
<path d="M-32,-74 L-30,-8 L-6,-8 L-4,-74Z M4,-74 L6,-8 L30,-8 L32,-74Z" fill="#1c1c24" {O}/>
<path d="M-34,0 Q-36,-10 -26,-12 L-4,-12 Q2,-6 -2,0Z M2,0 Q0,-8 6,-12 L28,-12 Q42,-10 40,0Z" fill="#050508" {O}/>
<path d="M-44,-200 Q-58,-140 -46,-70 L46,-70 Q58,-140 44,-200 Q0,-212 -44,-200Z" fill="url(#gSuit)" {O}/>
<path d="M-10,-204 L0,-150 L10,-204Z" fill="#f2f2f2" {O1}/><path d="M-4,-200 h8 l3,40 l-7,9 l-7,-9Z" fill="#c0182e" {O1}/>
<path d="M-44,-200 L-10,-204 L-4,-150 L-22,-176Z M44,-200 L10,-204 L4,-150 L22,-176Z" fill="#2a2a36" {O1}/>
<circle cx="0" cy="-110" r="2.2" fill="#9a9aa8"/><circle cx="0" cy="-94" r="2.2" fill="#9a9aa8"/>
<path d="M-50,-170 Q-62,-130 -30,-124 L30,-124 Q60,-130 50,-170" stroke="{INK}" stroke-width="28" fill="none" stroke-linecap="round"/>
<path d="M-50,-170 Q-62,-130 -30,-124 L30,-124 Q60,-130 50,-170" stroke="url(#gSuit)" stroke-width="24" fill="none" stroke-linecap="round"/>
<path d="M-36,-136 L24,-136 M-26,-118 L34,-118" stroke="#2a2a36" stroke-width="2"/>
<path d="M28,-138 q12,-6 18,4 q-2,10 -12,10 q-8,-2 -6,-14Z M-34,-124 q-12,-4 -16,6 q4,10 12,8 q8,-4 4,-14Z" fill="url(#gWolf)" {O1}/>
<path d="M-26,-228 L-36,-290 L-4,-250Z" fill="url(#gWolf)" {O}/><path d="M8,-254 L22,-296 L32,-240Z" fill="url(#gWolf)" {O}/>
<path d="M-24,-236 L-30,-276 L-10,-252Z M12,-254 L21,-284 L28,-244Z" fill="#3a3a48"/>
<path d="M-32,-226 C-36,-256 -6,-268 14,-264 C30,-262 42,-252 52,-240 L88,-228 Q96,-222 88,-216 L62,-206 Q42,-188 14,-190 C-16,-192 -30,-206 -32,-226Z" fill="url(#gWolf)" {O}/>
<path d="M14,-190 Q42,-188 62,-206 L88,-216 Q70,-196 44,-188 Q26,-184 14,-190Z" fill="#d8d8e2"/>
<path d="M-30,-214 l-12,4 l8,6 l-10,4 l12,2 Q-18,-196 -8,-194" fill="#c8c8d4" {O1}/>
<ellipse cx="91" cy="-224" rx="6" ry="5" fill="#0c0a08"/><ellipse cx="89" cy="-226" rx="2" ry="1.2" fill="#fff" opacity=".6"/>
{dollar_eye(6, -236, 0.92)}{dollar_eye(30, -238, 1.0)}
{brows(b, (6, -236), (30, -238), 8, 13, color="#2a2a36", sw=3.4)}
{mouth_svg[m]}
{arrows_svg}
</g>'''


CAST = {
    "reynard": reynard, "mira": mira, "badger": badger, "bull": bull,
    "rat": rat, "lion": lion, "wolf": wolf, "frog": frog,
}


# Canonical relative sizes: draw every character at CANON_SCALE so heights agree on every card.
CANON_SCALE = {"reynard": 1.0, "mira": 0.65, "badger": 1.0, "bull": 1.2, "lion": 1.05, "wolf": 1.0, "rat": 0.7, "frog": 0.8}
