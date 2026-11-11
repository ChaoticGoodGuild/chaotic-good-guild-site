"""Settings and props for the Guild tarot deck. The art canvas is 620 x 870; ground sits near y = 700-850."""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scene  # noqa: E402
import characters as C  # noqa: E402
import cards as K  # noqa: E402
from characters import O, O1, INK  # noqa: E402

ROOT = os.path.dirname(HERE)
STAR = open(os.path.join(ROOT, "src", "star.b64")).read()

DEFS = f"""
<image id="gStarImg" href="data:image/png;base64,{STAR}" width="100" height="96"/>
<linearGradient id="kDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a86d6"/><stop offset=".7" stop-color="#a8d8f0"/><stop offset="1" stop-color="#f6e9b8"/></linearGradient>
<linearGradient id="kDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a5a"/><stop offset=".5" stop-color="#b8487a"/><stop offset=".8" stop-color="#f2a65a"/><stop offset="1" stop-color="#ffe9a8"/></linearGradient>
<linearGradient id="kWorld" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c3f96"/><stop offset=".5" stop-color="#5aa0e0"/><stop offset=".8" stop-color="#e8704a"/><stop offset="1" stop-color="#6e0f1e"/></linearGradient>
<radialGradient id="kCosmos" cx=".5" cy=".45" r=".8"><stop offset="0" stop-color="#4a1c8a"/><stop offset=".6" stop-color="#14062e"/><stop offset="1" stop-color="#05010c"/></radialGradient>
<linearGradient id="kGrassDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ab85a"/><stop offset="1" stop-color="#2a5a30"/></linearGradient>
<linearGradient id="kGrassDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a78"/><stop offset="1" stop-color="#161030"/></linearGradient>
<linearGradient id="kWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5ab8"/><stop offset="1" stop-color="#14103a"/></linearGradient>
<linearGradient id="kOffice" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a8088"/><stop offset="1" stop-color="#565c66"/></linearGradient>
<linearGradient id="kStone" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a8494"/><stop offset="1" stop-color="#4a4456"/></linearGradient>
<linearGradient id="kSnow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3f0ff"/><stop offset="1" stop-color="#8a86c0"/></linearGradient>
<pattern id="kBrick" width="48" height="28" patternUnits="userSpaceOnUse"><rect width="48" height="28" fill="#4a1a20"/><path d="M0,0 h48 M0,14 h48 M0,0 v14 M24,14 v14" stroke="#1c080c" stroke-width="2.5"/><rect x="3" y="3" width="16" height="3" fill="#7a2c34" opacity=".5"/><rect x="28" y="17" width="14" height="3" fill="#7a2c34" opacity=".4"/></pattern>
<pattern id="kPlank" width="62" height="220" patternUnits="userSpaceOnUse"><rect width="62" height="220" fill="#3a2418"/><path d="M0,0 v220" stroke="#1e100a" stroke-width="3"/><path d="M20,30 q6,40 -2,90 M44,110 q-5,40 3,80" stroke="#2a180e" stroke-width="1.5" fill="none"/><ellipse cx="34" cy="60" rx="5" ry="9" fill="none" stroke="#2a180e" stroke-width="1.5"/></pattern>
<pattern id="kHatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><path d="M0,0 v6" stroke="#1a0a2e" stroke-width="1.2"/></pattern>
<radialGradient id="kVig" cx=".5" cy=".46" r=".8"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>
<filter id="fGold"><feColorMatrix type="matrix" values=".5 .55 .15 0 .14  .42 .46 .12 0 .09  .08 .1 .04 0 0  0 0 0 1 0"/></filter>
<filter id="fGrey"><feColorMatrix type="matrix" values=".3 .3 .3 0 .1  .3 .3 .3 0 .1  .3 .3 .3 0 .14  0 0 0 1 0"/></filter>
"""

_n = [0]


def uid(p="u"):
    _n[0] += 1
    return f"{p}{_n[0]}"


SHW = {"reynard": 70, "mira": 60, "badger": 75, "bull": 70, "lion": 70, "wolf": 60, "rat": 38, "frog": 20}


def ch(name, x, y, k=1.5, flip=False, rot=0, sh=True, **kw):
    """Place a cast member with feet at (x, y). k multiplies the character's canonical size."""
    s = C.CANON_SCALE[name] * k
    out = f'<ellipse cx="{x}" cy="{y+2}" rx="{SHW[name]*s:.0f}" ry="{max(5, 9*s):.0f}" fill="#000" opacity=".3"/>' if sh and rot == 0 else ""
    return out + K.place(C.CAST[name](**kw), x, y, s, flip, rot)


def gstar(x, y, size, glow=True):
    g = f'<circle cx="{x}" cy="{y}" r="{size*0.75:.0f}" fill="url(#halo)"/>' if glow else ""
    return g + f'<use href="#gStarImg" transform="translate({x-size/2:.0f},{y-size*0.48:.0f}) scale({size/100:.2f})"/>'


K.guild_star = gstar


def sp(x, y, s=1.0, col="#e9d701"):
    return f'<use href="#sparkle" fill="{col}" transform="translate({x} {y}) scale({s})"/>'


SKY = {"night": "kNight", "red": "kRed", "dusk": "kDusk", "day": "kDay", "dawn": "kDawn", "cosmos": "kCosmos", "world": "kWorld"}


def sky(kind, seed=1, n=None):
    s = f'<rect width="620" height="870" fill="url(#{SKY[kind]})"/>'
    n = {"night": 110, "dusk": 45, "cosmos": 190, "dawn": 14}.get(kind, 0) if n is None else n
    if n:
        s += K.stars(n, seed, 870 if kind == "cosmos" else 560)
    if kind == "red":
        s += clouds(seed, 40, 260, 4, "#1e0408", .55)
    return s


def clouds(seed, y0, y1, n=4, col="#fff", op=.5):
    r = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y, w = r.uniform(-40, 600), r.uniform(y0, y1), r.uniform(70, 150)
        out += (f'<g fill="{col}" opacity="{op}"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{w*.2:.0f}"/>'
                f'<ellipse cx="{x-w*.3:.0f}" cy="{y-w*.12:.0f}" rx="{w*.4:.0f}" ry="{w*.2:.0f}"/><ellipse cx="{x+w*.25:.0f}" cy="{y-w*.16:.0f}" rx="{w*.45:.0f}" ry="{w*.24:.0f}"/></g>')
    return out


def moon(x, y, r=70):
    return (f'<circle cx="{x}" cy="{y}" r="{r*2.3:.0f}" fill="url(#moonGlow)"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#gMoon)"/>'
            f'<g fill="#cdbf92" opacity=".7"><circle cx="{x-r*.3:.0f}" cy="{y-r*.3:.0f}" r="{r*.18:.0f}"/><circle cx="{x+r*.35:.0f}" cy="{y+r*.25:.0f}" r="{r*.24:.0f}"/>'
            f'<circle cx="{x+r*.2:.0f}" cy="{y-r*.45:.0f}" r="{r*.1:.0f}"/><circle cx="{x-r*.4:.0f}" cy="{y+r*.35:.0f}" r="{r*.1:.0f}"/></g>')


def sun(x, y, r=60):
    rays_ = "".join(f'<path d="M0,{-r*1.2:.0f} L{r*.14:.0f},{-r*1.75:.0f} L{-r*.14:.0f},{-r*1.75:.0f}Z" transform="rotate({a})"/>' for a in range(0, 360, 30))
    return f'<g transform="translate({x},{y})"><circle r="{r*2.6:.0f}" fill="url(#gWarm)"/><g fill="#ffd75a">{rays_}</g><circle r="{r}" fill="#ffe27a" stroke="#e9a800" stroke-width="3"/></g>'


def rays(x, y, n=7, L=900, col="#fff3a0", op=.09, a0=55, a1=125):
    out = ""
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n - 1))
        d = math.radians(2.6)
        out += f'<polygon points="{x},{y} {x+L*math.cos(a-d):.0f},{y+L*math.sin(a-d):.0f} {x+L*math.cos(a+d):.0f},{y+L*math.sin(a+d):.0f}"/>'
    return f'<g fill="{col}" opacity="{op}">{out}</g>'


def consts(seed=3, n=3, col="#fff3a0"):
    r = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y = r.uniform(60, 520), r.uniform(50, 330)
        pts = [(x, y)]
        for _ in range(r.randint(3, 5)):
            x, y = x + r.uniform(25, 60), y + r.uniform(-40, 40)
            pts.append((x, y))
        out += f'<path d="M{" L".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" stroke="{col}" stroke-opacity=".4" stroke-width="1.4" fill="none"/>'
        out += "".join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="2.6" fill="{col}"/>' for a, b in pts)
    return out


def far_city(x, y, s=1.0, op=1.0, col="#2b0812", glow=True):
    tw = [(-130, -96, 34), (-52, -160, 48), (52, -120, 40), (112, -70, 30)]
    b = '<rect x="-170" y="-34" width="340" height="34"/>' + "".join(f'<rect x="{-170+i*24}" y="-44" width="12" height="10"/>' for i in range(15))
    li = '<rect x="-96" y="-22" width="7" height="10"/><rect x="20" y="-22" width="7" height="10"/><rect x="88" y="-22" width="7" height="10"/>'
    fl = ""
    for tx, ty, w in tw:
        b += f'<rect x="{tx}" y="{ty}" width="{w}" height="{-ty}"/><polygon points="{tx-5},{ty} {tx+w/2:.0f},{ty-w*1.1:.0f} {tx+w+5},{ty}"/>'
        li += f'<rect x="{tx+w/2-3:.0f}" y="{ty+16}" width="6" height="10"/>'
        fl += f'<path d="M{tx+w/2:.0f},{ty-w*1.1:.0f} v-14 l12,4 l-12,4" fill="#c0182e" stroke="{col}" stroke-width="1.5"/>'
    g = '<ellipse cx="0" cy="-70" rx="270" ry="160" fill="url(#redGlow)"/>' if glow else ""
    return f'<g transform="translate({x},{y}) scale({s})" opacity="{op}">{g}<g fill="{col}">{b}</g><g fill="#ff6a3c">{li}</g>{fl}</g>'


