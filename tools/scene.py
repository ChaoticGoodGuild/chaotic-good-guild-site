import math, random, re, os
HERE=os.path.dirname(os.path.abspath(__file__))
star=open(os.path.join(HERE,'..','src','star.b64')).read()
random.seed(7)
O='stroke="#160a22" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
O1='stroke="#160a22" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"'

def phase(cx,cy,r,p):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2c1d4d" stroke="#e9d701" stroke-opacity=".5" stroke-width="1"/>'
    if p==0: return s
    if p==.5: return s+f'<circle cx="{cx}" cy="{cy}" r="{r-1}" fill="#f6eecb"/>'
    q=p if p<.5 else 1-p
    rx=(r-1)*abs(math.cos(2*math.pi*q)); sw=0 if q<.25 else 1
    d=f'M0,{-(r-1)} A{r-1},{r-1} 0 0,1 0,{r-1} A{rx:.2f},{r-1} 0 0,{sw} 0,{-(r-1)}Z'
    fl='' if p<.5 else ' scale(-1,1)'
    return s+f'<path d="{d}" fill="#f6eecb" transform="translate({cx} {cy}){fl}"/>'

def pine(x,y,h,c1,c2):
    w=h*.42; s=f'<rect x="{x-h*.03:.1f}" y="{y-h*.12:.1f}" width="{h*.06:.1f}" height="{h*.14:.1f}" fill="#1a0d14"/>'
    for i in range(5):
        t=i/5; yy=y-h*.1-h*.9*t; ww=w*(1-t*.8); hh=h*.3
        pts=[(x-ww,yy)]
        n=6
        for k in range(1,n):
            px=x-ww+2*ww*k/n; pts.append((px,yy+(4 if k%2 else -3)*h/200))
        pts+= [(x+ww,yy),(x,yy-hh)]
        s+=f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{c1}"/>'
        s+=f'<polygon points="{x:.1f},{yy-hh:.1f} {x+ww:.1f},{yy:.1f} {x+ww*.3:.1f},{yy:.1f}" fill="{c2}" opacity=".5"/>'
    return s

def minihouse(x,y,s,cap,lit="#ffd75a"):
    return f'''<g transform="translate({x} {y}) scale({s})">
<path d="M-34,0 Q-30,-50 -24,-70 L24,-70 Q30,-50 34,0Z" fill="#bfae90"/><path d="M8,-70 L24,-70 Q30,-50 34,0 L16,0Z" fill="#000" opacity=".22"/>
<rect x="30" y="-150" width="14" height="40" fill="#5a4a52"/><rect x="27" y="-154" width="20" height="7" fill="#3a2e36"/>
<path d="M-80,-66 C-76,-130 -30,-158 0,-160 C30,-158 76,-130 80,-66 Q0,-52 -80,-66Z" fill="{cap}"/>
<path d="M-80,-66 C-76,-130 -30,-158 0,-160 C-40,-140 -56,-100 -58,-63Z" fill="#fff" opacity=".12"/>
<circle cx="-30" cy="-110" r="10" fill="#f6e9a8" opacity=".9"/><circle cx="22" cy="-128" r="8" fill="#f6e9a8" opacity=".9"/><circle cx="46" cy="-92" r="9" fill="#f6e9a8" opacity=".9"/><circle cx="-56" cy="-82" r="6" fill="#f6e9a8" opacity=".9"/>
<circle cx="-2" cy="-44" r="26" fill="url(#gWarm)"/><circle cx="-2" cy="-44" r="11" fill="{lit}" stroke="#3a2416" stroke-width="3"/><path d="M-13,-44 h22 M-2,-55 v22" stroke="#3a2416" stroke-width="2"/>
<path d="M8,0 V-22 Q8,-32 17,-32 Q26,-32 26,-22 V0Z" fill="#5a3a22" stroke="#2a1810" stroke-width="2"/></g>'''

def tufts(n,x0,x1,yf,col,h=10):
    s=''
    for i in range(n):
        x=random.uniform(x0,x1); y=yf(x)+random.uniform(-2,3); hh=h*random.uniform(.6,1.3)
        s+=f'<path d="M{x-4:.1f},{y:.1f} q1,{-hh*.7:.1f} -2,{-hh:.1f} M{x:.1f},{y:.1f} q0,{-hh:.1f} 1,{-hh*1.2:.1f} M{x+4:.1f},{y:.1f} q0,{-hh*.7:.1f} 3,{-hh*.9:.1f}"/>'
    return f'<g stroke="{col}" stroke-width="1.6" fill="none" stroke-linecap="round">{s}</g>'

def flowers(n,x0,x1,y0,y1,avoid):
    s=''; cols=['#e9d701','#b06cff','#ff7eb6','#f3ecff']
    for i in range(n):
        x=random.uniform(x0,x1); y=random.uniform(y0,y1)
        if any(a<=x<=b and c<=y<=d for a,b,c,d in avoid): continue
        c=random.choice(cols); r=random.uniform(2,3.4)
        s+=f'<path d="M{x:.1f},{y:.1f} v9" stroke="#3f7a3a" stroke-width="1.4"/>'
        for k in range(5):
            a=k*2*math.pi/5; s+=f'<circle cx="{x+math.cos(a)*r:.1f}" cy="{y+math.sin(a)*r:.1f}" r="{r*.75:.1f}" fill="{c}"/>'
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*.55:.1f}" fill="#fff6c0"/>'
    return s

def cobbles():
    s=''
    for row in range(16):
        t=row/15; y=700+t*200; half=30+t*80; cx=772+t*85-(t*t)*10
        n=3+int(t*4); w=2*half/n
        for k in range(n):
            x=cx-half+k*w+(w/2 if row%2 else 0)*.5
            sh=random.choice(['#3a2660','#44306c','#33205a','#4b3676'])
            s+=f'<ellipse cx="{x+w/2:.1f}" cy="{y:.1f}" rx="{w*.44:.1f}" ry="{5+t*4:.1f}" fill="{sh}" stroke="#1a0d2e" stroke-width="1.2"/>'
    return s

def lstring(x0,y0,x1,y1,sag,n):
    cx=(x0+x1)/2; cy=(y0+y1)/2+sag
    s=f'<path d="M{x0},{y0} Q{cx},{cy} {x1},{y1}" stroke="#2a1810" stroke-width="2" fill="none"/>'
    cols=['#e9d701','#b06cff','#ffb347']
    for i in range(1,n):
        t=i/n; x=(1-t)**2*x0+2*(1-t)*t*cx+t*t*x1; y=(1-t)**2*y0+2*(1-t)*t*cy+t*t*y1
        c=cols[i%3]
        s+=f'<circle cx="{x:.1f}" cy="{y+7:.1f}" r="13" fill="{c}" opacity=".18"/><rect x="{x-4:.1f}" y="{y+1:.1f}" width="8" height="11" rx="3" fill="{c}" stroke="#2a1810" stroke-width="1.2" class="twinkle" style="animation-delay:{i*.4:.1f}s;animation-duration:5s"/>'
    return s

def star_poly(cx,cy,r1,r2,n):
    pts=[]
    for i in range(n*2):
        a=i*math.pi/n; r=r1 if i%2==0 else r2
        pts.append(f'{cx+math.cos(a)*r:.1f},{cy+math.sin(a)*r:.1f}')
    return ' '.join(pts)

def cren(x0,x1,y,w=10,h=8):
    s='' ; x=x0
    while x<x1:
        s+=f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}"/>'; x+=w*2
    return s

DEFS=r'''
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05010c"/><stop offset=".5" stop-color="#1c0838"/><stop offset="1" stop-color="#43116a"/></linearGradient>
<linearGradient id="gGround" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d0d38"/><stop offset="1" stop-color="#0b0416"/></linearGradient>
<linearGradient id="gFox" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f59545"/><stop offset="1" stop-color="#bd4a17"/></linearGradient>
<linearGradient id="gCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6e6"/><stop offset="1" stop-color="#e3c9a6"/></linearGradient>
<linearGradient id="gCat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#aeabc0"/><stop offset="1" stop-color="#63607a"/></linearGradient>
<linearGradient id="gBadger" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8e8e9c"/><stop offset="1" stop-color="#4c4c5a"/></linearGradient>
<linearGradient id="gBull" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a6040"/><stop offset="1" stop-color="#5a301c"/></linearGradient>
<linearGradient id="gLeather" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a6234"/><stop offset="1" stop-color="#5e3618"/></linearGradient>
<linearGradient id="gWood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a6e40"/><stop offset="1" stop-color="#5a3a20"/></linearGradient>
<linearGradient id="gWoodV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6038"/><stop offset="1" stop-color="#4a2c16"/></linearGradient>
<linearGradient id="gGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff6a8"/><stop offset=".5" stop-color="#e9d701"/><stop offset="1" stop-color="#9a7c00"/></linearGradient>
<linearGradient id="gPurple" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d1fd6"/><stop offset="1" stop-color="#3d0872"/></linearGradient>
<linearGradient id="gTunic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a07c5c"/><stop offset="1" stop-color="#6a4c34"/></linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0303c"/><stop offset="1" stop-color="#9c1420"/></linearGradient>
<linearGradient id="gGreen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3f8a4a"/><stop offset="1" stop-color="#1f4a28"/></linearGradient>
<linearGradient id="gRat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b0a8c0"/><stop offset="1" stop-color="#6e667e"/></linearGradient>
<linearGradient id="gStem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2d5b6"/><stop offset=".6" stop-color="#c9ba99"/><stop offset="1" stop-color="#8e8068"/></linearGradient>
<radialGradient id="gCap" cx=".35" cy=".25" r=".9"><stop offset="0" stop-color="#9a3cf0"/><stop offset=".55" stop-color="#6000AE"/><stop offset="1" stop-color="#2e0558"/></radialGradient>
<radialGradient id="gMoon" cx=".38" cy=".35" r=".8"><stop offset="0" stop-color="#fffbe6"/><stop offset=".7" stop-color="#f1e6b8"/><stop offset="1" stop-color="#c9b98a"/></radialGradient>
<radialGradient id="gWarm"><stop offset="0" stop-color="#ffd75a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd75a" stop-opacity="0"/></radialGradient>
<radialGradient id="redGlow"><stop offset="0" stop-color="#ff3b3b" stop-opacity=".6"/><stop offset=".5" stop-color="#b3122a" stop-opacity=".24"/><stop offset="1" stop-color="#b3122a" stop-opacity="0"/></radialGradient>
<radialGradient id="ballGlow" cx=".4" cy=".35"><stop offset="0" stop-color="#fffbe0"/><stop offset=".4" stop-color="#e9d701"/><stop offset=".8" stop-color="#9a4fe6"/><stop offset="1" stop-color="#4b0f86"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#e9d701" stop-opacity=".55"/><stop offset="1" stop-color="#e9d701" stop-opacity="0"/></radialGradient>
<radialGradient id="moonGlow"><stop offset="0" stop-color="#fff6d0" stop-opacity=".38"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<pattern id="stripes" patternUnits="userSpaceOnUse" width="44" height="44"><rect width="44" height="44" fill="#6000AE"/><rect width="22" height="44" fill="#e9d701"/></pattern>
<pattern id="tent" patternUnits="userSpaceOnUse" width="40" height="40"><rect width="40" height="40" fill="#4b0f86"/><rect width="20" height="40" fill="#35096a"/></pattern>
<filter id="blur8" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="blur3"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0"/></filter>
<path id="cggStar" d="M0,-56 C5,-12 12,-5 56,0 C12,5 5,12 0,56 C-5,12 -12,5 -56,0 C-12,-5 -5,-12 0,-56Z M0,-30 C4,-6 6,-4 30,0 C6,4 4,6 0,30 C-4,6 -6,4 -30,0 C-6,-4 -4,-6 0,-30Z"/>
<path id="sparkle" d="M0,-10 C1.5,-2 2,-1.5 10,0 C2,1.5 1.5,2 0,10 C-1.5,2 -2,1.5 -10,0 C-2,-1.5 -1.5,-2 0,-10Z"/>
<g id="coin"><ellipse rx="13" ry="13" fill="url(#gGold)" stroke="#7a6200" stroke-width="1.5"/><circle r="9.5" fill="none" stroke="#7a6200" stroke-width="1"/><use href="#sparkle" fill="#7a6200" transform="scale(.75)"/></g>
<g id="rat">
<path d="M-14,-10 Q-36,-4 -32,8 Q-28,18 -46,15" stroke="#e8a3b8" stroke-width="3.2" fill="none" stroke-linecap="round"/>
<ellipse cx="-6" cy="-1" rx="7" ry="3.2" fill="#e8a3b8" stroke="#160a22" stroke-width="1.2"/><ellipse cx="9" cy="-1" rx="7" ry="3.2" fill="#e8a3b8" stroke="#160a22" stroke-width="1.2"/>
<ellipse cx="0" cy="-22" rx="16" ry="20" fill="url(#gRat)" stroke="#160a22" stroke-width="1.6"/>
<ellipse cx="3" cy="-18" rx="9" ry="12" fill="#d4cde0"/>
<circle cx="0" cy="-58" r="8" fill="url(#gRat)" stroke="#160a22" stroke-width="1.5"/><circle cx="0" cy="-58" r="4.6" fill="#e8a3b8"/>
<path d="M-4,-46 Q-2,-58 10,-58 Q22,-56 30,-46 Q32,-42 27,-41 Q14,-34 2,-36 Q-5,-38 -4,-46Z" fill="url(#gRat)" stroke="#160a22" stroke-width="1.6"/>
<circle cx="29" cy="-44.5" r="2.8" fill="#e8a3b8" stroke="#160a22" stroke-width="1"/>
<circle cx="13" cy="-49" r="3.8" fill="#fff"/><circle cx="14.2" cy="-49" r="2.2" fill="#160a22"/><circle cx="13.4" cy="-50" r=".8" fill="#fff"/>
<path d="M24,-43 l12,-4 M24,-41 l13,0 M24,-39 l11,4" stroke="#f3ecff" stroke-width=".8" opacity=".8"/>
<path d="M16,-39 q5,3 9,0" stroke="#160a22" stroke-width="1" fill="none"/>
</g>
</defs>'''