def hills(y, col, amp=26, ph=0.0, f=1.0):
    pts = " ".join(f"L{x},{y+amp*math.sin(ph+x/620*math.pi*2*f):.0f}" for x in range(0, 641, 40))
    return f'<path d="M0,870 {pts} L620,870Z" fill="{col}"/>'


GR = {"night": ("url(#kGrass)", "#4a3a78"), "day": ("url(#kGrassDay)", "#2f6b3a"), "dusk": ("url(#kGrassDusk)", "#6a6a9a"),
      "purple": ("url(#kGroundPurple)", "#3b2468")}


def ground(kind="night", y=690, fl=12, tufts=34):
    fill, tc = GR[kind]
    s = f'<path d="M0,{y+20} Q310,{y-30} 620,{y+20} L620,870 L0,870Z" fill="{fill}"/>'
    s += scene.tufts(tufts, 0, 620, lambda x: y + 30 + random.uniform(0, 150), tc, 10)
    if fl:
        s += scene.flowers(fl, 10, 610, y + 40, 860, [])
    return s


def street(y=640, fill="url(#kStreet)", seed=3):
    r = random.Random(seed)
    s = f'<path d="M0,{y} Q310,{y-22} 620,{y} L620,870 L0,870Z" fill="{fill}"/>'
    cob, yy, w = "", y + 26, 30
    while yy < 880:
        x = -r.uniform(0, w)
        while x < 620:
            cob += f'<path d="M{x:.0f},{yy:.0f} q{w/2:.0f},{-w*.24:.0f} {w:.0f},0"/>'
            x += w + 3
        yy += w * .5
        w *= 1.13
    return s + f'<g stroke="#0c0306" stroke-opacity=".55" stroke-width="2" fill="none">{cob}</g>'


def le_houses(seed=1, base=660, left=True, right=True):
    r = random.Random(seed)

    def house(x, w, h, c):
        s = (f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{c}"/>'
             f'<rect x="{x+w*.68:.0f}" y="{base-h-w*.5:.0f}" width="13" height="{w*.4:.0f}" fill="#1a050a"/>'
             f'<polygon points="{x-9},{base-h} {x+w/2:.0f},{base-h-w*.55:.0f} {x+w+9},{base-h}" fill="#1e060c"/>'
             f'<path d="M{x},{base-h+12} h{w} M{x+w/2:.0f},{base-h} v{h}" stroke="#1a050a" stroke-width="4" opacity=".7"/>')
        for wy in range(int(base - h + 28), base - 56, 58):
            for wx in (x + w * .16, x + w * .62):
                lit = r.random() < .6
                s += f'<rect x="{wx:.0f}" y="{wy}" width="{w*.2:.0f}" height="26" fill="{"#ff8a4c" if lit else "#14040a"}" stroke="#14040a" stroke-width="2.5"/>'
        return s
    out = ""
    if left:
        out += house(60, 92, r.randint(150, 200), "#4a1422") + house(-34, 124, r.randint(240, 300), "#3a0f18")
    if right:
        out += house(468, 92, r.randint(150, 210), "#4a1422") + house(530, 130, r.randint(240, 310), "#3a0f18")
    return out


def city(time="red", far=1.0, seed=1, houses=True):
    return sky(time, seed) + far_city(310, 620, far) + (le_houses(seed) if houses else "") + street(640)


def castle(balcony="", on_rail="", banners=True):
    s = f'''<circle cx="360" cy="300" r="230" fill="#ff5a3c" opacity=".12"/><g fill="#2b0812">
<rect x="160" y="300" width="400" height="330"/>{''.join(f'<rect x="{x}" y="288" width="22" height="14"/>' for x in range(160, 560, 40))}
<rect x="120" y="180" width="80" height="450"/><polygon points="110,180 160,90 210,180"/>
<rect x="520" y="160" width="84" height="470"/><polygon points="510,160 562,70 614,160"/>
<rect x="300" y="120" width="120" height="200"/><polygon points="290,120 360,30 430,120"/></g>
<g stroke="#1a040a" stroke-width="2" opacity=".8">{''.join(f'<path d="M160,{y} h400"/>' for y in range(440, 630, 32))}{''.join(f'<path d="M{x},{y} v32"/>' for y in range(440, 600, 64) for x in range(190, 560, 60))}</g>
<g fill="#ff6a3c" opacity=".9"><path d="M146,230 q8,-12 16,0 v26 h-16Z M548,220 q8,-12 16,0 v26 h-16Z M340,170 q10,-14 20,0 v30 h-20Z M146,320 q8,-12 16,0 v26 h-16Z M548,320 q8,-12 16,0 v26 h-16Z M200,480 q8,-12 16,0 v26 h-16Z M500,480 q8,-12 16,0 v26 h-16Z"/></g>
<path d="M330,630 v-70 q30,-40 60,0 v70Z" fill="#0c0206"/><g stroke="#3a0c18" stroke-width="3"><path d="M342,630 v-74 M360,630 v-84 M378,630 v-74 M330,590 h60"/></g>
<g stroke="#2b0812" stroke-width="3"><path d="M160,90 v-26 M562,70 v-26 M360,30 v-24"/></g>
<g fill="#a3162c"><path d="M160,64 l24,7 l-24,8Z M562,44 l24,7 l-24,8Z M360,6 l26,8 l-26,8Z"/></g>
<rect x="250" y="240" width="250" height="110" fill="#14040a"/>{balcony}
<path d="M240,350 h270 v12 h-270Z" fill="#4a1020" {O}/>{''.join(f'<rect x="{x}" y="362" width="8" height="34" fill="#3a0c18" {O1}/>' for x in range(250, 506, 22))}<path d="M240,396 h270 v10 h-270Z" fill="#4a1020" {O}/>{on_rail}'''
    if banners:
        s += f'<g transform="translate(262,406)">{C.leo_banner(38, 80)}</g><g transform="translate(450,406)">{C.leo_banner(38, 80)}</g>'
    return s


def duo(le="laugh", we="laugh", arrows=False, crown=True):
    return K.place(C.lion(le, crown), 330, 400, 1.05 * .62) + K.place(C.wolf(we, arrows=arrows), 456, 400, .6)


def alley(seed=1, lamp=True, sky_kind="red"):
    s = sky(sky_kind, seed) + far_city(310, 600, .75)
    s += '<polygon points="0,0 210,0 176,640 0,740" fill="url(#kBrick)"/><polygon points="620,0 410,0 444,640 620,740" fill="url(#kBrick)"/>'
    s += '<polygon points="0,0 210,0 176,640 0,740" fill="#000" opacity=".38"/><polygon points="620,0 410,0 444,640 620,740" fill="#000" opacity=".12"/>'
    s += f'<path d="M210,0 L176,640 M410,0 L444,640" stroke="{INK}" stroke-width="4"/>'
    s += '<g stroke="#14040a" stroke-width="3"><polygon points="40,210 120,196 118,300 40,322" fill="#ff8a4c" opacity=".85"/><polygon points="580,200 500,188 502,290 580,310" fill="#2a0a10"/><polygon points="60,420 130,404 128,470 60,492" fill="#2a0a10"/></g>'
    s += '<path d="M560,0 V640" stroke="#2a2430" stroke-width="12"/><path d="M552,150 h16 M552,400 h16" stroke="#4a4458" stroke-width="5"/>'
    s += '<path d="M0,740 L176,640 L444,640 L620,740 L620,870 L0,870Z" fill="url(#kStreet)"/>'
    r = random.Random(seed)
    cob, yy, w = "", 664, 30
    while yy < 880:
        x = -r.uniform(0, w)
        while x < 620:
            cob += f'<path d="M{x:.0f},{yy:.0f} q{w/2:.0f},{-w*.24:.0f} {w:.0f},0"/>'
            x += w + 3
        yy += w * .5
        w *= 1.13
    s += f'<g stroke="#0c0306" stroke-opacity=".55" stroke-width="2" fill="none">{cob}</g>'
    s += '<ellipse cx="300" cy="826" rx="70" ry="12" fill="#5a1a2a" opacity=".5"/>'
    if lamp:
        s += f'<path d="M444,330 h-40 v14" stroke="#14040a" stroke-width="5" fill="none"/><circle cx="404" cy="366" r="90" fill="url(#kCandle)"/><path d="M392,344 h24 l5,34 h-34Z" fill="#ffd75a" {O1}/>'
    return s


def forest(time="night", seed=1, moon_at=None, far=True):
    s = sky(time, seed)
    if moon_at:
        s += moon(*moon_at)
    c = {"night": ("#241446", "#170a2e", "#2b1650"), "dusk": ("#4a2a6a", "#2a1648", "#3d2466"), "day": ("#5a9a6a", "#2a5a3a", "#3f8a4a")}[time]
    r = random.Random(seed)
    if far:
        s += "".join(scene.pine(x, 640, r.uniform(230, 330), c[0], c[0]) for x in range(20, 620, 62))
    s += f'<path d="M0,640 Q310,600 620,640 L620,700 L0,700Z" fill="{c[0]}" opacity=".6"/>'
    s += "".join(scene.pine(x, y, h, c[1], c[2]) for x, y, h in ((-6, 700, 420), (66, 705, 330), (562, 700, 370), (628, 706, 450)))
    s += ground({"night": "purple", "dusk": "dusk", "day": "day"}[time], 690, fl=10)
    s += shrooms(seed)
    return s


def shrooms(seed=1, n=5):
    r = random.Random(seed + 40)
    out = ""
    for _ in range(n):
        x, y, sc = r.choice([r.uniform(10, 150), r.uniform(470, 610)]), r.uniform(770, 860), r.uniform(.9, 1.7)
        c = r.choice(["#e9d701", "#b06cff", "#ff7eb6"])
        out += (f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.1f})"><ellipse cx="0" cy="-4" rx="18" ry="18" fill="{c}" opacity=".2"/><rect x="-3" y="-8" width="6" height="12" rx="2" fill="#e2d5b6"/>'
                f'<path d="M-13,-7 q13,-20 26,0Z" fill="{c}" {O1}/><circle cx="-4" cy="-12" r="1.8" fill="#fff" opacity=".8"/></g>')
    return out


def fireflies(seed=1, n=10, y0=300, y1=820):
    r = random.Random(seed + 9)
    return "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#e9d701" opacity=".14"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2.6" fill="#fff3a0"/>'
                   for x, y in ((r.uniform(10, 610), r.uniform(y0, y1)) for _ in range(n)))


def village(time="dusk", far=True, seed=1, strings=True, houses=None):
    s = sky(time, seed)
    if time == "day":
        s += sun(520, 110, 46) + clouds(seed, 60, 240, 3)
    if far:
        s += far_city(120, 588, .42, op=.55 if time == "day" else .8, glow=time != "day")
    s += hills(600, {"day": "#5a9a5a", "dusk": "#3a2a5a", "night": "#1a0b32"}[time], 18, seed)
    houses = houses or [(86, 640, .95, '#7a1fb8', '#ffd75a'), (540, 630, .9, '#a3162c', '#ffe08a'), (430, 648, .58, '#6000AE', '#ffd75a'), (210, 652, .5, '#b8860b', '#ffd75a')]
    s += "".join(scene.minihouse(*h) for h in houses)
    s += ground({"day": "day", "dusk": "dusk", "night": "night"}[time], 660)
    if strings:
        s += scene.lstring(-10, 300, 630, 280, 60, 10)
    return s


def meadow(time="day", far=True, seed=1):
    s = sky(time, seed)
    if time == "day":
        s += sun(110, 120, 46) + clouds(seed, 60, 260, 3)
    if far:
        s += far_city(480, 590, .45, op=.5 if time == "day" else .8, glow=time != "day")
    s += hills(610, {"day": "#6aa86a", "dusk": "#3a2a5a", "night": "#1a0b32", "dawn": "#4a2f6a"}[time], 22, seed)
    s += ground({"day": "day", "dusk": "dusk", "night": "night", "dawn": "dusk"}[time], 670)
    return s


def tree(x, y, s=1.0, leaf="#2f6b3a", leaf2="#4c9a4a"):
    blobs = [(-70, -250, 70), (0, -300, 86), (74, -250, 72), (-36, -210, 64), (40, -205, 66), (0, -250, 70)]
    b = "".join(f'<circle cx="{a}" cy="{c}" r="{r}" fill="{leaf}" {O}/>' for a, c, r in blobs[:3])
    b += "".join(f'<circle cx="{a}" cy="{c}" r="{r}" fill="{leaf}"/>' for a, c, r in blobs)
    b += "".join(f'<circle cx="{a-r*.25:.0f}" cy="{c-r*.3:.0f}" r="{r*.5:.0f}" fill="{leaf2}" opacity=".7"/>' for a, c, r in blobs)
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-22,0 Q-10,-80 -16,-190 L16,-190 Q10,-80 26,0Z" fill="url(#gWoodV)" {O}/>'
            f'<path d="M-6,-20 q4,-60 -2,-150 M8,-40 q-2,-50 2,-120" stroke="#2a1608" stroke-width="2" fill="none"/>{b}</g>')


def cosmos(seed=1):
    r = random.Random(seed)
    s = sky("cosmos", seed)
    for col in ("#b06cff", "#e9d701", "#ff7eb6", "#4a8af0"):
        s += f'<ellipse cx="{r.uniform(60, 560):.0f}" cy="{r.uniform(80, 760):.0f}" rx="{r.uniform(120, 220):.0f}" ry="{r.uniform(60, 120):.0f}" fill="{col}" opacity=".16" filter="url(#blur8)" transform="rotate({r.uniform(-30, 30):.0f} 310 435)"/>'
    return s + consts(seed, 4)


def room(win="city", seed=1):
    inner = {"city": '<rect width="230" height="290" fill="url(#kRed)"/>' + far_city(115, 290, .72, glow=False),
             "dawn": '<rect width="230" height="290" fill="url(#kDawn)"/>' + gstar(120, 110, 120) + '<path d="M0,290 Q115,230 230,290Z" fill="#3a2a5a"/>',
             "rain": '<rect width="230" height="290" fill="url(#kRed)"/>' + far_city(115, 290, .72, glow=False) + rain(seed, 40, 230, 290)}[win]
    c = uid("rw")
    return f'''<rect width="620" height="870" fill="url(#kWall)"/><rect width="620" height="720" fill="url(#kPlank)" opacity=".55"/>
<g transform="translate(350,70)"><clipPath id="{c}"><rect width="230" height="290" rx="10"/></clipPath><g clip-path="url(#{c})">{inner}</g>
<path d="M115,0 v290 M0,145 h230" stroke="#4a2c18" stroke-width="10"/><rect width="230" height="290" rx="10" fill="none" stroke="#4a2c18" stroke-width="14"/><rect x="-6" y="286" width="242" height="16" rx="4" fill="#5a3a22" {O1}/>
<path d="M-26,-14 q20,150 -10,300 l-30,0 q20,-150 6,-300Z M256,-14 q-20,150 10,300 l30,0 q-20,-150 -6,-300Z" fill="#4b0f86" {O1}/></g>
<rect y="716" width="620" height="10" fill="#22130c"/><path d="M0,724 h620 v146 h-620Z" fill="#3a2416"/><g stroke="#22130c" stroke-width="2">{''.join(f'<path d="M0,{y} h620"/>' for y in (760, 800, 842))}<path d="M120,724 v36 M400,724 v36 M250,760 v40 M520,760 v40 M80,800 v42 M340,800 v42"/></g>'''


def office(door=False):
    wx = 210 if door else 420
    c = uid("ow")
    s = '<rect width="620" height="870" fill="url(#kOffice)"/><rect width="620" height="56" fill="#3a3f48"/>'
    for x in (150, 440):
        s += f'<polygon points="{x-70},56 {x+70},56 {x+190},640 {x-190},640" fill="#f3ffd8" opacity=".07"/><rect x="{x-70}" y="42" width="140" height="14" fill="#f0f6d8" stroke="#2a2e36" stroke-width="2"/>'
    s += (f'<g transform="translate({wx},100)"><clipPath id="{c}"><rect width="160" height="180"/></clipPath><g clip-path="url(#{c})"><rect width="160" height="180" fill="url(#kRed)"/>{far_city(80, 180, .5, glow=False)}</g>'
          f'<g stroke="#c9ccd2" stroke-width="3" opacity=".8">{"".join(f"<path d=\'M0,{y} h160\'/>" for y in range(14, 180, 18))}</g><rect width="160" height="180" fill="none" stroke="#2a2e36" stroke-width="8"/></g>')
    s += (f'<g transform="translate(40,96)"><rect width="120" height="160" fill="#efe6cf" {O1}/><path d="M34,84 L30,50 L46,66 L60,40 L74,66 L90,50 L86,84Z" fill="#14040a"/>'
          f'<text x="60" y="130" text-anchor="middle" font-family="Georgia, serif" font-weight="700" font-size="30" fill="#a3162c">OBEY</text></g>')
    s += f'<g transform="translate({330 if not door else 430},150)"><circle r="34" fill="#f3f0e6" {O1}/><path d="M0,0 v-22 M0,0 l14,8" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/></g>'
    s += '<rect y="330" width="620" height="310" fill="#5a6a80"/><rect y="330" width="620" height="310" fill="url(#kHatch)" opacity=".12"/><rect y="322" width="620" height="14" fill="#8a96a8" stroke="#2a2e36" stroke-width="2"/>'
    s += '<g stroke="#2a2e36" stroke-width="4">' + "".join(f'<path d="M{x},330 v310"/>' for x in (155, 310, 465)) + '</g>'
    for x in (24, 86):
        s += f'<rect x="{x}" y="420" width="58" height="220" fill="#8a8f98" {O1}/>' + "".join(f'<rect x="{x+6}" y="{y}" width="46" height="62" fill="#9a9fa8" stroke="#2a2e36" stroke-width="2"/><rect x="{x+20}" y="{y+26}" width="18" height="6" fill="#2a2e36"/>' for y in (428, 498, 568))
    s += '<g fill="#ffe27a" stroke="#2a2e36" stroke-width="1.5"><rect x="330" y="372" width="26" height="26" transform="rotate(-6 343 385)"/><rect x="366" y="380" width="26" height="26" transform="rotate(5 379 393)" fill="#ff9ab8"/></g>'
    if door:
        s += f'<rect x="508" y="290" width="104" height="350" fill="#2a2e36"/><rect x="516" y="298" width="88" height="342" fill="#14161c"/><rect x="524" y="250" width="72" height="30" fill="#1f8a3a" {O1}/><text x="560" y="272" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="20" fill="#eaffea">EXIT</text>'
    s += '<rect y="640" width="620" height="230" fill="#3a3a46"/><g stroke="#2a2a34" stroke-width="2">' + "".join(f'<path d="M0,{y} h620"/>' for y in (680, 730, 794)) + "".join(f'<path d="M{310+(x-310)*.72:.0f},640 L{x},870"/>' for x in range(-200, 840, 100)) + '</g>'
    return s