# ---------- SKY ----------
ph=''.join(phase(230+96*math.sin(i*math.pi/4), 140-96*math.cos(i*math.pi/4), 10, i/8) for i in range(8))
ticks=''.join(f'<line x1="{230+112*math.sin(a):.1f}" y1="{140-112*math.cos(a):.1f}" x2="{230+(120 if k%3==0 else 116)*math.sin(a):.1f}" y2="{140-(120 if k%3==0 else 116)*math.cos(a):.1f}"/>' for k in range(24) for a in [k*math.pi/12])

def _stars():
    r=random.Random(20241105); out=[]
    for i in range(170):
        cx=r.random()*1600; cy=r.random()*470; rad=r.random()*1.6+.4
        fill='#e9d701' if r.random()<.2 else '#f3ecff'; op=r.random()*.6+.3
        tw=r.random()<.3; d=r.random()*3.5
        cls=f' class="twinkle" style="animation-delay:{d:.2f}s"' if tw else ''
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.2f}" fill="{fill}" opacity="{op:.2f}"{cls}/>')
    return '<g>'+''.join(out)+'</g>'
STARS=_stars()
MARKERS='{MARKERS}'
SKY=f'''
<rect width="1600" height="900" fill="url(#sky)"/>
<path d="M0,250 C300,170 520,300 820,215 S1300,140 1600,235 L1600,300 C1300,215 1100,330 820,285 S300,255 0,335Z" fill="#8a2be2" opacity=".28" filter="url(#blur8)"/>
<path d="M0,330 C340,270 600,360 900,300 S1380,250 1600,310 L1600,345 C1300,300 1000,370 760,345 S260,330 0,372Z" fill="#e9d701" opacity=".08" filter="url(#blur8)"/>
{STARS}
<!-- fox constellation -->
<g stroke="#e9d701" stroke-opacity=".35" stroke-width="1.4" fill="none"><path d="M452,84 L478,128 L520,118 L548,150 L590,140 L640,170 L610,205 L560,196 L520,214 M478,128 L470,170 L520,214 M590,140 L602,96 L640,170"/><path d="M1010,70 L1052,112 L1108,96 L1150,140 L1118,186 L1064,170 L1052,112"/></g>
<g fill="#fff3a0">{''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in [(452,84,2.6),(478,128,3.2),(520,118,2.4),(548,150,2.8),(590,140,3.2),(640,170,3.6),(610,205,2.4),(560,196,2.6),(520,214,3),(470,170,2.4),(602,96,3),(1010,70,2.6),(1052,112,3.2),(1108,96,2.6),(1150,140,3),(1118,186,2.6),(1064,170,2.8)])}</g>
<path d="M980,250 l90,-34" stroke="#fff" stroke-width="1.6" opacity=".6" stroke-linecap="round"/><circle cx="980" cy="250" r="2" fill="#fff"/>
<g transform="translate(800,118)"><circle r="120" fill="url(#halo)" opacity=".8"/><g class="bigstar"><image href="data:image/png;base64,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" x="-74" y="-70" width="147" height="140"/></g></g>
<path d="M0,520 L90,430 L150,470 L250,380 L330,450 L420,410 L520,480 L640,430 L760,490 L880,440 L1000,500 L1100,470 L1600,540 L1600,620 L0,620Z" fill="#150829"/>
<path d="M250,380 L280,420 L262,416 L240,440 L232,404Z M90,430 L112,456 L96,452 L80,470Z M640,430 L668,462 L650,458 L630,476Z M880,440 L902,468 L884,464Z" fill="#3a2360" opacity=".7"/>
'''
MOON=f'''
<g class="spot" data-key="calendar" tabindex="0" role="link">
<rect class="hit" x="100" y="10" width="260" height="260" rx="130" fill="none" pointer-events="all"/>
<g class="art">
<circle cx="230" cy="140" r="150" fill="url(#moonGlow)"/>
<circle cx="230" cy="140" r="122" fill="none" stroke="#e9d701" stroke-opacity=".5" stroke-width="1.5"/>
<circle cx="230" cy="140" r="110" fill="none" stroke="#e9d701" stroke-opacity=".3" stroke-width="1"/>
<g stroke="#e9d701" stroke-opacity=".7" stroke-width="1.5">{ticks}</g>
<circle cx="230" cy="140" r="96" fill="none" stroke="#b9a8d6" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 6"/>
{ph}
<circle cx="230" cy="140" r="62" fill="url(#gMoon)"/>
<g fill="#cdbf92" opacity=".75"><circle cx="210" cy="120" r="11"/><circle cx="252" cy="158" r="15"/><circle cx="242" cy="112" r="6"/><circle cx="206" cy="162" r="6"/><circle cx="228" cy="184" r="4"/><circle cx="268" cy="126" r="4"/></g>
<g fill="none" stroke="#fffbe6" stroke-opacity=".6" stroke-width="1.5"><path d="M201,116 a11,11 0 0,1 16,-6"/><path d="M240,150 a15,15 0 0,1 22,-6"/></g>
<path d="M230,78 A62,62 0 0,1 230,202 A80,62 0 0,0 230,78Z" fill="#2c1d4d" opacity=".28"/>
<g fill="#2a1450" opacity=".85"><path d="M140,196 q30,-22 60,-6 q24,-18 52,-2 q30,-10 44,12 q-80,14 -156,-4Z"/></g>
<g fill="#5a3a8a" opacity=".5"><path d="M150,192 q26,-14 50,-2 q-24,-4 -50,2Z"/></g>
</g></g>'''