def tavern():
    s = '<rect width="620" height="870" fill="url(#kPlank)"/><rect width="620" height="870" fill="#ff9a3c" opacity=".08"/>'
    s += f'<rect y="70" width="620" height="30" fill="url(#gWood)" {O1}/><rect x="26" y="0" width="30" height="680" fill="url(#gWood)" {O1}/><rect x="564" y="0" width="30" height="680" fill="url(#gWood)" {O1}/>'
    s += "".join(f'<path d="M{x},100 l22,0 l-11,34Z" fill="{"#6000AE" if i % 2 == 0 else "#e9d701"}" {O1}/>' for i, x in enumerate(range(70, 550, 30)))
    s += gstar(310, 250, 170)
    for x in (150, 470):
        s += f'<circle cx="{x}" cy="200" r="110" fill="url(#kCandle)"/><path d="M{x},100 v70" stroke="{INK}" stroke-width="3"/><path d="M{x-12},170 h24 l5,34 h-34Z" fill="#ffd75a" {O1}/>'
    s += f'<path d="M56,100 q60,220 10,470 l70,0 q-30,-240 -10,-470Z M564,100 q-60,220 -10,470 l-70,0 q30,-240 10,-470Z" fill="#4b0f86" {O}/><path d="M80,110 q30,220 6,450 M540,110 q-30,220 -6,450" stroke="#2a0652" stroke-width="3" fill="none"/>'
    s += f'<rect x="50" y="560" width="520" height="34" fill="url(#gWood)" {O}/><rect x="60" y="594" width="500" height="80" fill="url(#gWoodV)" {O}/><g stroke="#2a1608" stroke-width="2">{"".join(f"<path d=\'M{x},596 v76\'/>" for x in range(110, 560, 50))}</g>'
    s += '<rect y="674" width="620" height="196" fill="#2a1810"/><g stroke="#1a0e08" stroke-width="2.5">' + "".join(f'<path d="M0,{y} h620"/>' for y in (712, 760, 816)) + '</g>'
    return s