# ---------- CASTLE ----------
mane=star_poly(0,-40,19,13,13)
CASTLE=f'''
<path d="M1040,570 Q1190,440 1340,446 Q1480,452 1600,515 L1600,610 L1040,610Z" fill="#1a0820"/>
<g class="spot" data-key="quiz" tabindex="0" role="link">
<rect class="hit" x="1150" y="170" width="380" height="300" fill="none" pointer-events="all"/>
<g class="art"><g transform="translate(1340 462) scale(1.22) translate(-1340 -462)">
<ellipse cx="1340" cy="380" rx="290" ry="170" fill="url(#redGlow)"/>
<polygon points="1280,262 1180,150 1210,140" fill="#ff5a3c" opacity=".07"/><polygon points="1400,274 1500,150 1470,140" fill="#ff5a3c" opacity=".07"/>
<g fill="#3a0c18" opacity=".8"><ellipse cx="1456" cy="318" rx="22" ry="10"/><ellipse cx="1474" cy="300" rx="28" ry="12"/><ellipse cx="1500" cy="282" rx="34" ry="13"/></g>
<g fill="#24070f">
<rect x="1440" y="330" width="12" height="70"/><rect x="1460" y="344" width="10" height="56"/>
<rect x="1180" y="430" width="320" height="34"/>{cren(1180,1500,430)}
<rect x="1196" y="396" width="56" height="68"/>{cren(1196,1252,396,8,7)}
<rect x="1424" y="388" width="60" height="76"/>{cren(1424,1484,388,8,7)}
<rect x="1284" y="326" width="112" height="138"/>{cren(1284,1396,326,8,8)}
<rect x="1262" y="296" width="32" height="168"/><polygon points="1256,296 1278,246 1300,296"/>
<rect x="1386" y="306" width="32" height="158"/><polygon points="1380,306 1402,262 1424,306"/>
<rect x="1320" y="262" width="40" height="70"/><polygon points="1313,262 1340,208 1367,262"/>
</g>
<g stroke="#12030a" stroke-width="1" opacity=".8">{''.join(f'<path d="M1284,{y} h112"/>' for y in range(346,460,16))}{''.join(f'<path d="M1180,{y} h320"/>' for y in (442,454))}</g>
<g stroke="#24070f" stroke-width="1.5"><path d="M1278,246 v-20 M1402,262 v-18 M1340,208 v-24"/></g>
<g fill="#c0182e"><path d="M1278,226 l18,5 l-18,6Z"/><path d="M1402,244 l16,5 l-16,5Z"/><path d="M1340,184 l22,7 l-22,7Z"/></g>
<g fill="#ff6a3c">
<path d="M1206,412 h8 v14 h-8Z M1232,412 h8 v14 h-8Z M1436,404 h8 v14 h-8Z M1460,404 h8 v14 h-8Z M1448,428 h8 v14 h-8Z"/>
<path d="M1273,318 q5,-8 10,0 v12 h-10Z M1397,326 q5,-8 10,0 v12 h-10Z M1334,280 q6,-10 12,0 v14 h-12Z M1273,360 q5,-8 10,0 v12 h-10Z M1397,366 q5,-8 10,0 v12 h-10Z"/>
<path d="M1296,424 q6,-9 12,0 v16 h-12Z M1372,424 q6,-9 12,0 v16 h-12Z"/></g>
<path d="M1328,464 v-22 q12,-16 24,0 v22Z" fill="#0c0206"/><g stroke="#3a0c18" stroke-width="1.5"><path d="M1332,464 v-22 M1338,464 v-27 M1344,464 v-27 M1350,464 v-22 M1328,450 h24"/></g>
<rect x="1300" y="344" width="16" height="42" fill="#a3162c"/><polygon points="1300,386 1308,378 1316,386" fill="#24070f"/><rect x="1302" y="347" width="12" height="32" fill="none" stroke="#0a0406" stroke-width="1.5"/><path d="M1302,364 l-1,-8 l4,3 l3,-6 l3,6 l4,-3 l-1,8Z" fill="#0a0406"/>
<rect x="1364" y="344" width="16" height="42" fill="#a3162c"/><polygon points="1364,386 1372,378 1380,386" fill="#24070f"/><rect x="1366" y="347" width="12" height="32" fill="none" stroke="#0a0406" stroke-width="1.5"/><path d="M1366,364 l-1,-8 l4,3 l3,-6 l3,6 l4,-3 l-1,8Z" fill="#0a0406"/>
<!-- balcony -->
<path d="M1290,392 h100 v8 h-100Z" fill="#5a1626"/><g fill="#40101c">{''.join(f'<rect x="{x}" y="400" width="4" height="12"/>' for x in range(1294,1388,9))}</g><rect x="1290" y="410" width="100" height="4" fill="#5a1626"/>
<!-- LEO Lion -->
<g transform="translate(1318,392)">
<path d="M-17,0 L-14,-27 Q0,-36 14,-27 L17,0Z" fill="#8a1428" {O1}/><path d="M-4,-30 L0,0 L4,-30Z" fill="#f2ece0"/><g fill="#160a22"><circle cx="0" cy="-22" r="1"/><circle cx="0" cy="-14" r="1"/><circle cx="0" cy="-6" r="1"/></g>
<polygon points="{mane}" fill="#8a4a12" {O1}/>
<circle cx="-9" cy="-50" r="4" fill="#c98a2e" {O1}/><circle cx="9" cy="-50" r="4" fill="#c98a2e" {O1}/>
<circle cx="0" cy="-40" r="11" fill="#e3ab4c" {O1}/>
<path d="M-8,-45 l6,3 M8,-45 l-6,3" stroke="#160a22" stroke-width="1.6"/><circle cx="-4.5" cy="-41" r="1.4" fill="#160a22"/><circle cx="4.5" cy="-41" r="1.4" fill="#160a22"/>
<path d="M-2.5,-37 h5 l-2.5,3Z" fill="#5a2a12"/><path d="M-5,-32 q5,-3 10,0 q-5,5 -10,0Z" fill="#fff" {O1}/>
<polygon points="-10,-51 -11,-63 -5,-56 0,-66 5,-56 11,-63 10,-51" fill="url(#gGold)" {O1}/><circle cx="0" cy="-66" r="1.6" fill="#ff3b3b"/>
<path d="M19,-2 v-40" stroke="url(#gGold)" stroke-width="2.4"/><circle cx="19" cy="-44" r="3.4" fill="url(#gGold)" {O1}/>
</g>
<!-- Corporate Wolf -->
<g transform="translate(1364,392)">
<path d="M-15,0 L-13,-25 Q0,-33 13,-25 L15,0Z" fill="#15151c" {O1}/><path d="M-5,-29 L0,-12 L5,-29Z" fill="#f2f2f2"/><path d="M-1.6,-27 h3.2 l1.4,13 l-3,4 l-3,-4Z" fill="#c0182e"/>
<path d="M-13,-25 L-4,-12 L-5,-29Z M13,-25 L4,-12 L5,-29Z" fill="#2a2a34"/>
<polygon points="-9,-44 -10,-58 -2,-48" fill="#5c5c68" {O1}/><polygon points="7,-46 10,-58 13,-44" fill="#5c5c68" {O1}/>
<path d="M-11,-40 Q-10,-50 2,-50 Q12,-49 20,-41 Q22,-37 17,-36 Q8,-28 -4,-30 Q-11,-32 -11,-40Z" fill="#6e6e7a" {O1}/>
<path d="M2,-36 Q12,-32 18,-36 Q10,-30 0,-31Z" fill="#fff"/><path d="M4,-35 l2,3 l2,-3 l2,3 l2,-3 l2,2" stroke="#160a22" stroke-width=".7" fill="none"/>
<circle cx="19.5" cy="-40" r="2" fill="#160a22"/>
<circle cx="-3" cy="-42" r="3.6" fill="#0c1a08"/><circle cx="7" cy="-43" r="3.4" fill="#0c1a08"/>
<text x="-3" y="-39.6" font-size="6.5" font-weight="700" text-anchor="middle" fill="#e9d701" font-family="Arial, sans-serif">$</text><text x="7" y="-40.6" font-size="6.5" font-weight="700" text-anchor="middle" fill="#e9d701" font-family="Arial, sans-serif">$</text>
<path d="M22,-62 v9 m-3,-3 l3,3 l3,-3 M30,-54 v9 m-3,-3 l3,3 l3,-3 M-16,-60 v9 m-3,-3 l3,3 l3,-3" stroke="#ff3b3b" stroke-width="1.8" fill="none"/>
<g transform="translate(20,-4) scale(.3)"><use href="#coin" x="0" y="0"/><use href="#coin" x="22" y="2"/><use href="#coin" x="10" y="-16"/></g>
</g>
</g></g></g>'''