# ------------------------------------------------------------------ props
def gal(x, y, r=14, sq=1.0, rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale(1,{sq})">{C.galleon(r)}</g>'


def gals(pts, r=14):
    return "".join(gal(p[0], p[1], p[2] if len(p) > 2 else r, p[3] if len(p) > 3 else 1.0) for p in pts)


def bunting(n, y=44, sag=34, r=16):
    x0, x1, cx, cy = 14, 606, 310, y + 2 * sag
    s = f'<path d="M{x0},{y} Q{cx},{cy} {x1},{y}" stroke="#3a2414" stroke-width="3" fill="none"/>'
    for i in range(n):
        t = (i + 1) / (n + 1)
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
        py = (1 - t) ** 2 * y + 2 * (1 - t) * t * cy + t * t * y
        s += f'<path d="M{px:.0f},{py:.0f} v10" stroke="#3a2414" stroke-width="2"/>' + gal(round(px), round(py + 10 + r), r)
    return s


def notes(pts, col="#e9d701"):
    out = ""
    for i, p in enumerate(pts):
        x, y = p[0], p[1]
        size = round((p[2] if len(p) > 2 else 52) * 1.45)
        g = "&#9835;" if i % 2 else "&#9834;"
        out += f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" stroke="{INK}" stroke-width="1.4" font-family="Georgia, serif" transform="rotate({(i*37)%30-15} {x} {y})">{g}</text>'
    return out


def q(x, y, rot=0, s=1.0):
    return f'<g transform="translate({x},{y}) rotate({rot})">{C.quill(s)}</g>'


def bigmirror(x, y, rx, ry, inner="", glass="#bfe6ff", crack=False, stand=False):
    c = uid("mc")
    s = f'<g transform="translate({x},{y})">'
    if stand:
        s += (f'<path d="M-{rx*.6:.0f},{ry+56:.0f} L0,{ry-6:.0f} L{rx*.6:.0f},{ry+56:.0f}" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/>'
              f'<path d="M-{rx*.6:.0f},{ry+56:.0f} L0,{ry-6:.0f} L{rx*.6:.0f},{ry+56:.0f}" stroke="url(#gGold)" stroke-width="8" fill="none" stroke-linecap="round"/>')
    s += (f'<ellipse rx="{rx+12}" ry="{ry+12}" fill="url(#gGold)" {O}/><ellipse rx="{rx+5}" ry="{ry+5}" fill="none" stroke="#7a6200" stroke-width="1.5"/>'
          f'<clipPath id="{c}"><ellipse rx="{rx}" ry="{ry}"/></clipPath><ellipse rx="{rx}" ry="{ry}" fill="{glass}"/><g clip-path="url(#{c})">{inner}</g><ellipse rx="{rx}" ry="{ry}" fill="none" {O1}/>'
          f'<path d="M-{rx*.6:.0f},-{ry*.3:.0f} l{rx*.5:.0f},-{ry*.45:.0f} M-{rx*.5:.0f},{ry*.05:.0f} l{rx*.6:.0f},-{ry*.55:.0f}" stroke="#fff" stroke-width="{max(2, rx*.06):.0f}" opacity=".5" stroke-linecap="round"/>'
          f'<circle cy="-{ry+12}" r="{max(4, rx*.12):.0f}" fill="#b06cff" {O1}/>')
    if crack:
        s += f'<path d="M-{rx*.2:.0f},-{ry:.0f} l{rx*.3:.0f},{ry*.6:.0f} l-{rx*.4:.0f},{ry*.4:.0f} l{rx*.5:.0f},{ry*.5:.0f} M{rx*.1:.0f},-{ry*.4:.0f} l{rx*.6:.0f},{ry*.2:.0f}" stroke="{INK}" stroke-width="3" fill="none"/>'
    return s + '</g>'


def hmirror(x, y, s=1.0, rot=0, glass="#bfe6ff"):
    return f'<g transform="translate({x},{y}) rotate({rot})">{C.mirror(s, glass)}</g>'


def mini_village(rx, ry):
    return (f'<rect x="-{rx}" y="-{ry}" width="{2*rx}" height="{2*ry}" fill="url(#kDay)"/><circle cx="{rx*.5:.0f}" cy="-{ry*.55:.0f}" r="{rx*.16:.0f}" fill="#ffe27a"/>'
            f'<path d="M-{rx},{ry*.25:.0f} Q0,{ry*.05:.0f} {rx},{ry*.25:.0f} V{ry} H-{rx}Z" fill="url(#kGrassDay)"/>'
            + scene.minihouse(-rx * .35, ry * .55, rx / 150, '#7a1fb8') + scene.minihouse(rx * .4, ry * .5, rx / 190, '#a3162c', '#ffe08a'))


def mini_city(rx, ry):
    return f'<rect x="-{rx}" y="-{ry}" width="{2*rx}" height="{2*ry}" fill="url(#kRed)"/>' + far_city(0, ry * .8, rx / 150, glow=False)


def table(x, y, w, h=110, cloth=None):
    if cloth:
        return (f'<path d="M{x-w/2:.0f},{y} h{w} l12,{h} h-{w+24}Z" fill="{cloth}" {O}/><path d="M{x-w/4:.0f},{y+6} q-6,{h/2:.0f} -10,{h-6} M{x+w/4:.0f},{y+6} q6,{h/2:.0f} 10,{h-6}" stroke="#000" stroke-opacity=".25" stroke-width="3" fill="none"/>'
                f'<rect x="{x-w/2-6:.0f}" y="{y-10}" width="{w+12}" height="14" rx="4" fill="#35096a" {O}/><path d="M{x-w/2-10:.0f},{y+h-8} h{w+20}" stroke="#e9d701" stroke-width="4"/>'
                + sp(x, y + h * .5, 1.8))
    return (f'<rect x="{x-w/2+14:.0f}" y="{y}" width="14" height="{h}" fill="url(#gWoodV)" {O}/><rect x="{x+w/2-28:.0f}" y="{y}" width="14" height="{h}" fill="url(#gWoodV)" {O}/>'
            f'<rect x="{x-w/2:.0f}" y="{y-12}" width="{w}" height="18" rx="4" fill="url(#gWood)" {O}/>')


def desk(x, y, w, h=130):
    return (f'<rect x="{x-w/2:.0f}" y="{y-20}" width="{w}" height="22" fill="url(#gWood)" {O}/><rect x="{x-w/2+18:.0f}" y="{y+2}" width="{w-36}" height="{h}" fill="url(#gWoodV)" {O}/>'
            f'<rect x="{x-60}" y="{y+30}" width="120" height="40" rx="4" fill="#5a3a22" {O1}/><circle cx="{x}" cy="{y+50}" r="5" fill="url(#gGold)" {O1}/>')


def cauldron(x, y, s=1.0, fire=True):
    f = f'<path d="M-50,80 q-8,-26 10,-40 q2,16 14,20 q-4,-24 12,-36 q6,22 16,28 q8,-10 4,-20 q18,16 12,48Z" fill="#ff8a3c" {O1}/>' if fire else ""
    return f'''<g transform="translate({x},{y}) scale({s})"><g {O1}><rect x="-90" y="60" width="180" height="14" rx="6" fill="#5a3a22" transform="rotate(6)"/><rect x="-90" y="60" width="180" height="14" rx="6" fill="#6b4426" transform="rotate(-8)"/></g>{f}
<path d="M-120,-30 Q-136,60 -60,72 L60,72 Q136,60 120,-30Z" fill="#15101c" {O}/><path d="M-104,-10 q-8,46 22,64" stroke="#3a3048" stroke-width="4" fill="none"/>
<ellipse cx="0" cy="-34" rx="128" ry="26" fill="#2a2434" {O}/><ellipse cx="0" cy="-34" rx="112" ry="19" fill="url(#kBrew)"/>
<path d="M-90,-34 C-60,-58 -10,-10 20,-34 C50,-56 80,-20 100,-36" stroke="#e9d701" stroke-width="5" fill="none"/>
<circle cx="-134" cy="-4" r="11" fill="none" stroke="#3a3048" stroke-width="5"/><circle cx="134" cy="-4" r="11" fill="none" stroke="#3a3048" stroke-width="5"/>{sp(0, 20, 2.2)}</g>'''


def shack(x, y, s=1.0, lit="#ffd75a"):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-60,0 L-56,-90 L56,-96 L60,0Z" fill="url(#gWoodV)" {O}/>'
            f'<g stroke="#2a1608" stroke-width="2"><path d="M-30,-2 l2,-90 M0,-2 v-93 M30,-2 l-2,-93"/></g>'
            f'<path d="M-76,-84 L-10,-140 L78,-92 L70,-78 L-8,-120 L-68,-70Z" fill="#6a4a3a" {O}/><rect x="-40" y="-60" width="26" height="24" fill="{lit}" {O1}/>'
            f'<path d="M8,0 v-52 q14,-12 28,0 v52Z" fill="#1a0e06" {O1}/><rect x="-52" y="-30" width="18" height="14" fill="#a3162c" stroke="{INK}" stroke-width="1" stroke-dasharray="3 2"/></g>')


def wreck(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M-10,180 L60,40 L72,46 L6,186Z" fill="#6b4426" {O}/><path d="M40,184 L210,150 L214,166 L46,198Z" fill="#5a3a22" {O}/>
<path d="M120,180 L150,30 L166,34 L138,182Z" fill="#7a5630" {O}/><path d="M30,120 L230,70 L240,96 L44,150Z" fill="#8a6038" {O} transform="rotate(14 130 110)"/>
<path d="M190,186 L250,110 L262,118 L206,190Z" fill="#5a3a22" {O}/><g fill="#4a2c16" {O1}><rect x="70" y="170" width="40" height="10" transform="rotate(-8 90 175)"/><rect x="150" y="176" width="34" height="8" transform="rotate(10 167 180)"/></g></g>'''


def crate(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-40" y="-70" width="80" height="70" fill="url(#gWoodV)" {O}/>'
            f'<path d="M-40,-70 L40,0 M40,-70 L-40,0 M-40,-56 h80 M-40,-14 h80" stroke="#2a1608" stroke-width="4"/></g>')


def barrel(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-30,0 Q-42,-45 -30,-90 L30,-90 Q42,-45 30,0Z" fill="url(#gWood)" {O}/>'
            f'<path d="M-36,-64 h72 M-37,-28 h74" stroke="#4a4a58" stroke-width="6"/><ellipse cx="0" cy="-90" rx="30" ry="8" fill="#5a3a22" {O1}/></g>')


def stall(x, y, w, c1="#6000AE", c2="#e9d701", goods=True, inside=""):
    n = max(4, int(w // 30))
    d = w / n
    st = "".join(f'<path d="M{x-w/2+i*d:.0f},{y-236} h{d:.0f} v44 q-{d/2:.0f},24 -{d:.0f},0Z" fill="{c1 if i % 2 == 0 else c2}" {O1}/>' for i in range(n))
    g = ""
    if goods:
        g = (f'<g {O1}><ellipse cx="{x-w*.3:.0f}" cy="{y-96}" rx="22" ry="11" fill="#d9a05a"/><ellipse cx="{x-w*.3+14:.0f}" cy="{y-104}" rx="20" ry="10" fill="#e0b070"/>'
             f'<circle cx="{x-10:.0f}" cy="{y-98}" r="10" fill="#d23a4a"/><circle cx="{x+8:.0f}" cy="{y-98}" r="10" fill="#d23a4a"/><circle cx="{x-1:.0f}" cy="{y-112}" r="10" fill="#e85a5a"/>'
             f'<path d="M{x+w*.26:.0f},{y-88} v-26 q8,-10 16,0 v26Z" fill="#b06cff"/><path d="M{x+w*.26+22:.0f},{y-88} v-20 q7,-8 14,0 v20Z" fill="#7de3ff"/></g>')
    return (f'<rect x="{x-w/2:.0f}" y="{y-236}" width="10" height="236" fill="url(#gWood)" {O}/><rect x="{x+w/2-10:.0f}" y="{y-236}" width="10" height="236" fill="url(#gWood)" {O}/>'
            f'<rect x="{x-w/2+10:.0f}" y="{y-190}" width="{w-20}" height="104" fill="#1c0a30" opacity=".7"/>{inside}{st}'
            f'<rect x="{x-w/2-6:.0f}" y="{y-90}" width="{w+12}" height="14" rx="3" fill="url(#gWood)" {O}/><rect x="{x-w/2:.0f}" y="{y-76}" width="{w}" height="76" fill="url(#gWoodV)" {O}/>{g}')


def heap(x, y, w, h, fake=False, seed=1):
    r = random.Random(seed)
    s = f'<path d="M{x-w/2:.0f},{y} Q{x-w/4:.0f},{y-h*1.3:.0f} {x},{y-h} Q{x+w/4:.0f},{y-h*1.25:.0f} {x+w/2:.0f},{y}Z" fill="url(#gGold)" {O}/>'
    for _ in range(int(w * h / 420)):
        px = r.uniform(-w / 2 + 16, w / 2 - 16)
        top = h * (1 - (px / (w / 2)) ** 2)
        py = r.uniform(4, max(6, top - 8))
        col = "#7a5a3a" if fake and (py < h * .28 or px < -w * .2 and py < h * .5) else "#fff3a0"
        s += f'<ellipse cx="{x+px:.0f}" cy="{y-py:.0f}" rx="11" ry="4.5" fill="{col}" stroke="#7a6200" stroke-width="1.5"/>'
    return s


def tarot(x, y, n=3, s=1.0, fan=False):
    out = ""
    for i in range(n):
        t = f'rotate({(i-(n-1)/2)*16:.0f}) translate(0,-8)' if fan else f'translate({(i-(n-1)/2)*34:.0f},0)'
        out += f'<g transform="{t}"><rect x="-13" y="-40" width="26" height="40" rx="3" fill="#4b0f86" stroke="#e9d701" stroke-width="1.6"/>{sp(0, -20, .55)}</g>'
    return f'<g transform="translate({x},{y}) scale({s})">{out}</g>'


def crystals(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})" {O1}><path d="M-4,0 l4,-30 l8,-8 l6,10 l2,28Z" fill="#b06cff"/><path d="M-14,0 l3,-16 l7,-6 l4,22Z" fill="#7de3ff"/><path d="M14,0 l4,-18 l6,2 l2,16Z" fill="#ff7eb6"/></g>'


def bread(x, y, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})" {O1}><path d="M-34,0 q-4,-22 16,-22 h10 l4,22Z" fill="#d9a05a"/><path d="M4,0 l4,-22 h10 q20,0 16,22Z" fill="#e0b070"/><path d="M-24,-14 l6,6 M16,-14 l6,6" stroke="#8a5a2a" fill="none"/></g>'


def flower_crack(x, y, s=1.0):
    pet = "".join(f'<ellipse cx="{9*math.cos(a):.1f}" cy="{-52+9*math.sin(a):.1f}" rx="7" ry="5" transform="rotate({math.degrees(a):.0f} {9*math.cos(a):.1f} {-52+9*math.sin(a):.1f})"/>' for a in [k * math.pi / 3 for k in range(6)])
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-30,4 l14,-6 l10,6 l12,-8 l16,6" stroke="#0c0306" stroke-width="3" fill="none"/>'
            f'<path d="M0,0 q-4,-26 0,-46" stroke="#3f8a4a" stroke-width="4" fill="none"/><path d="M0,-20 q-14,-4 -16,-16 q12,0 16,12Z" fill="#5fae4a" {O1}/><g fill="#ff7eb6" {O1}>{pet}</g><circle cy="-52" r="5" fill="#ffe27a" {O1}/></g>')


def lantern(x, y, s=1.0, star=True):
    inner = f'<use href="#gStarImg" transform="translate(-13,-36) scale(.26)"/>' if star else '<path d="M0,-14 q7,-12 0,-22 q-7,10 0,22Z" fill="#fff3a0"/>'
    return (f'<g transform="translate({x},{y}) scale({s})"><circle cy="-24" r="70" fill="url(#kCandle)"/><path d="M0,-66 a10,10 0 1,1 0.1,0" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-16,-46 h32 l-4,-10 h-24Z" fill="#3a2414" {O1}/><rect x="-14" y="-46" width="28" height="42" fill="#ffe9a0" {O1}/>{inner}<path d="M-18,-4 h36 v6 h-36Z" fill="#3a2414" {O1}/></g>')


def pedestal(x, y, w, h):
    return (f'<rect x="{x-w/2:.0f}" y="{y-h}" width="{w}" height="{h}" fill="url(#kStone)" {O}/><rect x="{x-w/2-10:.0f}" y="{y-h-12}" width="{w+20}" height="14" fill="#9a94a4" {O}/>'
            f'<rect x="{x-w/2-10:.0f}" y="{y-12}" width="{w+20}" height="14" fill="#6a6474" {O}/>')


def statue(x, y, k=1.0, expr="smug", ped=70, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">' + pedestal(x, y, 150 * k, ped)
            + f'<g filter="url(#fGold)">{K.place(C.lion(expr), x, y - ped - 10, 1.05 * k)}</g></g>')


def stocks(x, ytop, w, yground, h=46):
    return (f'<rect x="{x-w/2-6:.0f}" y="{ytop-20}" width="16" height="{yground-ytop+20}" fill="url(#gWoodV)" {O}/><rect x="{x+w/2-10:.0f}" y="{ytop-20}" width="16" height="{yground-ytop+20}" fill="url(#gWoodV)" {O}/>'
            f'<rect x="{x-w/2-14:.0f}" y="{ytop}" width="{w+28}" height="{h}" rx="5" fill="url(#gWood)" {O}/><path d="M{x-w/2-14:.0f},{ytop+h/2:.0f} h{w+28}" stroke="#2a1608" stroke-width="2"/>'
            f'<circle cx="{x-w*.34:.0f}" cy="{ytop+h/2:.0f}" r="11" fill="#1a0e06" {O1}/><circle cx="{x+w*.34:.0f}" cy="{ytop+h/2:.0f}" r="11" fill="#1a0e06" {O1}/>'
            f'<rect x="{x+w/2-4:.0f}" y="{ytop+h/2-9:.0f}" width="20" height="18" rx="3" fill="#4a4a58" {O1}/>')


def horse(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
<path d="M-96,-130 C-140,-120 -150,-60 -128,-20 C-120,-60 -112,-90 -84,-104Z" fill="#3a1c0e" {O}/>
<g fill="url(#gBull)" {O}><rect x="-78" y="-92" width="22" height="88" rx="6"/><rect x="-44" y="-92" width="22" height="88" rx="6"/><rect x="38" y="-92" width="22" height="88" rx="6"/><rect x="70" y="-92" width="22" height="88" rx="6"/></g>
<g fill="#1a1010" {O1}><rect x="-80" y="-12" width="26" height="14" rx="3"/><rect x="-46" y="-12" width="26" height="14" rx="3"/><rect x="36" y="-12" width="26" height="14" rx="3"/><rect x="68" y="-12" width="26" height="14" rx="3"/></g>
<ellipse cx="0" cy="-120" rx="104" ry="52" fill="url(#gBull)" {O}/>
<path d="M56,-150 Q84,-210 110,-250 L150,-236 Q132,-180 104,-120Z" fill="url(#gBull)" {O}/>
<path d="M104,-262 Q150,-280 186,-238 Q196,-218 180,-210 Q150,-206 128,-222 Q108,-236 104,-262Z" fill="url(#gBull)" {O}/>
<path d="M112,-262 L108,-292 L130,-270Z" fill="url(#gBull)" {O}/>
<path d="M60,-156 Q76,-214 106,-262 L122,-258 Q92,-210 80,-150Z" fill="#3a1c0e" {O1}/>
<circle cx="146" cy="-246" r="6" fill="#fff" {O1}/><circle cx="148" cy="-246" r="3.2" fill="{INK}"/><ellipse cx="182" cy="-222" rx="3" ry="4" fill="#3a1c0e"/>
<path d="M170,-212 q8,6 14,0" stroke="{INK}" stroke-width="2" fill="none"/><path d="M128,-224 L176,-236 M132,-262 L128,-224" stroke="#6000AE" stroke-width="4"/>
<path d="M-52,-170 Q0,-186 52,-170 L60,-104 Q0,-92 -60,-104Z" fill="url(#gPurple)" {O}/><path d="M-58,-110 Q0,-98 58,-110" stroke="#e9d701" stroke-width="5" fill="none"/>{sp(0, -138, 1.6)}</g>'''


def wreath(x, y, s=1.0):
    lv = "".join(f'<ellipse cx="{38*math.cos(a):.1f}" cy="{-26*math.sin(a):.1f}" rx="11" ry="5" transform="rotate({-math.degrees(a)+70:.0f} {38*math.cos(a):.1f} {-26*math.sin(a):.1f})"/>' for a in [math.radians(d) for d in range(0, 181, 18)])
    return f'<g transform="translate({x},{y}) scale({s})" fill="#4c9a4a" {O1}>{lv}</g>'


def arrow(x, y, rot=0, L=120):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><path d="M0,0 h{L}" stroke="#8a6038" stroke-width="5" stroke-linecap="round"/><path d="M{L},0 l-16,-9 v18Z" fill="#b9b9c4" {O1}/>'
            f'<path d="M0,0 l-12,-10 h14 l8,10 l-8,10 h-14Z" fill="#c0182e" {O1}/></g>')


def boat(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-170,-50 Q-150,26 -90,34 L96,34 Q150,24 180,-64 Q0,-30 -170,-50Z" fill="url(#gWoodV)" {O}/>'
            f'<path d="M-158,-26 Q0,-4 166,-36 M-140,4 Q0,22 146,-6" stroke="#2a1608" stroke-width="2.5" fill="none"/><path d="M-170,-50 Q0,-30 180,-64" stroke="url(#gGold)" stroke-width="5" fill="none"/></g>')


def bed(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-150" y="-150" width="20" height="150" fill="url(#gWoodV)" {O}/><path d="M-150,-150 q70,-40 140,0 v60 h-140Z" fill="url(#gWood)" {O}/>'
            f'<rect x="-140" y="-70" width="290" height="50" rx="8" fill="#efe6cf" {O}/><ellipse cx="-90" cy="-78" rx="46" ry="18" fill="#fff" {O}/>'
            f'<path d="M-40,-80 Q60,-100 150,-74 L156,-8 L-46,-8Z" fill="url(#gPurple)" {O}/><path d="M-44,-20 h198" stroke="#e9d701" stroke-width="4"/>{sp(60, -46, 1.6)}'
            f'<rect x="-146" y="-20" width="300" height="20" fill="url(#gWoodV)" {O}/><rect x="140" y="-60" width="16" height="60" fill="url(#gWoodV)" {O}/></g>')


def papers(x, y, n=5, w=70):
    r = random.Random(x * 3 + y)
    return "".join(f'<rect x="{x-w/2+r.uniform(-5, 5):.0f}" y="{y-(i+1)*6}" width="{w}" height="6" fill="{"#f6f0e2" if i % 2 else "#e8dfc8"}" stroke="{INK}" stroke-width="1"/>' for i in range(n))


def paper(x, y, w=60, h=76, rot=0, seal=None):
    s = f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h}" fill="#f6f0e2" {O1}/><g stroke="#8a7a6a" stroke-width="1.5">' + "".join(f'<path d="M{-w/2+8},{-h+12+i*10} h{w-16-(i%3)*8}"/>' for i in range(int((h - 34) / 10))) + '</g>'
    if seal == "star":
        s += f'<circle cx="{w/2-14}" cy="-14" r="10" fill="#6000AE" {O1}/>' + sp(w / 2 - 14, -14, .6)
    elif seal == "crown":
        s += f'<circle cx="{w/2-14}" cy="-14" r="10" fill="#a3162c" {O1}/><path d="M{w/2-20},-10 l-1,-8 l4,3 l3,-5 l3,5 l4,-3 l-1,8Z" fill="#14040a"/>'
    return s + '</g>'


def arcade(x, y, s=1.0, col="#3f7fd8", flip=False):
    return (f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})"><circle cx="0" cy="-150" r="120" fill="{col}" opacity=".16"/>'
            f'<path d="M-50,0 V-220 L-30,-250 H44 V0Z" fill="#1c1c2c" {O}/><rect x="-44" y="-246" width="84" height="26" fill="{col}" {O1}/>'
            f'<rect x="-38" y="-206" width="70" height="66" fill="#0a1a2a" {O1}/><g fill="{col}"><rect x="-26" y="-190" width="10" height="10"/><rect x="-6" y="-176" width="10" height="10"/><rect x="12" y="-194" width="10" height="10"/><rect x="-18" y="-160" width="30" height="6"/></g>'
            f'<path d="M-50,-130 L44,-130 L52,-104 L-50,-104Z" fill="#2c2c40" {O1}/><path d="M-20,-116 v-18" stroke="{INK}" stroke-width="4"/><circle cx="-20" cy="-136" r="6" fill="#d23a4a" {O1}/><circle cx="14" cy="-116" r="5" fill="#e9d701" {O1}/><circle cx="30" cy="-116" r="5" fill="#62ffa1" {O1}/></g>')


def slot(x, y, s=1.0, flip=False):
    return (f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})"><circle cx="0" cy="-140" r="120" fill="#e9d701" opacity=".14"/>'
            f'<path d="M-52,0 V-190 Q0,-250 52,-190 V0Z" fill="#a3162c" {O}/><path d="M-40,-196 Q0,-234 40,-196Z" fill="url(#gGold)" {O1}/>'
            f'<rect x="-42" y="-176" width="84" height="56" fill="#f6f0e2" {O1}/><path d="M-14,-176 v56 M14,-176 v56" stroke="{INK}" stroke-width="2"/>'
            f'<g font-family="Georgia, serif" font-weight="700" font-size="30" text-anchor="middle" fill="#c0182e"><text x="-28" y="-138">7</text><text x="0" y="-138">$</text><text x="28" y="-138">7</text></g>'
            f'<rect x="-40" y="-104" width="80" height="26" fill="#14040a" {O1}/><g fill="#e9d701"><circle cx="-24" cy="-91" r="5"/><circle cx="0" cy="-91" r="5"/><circle cx="24" cy="-91" r="5"/></g>'
            f'<rect x="-30" y="-60" width="60" height="16" fill="#14040a" {O1}/><path d="M52,-130 h16 v-50" stroke="{INK}" stroke-width="6" fill="none"/><circle cx="68" cy="-186" r="10" fill="#e9d701" {O1}/></g>')