# ---------- MIDGROUND ----------
pines=''.join(pine(x,y,h,'#190b31','#2b1650') for x,y,h in [(20,600,250),(75,610,300),(128,600,220),(455,575,190),(498,580,240),(540,572,170),(1560,640,260),(1590,650,200)])
pines2=''.join(pine(x,y,h,'#22103f','#3a2266') for x,y,h in [(-5,660,260),(50,668,210),(1530,690,230),(1585,700,280)])
MID=f'''
<path d="M0,565 Q200,505 420,545 Q600,580 800,550 Q1000,518 1150,555 Q1350,595 1600,558 L1600,900 L0,900Z" fill="#190a30"/>
{pines}
{minihouse(606,560,.46,'#7a1fb8')}{minihouse(905,552,.5,'#a3162c','#ffe08a')}{minihouse(968,566,.36,'#6000AE')}{minihouse(520,588,.34,'#b8860b')}
<g opacity=".5" fill="#b9a8d6"><ellipse cx="624" cy="486" rx="6" ry="4" class="fume"/><ellipse cx="628" cy="474" rx="8" ry="5" class="fume"/><ellipse cx="924" cy="470" rx="7" ry="4" class="fume"/><ellipse cx="930" cy="458" rx="9" ry="5" class="fume"/></g>
<path d="M0,640 Q400,600 800,640 T1600,630 L1600,700 L0,700Z" fill="#8a2be2" opacity=".1" filter="url(#blur8)"/>
{pines2}
<path d="M0,706 Q300,678 600,704 Q900,734 1200,708 Q1400,690 1600,708 L1600,900 L0,900Z" fill="url(#gGround)"/>
<path d="M742,700 L802,700 Q850,790 950,900 L770,900 Q800,800 742,700Z" fill="#241340"/>
{cobbles()}
'''
gy=lambda x: 706+ (-28*math.sin(math.pi*x/1200) if x<600 else (26*math.sin(math.pi*(x-600)/1200) if x<1200 else -16*math.sin(math.pi*(x-1200)/800)))*.0 + (704 if False else 0)
GROUNDFX=tufts(150,0,1600,lambda x:712+random.uniform(0,170),'#2f1a55',9)+tufts(60,0,1600,lambda x:708,'#3b2468',11)+flowers(46,10,1590,725,880,[(520,760,700,900),(760,960,700,900),(1170,1500,700,840),(80,480,700,770)])
GROUNDFX+=''.join(f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="-4" rx="16" ry="16" fill="{c}" opacity=".18"/><rect x="-3" y="-8" width="6" height="12" rx="2" fill="#e2d5b6"/><path d="M-13,-7 q13,-20 26,0Z" fill="{c}" stroke="#160a22" stroke-width="1.4"/><circle cx="-4" cy="-12" r="1.8" fill="#fff" opacity=".8"/><circle cx="4" cy="-10" r="1.4" fill="#fff" opacity=".8"/></g>' for x,y,s,c in [(40,760,1.2,'#e9d701'),(64,772,.8,'#b06cff'),(1546,790,1.3,'#b06cff'),(1568,800,.8,'#e9d701'),(500,840,1.1,'#ff7eb6'),(1120,850,1.2,'#e9d701'),(1010,790,.8,'#b06cff'),(250,850,1,'#b06cff')])

# ---------- GUILD HALL ----------
spots=''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.86:.1f}" fill="#f6e9a8"/><ellipse cx="{x+r*.25:.1f}" cy="{y+r*.25:.1f}" rx="{r*.72:.1f}" ry="{r*.6:.1f}" fill="#d9c77e" opacity=".7"/><ellipse cx="{x-r*.3:.1f}" cy="{y-r*.3:.1f}" rx="{r*.3:.1f}" ry="{r*.2:.1f}" fill="#fff" opacity=".7"/>' for x,y,r in [(660,382,19),(762,318,24),(872,370,17),(718,430,13),(832,438,14),(908,440,10),(620,450,10),(700,330,8),(820,300,9),(930,408,7),(600,410,7)])
gills=''.join(f'<path d="M{770+ (x-770)*.25:.1f},474 L{x},{492-abs(x-770)*.03:.1f}"/>' for x in range(580,965,12))
def window(cx,cy,r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r*2.2}" fill="url(#gWarm)"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffd75a"/><path d="M{cx-r},{cy} h{2*r} M{cx},{cy-r} v{2*r}" stroke="#3a2416" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#5a3a22" stroke-width="4.5"/><circle cx="{cx}" cy="{cy}" r="{r+3}" fill="none" stroke="#2a1810" stroke-width="1.5"/><path d="M{cx-r-6},{cy+r+3} h{2*r+12} v6 h-{2*r+12}Z" fill="#5a3a22" {O1}/><g fill="#ff7eb6"><circle cx="{cx-r}" cy="{cy+r+2}" r="3.5"/><circle cx="{cx}" cy="{cy+r+1}" r="3.5"/><circle cx="{cx+r}" cy="{cy+r+2}" r="3.5"/></g><g fill="#3f7a3a"><circle cx="{cx-r/2}" cy="{cy+r+3}" r="3"/><circle cx="{cx+r/2}" cy="{cy+r+3}" r="3"/></g>'
def banner(x,y,col,emb):
    return f'<path d="M{x-2},{y} h30" stroke="#2a1810" stroke-width="3"/><path d="M{x},{y} h26 v58 l-13,-12 l-13,12Z" fill="{col}" {O1}/><path d="M{x+3},{y+3} h20 v44 l-10,-9 l-10,9Z" fill="none" stroke="#e9d701" stroke-width="1"/>{emb}'
foxemb=lambda x,y:f'<g transform="translate({x+13} {y+24})"><path d="M-8,-8 L-4,0 L0,-3 L4,0 L8,-8 L6,6 L0,12 L-6,6Z" fill="#e9d701"/><circle cx="-3" cy="3" r="1" fill="#3d0872"/><circle cx="3" cy="3" r="1" fill="#3d0872"/></g>'
staremb=lambda x,y:f'<use href="#sparkle" fill="#e9d701" transform="translate({x+13} {y+24}) scale(.9)"/>'
HALL=f'''
<ellipse cx="770" cy="704" rx="150" ry="14" fill="#000" opacity=".4"/>
<rect x="846" y="282" width="26" height="70" fill="#6a5a66" {O}/><rect x="841" y="274" width="36" height="12" fill="#4a3c46" {O}/>
<g fill="#b9a8d6" opacity=".45"><ellipse class="fume" cx="860" cy="258" rx="12" ry="8"/><ellipse class="fume" cx="870" cy="236" rx="16" ry="10" style="animation-delay:1s"/><ellipse class="fume" cx="884" cy="210" rx="20" ry="11" style="animation-delay:2s"/></g>
<path d="M676,700 Q688,570 704,474 L836,474 Q852,570 864,700Z" fill="url(#gStem)" {O}/>
<g stroke="#8e8068" stroke-width="1.2" opacity=".6" fill="none"><path d="M700,520 q4,60 -8,150 M730,500 q2,40 -2,80 M845,540 q6,70 8,140 M800,490 q3,30 2,60"/></g>
<g stroke="#5a3a22" stroke-width="7" stroke-linecap="round"><path d="M690,596 H850"/><path d="M700,500 L690,596 M840,500 L850,596"/></g>
<path d="M565,484 Q770,512 975,484 L960,496 Q770,522 580,496Z" fill="#1d0438" {O}/>
<g stroke="#4a1a7a" stroke-width="1.2">{gills}</g>
<path d="M565,484 C575,330 680,264 770,262 C860,264 965,330 975,484 Q770,510 565,484Z" fill="url(#gCap)" {O}/>
<path d="M586,470 C598,350 680,292 762,280 C700,312 642,372 626,478Z" fill="#fff" opacity=".1"/>
<path d="M975,484 C972,420 950,360 900,318 C940,380 946,440 940,490Z" fill="#000" opacity=".2"/>
{spots}
{window(726,540,16)}{window(814,540,16)}
<circle cx="770" cy="446" r="26" fill="url(#gWarm)"/><path d="M756,470 v-22 q14,-18 28,0 v22Z" fill="#ffd75a" stroke="#5a3a22" stroke-width="4"/><path d="M770,438 v32 M756,456 h28" stroke="#3a2416" stroke-width="2.5"/>
{banner(690,604,'#6000AE',foxemb(690,604))}{banner(824,604,'#6000AE',staremb(824,604))}
<path d="M708,572 h124 l-6,22 h-112Z" fill="url(#gWoodV)" {O}/><text x="770" y="589" font-family="Pirata One, Georgia, serif" font-size="15" fill="#e9d701" text-anchor="middle" textLength="92" lengthAdjust="spacingAndGlyphs">GUILD HALL</text>
<g stroke="#2f6b3a" stroke-width="2.5" fill="none"><path d="M684,700 q-6,-60 8,-100 q10,-30 4,-70"/><path d="M858,700 q8,-50 -4,-90 q-6,-30 2,-60"/></g>
<g fill="#4c9a4a">{''.join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="3.5" transform="rotate({r} {x} {y})"/>' for x,y,r in [(682,680,30),(688,650,-30),(690,620,40),(698,590,-20),(696,560,30),(862,676,-30),(858,646,30),(852,616,-40),(854,586,20)])}</g>
'''
DOOR=f'''
<g class="spot" data-key="join" tabindex="0" role="link">
<rect class="hit" x="722" y="596" width="96" height="112" fill="none" pointer-events="all"/>
<g class="art">
<ellipse cx="770" cy="650" rx="52" ry="60" fill="#e9d701" opacity=".14"/>
<path d="M732,702 V636 Q732,598 770,598 Q808,598 808,636 V702Z" fill="#7a6a7a" {O}/>
<g stroke="#4a3c4c" stroke-width="1.5" fill="none"><path d="M732,660 h8 M732,680 h8 M800,660 h8 M800,680 h8 M736,624 l7,4 M804,624 l-7,4 M752,604 l3,7 M788,604 l-3,7"/></g>
<path d="M741,702 V636 Q741,607 770,607 Q799,607 799,636 V702Z" fill="url(#gWoodV)" {O}/>
<path d="M755,612 V702 M770,608 V702 M785,612 V702" stroke="#3a2212" stroke-width="1.8"/>
<g fill="#2a2430" {O1}><path d="M741,640 h20 v5 h-20Z M741,682 h20 v5 h-20Z"/></g>
<circle cx="770" cy="632" r="11" fill="#2a1450" stroke="url(#gGold)" stroke-width="2.5"/><use href="#sparkle" fill="url(#gGold)" transform="translate(770 632) scale(.8)"/>
<circle cx="790" cy="662" r="4.5" fill="none" stroke="url(#gGold)" stroke-width="2.5"/><circle cx="790" cy="657" r="2" fill="url(#gGold)"/>
<path d="M724,702 h92 v7 h-92Z" fill="#5a4a5c" {O}/><path d="M716,709 h108 v7 h-108Z" fill="#4a3c4c" {O}/>
<g><line x1="716" y1="636" x2="716" y2="648" stroke="#2a1810" stroke-width="2"/><circle cx="716" cy="660" r="24" fill="url(#halo)"/><path d="M709,648 h14 l2,22 h-18Z" fill="#ffd75a" {O1}/><path d="M707,648 h18 l-9,-7Z" fill="#2a1810"/></g>
<g><line x1="824" y1="636" x2="824" y2="648" stroke="#2a1810" stroke-width="2"/><circle cx="824" cy="660" r="24" fill="url(#halo)"/><path d="M817,648 h14 l2,22 h-18Z" fill="#ffd75a" {O1}/><path d="M815,648 h18 l-9,-7Z" fill="#2a1810"/></g>
</g></g>'''

# ---------- MIRA ----------
fringe=''.join(f'<path d="M{x},302 v9" /><circle cx="{x}" cy="313" r="2.2" fill="#e9d701" stroke="none"/>' for x in range(20,304,12))
scallop='M-14,58 '+' '.join(f'Q{-14+i*28+14},{86 if True else 0} {-14+(i+1)*28},{66}' for i in range(12))
MIRA=f'''
<g class="spot" data-key="tarot" tabindex="0" role="link">
<rect class="hit" x="15" y="400" width="400" height="430" fill="none" pointer-events="all"/>
<g class="art"><g transform="translate(90,448)">
<ellipse cx="170" cy="318" rx="210" ry="14" fill="#000" opacity=".4"/>
<rect x="18" y="58" width="274" height="186" fill="#1c0638"/>
<g stroke="#e9d701" stroke-opacity=".35" stroke-width="1" fill="none"><path d="M40,100 l22,-14 l20,10 l16,-18 M230,92 l20,12 l18,-10 l10,16"/></g>
<g fill="#e9d701" opacity=".7">{''.join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x,y in [(40,100),(62,86),(82,96),(98,78),(230,92),(250,104),(268,94),(278,110),(150,84),(180,96)])}</g>
<path d="M18,58 Q40,150 22,244 L18,244Z M292,58 Q270,150 288,244 L292,244Z" fill="#4b0f86"/><path d="M18,58 q26,90 6,186" fill="none" stroke="#e9d701" stroke-width="1.5"/><path d="M292,58 q-26,90 -6,186" fill="none" stroke="#e9d701" stroke-width="1.5"/>
<rect x="8" y="40" width="11" height="278" fill="url(#gWood)" {O}/><rect x="291" y="40" width="11" height="278" fill="url(#gWood)" {O}/>
<path d="M-14,58 Q155,-34 324,58 L324,66 {' '.join(f'Q{324-i*26-13},{92} {324-(i+1)*26},{66}' for i in range(13))}Z" fill="url(#tent)" {O}/>
<path d="M-14,58 Q155,-34 324,58" fill="none" stroke="#e9d701" stroke-width="2.5"/>
<path d="M-14,62 Q155,-22 324,62" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="5"/>
<g fill="#e9d701">{''.join(f'<circle cx="{-14+i*26}" cy="68" r="3.2"/>' for i in range(14))}</g>
<path d="M155,10 v-22" stroke="#2a1810" stroke-width="3"/><use href="#sparkle" fill="url(#gGold)" transform="translate(155 -22) scale(1.5)"/>
<g stroke="#b9a8d6" stroke-width="1" opacity=".8"><path d="M52,66 v30 M250,66 v26 M214,60 v18"/></g>
<path d="M52,96 l-6,10 l6,14 l6,-14Z" fill="#b06cff" {O1}/><path d="M250,92 l-5,9 l5,12 l5,-12Z" fill="#7de3ff" {O1}/><path d="M214,84 a7,7 0 1,0 6,10 a5.5,5.5 0 1,1 -6,-10Z" fill="url(#gGold)" {O1}/>
<!-- Mira -->
<path d="M30,244 Q26,180 60,166 L118,166 Q150,180 146,244Z" fill="url(#gCat)" {O}/>
<path d="M46,130 L40,84 L76,110Z" fill="url(#gCat)" {O}/><path d="M130,130 L136,84 L100,110Z" fill="url(#gCat)" {O}/>
<path d="M51,121 L48,96 L67,112Z M125,121 L128,96 L109,112Z" fill="#e8a3b8"/>
<path d="M88,98 C124,98 132,122 130,142 L140,150 L130,154 L138,164 L124,166 Q106,182 88,182 Q70,182 52,166 L38,164 L46,154 L36,150 L46,142 C44,122 52,98 88,98Z" fill="url(#gCat)" {O}/>
<g stroke="#4a4760" stroke-width="2.6" fill="none"><path d="M80,112 q-2,8 2,14 M88,110 v16 M96,112 q2,8 -2,14 M50,146 l10,2 M52,156 l9,-1 M126,146 l-10,2 M124,156 l-9,-1"/></g>
<ellipse cx="88" cy="162" rx="17" ry="11" fill="#d6d3e2"/>
<ellipse cx="71" cy="142" rx="10.5" ry="11.5" fill="#e4ff7a" {O1}/><ellipse cx="71" cy="142" rx="10.5" ry="11.5" fill="url(#halo)" opacity=".5"/><ellipse cx="72" cy="142.5" rx="3" ry="9.5" fill="#160a22"/><circle cx="68" cy="137.5" r="2.4" fill="#fff"/>
<ellipse cx="105" cy="142" rx="10.5" ry="11.5" fill="#e4ff7a" {O1}/><ellipse cx="106" cy="142.5" rx="3" ry="9.5" fill="#160a22"/><circle cx="102" cy="137.5" r="2.4" fill="#fff"/>
<path d="M59,134 q10,-9 22,-3 M95,131 q12,-6 22,3" stroke="#160a22" stroke-width="2.4" fill="none"/><path d="M59,134 l-5,-4 M117,134 l5,-4" stroke="#160a22" stroke-width="1.8"/>
<path d="M83,155 h10 l-5,6Z" fill="#e8a3b8" {O1}/><path d="M88,161 q-6,8 -13,3 M88,161 q6,8 13,3" stroke="#160a22" stroke-width="1.8" fill="none"/>
<path d="M70,160 L40,154 M70,164 L42,168 M106,160 L136,154 M106,164 L134,168" stroke="#f3ecff" stroke-opacity=".8" stroke-width="1.2"/>
<!-- hat -->
<path d="M22,108 Q88,84 154,108 Q150,120 88,116 Q26,120 22,108Z" fill="#2b0a52" {O}/>
<path d="M56,104 Q68,66 78,44 Q88,14 124,-2 Q130,6 138,4 Q118,22 112,50 Q112,80 122,104 Q88,96 56,104Z" fill="url(#gPurple)" {O}/>
<path d="M78,44 q14,6 30,2 M70,66 q20,8 42,2" stroke="#2b0a52" stroke-width="2" fill="none"/>
<path d="M58,96 Q88,86 120,96 L122,105 Q88,95 56,105Z" fill="#0a0410" {O1}/><rect x="80" y="88" width="16" height="13" rx="2" fill="none" stroke="url(#gGold)" stroke-width="3"/>
<path d="M138,4 v14" stroke="#e9d701" stroke-width="1"/><use href="#sparkle" fill="url(#gGold)" transform="translate(138 24) scale(.7)"/>
<g fill="#e9d701" opacity=".8"><use href="#sparkle" transform="translate(96 60) scale(.35)"/><use href="#sparkle" transform="translate(104 30) scale(.3)"/><use href="#sparkle" transform="translate(84 76) scale(.28)"/></g>
<!-- scarf -->
<path d="M46,170 Q88,194 130,170 L134,190 Q88,214 42,190Z" fill="url(#gPurple)" {O}/>
<g stroke="#e9d701" stroke-width="3" fill="none"><path d="M45,177 Q88,201 131,177"/><path d="M43,185 Q88,209 133,185"/></g>
<path d="M108,194 L128,244 L106,240 L98,198Z" fill="url(#gPurple)" {O}/><path d="M104,214 l20,6 M106,226 l21,6" stroke="#e9d701" stroke-width="3"/>
<!-- table -->
<path d="M20,228 L300,228 L310,308 L10,308Z" fill="url(#gPurple)" {O}/>
<path d="M20,222 h280 v10 h-280Z" fill="#35096a" {O}/>
<g stroke="#2a0652" stroke-width="2" opacity=".6" fill="none"><path d="M70,232 q-4,40 -10,74 M250,232 q4,40 10,74 M160,232 v74"/></g>
<path d="M11,300 L309,300" stroke="#e9d701" stroke-width="3"/><g stroke="#e9d701" stroke-width="1.6">{fringe}</g>
<use href="#cggStar" fill="url(#gGold)" transform="translate(160 266) scale(.42)"/>
{phase(104,266,8,.25)}{phase(126,266,8,.375)}{phase(194,266,8,.625)}{phase(216,266,8,.75)}
<!-- paws -->
<path d="M112,222 q0,-12 14,-12 q14,0 14,12Z" fill="url(#gCat)" {O}/><path d="M122,222 v-6 M130,222 v-6" stroke="#160a22" stroke-width="1.2"/>
<!-- crystal ball -->
<circle cx="196" cy="178" r="62" fill="url(#halo)"/>
<path d="M172,224 q24,-14 48,0 l4,6 h-56Z" fill="url(#gGold)" {O}/><path d="M178,214 q-8,-10 -4,-22 M214,214 q8,-10 4,-22 M196,214 v-6" stroke="url(#gGold)" stroke-width="4" fill="none"/>
<circle cx="196" cy="178" r="32" fill="url(#ballGlow)" {O}/>
<path d="M176,186 q10,-18 22,-8 q10,8 20,-6" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none"/><use href="#sparkle" fill="#fff" opacity=".9" transform="translate(200 180) scale(.9)"/>
<path d="M174,164 a26,26 0 0,1 22,-14" stroke="#fff" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>
<!-- mirror -->
<g transform="translate(40,196) rotate(-12)"><rect x="-3" y="14" width="6" height="18" rx="2" fill="url(#gGold)" {O1}/><ellipse rx="15" ry="19" fill="url(#gGold)" {O}/><ellipse rx="10.5" ry="14.5" fill="#bfe6ff" {O1}/><path d="M-6,-6 l8,-6 M-4,2 l10,-8" stroke="#fff" stroke-width="2" opacity=".8"/><circle cy="-19" r="3" fill="#b06cff" {O1}/></g>
<!-- frog -->
<g transform="translate(60,220)"><ellipse cx="0" cy="2" rx="13" ry="3" fill="#b06cff"/><ellipse cx="0" cy="-6" rx="13" ry="8" fill="#58b85a" {O1}/><circle cx="-6" cy="-14" r="5" fill="#58b85a" {O1}/><circle cx="6" cy="-14" r="5" fill="#58b85a" {O1}/><circle cx="-6" cy="-14.5" r="2.8" fill="#fff"/><circle cx="6" cy="-14.5" r="2.8" fill="#fff"/><circle cx="-5.4" cy="-14" r="1.5" fill="#111"/><circle cx="6.6" cy="-14" r="1.5" fill="#111"/><path d="M-6,-5 q6,4 12,0" stroke="#1f5e22" stroke-width="1.4" fill="none"/><circle cx="-8" cy="-3" r="1.4" fill="#2f8a34"/><circle cx="8" cy="-4" r="1.2" fill="#2f8a34"/></g>
<!-- cards -->
<g transform="translate(262,206)">{''.join(f'<g transform="rotate({a}) translate(0,-6)"><rect x="-10" y="-30" width="20" height="30" rx="2.5" fill="#4b0f86" stroke="url(#gGold)" stroke-width="1.6"/><rect x="-7" y="-27" width="14" height="24" rx="1.5" fill="none" stroke="#e9d701" stroke-width=".7"/><use href="#sparkle" fill="#e9d701" transform="translate(0 -15) scale(.5)"/></g>' for a in (-34,-17,0,17,34))}</g>
<!-- candles, crystals, bottle, lamp -->
<g><circle cx="288" cy="188" r="16" fill="url(#gWarm)"/><rect x="284" y="198" width="8" height="24" fill="#f3e6c4" {O1}/><path class="twinkle" d="M288,186 q5,7 0,12 q-5,-5 0,-12Z" fill="#ffd75a" style="animation-duration:1.6s"/></g>
<g><circle cx="24" cy="196" r="14" fill="url(#gWarm)"/><rect x="21" y="204" width="7" height="18" fill="#f3e6c4" {O1}/><path class="twinkle" d="M24.5,193 q4,6 0,11 q-4,-5 0,-11Z" fill="#ffd75a" style="animation-duration:1.9s"/></g>
<g {O1}><path d="M232,222 l4,-20 l6,-6 l5,8 l1,18Z" fill="#b06cff"/><path d="M226,222 l2,-10 l5,-4 l3,14Z" fill="#7de3ff"/><path d="M244,222 l3,-12 l4,2 l1,10Z" fill="#ff7eb6"/></g>
<g transform="translate(146,214)" {O1}><path d="M-12,8 q-2,-10 12,-10 q14,0 16,6 q8,-6 10,-2 q-4,2 -8,8Z" fill="url(#gGold)"/><path d="M-12,2 q-8,-2 -6,4 q2,4 6,0" fill="none" stroke="url(#gGold)" stroke-width="2"/><circle cx="2" cy="-4" r="2" fill="url(#gGold)"/></g>
<!-- cauldron -->
<g transform="translate(8,52)">
<ellipse cx="0" cy="318" rx="50" ry="8" fill="#000" opacity=".4"/>
<g {O1}><rect x="-36" y="302" width="72" height="9" rx="4" fill="#5a3a22" transform="rotate(8 0 306)"/><rect x="-36" y="302" width="72" height="9" rx="4" fill="#6b4426" transform="rotate(-10 0 306)"/></g>
<g class="twinkle" style="animation-duration:1.4s"><path d="M-22,306 q-4,-16 6,-24 q0,10 8,12 q-2,-14 8,-22 q2,14 10,18 q4,-6 2,-12 q10,10 6,28Z" fill="#ff8a3c"/><path d="M-10,306 q-2,-10 6,-16 q2,8 8,8 q4,4 2,8Z" fill="#ffd75a"/></g>
<g class="fume"><path d="M-12,246 q-14,-22 4,-40 q14,-16 -2,-36" stroke="#b06cff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/><path d="M14,248 q14,-20 -2,-38 q-12,-16 4,-34" stroke="#e9d701" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/></g>
<path d="M-40,262 Q-48,300 -20,304 L20,304 Q48,300 40,262Z" fill="#15101c" {O}/>
<path d="M-34,270 q-4,22 12,28" stroke="#3a3048" stroke-width="3" fill="none"/>
<ellipse cx="0" cy="260" rx="42" ry="10" fill="#2a2434" {O}/><ellipse cx="0" cy="260" rx="34" ry="7" fill="#8a2be2"/>
<path d="M-30,260 q10,-5 20,0 t20,0 t20,0" stroke="#e9d701" stroke-width="2.4" fill="none"/>
<g fill="#b06cff" stroke="#e9d701" stroke-width="1"><circle cx="-14" cy="254" r="5"/><circle cx="10" cy="250" r="4"/><circle cx="22" cy="256" r="3"/></g>
<circle cx="-42" cy="276" r="5" fill="none" stroke="#3a3048" stroke-width="3"/><circle cx="42" cy="276" r="5" fill="none" stroke="#3a3048" stroke-width="3"/>
<use href="#sparkle" fill="#e9d701" opacity=".5" transform="translate(0 284) scale(.9)"/>
</g>
</g></g></g>'''

# ---------- NOTICE BOARD ----------
BOARD=f'''
<g class="spot" data-key="board" tabindex="0" role="link">
<rect class="hit" x="380" y="515" width="215" height="205" fill="none" pointer-events="all"/>
<g class="art" ><g transform="translate(-44,0)">
<ellipse cx="540" cy="712" rx="110" ry="9" fill="#000" opacity=".4"/>
<rect x="516" y="556" width="10" height="154" fill="url(#gWood)" {O}/><rect x="598" y="556" width="10" height="154" fill="url(#gWood)" {O}/>
<rect x="504" y="562" width="116" height="88" fill="#8a5a32" {O}/><rect x="510" y="568" width="104" height="76" fill="#b08a5a" stroke="#5a3a22" stroke-width="1.5"/>
<path d="M490,562 L562,522 L634,562 L626,570 L562,536 L498,570Z" fill="#6000AE" {O}/>
<g stroke="#3d0872" stroke-width="1.5">{''.join(f'<path d="M{562-d},{536+d*.48:.0f} l-6,-9 M{562+d},{536+d*.48:.0f} l6,-9"/>' for d in range(10,64,11))}</g>
<path d="M528,548 h68 v14 h-68Z" fill="url(#gWoodV)" {O1}/><text x="562" y="559.5" font-family="Pirata One, Georgia, serif" font-size="12" fill="#e9d701" text-anchor="middle" textLength="54" lengthAdjust="spacingAndGlyphs">NOTICES</text>
<g {O1}><rect x="514" y="573" width="28" height="24" fill="#f3e6c4" transform="rotate(-5 528 585)"/><rect x="548" y="571" width="26" height="32" fill="#e9d701" transform="rotate(3 561 587)"/><rect x="580" y="574" width="28" height="26" fill="#d7c6ff" transform="rotate(-2 594 587)"/><rect x="518" y="604" width="32" height="30" fill="#f3e6c4" transform="rotate(4 534 619)"/><rect x="558" y="610" width="46" height="26" fill="#ffd1dc" transform="rotate(-3 581 623)"/></g>
<use href="#sparkle" fill="#6000AE" transform="translate(561 586) scale(.8)"/>
<path d="M526,612 l8,10 l8,-12 l6,12" stroke="#a3162c" stroke-width="1.6" fill="none"/>
<g stroke="#6b5a70" stroke-width="1.1"><path d="M518,581 h18 M518,586 h14 M518,591 h16 M584,582 h20 M584,587 h14 M584,592 h18 M564,618 h34 M564,623 h26 M564,628 h30 M524,628 h20"/></g>
<g fill="#d23a4a" {O1}><circle cx="528" cy="575" r="2.6"/><circle cx="561" cy="573" r="2.6"/><circle cx="594" cy="576" r="2.6"/><circle cx="534" cy="606" r="2.6"/><circle cx="581" cy="612" r="2.6"/></g>
<g><line x1="608" y1="580" x2="628" y2="580" stroke="#2a1810" stroke-width="3"/><circle cx="626" cy="596" r="20" fill="url(#halo)"/><path d="M620,584 h12 l2,20 h-16Z" fill="#ffd75a" {O1}/></g>
<!-- scribe rat with quill -->
<g transform="translate(452,712) scale(1.15)"><use href="#rat"/><path d="M-15,-34 Q0,-42 14,-34 L16,-8 Q0,-2 -16,-8Z" fill="url(#gPurple)" {O1}/><path d="M-4,-36 l6,6 l6,-6" stroke="#e9d701" stroke-width="1.6" fill="none"/>
<path d="M-8,-60 Q4,-74 20,-62 Q8,-58 -8,-60Z" fill="#6000AE" {O1}/><circle cx="6" cy="-70" r="3" fill="#6000AE" {O1}/>
<path d="M14,-26 q10,-2 14,-8" stroke="url(#gRat)" stroke-width="5" stroke-linecap="round" fill="none"/>
<path d="M28,-34 L46,-70 Q52,-62 44,-50 Q40,-40 30,-32Z" fill="#f3ecff" {O1}/><path d="M28,-34 L44,-66" stroke="#b9a8d6" stroke-width="1"/><path d="M27,-33 l-2,5" stroke="#160a22" stroke-width="1.6"/>
<path d="M18,-22 h16 v14 h-16Z" fill="#f3e6c4" {O1} transform="rotate(-10 26 -15)"/></g>
<!-- hooded rat with satchel -->
<g transform="translate(508,708) rotate(-5)"><use href="#rat"/><path d="M-15,-34 Q0,-42 14,-34 L15,-10 Q0,-4 -16,-10Z" fill="url(#gGreen)" {O1}/><path d="M-12,-36 L12,-8" stroke="#5a3a22" stroke-width="2.5"/><rect x="6" y="-14" width="12" height="10" rx="2" fill="url(#gLeather)" {O1}/>
<path d="M-8,-58 L24,-62 L6,-76Z" fill="url(#gGreen)" {O1}/><path d="M4,-72 q-8,-14 -2,-20" stroke="#d23a4a" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>
<!-- small rat in patched cloak, pointing up -->
<g transform="translate(636,714) scale(-.78,.78)"><use href="#rat"/><path d="M-16,-36 Q0,-44 12,-36 L16,-4 Q0,2 -18,-4Z" fill="#7a5a3a" {O1}/><rect x="-8" y="-20" width="8" height="8" fill="#a3162c" stroke="#160a22" stroke-width=".8" stroke-dasharray="2 1"/><path d="M12,-28 q10,-8 12,-18" stroke="url(#gRat)" stroke-width="4.5" stroke-linecap="round" fill="none"/></g>
</g></g></g>'''

# ---------- BULL ----------
shingles=''.join(f'<path d="M{1012+i*12+ (6 if r%2 else 0)},{560-r*13} q6,10 12,0" />' for r in range(4) for i in range(0, max(1,6-r)))
BULL=f'''
<g class="spot" data-key="about" tabindex="0" role="link">
<rect class="hit" x="925" y="470" width="270" height="245" fill="none" pointer-events="all"/>
<g class="art">
<ellipse cx="1070" cy="710" rx="140" ry="10" fill="#000" opacity=".4"/>
<!-- frame house -->
<path d="M1006,572 Q1026,512 1084,498 L1084,572Z" fill="url(#gCap)" {O}/><g stroke="#2e0558" stroke-width="1.4" fill="none">{shingles}</g>
<circle cx="1040" cy="548" r="6" fill="#f6e9a8"/><circle cx="1064" cy="524" r="5" fill="#f6e9a8"/>
<g stroke="url(#gWood)" stroke-width="7" fill="none" stroke-linecap="round"><path d="M1006,572 Q1084,452 1160,572"/><path d="M1084,498 V572 M1084,498 L1122,572 M1002,572 H1164"/><path d="M1052,572 V704 M1112,572 V704 M1154,572 V704 M1052,612 H1154 M1052,656 H1154 M1112,612 L1154,656"/></g>
<g stroke="#160a22" stroke-width="1" fill="none" opacity=".6"><path d="M1006,576 H1164 M1056,572 V704 M1116,572 V704"/></g>
<g fill="#b9b9c4">{''.join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x,y in [(1052,572),(1112,572),(1154,572),(1052,612),(1112,612),(1154,612),(1052,656),(1154,656),(1084,572)])}</g>
<g stroke="#a07a4c" stroke-width="3.5"><path d="M1172,560 V706 M1192,560 V706"/>{''.join(f'<path d="M1172,{y} H1192"/>' for y in range(578,700,22))}</g>
<g {O1}><rect x="1086" y="694" width="70" height="8" fill="#a07a4c"/><rect x="1092" y="686" width="60" height="8" fill="#8a6038"/><rect x="1098" y="678" width="52" height="8" fill="#b08a5a"/></g>
<g transform="translate(1136,706)" {O1}><path d="M-10,0 l2,-14 h16 l2,14Z" fill="#6a6a74"/><path d="M-8,-14 q8,-12 16,0" fill="none"/><g stroke="#b9b9c4" stroke-width="1.5"><path d="M-3,-14 v-6 M2,-14 v-8 M6,-14 v-5"/></g></g>
<path d="M940,704 h34 l-4,-22 h-26Z" fill="#f3e6c4" {O1} transform="rotate(-6 957 693)"/><g stroke="#3b5f8a" stroke-width="1" fill="none" transform="rotate(-6 957 693)"><path d="M948,698 v-10 l8,-6 l8,6 v10Z M954,698 v-5 h4 v5"/></g>
<!-- bull -->
<path d="M966,640 q-14,10 -8,30 q2,8 -4,10" stroke="#5a301c" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M950,676 q4,8 10,4 q-2,-6 -6,-8Z" fill="#2a1810"/>
<path d="M972,640 h20 v54 h-20Z M1004,640 h20 v54 h-20Z" fill="#4a3a30" {O}/>
<path d="M968,690 h26 v12 h-28Z M1000,690 h26 l2,12 h-28Z" fill="#1a1010" {O}/>
<path d="M952,612 Q950,566 998,562 Q1046,566 1044,612 Q1044,660 998,662 Q952,660 952,612Z" fill="url(#gBull)" {O}/>
<path d="M962,596 L1034,596 L1032,660 Q998,676 964,660Z" fill="url(#gLeather)" {O}/>
<path d="M970,596 L980,570 M1026,596 L1016,570" stroke="#5e3618" stroke-width="6"/>
<g stroke="#e9d701" stroke-width="1" stroke-dasharray="3 3" fill="none"><path d="M966,602 h64 M968,656 q30,12 60,0"/></g>
<rect x="984" y="614" width="28" height="18" rx="2" fill="#5e3618" {O1}/><path d="M990,614 v-8 M998,614 v-10 M1006,614 v-7" stroke="#b9b9c4" stroke-width="2"/>
<use href="#sparkle" fill="#e9d701" transform="translate(998 646) scale(.6)"/>
<path d="M960,588 Q944,612 952,640" stroke="url(#gBull)" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M960,588 Q944,612 952,640" stroke="#160a22" stroke-width="22" fill="none" stroke-linecap="round" opacity="0"/>
<circle cx="952" cy="642" r="10" fill="#5a301c" {O1}/>
<path d="M1034,584 Q1054,572 1062,552" stroke="url(#gBull)" stroke-width="18" fill="none" stroke-linecap="round"/>
<path d="M1028,578 q8,-2 14,-8" stroke="#f2ece0" stroke-width="18" fill="none" stroke-linecap="round" opacity=".0"/>
<line x1="1064" y1="560" x2="1072" y2="508" stroke="url(#gWood)" stroke-width="7" stroke-linecap="round"/><line x1="1064" y1="560" x2="1072" y2="508" stroke="#160a22" stroke-width="1" opacity=".5"/>
<path d="M1054,494 h34 v16 h-34Z" fill="#7a7a86" {O} transform="rotate(-8 1071 502)"/><path d="M1056,497 h30" stroke="#b9b9c4" stroke-width="2" transform="rotate(-8 1071 502)"/>
<circle cx="1063" cy="556" r="10" fill="#5a301c" {O1}/>
<!-- head -->
<path d="M984,532 Q956,512 962,486 Q966,478 972,486 Q974,508 998,520Z" fill="url(#gCream)" {O}/><path d="M1038,530 Q1066,510 1060,484 Q1056,476 1050,484 Q1048,506 1024,518Z" fill="url(#gCream)" {O}/>
<path d="M966,492 q4,12 16,22 M1056,490 q-4,12 -16,22" stroke="#c9b08a" stroke-width="1.5" fill="none"/>
<ellipse cx="974" cy="542" rx="12" ry="7" fill="url(#gBull)" {O} transform="rotate(-24 974 542)"/><ellipse cx="1048" cy="540" rx="12" ry="7" fill="url(#gBull)" {O} transform="rotate(24 1048 540)"/>
<path d="M980,546 Q980,516 1011,514 Q1042,516 1042,546 Q1042,566 1011,578 Q980,566 980,546Z" fill="url(#gBull)" {O}/>
<path d="M996,522 q4,-12 10,-2 q4,-12 10,0 q6,-8 8,4 q-16,6 -28,-2Z" fill="#3a1c0e" {O1}/>
<path d="M990,566 Q990,552 1012,552 Q1036,552 1036,566 Q1036,582 1012,582 Q990,582 990,566Z" fill="#e0aa86" {O}/>
<ellipse cx="1004" cy="566" rx="3.4" ry="4.4" fill="#5a3420"/><ellipse cx="1022" cy="566" rx="3.4" ry="4.4" fill="#5a3420"/>
<path d="M1004,574 q9,10 18,0" stroke="url(#gGold)" stroke-width="3.4" fill="none" stroke-linecap="round"/>
<ellipse cx="999" cy="540" rx="6.5" ry="7" fill="#fff" {O1}/><circle cx="1001" cy="541" r="3.6" fill="#2a1408"/><circle cx="999.6" cy="539.4" r="1.2" fill="#fff"/>
<ellipse cx="1024" cy="540" rx="6.5" ry="7" fill="#fff" {O1}/><circle cx="1026" cy="541" r="3.6" fill="#2a1408"/><circle cx="1024.6" cy="539.4" r="1.2" fill="#fff"/>
<path d="M990,530 L1006,533 M1034,530 L1018,533" stroke="#2a1408" stroke-width="3.4" stroke-linecap="round"/>
</g></g>'''

# ---------- BADGER MARKET ----------
aw=''.join(f'<path d="M{1168+i*28},606 q14,22 28,0Z" fill="{"#6000AE" if i%2==0 else "#e9d701"}" {O1}/>' for i in range(12))
herbs=''.join(f'<g transform="translate({x},606)"><path d="M0,0 v10" stroke="#2a1810" stroke-width="1.5"/><path d="M0,10 q-9,10 -6,24 q6,-4 6,-12 q0,8 6,12 q3,-14 -6,-24Z" fill="{c}" {O1}/><path d="M-3,12 h6" stroke="#a3162c" stroke-width="2"/></g>' for x,c in [(1226,'#5fae4a'),(1250,'#8a6fd0'),(1420,'#5fae4a'),(1446,'#c9a24a')])
MARKET=f'''
<g class="spot" data-key="shop" tabindex="0" role="link">
<rect class="hit" x="1160" y="510" width="400" height="330" fill="none" pointer-events="all"/>
<g class="art">
<ellipse cx="1350" cy="830" rx="210" ry="12" fill="#000" opacity=".4"/>
<rect x="1193" y="572" width="12" height="256" fill="url(#gWood)" {O}/><rect x="1465" y="572" width="12" height="256" fill="url(#gWood)" {O}/>
<rect x="1205" y="610" width="260" height="130" fill="#1c0a30"/>
<g {O1}><rect x="1214" y="640" width="64" height="6" fill="#8a6038"/><rect x="1392" y="640" width="64" height="6" fill="#8a6038"/><path d="M1220,640 v-18 q6,-8 12,0 v18Z" fill="#b06cff"/><path d="M1240,640 v-14 h12 v14Z" fill="#7de3ff"/><path d="M1258,640 v-20 q6,-6 12,0 v20Z" fill="#ff7eb6"/><rect x="1398" y="620" width="16" height="20" fill="#4b0f86" stroke="#e9d701"/><rect x="1418" y="624" width="16" height="16" fill="#a3162c"/><rect x="1438" y="618" width="14" height="22" fill="#4b0f86" stroke="#e9d701"/></g>
{herbs}
<!-- badger -->
<path d="M1276,748 Q1270,690 1300,676 L1370,676 Q1400,690 1394,748Z" fill="url(#gBadger)" {O}/>
<path d="M1284,700 Q1335,668 1386,700 L1382,748 L1288,748Z" fill="url(#gLeather)" {O}/>
<path d="M1276,696 q-2,-20 22,-22 q8,10 0,24 q-12,6 -22,-2Z M1394,696 q2,-20 -22,-22 q-8,10 0,24 q12,6 22,-2Z" fill="url(#gLeather)" {O}/>
<g stroke="#e9d701" stroke-width="1" stroke-dasharray="3 3" fill="none"><path d="M1290,704 Q1335,676 1380,704 M1282,692 q8,-8 14,-10 M1388,692 q-8,-8 -14,-10"/></g>
<path d="M1302,686 L1314,748 M1368,686 L1356,748" stroke="#4a2c18" stroke-width="5"/>
<g fill="url(#gGold)" {O1}><circle cx="1305" cy="702" r="3"/><circle cx="1309" cy="722" r="3"/><circle cx="1365" cy="702" r="3"/><circle cx="1361" cy="722" r="3"/></g>
<path d="M1320,704 h30 v26 q-15,8 -30,0Z" fill="url(#gGreen)" {O}/><path d="M1320,704 h30 l-15,10Z" fill="#2f6b3a" {O1}/><path d="M1335,726 Q1326,718 1330,710 Q1340,714 1335,726Z" fill="#b8e88a"/>
<g {O1}><path d="M1326,704 q-4,-12 2,-16 q4,6 2,16 M1338,704 q0,-14 6,-16 q2,8 -2,16" fill="#5fae4a"/></g>
<circle cx="1302" cy="616" r="11" fill="#1b1b22" {O}/><circle cx="1368" cy="616" r="11" fill="#1b1b22" {O}/><circle cx="1302" cy="616" r="5" fill="#8e8e9c"/><circle cx="1368" cy="616" r="5" fill="#8e8e9c"/>
<path d="M1335,610 C1372,610 1378,634 1376,650 L1384,658 L1374,662 Q1362,686 1335,688 Q1308,686 1296,662 L1286,658 L1294,650 C1292,634 1298,610 1335,610Z" fill="#f4f1f7" {O}/>
<path d="M1304,618 Q1318,608 1328,618 L1331,664 Q1322,676 1314,666 Q1300,642 1304,618Z" fill="#1b1b22" {O1}/><path d="M1366,618 Q1352,608 1342,618 L1339,664 Q1348,676 1356,666 Q1370,642 1366,618Z" fill="#1b1b22" {O1}/>
<ellipse cx="1318" cy="640" rx="6" ry="7" fill="#fff"/><circle cx="1319.5" cy="641" r="3.6" fill="#3a2408"/><circle cx="1318" cy="639.4" r="1.2" fill="#fff"/>
<ellipse cx="1352" cy="640" rx="6" ry="7" fill="#fff"/><circle cx="1353.5" cy="641" r="3.6" fill="#3a2408"/><circle cx="1352" cy="639.4" r="1.2" fill="#fff"/>
<path d="M1310,630 q8,-5 16,0 M1344,630 q8,-5 16,0" stroke="#f4f1f7" stroke-width="1.4" fill="none" opacity=".5"/>
<ellipse cx="1335" cy="669" rx="8.5" ry="6" fill="#1b1b22"/><ellipse cx="1333" cy="667" rx="3" ry="1.6" fill="#fff" opacity=".5"/>
<path d="M1322,679 Q1335,692 1348,679" stroke="#1b1b22" stroke-width="2.4" fill="none" stroke-linecap="round"/>
<g {O1}><g fill="#ff7eb6">{''.join(f'<ellipse cx="{1380+9*math.cos(a):.1f}" cy="{613+9*math.sin(a):.1f}" rx="7" ry="5" transform="rotate({math.degrees(a):.0f} {1380+9*math.cos(a):.1f} {613+9*math.sin(a):.1f})"/>' for a in [k*2*math.pi/6 for k in range(6)])}</g><circle cx="1380" cy="613" r="5" fill="url(#gGold)"/></g><path d="M1370,622 q-8,6 -6,14 q8,-4 6,-14Z" fill="#5fae4a" {O1}/>
<!-- awning -->
<path d="M1176,566 L1494,566 L1504,606 L1166,606Z" fill="url(#stripes)" {O}/><path d="M1176,566 L1494,566 L1497,578 L1173,578Z" fill="#000" opacity=".18"/>
{aw}
<path d="M1262,534 v-10 M1408,534 v-10" stroke="#2a1810" stroke-width="2.5"/>
<path d="M1246,534 h178 l-6,30 h-166Z" fill="url(#gWoodV)" {O}/><text x="1335" y="556" font-family="Pirata One, Georgia, serif" font-size="18" fill="#e9d701" text-anchor="middle" textLength="150" lengthAdjust="spacingAndGlyphs">GALLEON MARKET</text>
<!-- counter -->
<rect x="1198" y="746" width="274" height="84" fill="url(#gWoodV)" {O}/><rect x="1190" y="736" width="290" height="14" rx="3" fill="url(#gWood)" {O}/>
<g stroke="#2a1810" stroke-width="1.6"><path d="M1244,750 V830 M1290,750 V830 M1380,750 V830 M1426,750 V830"/></g>
<g stroke="#3a2212" stroke-width="1" fill="none" opacity=".7"><path d="M1210,770 q10,-6 22,0 M1300,790 q20,8 40,0 M1392,772 q10,6 24,0 M1436,804 q12,-6 26,0"/></g>
<path d="M1310,760 h50 l-6,56 l-19,-10 l-19,10Z" fill="url(#gPurple)" {O}/><use href="#sparkle" fill="url(#gGold)" transform="translate(1335 782) scale(1.3)"/>
<!-- goods -->
<g transform="translate(1224,728)"><use href="#coin" transform="translate(0,0) scale(1,.4)"/><use href="#coin" transform="translate(0,-6) scale(1,.4)"/><use href="#coin" transform="translate(0,-12) scale(1,.4)"/><use href="#coin" transform="translate(0,-18) scale(1,.4)"/><use href="#coin" transform="translate(24,2) scale(1,.4)"/><use href="#coin" transform="translate(24,-4) scale(1,.4)"/><use href="#coin" transform="translate(13,-34) scale(.9)"/></g>
<g {O1}><path d="M1268,736 h36 l-4,-22 h-28Z" fill="#a07a4c"/><path d="M1276,714 q-8,-22 6,-28 q2,14 0,28 M1288,714 q2,-24 12,-26 q-2,14 -6,26" fill="#5fae4a"/></g>
<g {O1}><path d="M1372,736 v-18 h30 v18Z" fill="url(#gPurple)"/><path d="M1376,718 v-6 h22 v6" fill="#35096a"/><path d="M1372,724 h30" stroke="#e9d701"/></g><use href="#sparkle" fill="#e9d701" transform="translate(1387 730) scale(.4)"/>
<g {O1}><rect x="1414" y="706" width="20" height="30" rx="2" fill="#4b0f86" stroke="#e9d701" transform="rotate(-8 1424 721)"/><rect x="1432" y="706" width="20" height="30" rx="2" fill="#4b0f86" stroke="#e9d701" transform="rotate(6 1442 721)"/></g>
<path d="M1396,744 q0,-12 12,-12 q12,0 12,12Z" fill="url(#gBadger)" {O}/>
<!-- garden -->
<g transform="translate(1500,790)">
<path d="M-10,34 q40,-14 90,0 l4,10 h-98Z" fill="#2a1810" {O1}/>
<g {O1}><g fill="#5fae4a"><circle cx="6" cy="24" r="9"/><circle cx="30" cy="20" r="10"/><circle cx="56" cy="24" r="9"/></g><g fill="#8fd06a"><circle cx="6" cy="23" r="4"/><circle cx="30" cy="19" r="5"/><circle cx="56" cy="23" r="4"/></g></g>
<g stroke="url(#gWood)" stroke-width="5" stroke-linecap="round"><path d="M-14,44 v-26 M12,46 v-24 M38,46 v-24 M64,46 v-24 M88,44 v-26 M-16,30 H90"/></g>
</g>
</g></g>'''

# ---------- REYNARD ----------
REY=f'''
<g class="spot" data-key="stories" tabindex="0" role="link">
<rect class="hit" x="545" y="590" width="200" height="300" fill="none" pointer-events="all"/>
<g class="art"><g transform="translate(664,800) scale(1.12)">
<ellipse cx="0" cy="76" rx="110" ry="11" fill="#000" opacity=".45"/>
<path d="M-56,0 L-64,70 Q-80,72 -88,80 L-50,78 L50,78 L88,80 Q80,72 64,70 L56,0Z" fill="url(#gWoodV)" {O}/>
<g stroke="#2a1608" stroke-width="1.6" fill="none"><path d="M-40,12 q-4,30 -8,56 M-14,14 q2,30 -2,58 M16,14 q4,28 2,58 M40,12 q6,30 8,56"/></g>
<path d="M-60,40 q10,-8 22,-2 q-2,10 -22,8Z M30,56 q12,-8 26,0 q-8,8 -26,6Z" fill="#3f8a4a" opacity=".8"/>
<ellipse cx="0" cy="0" rx="56" ry="13" fill="#b08a5a" {O}/><ellipse cx="0" cy="0" rx="38" ry="8" fill="none" stroke="#7a5630" stroke-width="1.6"/><ellipse cx="0" cy="0" rx="20" ry="4" fill="none" stroke="#7a5630" stroke-width="1.6"/>
<g transform="translate(70,74)"><rect x="-2.5" y="-10" width="5" height="10" fill="#e2d5b6" {O1}/><path d="M-11,-9 q11,-16 22,0Z" fill="#d23a4a" {O1}/><circle cx="-3" cy="-13" r="1.5" fill="#fff"/><circle cx="4" cy="-12" r="1.2" fill="#fff"/></g>
<!-- tail -->
<path d="M-26,-12 C-70,-34 -122,-10 -116,38 C-112,72 -72,78 -44,58 C-68,42 -64,16 -28,8Z" fill="url(#gFox)" {O}/>
<path d="M-117,30 l12,6 l-2,-12 l12,10 l0,-12 l12,14 l4,-10 l8,16 l8,-4 l4,16 l8,2 l7,14 C-72,78 -112,72 -117,30Z" fill="#fffaf4" {O}/>
<g stroke="#9a3a12" stroke-width="1.6" fill="none" opacity=".7"><path d="M-60,-14 q-20,2 -32,14 M-70,-2 q-16,6 -22,20 M-52,4 q-12,8 -12,22"/></g>
<!-- legs: dark trousers and boots -->
<path d="M-26,-6 L-30,38 L-10,38 L-8,-6Z M8,-6 L10,38 L30,38 L26,-6Z" fill="#4a3a30" {O}/>
<path d="M-34,30 L-8,30 L-6,54 L-40,54 Q-42,46 -34,44Z M8,30 L33,30 L34,44 Q44,46 42,54 L6,54Z" fill="#2e1c10" {O}/>
<path d="M-36,28 h30 v9 h-30Z M6,28 h30 v9 h-30Z" fill="url(#gLeather)" {O}/>
<!-- brown sleeveless tunic -->
<path d="M-35,4 Q-42,-50 -24,-74 L24,-74 Q42,-50 35,4 Q0,12 -35,4Z" fill="url(#gTunic)" {O}/>
<path d="M24,-74 Q42,-50 35,4 Q30,6 24,7 Q30,-40 16,-72Z" fill="#000" opacity=".2"/>
<g stroke="#4a3424" stroke-width="1.4" fill="none" opacity=".8"><path d="M-22,-10 q-2,10 -4,16 M6,-12 q2,10 0,18 M24,-14 q4,10 4,18"/></g>
<path d="M-36,-26 h72 v8 h-72Z" fill="#3a2414" {O}/><rect x="-6" y="-27" width="12" height="10" rx="1.5" fill="none" stroke="url(#gGold)" stroke-width="2"/>
<path d="M-34,-18 h14 v16 q-7,5 -14,0Z" fill="url(#gLeather)" {O1}/><circle cx="-27" cy="-10" r="1.6" fill="url(#gGold)"/>
<!-- red cowl draped around the neck and shoulders -->
<path d="M-36,-70 Q-30,-92 0,-94 Q30,-92 36,-70 Q42,-56 30,-50 Q18,-46 8,-52 Q0,-46 -8,-52 Q-18,-46 -30,-50 Q-42,-56 -36,-70Z" fill="url(#gRed)" {O}/>
<g stroke="#7a0f18" stroke-width="1.8" fill="none" stroke-linecap="round"><path d="M-26,-74 q4,12 -2,22 M-12,-80 q6,14 2,28 M10,-80 q-4,14 0,28 M24,-74 q-4,12 2,22"/></g>
<path d="M-30,-82 Q0,-74 30,-82" stroke="#ff6a6a" stroke-width="2" fill="none" opacity=".5"/>
<!-- lute -->
<path d="M-22,-64 Q4,-46 30,-28" stroke="#3a2414" stroke-width="4" fill="none"/>
<g transform="translate(6,-36) rotate(-30)">
<rect x="20" y="-5" width="60" height="10" fill="#6b4426" {O1}/><g stroke="#e9d701" stroke-width="1"><path d="M30,-5 v10 M39,-5 v10 M48,-5 v10 M57,-5 v10 M66,-5 v10 M75,-5 v10"/></g>
<path d="M78,-8 l20,-6 l3,12 l-20,6Z" fill="#3a2212" {O1}/><g fill="url(#gGold)" {O1}><circle cx="84" cy="-12" r="2.4"/><circle cx="93" cy="-14" r="2.4"/><circle cx="87" cy="8" r="2.4"/><circle cx="96" cy="5" r="2.4"/></g>
<path d="M22,-8 Q10,-24 -10,-24 Q-32,-22 -32,0 Q-32,22 -10,24 Q10,24 22,8Z" fill="#c98a3c" {O}/>
<path d="M-28,-10 Q-10,-18 14,-10 M-30,4 Q-8,-2 18,4 M-26,16 Q-8,10 12,16" stroke="#9a5e22" stroke-width="1.2" fill="none"/>
<circle cx="-2" cy="0" r="8.5" fill="#2a1408" {O1}/><circle cx="-2" cy="0" r="8.5" fill="none" stroke="url(#gGold)" stroke-width="1.6"/><use href="#sparkle" fill="#e9d701" opacity=".8" transform="translate(-2 0) scale(.6)"/>
<path d="M-22,-3 L80,-3 M-22,0 L80,0 M-22,3 L80,3" stroke="#f3e6c4" stroke-width=".8" opacity=".9"/>
<rect x="-25" y="-7" width="5" height="14" fill="#3a2212" {O1}/>
</g>
<!-- white sleeves -->
<path d="M-28,-64 Q-34,-42 -6,-34" stroke="#160a22" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M-28,-64 Q-34,-42 -6,-34" stroke="#f1edf6" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M-26,-56 q2,10 10,16" stroke="#c9c2d6" stroke-width="2" fill="none"/>
<path d="M-4,-40 q10,0 10,8 q-2,7 -10,5Z" fill="#e8742e" {O1}/>
<path d="M26,-66 Q44,-76 60,-68" stroke="#160a22" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M26,-66 Q44,-76 60,-68" stroke="#f1edf6" stroke-width="13.5" fill="none" stroke-linecap="round"/>
<path d="M56,-76 q12,2 10,11 q-4,6 -12,2Z" fill="#e8742e" {O1}/>
<!-- head -->
<g transform="translate(2,4)">
<path d="M-24,-116 L-34,-168 L-2,-134Z" fill="url(#gFox)" {O}/><path d="M8,-134 L32,-168 L34,-114Z" fill="url(#gFox)" {O}/>
<path d="M-22,-122 L-30,-158 L-8,-134Z M12,-134 L29,-158 L30,-120Z" fill="#3a1208"/>
<path d="M-22,-124 q2,-12 -2,-20 q6,8 6,16 q2,-10 0,-16 q6,8 4,22Z M28,-122 q-2,-12 2,-20 q-6,8 -6,16 q-2,-10 0,-16 q-6,8 -4,22Z" fill="#fffaf4"/>
<path d="M-32,-104 C-34,-130 -14,-142 4,-142 C24,-142 40,-130 38,-104 Q36,-86 4,-82 Q-30,-86 -32,-104Z" fill="url(#gFox)" {O}/>
<!-- cheek ruff and white muzzle -->
<path d="M-24,-110 L-50,-107 L-38,-101 L-54,-96 L-37,-93 L-42,-86 L-24,-88 Q-10,-77 4,-77 Q18,-77 30,-88 L48,-86 L43,-93 L60,-96 L44,-101 L56,-107 L30,-110 Q24,-98 4,-98 Q-16,-98 -24,-110Z" fill="#fffaf4" {O}/>
<path d="M-12,-108 Q4,-118 20,-108 Q14,-98 4,-98 Q-6,-98 -12,-108Z" fill="#fffaf4"/>
<!-- tuft -->
<path d="M-14,-136 Q-8,-156 10,-152 Q2,-148 2,-140 Q10,-154 26,-146 Q14,-142 14,-134 Q6,-138 -14,-136Z" fill="#e0611f" {O1}/>
<path d="M-4,-138 q4,-8 12,-10 M8,-136 q6,-6 12,-6" stroke="#b8461a" stroke-width="1.2" fill="none"/>
<!-- eyes and brows -->
<ellipse cx="-9" cy="-114" rx="7" ry="8" fill="#fff" {O1}/><ellipse cx="-7.5" cy="-113" rx="4.4" ry="5.4" fill="#160a22"/><circle cx="-9" cy="-115.5" r="1.6" fill="#fff"/>
<ellipse cx="17" cy="-114" rx="7" ry="8" fill="#fff" {O1}/><ellipse cx="18.5" cy="-113" rx="4.4" ry="5.4" fill="#160a22"/><circle cx="17" cy="-115.5" r="1.6" fill="#fff"/>
<path d="M-20,-124 Q-10,-130 0,-124" stroke="#2a1208" stroke-width="3.6" fill="none" stroke-linecap="round"/><path d="M8,-124 Q18,-130 28,-125" stroke="#2a1208" stroke-width="3.6" fill="none" stroke-linecap="round"/>
<!-- nose and open grin -->
<path d="M0,-102 Q4,-106 8,-102 Q4,-97 0,-102Z" fill="#160a22"/><ellipse cx="3" cy="-103" rx="1.4" ry=".8" fill="#fff" opacity=".7"/>
<path d="M4,-98 v3" stroke="#160a22" stroke-width="1.4"/>
<path d="M-12,-94 Q4,-90 20,-94 Q16,-78 4,-77 Q-8,-78 -12,-94Z" fill="#5a0f1a" {O1}/>
<path d="M-11,-93 Q4,-89 19,-93 L18,-91 Q4,-87 -10,-91Z" fill="#fff"/>
<path d="M-5,-82 Q4,-90 13,-82 Q10,-77 4,-77 Q-2,-77 -5,-82Z" fill="#f08a9a"/>
<path d="M-12,-94 q-3,-1 -4,-4 M20,-94 q3,-1 4,-4" stroke="#160a22" stroke-width="1.4" fill="none" stroke-linecap="round"/>
</g>
<!-- music -->
<g class="float" fill="#e9d701" font-family="Georgia, serif"><text x="78" y="-118" font-size="32">&#9834;</text><text x="108" y="-156" font-size="26">&#9835;</text><text x="70" y="-182" font-size="20">&#9834;</text></g>
</g></g></g>
'''

FRONT=f'''
<g>{lstring(596,476,404,480,22,6)}{lstring(948,474,1250,540,40,9)}</g>
<g fill="#e9d701">{''.join(f'<circle class="twinkle" cx="{x}" cy="{y}" r="{r}" style="animation-delay:{d}s"/><circle cx="{x}" cy="{y}" r="{r*3}" fill="#e9d701" opacity=".12"/>' for x,y,r,d in [(470,770,3,.3),(900,650,2.5,1.1),(1150,770,3,2),(60,720,2.5,.8),(1540,740,3,1.6),(1000,830,2.5,2.6),(330,810,2.5,1.9),(880,560,2,1.2),(1230,660,2,2.2),(180,640,2.5,.5)])}</g>
<rect width="1600" height="900" fill="url(#vig)" pointer-events="none"/>
<rect width="1600" height="900" filter="url(#grain)" opacity=".1" pointer-events="none" style="mix-blend-mode:overlay"/>
{MARKERS}'''


SVG_STYLE="""<style>
.twinkle{animation:twinkle 3.5s ease-in-out infinite}
.float{animation:floaty 4s ease-in-out infinite}
.fume{animation:fume 5s ease-in-out infinite}
.bigstar{animation:breathe 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.marker{pointer-events:none;animation:pulse 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes pulse{0%,100%{opacity:.35;transform:scale(.8)}50%{opacity:1;transform:scale(1.15)}}
@keyframes twinkle{0%,100%{opacity:.25}50%{opacity:1}}
@keyframes floaty{0%,100%{transform:translateY(0);opacity:.9}50%{transform:translateY(-10px);opacity:.5}}
@keyframes fume{0%,100%{transform:translateY(0);opacity:.75}50%{transform:translateY(-8px);opacity:.35}}
@keyframes breathe{0%,100%{transform:scale(1) rotate(0deg)}50%{transform:scale(1.06) rotate(4deg)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""

def make_svg(places, standalone=False):
    """places: list of dicts with key, marker [x,y], view [x,y,w,h]"""
    markers=''.join(f'<use href="#sparkle" x="{p["marker"][0]}" y="{p["marker"][1]}" fill="#e9d701" class="marker" style="animation-delay:{i*.3:.1f}s"/>' for i,p in enumerate(places))
    views=''.join(f'<view id="v-{p["slug"]}" viewBox="{" ".join(str(v) for v in p["view"])}"/>' for p in places)
    body=DEFS+SVG_STYLE+views+SKY+MOON+CASTLE+MID+GROUNDFX+HALL+DOOR+MIRA+BOARD+BULL+MARKET+REY+FRONT.replace('{MARKERS}', markers)
    if standalone:
        return '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">'+body+'</svg>'
    return '<svg id="scene" viewBox="0 0 1600 900" role="img" aria-label="The Chaotic Good Guild village at night.">'+body+'</svg>'