def sunface(x, y, r=110):
    ry_ = "".join(f'<path d="M0,{-r*1.12:.0f} L{r*.16:.0f},{-r*(1.62 if a % 45 == 0 else 1.4):.0f} L{-r*.16:.0f},{-r*(1.62 if a % 45 == 0 else 1.4):.0f}Z" transform="rotate({a})"/>' for a in list(range(0, 360, 22))[:16])
    return f'''<g transform="translate({x},{y})"><circle r="{r*2.4:.0f}" fill="url(#gWarm)"/><g fill="#ffb53c" {O1}>{ry_}</g>
<path d="M-{r*.62:.0f},-{r*.7:.0f} L-{r*.86:.0f},-{r*1.5:.0f} L-{r*.12:.0f},-{r*.98:.0f}Z M{r*.62:.0f},-{r*.7:.0f} L{r*.86:.0f},-{r*1.5:.0f} L{r*.12:.0f},-{r*.98:.0f}Z" fill="#f59545" {O}/>
<circle r="{r}" fill="#ffc94a" {O}/><path d="M-{r*.95:.0f},{r*.1:.0f} L-{r*1.3:.0f},{r*.2:.0f} L-{r:.0f},{r*.36:.0f} L-{r*1.2:.0f},{r*.56:.0f} L-{r*.8:.0f},{r*.6:.0f} Q0,{r*1.1:.0f} {r*.8:.0f},{r*.6:.0f} L{r*1.2:.0f},{r*.56:.0f} L{r:.0f},{r*.36:.0f} L{r*1.3:.0f},{r*.2:.0f} L{r*.95:.0f},{r*.1:.0f} Q0,{r*.5:.0f} -{r*.95:.0f},{r*.1:.0f}Z" fill="#fffaf4" {O}/>
<ellipse cx="-{r*.36:.0f}" cy="-{r*.22:.0f}" rx="{r*.15:.0f}" ry="{r*.18:.0f}" fill="#fff" {O1}/><ellipse cx="-{r*.33:.0f}" cy="-{r*.2:.0f}" rx="{r*.09:.0f}" ry="{r*.11:.0f}" fill="{INK}"/>
<path d="M{r*.2:.0f},-{r*.18:.0f} Q{r*.38:.0f},-{r*.38:.0f} {r*.56:.0f},-{r*.18:.0f}" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M-{r*.56:.0f},-{r*.5:.0f} Q-{r*.36:.0f},-{r*.62:.0f} -{r*.16:.0f},-{r*.48:.0f} M{r*.16:.0f},-{r*.5:.0f} Q{r*.38:.0f},-{r*.64:.0f} {r*.6:.0f},-{r*.46:.0f}" stroke="#7a3a0e" stroke-width="6" fill="none" stroke-linecap="round"/>
<ellipse cx="0" cy="{r*.14:.0f}" rx="{r*.1:.0f}" ry="{r*.07:.0f}" fill="{INK}"/>{C.mouth("grin", 0, r*.3, r*.32)}</g>'''


def cardinal(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
<path d="M-30,-40 L-70,30 L-44,26 L-36,44 L-10,-20Z" fill="#a3162c" {O}/>
<path d="M-12,0 v-14 M12,0 v-14" stroke="#e8742e" stroke-width="6"/><path d="M-24,2 h22 M2,2 h22" stroke="#e8742e" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="0" cy="-70" rx="48" ry="62" fill="#d8202e" {O}/><ellipse cx="6" cy="-56" rx="28" ry="40" fill="#f0503c"/>
<path d="M-40,-90 Q-62,-50 -34,-14 Q-18,-50 -22,-96Z" fill="#a3162c" {O}/>
<path d="M-30,-104 Q0,-88 34,-104 L30,-84 Q0,-70 -28,-84Z" fill="#f6f1e6" {O1}/><path d="M-4,-90 l8,0 l4,60 l-8,10 l-8,-10Z" fill="url(#gGold)" {O1}/>
<path d="M-20,-164 L-10,-216 L22,-166Z" fill="#d8202e" {O}/><circle cx="6" cy="-140" r="36" fill="#d8202e" {O}/>
<path d="M12,-152 Q44,-150 40,-124 Q24,-116 8,-128Z" fill="#14040a"/><path d="M30,-142 L66,-130 L30,-120Z" fill="#f59545" {O1}/>
<circle cx="18" cy="-146" r="7" fill="#fff" {O1}/><circle cx="20" cy="-146" r="3.6" fill="{INK}"/>
<path d="M64,6 V-232" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M64,6 V-232" stroke="url(#gWood)" stroke-width="7" stroke-linecap="round"/>
<path d="M64,-10 q-16,-20 0,-40 q16,-20 0,-40 q-16,-20 0,-40 q16,-20 0,-40" stroke="#3f8a4a" stroke-width="4" fill="none"/>
<g fill="#5fae4a" {O1}><ellipse cx="50" cy="-34" rx="9" ry="5"/><ellipse cx="78" cy="-74" rx="9" ry="5"/><ellipse cx="50" cy="-114" rx="9" ry="5"/><ellipse cx="78" cy="-154" rx="9" ry="5"/></g>
<circle cx="64" cy="-262" r="46" fill="url(#halo)"/><use href="#gStarImg" transform="translate(34,-292) scale(.6)"/>
<path d="M40,-92 q14,-4 22,6 q-4,10 -16,8Z" fill="#a3162c" {O1}/></g>'''


def scales(x, y, s=1.0, tilt=10, left="", right=""):
    t = math.radians(tilt)
    ax, ay = 150 * math.cos(t), 150 * math.sin(t)

    def pan(px, py, content):
        return (f'<path d="M{px:.0f},{py:.0f} l-44,110 M{px:.0f},{py:.0f} l44,110" stroke="#7a6200" stroke-width="2.5"/>'
                f'<g transform="translate({px:.0f},{py+110:.0f})">{content}<path d="M-56,0 Q0,44 56,0Z" fill="url(#gGold)" {O}/></g>')
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,-30 V330" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M0,-30 V330" stroke="url(#gGold)" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M{-ax:.0f},{ay:.0f} L{ax:.0f},{-ay:.0f}" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M{-ax:.0f},{ay:.0f} L{ax:.0f},{-ay:.0f}" stroke="url(#gGold)" stroke-width="9" stroke-linecap="round"/>'
            + pan(-ax, ay, left) + pan(ax, -ay, right) + f'<circle r="16" fill="url(#gGold)" {O}/>' + sp(0, 0, 1) + '</g>')


def wheel(x, y, r):
    sp_ = "".join(f'<path d="M0,0 L{r*.9*math.cos(a):.0f},{r*.9*math.sin(a):.0f}" />' for a in [k * math.pi / 4 for k in range(8)])
    studs = "".join(f'<circle cx="{r*.94*math.cos(a):.0f}" cy="{r*.94*math.sin(a):.0f}" r="6" fill="#fff3a0" {O1}/>' for a in [k * math.pi / 8 for k in range(16)])
    icons = "".join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="34" fill="#1c0638" stroke="#e9d701" stroke-width="3"/>' + K.suit_icon(suit, round(px), round(py))
                    for suit, px, py in (("galleons", 0, -r * .6), ("lutes", r * .6, 0), ("quills", 0, r * .6), ("mirrors", -r * .6, 0)))
    return (f'<g transform="translate({x},{y})"><circle r="{r*1.25:.0f}" fill="url(#halo)"/><circle r="{r}" fill="url(#gGold)" {O}/><circle r="{r*.88:.0f}" fill="#3d0872" {O}/>'
            f'<g stroke="url(#gGold)" stroke-width="10">{sp_}</g>{studs}{icons}<circle r="{r*.26:.0f}" fill="#1c0638" stroke="#e9d701" stroke-width="4"/>'
            f'<use href="#gStarImg" transform="translate({-r*.2:.0f},{-r*.19:.0f}) scale({r*.4/100:.2f})"/></g>')


def garden(x, y, w, kind="veg", seed=1):
    r = random.Random(seed)
    s = f'<path d="M{x-w/2:.0f},{y} q{w/2:.0f},-26 {w:.0f},0 l8,20 h-{w+16:.0f}Z" fill="#3a2416" {O}/><g stroke="#22130c" stroke-width="2" fill="none">' + "".join(f'<path d="M{x-w/2+10:.0f},{y-4+i*7} q{w/2-10:.0f},-22 {w-20:.0f},0"/>' for i in range(3)) + '</g>'
    n = int(w // 46)
    for i in range(n):
        px = x - w / 2 + 28 + i * (w - 56) / max(1, n - 1)
        py = y - 14 + 6 * math.sin(i)
        if kind == "sprouts":
            s += f'<path d="M{px:.0f},{py:.0f} v-18" stroke="#3f8a4a" stroke-width="3"/><path d="M{px:.0f},{py-16:.0f} q-12,-10 -16,2 q8,4 16,-2 q12,-10 16,2 q-8,4 -16,-2Z" fill="#8fd06a" {O1}/>'
        elif kind == "weeds":
            s += f'<path d="M{px:.0f},{py:.0f} q-10,-20 -18,-26 M{px:.0f},{py:.0f} q2,-24 -2,-40 M{px:.0f},{py:.0f} q10,-18 20,-22 M{px-4:.0f},{py-14:.0f} l-10,2 M{px+2:.0f},{py-22:.0f} l10,-4" stroke="#4a5a2a" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
        else:
            v = i % 4
            if v == 0:
                s += f'<g {O1}><circle cx="{px:.0f}" cy="{py-12:.0f}" r="16" fill="#5fae4a"/><circle cx="{px:.0f}" cy="{py-12:.0f}" r="8" fill="#9fe08a"/></g>'
            elif v == 1:
                s += f'<path d="M{px-6:.0f},{py:.0f} l6,-14 l6,14Z" fill="#f59545" {O1}/><path d="M{px:.0f},{py-12:.0f} q-10,-20 -4,-28 M{px:.0f},{py-12:.0f} q0,-22 4,-30 M{px:.0f},{py-12:.0f} q10,-16 12,-24" stroke="#3f8a4a" stroke-width="3" fill="none"/>'
            elif v == 2:
                s += f'<g {O1}><ellipse cx="{px:.0f}" cy="{py-12:.0f}" rx="20" ry="15" fill="#f08a2c"/><path d="M{px:.0f},{py-27:.0f} v30 M{px-10:.0f},{py-24:.0f} q-4,12 0,24 M{px+10:.0f},{py-24:.0f} q4,12 0,24" fill="none"/><path d="M{px:.0f},{py-27:.0f} q2,-8 8,-8" stroke="#3f8a4a" stroke-width="3" fill="none"/></g>'
            else:
                s += f'<path d="M{px:.0f},{py:.0f} v-46" stroke="#8a6038" stroke-width="3"/><path d="M{px:.0f},{py-8:.0f} q-14,-10 -10,-26 M{px:.0f},{py-18:.0f} q12,-8 10,-22" stroke="#3f8a4a" stroke-width="3" fill="none"/><g fill="#d23a4a" {O1}><circle cx="{px-9:.0f}" cy="{py-28:.0f}" r="6"/><circle cx="{px+9:.0f}" cy="{py-36:.0f}" r="6"/></g>'
    return s


def housefrm(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-90,-150 Q-70,-210 0,-226 L0,-150Z" fill="url(#gCap)" {O}/><circle cx="-50" cy="-178" r="8" fill="#f6e9a8"/><circle cx="-22" cy="-204" r="6" fill="#f6e9a8"/>'
            f'<g stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"><path d="M-90,-150 Q0,-290 90,-150 M0,-226 V-150 M-96,-150 H96 M-60,-150 V0 M10,-150 V0 M70,-150 V0 M-60,-100 H70 M-60,-50 H70 M10,-100 L70,-50"/></g>'
            f'<g stroke="url(#gWood)" stroke-width="7" fill="none" stroke-linecap="round"><path d="M-90,-150 Q0,-290 90,-150 M0,-226 V-150 M-96,-150 H96 M-60,-150 V0 M10,-150 V0 M70,-150 V0 M-60,-100 H70 M-60,-50 H70 M10,-100 L70,-50"/></g></g>')


def ladder(x, y, h, w=26):
    return f'<g stroke="#a07a4c" stroke-width="5" stroke-linecap="round"><path d="M{x-w/2},{y} v-{h} M{x+w/2},{y} v-{h}"/>' + "".join(f'<path d="M{x-w/2},{y-i} h{w}"/>' for i in range(18, h, 26)) + '</g>'


def sack(x, y, s=1.0, col="#8a6a4a"):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-36,0 Q-48,-50 -14,-70 L14,-70 Q48,-50 36,0Z" fill="{col}" {O}/><path d="M-16,-70 q16,-22 32,0 q-16,8 -32,0Z" fill="{col}" {O}/><path d="M-16,-68 h32" stroke="#3a2414" stroke-width="5"/></g>'


def pond(x, y, rx, ry, glint="#fff3a0"):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#kWater)" {O1}/><g stroke="#bcd0ff" stroke-opacity=".5" stroke-width="2" fill="none"><path d="M{x-rx*.6:.0f},{y-ry*.2:.0f} q{rx*.2:.0f},-6 {rx*.4:.0f},0 M{x:.0f},{y+ry*.3:.0f} q{rx*.2:.0f},-6 {rx*.4:.0f},0 M{x-rx*.3:.0f},{y+ry*.5:.0f} q{rx*.1:.0f},-4 {rx*.2:.0f},0"/></g>'
            f'<ellipse cx="{x+rx*.2:.0f}" cy="{y-ry*.1:.0f}" rx="{rx*.22:.0f}" ry="{ry*.22:.0f}" fill="{glint}" opacity=".35"/>'
            f'<g fill="#3f8a4a" {O1}><ellipse cx="{x-rx*.55:.0f}" cy="{y+ry*.2:.0f}" rx="16" ry="7"/><ellipse cx="{x+rx*.6:.0f}" cy="{y+ry*.1:.0f}" rx="13" ry="6"/></g>')


def rain(seed=1, n=90, w=620, h=870, col="#e8c9c9"):
    r = random.Random(seed)
    return "".join(f'<path d="M{r.random()*w:.0f},{r.random()*h:.0f} l-6,22" stroke="{col}" stroke-opacity=".28" stroke-width="1.6"/>' for _ in range(n))


def confetti(seed=1, n=40, y1=600):
    r = random.Random(seed)
    return "".join(f'<rect x="{r.uniform(0, 620):.0f}" y="{r.uniform(0, y1):.0f}" width="8" height="5" fill="{r.choice(["#e9d701", "#b06cff", "#ff7eb6", "#fff"])}" transform="rotate({r.uniform(0, 180):.0f} {r.uniform(0, 620):.0f} {r.uniform(0, y1):.0f})"/>' for _ in range(n))


def crowd(y, n=14, seed=1, s=1.0, x0=0, x1=620):
    r = random.Random(seed)
    out = ""
    for i in range(n):
        x = x0 + (i + r.uniform(.2, .8)) * (x1 - x0) / n
        yy = y + r.uniform(-6, 6)
        c = r.choice(["#6e667e", "#8a8298", "#5a546a", "#9a92a8"])
        cl = r.choice(["#2f6b3a", "#6000AE", "#a3162c", "#7a5a3a", "#3f7fd8"])
        out += (f'<g transform="translate({x:.0f},{yy:.0f}) scale({s})"><path d="M-17,0 Q-20,-34 0,-36 Q20,-34 17,0Z" fill="{cl}" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="-11" cy="-56" r="9" fill="{c}" stroke="{INK}" stroke-width="2"/><circle cx="11" cy="-56" r="9" fill="{c}" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="-11" cy="-56" r="4.5" fill="#e8a3b8"/><circle cx="11" cy="-56" r="4.5" fill="#e8a3b8"/><ellipse cx="0" cy="-42" rx="15" ry="13" fill="{c}" stroke="{INK}" stroke-width="2"/></g>')
    return out


def pole_banner(x, y, h=150, kind="fox", s=1.0):
    b = C.fox_banner(34 * s, 70 * s) if kind == "fox" else C.leo_banner(34 * s, 70 * s)
    return f'<path d="M{x},{y} v-{h}" stroke="{INK}" stroke-width="6"/><path d="M{x},{y} v-{h}" stroke="#8a6038" stroke-width="3"/><g transform="translate({x+2},{y-h})">{b}</g>'


def cart(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">{heap(0, -50, 150, 70, seed=4)}<path d="M-90,-56 h180 l-14,50 h-152Z" fill="url(#gWoodV)" {O}/>'
            f'<path d="M-60,-56 v48 M-20,-56 v50 M20,-56 v50 M60,-56 v48" stroke="#2a1608" stroke-width="2.5"/>'
            f'<g fill="url(#gWood)" {O}><circle cx="-56" cy="0" r="24"/><circle cx="56" cy="0" r="24"/></g><g fill="#2a1608"><circle cx="-56" cy="0" r="6"/><circle cx="56" cy="0" r="6"/></g></g>')


def crown(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M-24,0 L-28,-30 L-14,-16 L0,-40 L14,-16 L28,-30 L24,0Z" fill="url(#gGold)" {O}/>'
            f'<circle cx="0" cy="-12" r="4" fill="#c0182e" {O1}/></g>')


def reynard_back(x, y, k=1.0):
    s = C.CANON_SCALE["reynard"] * k
    return f'''<ellipse cx="{x}" cy="{y+2}" rx="{70*s:.0f}" ry="{9*s:.0f}" fill="#000" opacity=".3"/><g transform="translate({x},{y}) scale({s})">
<path d="M10,-60 C70,-80 120,-40 104,10 C96,36 60,34 44,14 C66,6 60,-22 14,-36Z" fill="url(#gFox)" {O}/><path d="M104,4 C98,34 62,34 46,14 l16,2 l2,-10 l14,10 l2,-12 l12,10Z" fill="#fffaf4" {O}/>
<path d="M-28,-60 L-30,-16 L-8,-16 L-6,-60Z M6,-60 L8,-16 L30,-16 L28,-60Z" fill="#4a3a30" {O}/>
<path d="M-34,-24 h28 v24 h-34 q-2,-10 6,-12Z M6,-24 h28 l0,12 q8,2 6,12 h-34Z" fill="#2e1c10" {O}/>
<path d="M-36,-52 Q-42,-104 -24,-128 L24,-128 Q42,-104 36,-52 Q0,-44 -36,-52Z" fill="url(#gTunic)" {O}/><path d="M-36,-80 h72 v8 h-72Z" fill="#3a2414" {O}/>
<path d="M-30,-120 Q-46,-90 -40,-66" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M-30,-120 Q-46,-90 -40,-66" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<g transform="translate(58,-70) rotate(96) scale(.9)">{C.lute()}</g>
<path d="M30,-120 Q48,-96 44,-72" stroke="{INK}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M30,-120 Q48,-96 44,-72" stroke="url(#gSleeve)" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<circle cx="-40" cy="-64" r="8" fill="#e8742e" {O1}/><circle cx="44" cy="-70" r="8" fill="#e8742e" {O1}/>
<path d="M-38,-124 Q-34,-146 0,-148 Q34,-146 38,-124 Q42,-108 28,-104 Q0,-98 -28,-104 Q-42,-108 -38,-124Z" fill="url(#gRed)" {O}/>
<path d="M-24,-168 L-34,-220 L-2,-188Z M2,-188 L32,-220 L26,-168Z" fill="url(#gFox)" {O}/><path d="M-30,-204 l-4,-16 l10,10Z M28,-204 l4,-16 l-10,10Z" fill="#3a1208"/>
<path d="M-32,-158 C-34,-184 -14,-196 0,-196 C16,-196 34,-184 32,-158 Q30,-138 0,-136 Q-30,-138 -32,-158Z" fill="url(#gFox)" {O}/>
<path d="M-30,-152 l-18,4 l10,6 l-12,6 l18,2 M30,-152 l18,4 l-10,6 l12,6 l-18,2" fill="#fffaf4" {O1}/><path d="M-10,-188 q4,10 0,22 M6,-190 q4,12 0,24" stroke="#b8461a" stroke-width="2" fill="none"/></g>'''


def fg(col="#0b0416", seed=1):
    r = random.Random(seed)
    s = ""
    for x0 in list(range(-10, 96, 13)) + list(range(530, 640, 13)):
        h, lean = r.uniform(40, 130), r.uniform(-34, 34)
        s += f'<path d="M{x0},884 Q{x0+lean*.3:.0f},{872-h*.6:.0f} {x0+lean:.0f},{872-h:.0f} Q{x0+lean*.5+8:.0f},{872-h*.5:.0f} {x0+13},884Z"/>'
    return f'<g fill="{col}" opacity=".88">{s}</g>'
