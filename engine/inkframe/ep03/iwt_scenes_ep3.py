"""I WAS THERE Ep3 - Pompeii, 79 AD. Palette: Pompeian red, ochre, olive, volcanic grey, ember orange."""
import os, sys, math, random
sys.path.insert(0, "/home/claude/ayatluma-videos/engine/inkframe")
import kit
kit.ACC = "#2EC4B6"
from kit import svg, text, render, INK, W, H
from ava import ava, TEAL
OUT = "/home/claude/work/iwt3/scenes"; os.makedirs(OUT, exist_ok=True)
PRED = "#a8322a"; OCHRE = "#d9a441"; OLIVE = "#6f7d3a"; ASH = "#7d7a76"; ASHD = "#3b3836"; EMBER = "#ff7a2a"
STONE = "#cfc3ad"; SKYB = "#8fc0dd"; CREAM = "#f2e6cc"; NIGHT = "#0f1020"; BREAD = "#c98a3e"

def ava_r(x, y, s=1.0, mood="calm", look=0):
    return ava(x, y, s, mood, look, coat="#b4552f", scarf=OCHRE)

def bigtext(x, y, s, size, fill="#f4f1ea", anchor="middle", sw=12):
    s = s.replace("&", "&amp;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-2">{s}</text>')

def grad(id_, top, bot):
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>'

def sky(top, bot, y1=H, id_=None):
    id_ = id_ or "g" + top[1:] + bot[1:]
    return grad(id_, top, bot) + f'<rect width="{W}" height="{y1}" fill="url(#{id_})"/>'

def vesuvius(cx, base, w, col=OLIVE, shade="#56632c", vines=True, twin=True):
    h = w * 0.36; half = w / 2
    p = f'M{cx-half} {base} Q{cx-half*0.45} {base-h*0.7} {cx-half*0.18} {base-h} L{cx+half*0.05} {base-h*0.96} Q{cx+half*0.12} {base-h*1.02} {cx+half*0.22} {base-h*0.93} Q{cx+half*0.55} {base-h*0.6} {cx+half} {base} Z'
    v = ""
    if vines:
        r = random.Random(int(cx))
        for i in range(28):
            x = r.uniform(cx - half * 0.7, cx + half * 0.7); y = r.uniform(base - h * 0.45, base - 10)
            v += f'<path d="M{x:.0f} {y:.0f} l40 -6" stroke="#3e4a1c" stroke-width="5" stroke-linecap="round" opacity="0.6"/>'
    tw = f'<path d="M{cx-half*0.18} {base-h} Q{cx-half*0.4} {base-h*0.88} {cx-half*0.6} {base-h*0.62}" fill="none" stroke="{INK}" stroke-width="4" opacity="0.5"/>' if twin else ""
    return f'<path d="{p}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><path d="M{cx} {base-h*0.98} Q{cx+half*0.3} {base-h*0.5} {cx+half} {base} L{cx} {base} Z" fill="{shade}" opacity="0.45"/>{v}{tw}'

def rhouse(x, y, w=260, h=180, wall=CREAM, band=PRED, door=True, roof=True):
    rf = f'<path d="M{x-14} {y} L{x+w/2} {y-60} L{x+w+14} {y} Z" fill="#b8562f" stroke="{INK}" stroke-width="6"/>' + "".join(f'<path d="M{x+i*26} {y} L{x+w/2} {y-58}" stroke="{INK}" stroke-width="2" opacity="0.25"/>' for i in range(int(w/26)+1)) if roof else ""
    d = f'<rect x="{x+w*0.38}" y="{y+h*0.4}" width="{w*0.24}" height="{h*0.6}" fill="#3a2418" stroke="{INK}" stroke-width="5"/>' if door else ""
    return f'{rf}<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}" stroke="{INK}" stroke-width="6"/><rect x="{x}" y="{y+h-46}" width="{w}" height="46" fill="{band}" stroke="{INK}" stroke-width="5"/>{d}'

def column(x, y, h=420, w=60, c=STONE, broken=False):
    top = f'<rect x="{x-12}" y="{y-26}" width="{w+24}" height="30" fill="{c}" stroke="{INK}" stroke-width="5"/>' if not broken else f'<path d="M{x} {y} L{x+w*0.4} {y-30} L{x+w*0.7} {y+10} L{x+w} {y-14}" fill="none" stroke="{INK}" stroke-width="5"/>'
    fl = "".join(f'<path d="M{x+i*w/4} {y+6} L{x+i*w/4} {y+h-6}" stroke="{INK}" stroke-width="2" opacity="0.35"/>' for i in range(1, 4))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="6"/>{fl}{top}<rect x="{x-12}" y="{y+h}" width="{w+24}" height="24" fill="{c}" stroke="{INK}" stroke-width="5"/>'

def loaf8(x, y, r=80, burnt=False):
    c = "#2a1d14" if burnt else BREAD
    cuts = "".join(f'<path d="M{x} {y} L{x+r*0.92*math.cos(a):.0f} {y+r*0.92*math.sin(a):.0f}" stroke="{INK}" stroke-width="{max(2,r/18):.0f}" opacity="0.8"/>' for a in [i * math.pi / 4 for i in range(8)])
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="{max(3,r/12):.0f}"/><circle cx="{x}" cy="{y}" r="{r*0.18:.0f}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.6"/>{cuts}'

def person(x, y, s=1.0, col="#6b4a3a", pose="walk", flip=False, op=1.0):
    fl = " translate(100 0) scale(-1 1)" if flip else ""
    legs = {"walk": "M40 200 L20 300 M60 200 L85 300", "stand": "M40 200 L38 300 M60 200 L62 300", "run": "M40 200 L0 280 M60 200 L100 270"}[pose]
    return f'''<g transform="translate({x} {y}) scale({s}){fl}" opacity="{op}"><path d="{legs}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/>
<path d="M22 90 Q50 76 78 90 L86 210 L14 210 Z" fill="{col}" stroke="{INK}" stroke-width="6"/><circle cx="50" cy="50" r="30" fill="#c99a7a" stroke="{INK}" stroke-width="6"/></g>'''

def pine_cloud(cx, base, h=700, w=900, col="#8a8580", dark="#5a5652"):
    r = random.Random(3); puffs = ""
    for i in range(26):
        a = r.uniform(-1, 1); px = cx + a * w / 2; py = base - h + r.uniform(-60, 90)
        puffs += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r.uniform(70,140):.0f}" fill="{col if i%3 else dark}" stroke="{INK}" stroke-width="5"/>'
    trunk = f'<path d="M{cx-60} {base} Q{cx-40} {base-h*0.5} {cx-90} {base-h+40} L{cx+90} {base-h+40} Q{cx+40} {base-h*0.5} {cx+60} {base} Z" fill="{dark}" stroke="{INK}" stroke-width="6"/>'
    return trunk + puffs

def pumice_fall(n, seed, y0=0, y1=H, op=0.8):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(3,9):.1f}" fill="#bdb6aa" opacity="{r.uniform(.4,op):.2f}"/>' for _ in range(n))

def ship(x, y, s=1.0, col="#6b3a22"):
    oars = "".join(f'<path d="M{60+i*40} 10 L{40+i*40} 70" stroke="{INK}" stroke-width="5"/>' for i in range(10))
    return f'''<g transform="translate({x} {y}) scale({s})">{oars}<path d="M0 -20 Q260 40 520 -20 L560 -70 Q540 30 260 40 Q-20 30 -30 -60 Z" fill="{col}" stroke="{INK}" stroke-width="7"/>
<path d="M260 -20 L260 -330" stroke="{INK}" stroke-width="10"/><path d="M150 -310 L370 -310 L360 -110 L160 -110 Z" fill="{CREAM}" stroke="{INK}" stroke-width="6"/><path d="M160 -210 L360 -210" stroke="{PRED}" stroke-width="16"/></g>'''

def sea(y, col="#2c5d7a"):
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{col}"/>' + "".join(f'<path d="M{i*160} {y+30+(i%3)*50} q40 -14 80 0" stroke="#f4f1ea" stroke-width="4" fill="none" opacity="0.35"/>' for i in range(13))

S = {}
S[1] = lambda: svg(f'''{sky("#2b2f55", "#e08a5a")}{vesuvius(1450, 900, 1100, "#3c4a2a", "#2a341c", False)}<rect x="0" y="880" width="{W}" height="200" fill="#5a3a2a"/>
<ellipse cx="560" cy="560" rx="560" ry="520" fill="url(#ylamp)"/>{ava_r(260, 150, 1.85, "calm", 6)}''', NIGHT)
S[2] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="{NIGHT}"/>{"".join(f'<circle cx="{random.Random(i).uniform(0,W):.0f}" cy="{random.Random(i+50).uniform(0,500):.0f}" r="2" fill="#fff" opacity="0.6"/>' for i in range(160))}
{vesuvius(1300, 760, 1500, "#1c2230", "#141822", False)}{"".join(rhouse(40 + i * 240, 760 + (i % 2) * 40, 200, 160, "#2a2a3a", "#3a2030", True, True) for i in range(8))}
{"".join(f'<rect x="{120+i*240}" y="{830+(i%2)*40}" width="30" height="30" fill="#ffcc66" opacity="0.8"/>' for i in range(8))}
{bigtext(960, 230, "ONE DAY LEFT", 130, "#f4f1ea")}''')
S[3] = lambda: svg(f'''{sky("#7fb6d9", "#f3d9a8")}{vesuvius(960, 860, 1500)}<rect x="0" y="840" width="{W}" height="240" fill="{OCHRE}" stroke="{INK}" stroke-width="6"/>
{"".join(rhouse(60 + i * 310, 760, 250, 160) for i in range(6))}
{bigtext(960, 190, "I WAS THERE", 150)}{text(960, 270, "POMPEII  ·  ITALY, 79 AD", 46, 800, "#2a1a10", "middle", 6, "Inter")}''')
S[4] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="{PRED}"/><rect x="0" y="0" width="{W}" height="120" fill="#7a2018"/>
<rect x="0" y="720" width="{W}" height="360" fill="#e8dcc0" stroke="{INK}" stroke-width="8"/>{"".join(f'<rect x="{1050+i*190}" y="180" width="150" height="380" fill="#8f2820" stroke="{INK}" stroke-width="5"/>' for i in range(4))}
{ava_r(250, 200, 1.4, "smile", 6)}{"".join(loaf8(1030 + i * 170, 700 - (i % 2) * 30, 70) for i in range(5))}''')
S[5] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a2418"/><ellipse cx="960" cy="560" rx="760" ry="420" fill="#ffb060" opacity="0.15" filter="url(#b30)"/>
{loaf8(960, 560, 330)}{text(1600, 300, "8", 220, 900, OCHRE, "middle")}{text(1600, 380, "PIECES", 54, 900, "#f4f1ea", "middle", 4)}''')
S[6] = lambda: svg(f'''{sky("#9fd0ea", "#f6e2b8")}{vesuvius(1500, 520, 900)}
<path d="M0 1080 L700 600 L1220 600 L1920 1080 Z" fill="#8a8478" stroke="{INK}" stroke-width="6"/>
{rhouse(-40, 380, 520, 420, CREAM, PRED)}{rhouse(1440, 380, 520, 420, "#e9c98a", "#2d5a4a")}
{person(720, 560, 0.75, "#2d5a8a")}{person(1050, 580, 0.7, "#8a3a2a", "walk", True)}{person(880, 640, 0.8, "#6a6a2a")}''')
S[7] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9d6b0"/><rect x="0" y="640" width="{W}" height="440" fill="#7a746a"/>
{"".join(f'<path d="M{i*130} 640 l120 0 l-10 440 l-120 0 Z" fill="none" stroke="{INK}" stroke-width="3" opacity="0.4"/>' for i in range(16))}
<path d="M0 820 L1920 820 M0 940 L1920 940" stroke="#4a463e" stroke-width="18" opacity="0.8"/>
<g transform="translate(600 520)"><rect x="0" y="0" width="520" height="200" fill="#8a5a2e" stroke="{INK}" stroke-width="7"/><circle cx="110" cy="260" r="90" fill="#5a3a1e" stroke="{INK}" stroke-width="8"/><circle cx="410" cy="260" r="90" fill="#5a3a1e" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M110 260 L{110+80*math.cos(a):.0f} {260+80*math.sin(a):.0f} M410 260 L{410+80*math.cos(a):.0f} {260+80*math.sin(a):.0f}" stroke="{INK}" stroke-width="5"/>' for a in [i*math.pi/4 for i in range(8)])}
{"".join(f'<ellipse cx="{80+i*90}" cy="-30" rx="40" ry="50" fill="#b06a30" stroke="{INK}" stroke-width="5"/>' for i in range(5))}</g>
{text(140, 200, "RATTLE.", 110, 900, "#2a1a10", "start", 2)}''')
S[8] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#6e6a62"/><rect x="0" y="0" width="{W}" height="300" fill="#bdb29a"/><rect x="0" y="780" width="{W}" height="300" fill="#bdb29a"/>
<path d="M0 300 L1920 300 M0 780 L1920 780" stroke="{INK}" stroke-width="8"/>{"".join(f'<ellipse cx="{560+i*400}" cy="540" rx="150" ry="110" fill="#c9bea6" stroke="{INK}" stroke-width="8"/>' for i in range(3))}
<g transform="translate(900 380) rotate(-10)"><path d="M0 0 Q60 -30 150 0 Q170 40 140 60 L10 60 Z" fill="#7a4a2a" stroke="{INK}" stroke-width="6"/><path d="M30 0 L60 60 M90 -6 L110 60" stroke="{INK}" stroke-width="4"/></g>
{text(960, 1020, "stepping stones - still there today", 46, 700, "#2a1a10", "middle", 0, "Inter")}''')
S[9] = lambda: svg(f'''{sky("#a7d4ec", "#e7f2f5")}{rhouse(60, 300, 600, 500, "#e9c98a", PRED, True, False)}{rhouse(1300, 260, 600, 540, CREAM, "#2d5a4a", True, False)}
<rect x="0" y="800" width="{W}" height="280" fill="#8a8478"/><rect x="740" y="620" width="440" height="220" fill="{STONE}" stroke="{INK}" stroke-width="8"/>
<rect x="900" y="420" width="120" height="220" fill="{STONE}" stroke="{INK}" stroke-width="7"/><circle cx="960" cy="480" r="38" fill="#c9a07a" stroke="{INK}" stroke-width="6"/>
<path d="M960 510 Q920 580 900 650" stroke="#6ac1e8" stroke-width="18" fill="none" stroke-linecap="round"/><path d="M760 650 L1160 650" stroke="#6ac1e8" stroke-width="20"/>''')
S[10] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e8d9b8"/>{"".join(f'<path d="M{random.Random(i).uniform(0,W):.0f} {random.Random(i+7).uniform(0,H):.0f} l{random.Random(i+3).uniform(20,90):.0f} {random.Random(i+4).uniform(-20,20):.0f}" stroke="#b9a582" stroke-width="3"/>' for i in range(90))}
{text(260, 260, "AMPLIATUS WAS HERE", 64, 800, "#2a1a10", "start", 6, "Inter")}{text(980, 380, "VOTE FOR SABINUS", 70, 900, PRED, "start", 4)}
{text(300, 560, "I OWE GAIUS 3 COINS", 58, 700, "#4a2a1a", "start", 4, "Inter")}{text(1060, 700, "MARCUS + SPENDUSA", 64, 800, "#2a1a10", "start", 4, "Inter")}
{text(420, 900, "BEST BREAD ON THE STREET", 62, 800, "#4a2a1a", "start", 4, "Inter")}{bigtext(960, 1020, "WORDS EVERYWHERE", 70, OCHRE, sw=10)}''')
S[11] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#f1e4c6"/><rect x="200" y="160" width="1520" height="460" fill="#fbf3de" stroke="{INK}" stroke-width="8"/>
{text(960, 320, "CN. HELVIUS SABINUS", 96, 900, PRED, "middle", 2)}{text(960, 440, "FOR AEDILE  ·  A GOOD MAN", 64, 800, "#2a1a10", "middle", 4)}
<g transform="translate(560 700)"><path d="M100 160 C-40 60 20 -40 100 30 C180 -40 240 60 100 160 Z" fill="{PRED}" stroke="{INK}" stroke-width="7"/></g>
<g transform="translate(1120 720)"><circle cx="90" cy="90" r="90" fill="{OCHRE}" stroke="{INK}" stroke-width="7"/>{text(90, 120, "IOU", 70, 900, "#2a1a10", "middle")}</g>''')
S[12] = lambda: svg(f'''{sky("#9fd0ea", "#f2ead2")}{vesuvius(960, 980, 2100)}
{"".join(f'<path d="M{100+i*160} 1080 L{220+i*120} 760" stroke="#3e4a1c" stroke-width="10" opacity="0.7"/>' for i in range(12))}
{"".join(f'<circle cx="{150+i*160}" cy="{900-(i%3)*40}" r="26" fill="#5a2a6a" stroke="{INK}" stroke-width="4"/>' for i in range(11))}''')
S[13] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1b1a17"/>{vesuvius(960, 1000, 1400, "#3e4a26", "#2a341a", False)}
{bigtext(960, 260, "“JUST A MOUNTAIN”", 140, "#f4f1ea")}{text(960, 370, "nobody called it a volcano", 54, 700, OCHRE, "middle", 0, "Inter")}''')
S[14] = lambda: svg(f'''{sky("#cfd8dc", "#f0e4c8")}<rect x="0" y="880" width="{W}" height="200" fill="{STONE}" stroke="{INK}" stroke-width="6"/>
{column(300, 420, 460)}{column(560, 420, 460)}{column(820, 520, 360, broken=True)}{column(1080, 420, 460)}<path d="M240 400 L1160 400 L1180 340 L220 340 Z" fill="{STONE}" stroke="{INK}" stroke-width="7"/>
<path d="M700 340 L760 410 L720 470 L790 560" stroke="{INK}" stroke-width="7" fill="none"/><rect x="980" y="820" width="140" height="70" fill="{STONE}" stroke="{INK}" stroke-width="5" transform="rotate(14 1050 850)"/>
{bigtext(1560, 520, "62 AD", 180, PRED)}{text(1560, 610, "the great earthquake", 48, 700, INK, "middle", 0, "Inter")}''')
S[15] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a2a20"/><rect x="0" y="700" width="{W}" height="380" fill="#6a4a30" stroke="{INK}" stroke-width="6"/>
<path d="M760 340 L1160 340 L1110 720 L810 720 Z" fill="#c4703a" stroke="{INK}" stroke-width="9"/><ellipse cx="960" cy="345" rx="200" ry="30" fill="#5a8aa0" stroke="{INK}" stroke-width="6"/>
{"".join(f'<ellipse cx="960" cy="345" rx="{60+i*45}" ry="{8+i*6}" fill="none" stroke="#e8f4f8" stroke-width="3" opacity="{0.8-i*0.2:.1f}"/>' for i in range(3))}
{text(960, 180, "the ground trembled again", 64, 700, "#f4e2c4", "middle", 0, "Inter")}''')
S[16] = lambda: svg(f'''{sky("#6f8fa8", "#e8b880")}<ellipse cx="960" cy="380" rx="700" ry="400" fill="{EMBER}" opacity="0.35" filter="url(#b30)"/>
{pine_cloud(960, 520, 520, 1100)}{vesuvius(960, 1000, 1800, "#4a5228", "#30361a", True, False)}
{"".join(f'<path d="M960 520 L{960+math.cos(a)*420:.0f} {520+math.sin(a)*300:.0f}" stroke="{EMBER}" stroke-width="9" opacity="0.8"/>' for a in [-2.6,-2.2,-1.8,-1.3,-0.9,-0.5])}''')
S[17] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a1e1a"/><ellipse cx="1300" cy="420" rx="800" ry="500" fill="{EMBER}" opacity="0.25" filter="url(#b30)"/>
{ava_r(380, 120, 2.0, "scared", 14)}{bigtext(1450, 520, "ROOOAR", 200, EMBER)}''')
S[18] = lambda: svg(f'''{sky("#7f9cb2", "#d9c3a0")}{pine_cloud(1100, 900, 820, 1300)}{vesuvius(1100, 1000, 1200, "#4a5228", "#30361a", False, False)}
{"".join(rhouse(20 + i * 170, 960, 150, 120, CREAM, PRED, False) for i in range(4))}{person(300, 820, 0.5, "#2d5a8a", "stand", True)}''')
S[19] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#efe6d2"/><path d="M960 120 L960 980" stroke="{INK}" stroke-width="6" stroke-dasharray="20 14"/>
<g transform="translate(480 0)"><path d="M-30 980 Q-20 600 -40 380 L40 380 Q20 600 30 980 Z" fill="#7a5a36" stroke="{INK}" stroke-width="7"/>
<ellipse cx="0" cy="300" rx="360" ry="150" fill="#3e6a2e" stroke="{INK}" stroke-width="8"/><ellipse cx="0" cy="240" rx="260" ry="90" fill="#4e7a36" stroke="{INK}" stroke-width="6"/></g>
<g transform="translate(-0 0)">{pine_cloud(1440, 980, 700, 720)}</g>{text(480, 1050, "a stone pine", 46, 800, INK, "middle")}{text(1440, 1050, "the cloud", 46, 800, INK, "middle")}''')
S[20] = lambda: svg(f'''{sky("#9cc4dc", "#f2d9a8", 620)}{pine_cloud(1500, 560, 420, 520)}{vesuvius(1500, 620, 600, "#5a6a3a", "#3a4422", False, False)}{sea(620)}
<rect x="0" y="760" width="900" height="320" fill="{CREAM}" stroke="{INK}" stroke-width="7"/><rect x="0" y="740" width="900" height="30" fill="{PRED}" stroke="{INK}" stroke-width="5"/>
{person(380, 480, 1.1, "#e8e0cc", "stand")}<rect x="520" y="620" width="160" height="110" fill="#c9a060" stroke="{INK}" stroke-width="6" transform="rotate(-12 600 670)"/>
{text(440, 880, "PLINY, 17", 60, 900, PRED, "middle")}{text(440, 950, "he wrote it all down", 40, 700, INK, "middle", 0, "Inter")}''')
S[21] = lambda: svg(f'''{sky("#4a4440", "#7a6a5a")}{pumice_fall(500, 21)}{"".join(rhouse(20 + i * 320, 720, 280, 220, "#bba98a", "#7a2a22") for i in range(6))}
<rect x="0" y="940" width="{W}" height="140" fill="#6a645a"/>{bigtext(960, 260, "THE SKY STARTED TO FALL", 110, "#f4f1ea")}''')
S[22] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#14110e"/>{text(960, 250, "WOULD YOU RUN...", 110, 900, "#f4f1ea", "middle", -2)}
{text(960, 420, "...OR STAY INSIDE?", 110, 900, OCHRE, "middle", -2)}{text(960, 620, "Tell me in the comments.", 56, 600, "#cfd3da", "middle", 0, "Inter")}
<rect x="720" y="760" width="480" height="120" rx="60" fill="#e23b3b"/>{text(960, 840, "SUBSCRIBE", 56, 900, "#ffffff", "middle")}<path d="M1260 790 q20 -40 40 0 l10 40 l-60 0 Z" fill="{OCHRE}" stroke="#f4f1ea" stroke-width="4"/>''')
S[23] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2724"/><ellipse cx="960" cy="560" rx="420" ry="330" fill="#cfc7b8" stroke="{INK}" stroke-width="10"/>
{"".join(f'<circle cx="{random.Random(i).uniform(640,1280):.0f}" cy="{random.Random(i+40).uniform(340,780):.0f}" r="{random.Random(i+80).uniform(6,20):.0f}" fill="#8a8274" stroke="{INK}" stroke-width="3"/>' for i in range(70))}
{bigtext(960, 160, "PUMICE", 130, "#f4f1ea")}{text(960, 1000, "light grey stone, full of holes", 48, 700, "#cfc7b8", "middle", 0, "Inter")}''')
S[24] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121010"/>{pumice_fall(420, 24, 0, H, 0.6)}
{"".join(rhouse(40 + i * 330, 560, 280, 260, "#3a3530", "#2a1a18") for i in range(6))}<rect x="0" y="820" width="{W}" height="260" fill="#4a4540"/>
{"".join(f'<circle cx="{200+i*330}" cy="700" r="60" fill="#ffb84a" opacity="0.25" filter="url(#b8)"/><circle cx="{200+i*330}" cy="700" r="12" fill="#ffcf6a"/>' for i in range(6))}
{text(960, 200, "NO SUN. NO NIGHT.", 90, 900, "#cfc7b8", "middle", 2)}''')
S[25] = lambda: svg(f'''{sky("#3a3530", "#5a5048")}{pumice_fall(300, 25)}<rect x="0" y="760" width="{W}" height="320" fill="#8a8274"/>
{"".join(person(80 + i * 220, 470 + (i % 2) * 40, 1.0, ["#6a3a2a", "#2d4a6a", "#5a5a2a", "#7a2a3a"][i % 4], "run") for i in range(8))}
{"".join(f'<rect x="{110+i*220}" y="{440+(i%2)*40}" width="60" height="50" fill="{OCHRE}" stroke="{INK}" stroke-width="4"/>' for i in range(0, 8, 2))}''')
S[26] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#4a4440"/>{pumice_fall(260, 26)}
<g transform="translate(560 160) scale(2.2)">{person(0, 0, 1.0, "#6a3a2a", "stand")}<rect x="8" y="-20" width="84" height="44" rx="18" fill="#efe2c8" stroke="{INK}" stroke-width="5"/><path d="M14 20 L40 80 M86 20 L60 80" stroke="#a8322a" stroke-width="5"/></g>
<g transform="translate(1180 200)">{person(0, 0, 1.6, "#2d4a6a", "walk")}{person(30, -40, 1.0, "#7a6a5a", "stand")}</g>{text(960, 1020, "pillows tied on with cloth", 50, 700, "#efe2c8", "middle", 0, "Inter")}''')
S[27] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a1e18"/><rect x="560" y="120" width="800" height="840" fill="#1a1210" stroke="{INK}" stroke-width="10"/>
<rect x="600" y="160" width="720" height="800" fill="#c86a3a" opacity="0.25"/><circle cx="960" cy="420" r="200" fill="#ffb84a" opacity="0.2" filter="url(#b30)"/>
{person(700, 560, 1.2, "#6a3a2a", "stand")}{person(880, 600, 1.0, "#2d4a6a", "stand", True)}{person(1060, 580, 1.1, "#5a5a2a", "stand")}
{pumice_fall(140, 27, 0, 120)}<rect x="0" y="960" width="{W}" height="120" fill="#8a8274"/>{text(260, 560, "OTHERS", 90, 900, "#efe2c8", "middle")}{text(260, 660, "STAYED", 90, 900, OCHRE, "middle")}''')
S[28] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a3632"/>{pumice_fall(300, 28, 0, 500)}
<path d="M200 600 L960 300 L1720 600 Z" fill="#b8562f" stroke="{INK}" stroke-width="9"/><path d="M200 600 L960 300 L1720 600" fill="none" stroke="{INK}" stroke-width="9"/>
<path d="M260 580 Q600 440 960 330 Q1300 440 1660 580 L1660 540 Q1300 400 960 300 Q600 400 260 540 Z" fill="#a8a094" stroke="{INK}" stroke-width="5"/>
<path d="M900 330 L940 420 L890 480 L960 560" stroke="{INK}" stroke-width="10" fill="none"/><rect x="260" y="600" width="1400" height="420" fill="#c9b898" stroke="{INK}" stroke-width="8"/>
{text(960, 820, "CRACK", 160, 900, "#2a1a10", "middle", 10)}''')
S[29] = lambda: svg(f'''{sky("#5a5a6a", "#c08a5a", 640)}{pine_cloud(1550, 600, 460, 600, "#6a6460", "#4a4440")}{sea(640, "#2a4a5e")}
{ship(200, 760, 1.15)}{ship(900, 820, 0.8, "#5a3020")}{text(560, 160, "PLINY THE ELDER", 76, 900, "#f4f1ea", "middle", 2)}{text(560, 240, "admiral of the Roman fleet", 44, 700, OCHRE, "middle", 0, "Inter")}''')
S[30] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#120e14"/><ellipse cx="1500" cy="460" rx="520" ry="380" fill="{EMBER}" opacity="0.3" filter="url(#b30)"/>
{vesuvius(1500, 700, 900, "#1e1a18", "#141210", False, False)}{sea(700, "#141e2a")}{ship(560, 820, 0.6, "#2a1a14")}{ship(900, 860, 0.45, "#2a1a14")}
{text(420, 300, "toward the mountain.", 64, 800, "#efe2c8", "middle", 0, "Inter")}{text(420, 380, "not away from it.", 64, 800, EMBER, "middle", 0, "Inter")}''')
S[31] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#151210"/>{pumice_fall(200, 31, 0, H, 0.5)}<path d="M0 900 Q960 760 1920 860 L1920 1080 L0 1080 Z" fill="#4a4540" stroke="{INK}" stroke-width="6"/>
<ellipse cx="900" cy="600" rx="380" ry="380" fill="#ffb84a" opacity="0.18" filter="url(#b30)"/>{ava_r(620, 200, 1.4, "determined", -8)}
<g transform="translate(1100 620)"><path d="M0 0 L60 0 L50 40 L10 40 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="5"/><path d="M30 0 q-14 -30 0 -50 q14 20 0 50" fill="#ffcf6a" stroke="{INK}" stroke-width="3"/></g>
{text(1500, 320, "BEFORE DAWN", 80, 900, "#efe2c8", "middle", 2)}''')
S[32] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0e0a0a"/><ellipse cx="960" cy="380" rx="900" ry="400" fill="{EMBER}" opacity="0.35" filter="url(#b30)"/>
{vesuvius(960, 820, 1800, "#1a1412", "#100c0a", False, False)}<path d="M960 180 L930 260 L990 330" stroke="#ffb84a" stroke-width="8" fill="none"/>
<path d="M0 820 L1920 820 L1920 1080 L0 1080 Z" fill="#1e1a18"/>{person(860, 640, 0.75, "#3a2a2a", "walk", True, 0.9)}''')
S[33] = lambda: svg(f'''{sky("#2a2220", "#6a5040")}<ellipse cx="900" cy="600" rx="1100" ry="420" fill="#8a7a6a" opacity="0.5" filter="url(#b30)"/>
{vesuvius(500, 820, 1300, "#2a2420", "#1a1614", False, False)}
{"".join(f'<circle cx="{200+i*95+random.Random(i).uniform(-30,30):.0f}" cy="{560+i*22+random.Random(i+9).uniform(-60,40):.0f}" r="{120-i*3}" fill="{["#6a625a","#5a524a","#7a6e62"][i%3]}" stroke="{INK}" stroke-width="5"/>' for i in range(18))}
<path d="M1500 640 l300 0 M1460 700 l360 0 M1520 760 l320 0" stroke="#f4f1ea" stroke-width="8" stroke-linecap="round" opacity="0.6"/>{bigtext(1200, 220, "FASTER THAN A HORSE", 84, EMBER)}''')
S[34] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#6a645c"/><rect x="0" y="0" width="{W}" height="{H}" fill="#9a928a" opacity="0.4" filter="url(#b30)"/>
{"".join(rhouse(40 + i * 330, 600, 280, 240, "#8a847c", "#6a645c") for i in range(6))}<rect x="0" y="840" width="{W}" height="240" fill="#8a847c"/>
{text(960, 300, "silence.", 110, 300, "#e8e2d8", "middle", 6, "Inter")}''')
S[35] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#9fc6df"/><rect x="0" y="260" width="{W}" height="820" fill="#8a8274"/>
{"".join(f'<rect x="0" y="{260+i*110}" width="{W}" height="110" fill="{["#9a9284","#837b6e","#a69e90","#77706a","#958c7e","#6e6862","#8a8274"][i%7]}"/>' for i in range(8))}
{"".join(rhouse(140 + i * 440, 820, 300, 200, "#cfc0a0", PRED, True, True) for i in range(4))}<path d="M0 260 L1920 260" stroke="{INK}" stroke-width="7"/>
<path d="M1820 260 L1820 1020" stroke="{INK}" stroke-width="6"/><path d="M1790 260 L1850 260 M1790 1020 L1850 1020" stroke="{INK}" stroke-width="6"/>{text(1720, 640, "4-6 m", 58, 900, "#f4f1ea", "end", 2)}
{bigtext(960, 190, "BURIED", 140, "#f4f1ea")}''')
S[36] = lambda: svg(f'''{sky("#a8d4ef", "#f5ead0", 700)}{vesuvius(1400, 700, 1000, OLIVE, "#56632c", True, False)}<rect x="0" y="700" width="{W}" height="380" fill="#8aa04a" stroke="{INK}" stroke-width="6"/>
{"".join(f'<path d="M{i*120} 1080 L{560+i*30} 700" stroke="#5a6e2a" stroke-width="6" opacity="0.6"/>' for i in range(17))}{person(400, 640, 0.7, "#6a5a3a", "walk")}
{bigtext(620, 280, "1,600+ YEARS", 130, "#f4f1ea")}{text(620, 370, "fields and vineyards on top", 48, 700, "#2a3a1a", "middle", 0, "Inter")}''')
S[37] = lambda: svg(f'''{sky("#cde4f2", "#f2e6cc", 560)}<rect x="0" y="560" width="{W}" height="520" fill="#9a9284" stroke="{INK}" stroke-width="6"/>
<path d="M300 1080 L420 700 L1500 700 L1620 1080 Z" fill="#6e6862" stroke="{INK}" stroke-width="6"/>{column(820, 760, 260)}{column(1040, 760, 260)}
{"".join(f'<g transform="translate({300+i*360} {420+(i%2)*30})">{person(0, 0, 0.9, ["#3a3a6a", "#6a3a2a", "#4a5a2a", "#5a2a4a"][i])}<path d="M90 120 L160 300" stroke="#7a5a36" stroke-width="12"/><path d="M140 290 l50 30 l-20 20 Z" fill="#9aa0a6" stroke="{INK}" stroke-width="4"/></g>' for i in range(4))}
{text(960, 140, "THE 1700s: DIGGING BEGINS", 70, 900, "#2a1a10", "middle", 2)}''')
S[38] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1c1612"/><path d="M360 980 L360 520 Q960 120 1560 520 L1560 980 Z" fill="#6a5a4a" stroke="{INK}" stroke-width="12"/>
<path d="M560 980 L560 640 Q960 360 1360 640 L1360 980 Z" fill="#14100c" stroke="{INK}" stroke-width="8"/>
{"".join(loaf8(660 + (i % 5) * 150, 900 - (i // 5) * 120, 62, True) for i in range(10))}{bigtext(1700, 300, "81", 220, OCHRE)}{text(1700, 380, "LOAVES", 60, 900, "#efe2c8", "middle", 4)}''')
S[39] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#a69e90"/>{"".join(f'<path d="M0 {120+i*90} Q960 {100+i*90+(i%2)*30} 1920 {120+i*90}" stroke="#8a8274" stroke-width="6" fill="none"/>' for i in range(11))}
<path d="M640 640 Q700 520 860 540 Q1000 500 1120 560 Q1260 600 1280 700 Q1200 760 960 740 Q760 760 640 700 Z" fill="#2a2622" stroke="{INK}" stroke-width="8"/>
{text(960, 200, "AN EMPTY SPACE IN THE ASH", 76, 900, "#2a1a10", "middle", 2)}''')
S[40] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e8dfcc"/><rect x="0" y="760" width="{W}" height="320" fill="#a69e90" stroke="{INK}" stroke-width="6"/>
<g transform="translate(560 220)">{person(0, 0, 1.6, "#2a2a3a", "stand")}<rect x="40" y="-110" width="80" height="60" fill="#1a1a1a" stroke="{INK}" stroke-width="5"/><rect x="20" y="-56" width="120" height="12" fill="#1a1a1a"/></g>
<path d="M860 420 L1000 460 L980 520 L840 480 Z" fill="#d8d0c0" stroke="{INK}" stroke-width="6"/><path d="M990 500 Q1040 600 1060 760" stroke="#ffffff" stroke-width="22" fill="none" stroke-linecap="round"/>
<circle cx="1060" cy="780" r="30" fill="#2a2622" stroke="{INK}" stroke-width="5"/>{text(1450, 380, "GIUSEPPE FIORELLI", 64, 900, "#2a1a10", "middle", 2)}{text(1450, 460, "1860s  ·  plaster", 50, 700, PRED, "middle", 0, "Inter")}''')
S[41] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#151413"/><ellipse cx="960" cy="760" rx="700" ry="160" fill="#e8e2d8" opacity="0.08" filter="url(#b30)"/>
<path d="M620 820 Q700 640 900 660 Q1080 600 1240 700 Q1320 780 1280 840 Z" fill="#d8d2c6" stroke="{INK}" stroke-width="7" opacity="0.9"/>
<path d="M900 700 Q960 640 1040 680" stroke="{INK}" stroke-width="4" fill="none" opacity="0.4"/>
{bigtext(960, 300, "1,000+", 200, "#efe8dc")}{text(960, 400, "people found in the city. Most escaped. Not everyone.", 44, 600, "#bdb6aa", "middle", 0, "Inter")}''')
S[42] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#f1e8d6"/>
<g transform="translate(260 260)"><rect width="560" height="520" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="8"/><rect width="560" height="130" rx="30" fill="#7a7a7a" stroke="{INK}" stroke-width="8"/>{text(280, 95, "AUGUST", 70, 900, "#ffffff", "middle")}{text(280, 400, "24", 230, 900, "#2a1a10", "middle")}<path d="M40 160 L520 490" stroke="{PRED}" stroke-width="26" stroke-linecap="round"/></g>
<path d="M880 520 L1040 520 M1000 470 L1050 520 L1000 570" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>
<g transform="translate(1100 260)"><rect width="560" height="520" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="8"/><rect width="560" height="130" rx="30" fill="{PRED}" stroke="{INK}" stroke-width="8"/>{text(280, 95, "OCTOBER", 70, 900, "#ffffff", "middle")}{text(280, 400, "24?", 230, 900, "#2a1a10", "middle")}</g>
{text(960, 940, "2018: a charcoal note on a wall changed the date", 50, 700, "#2a1a10", "middle", 0, "Inter")}''')
S[43] = lambda: svg(f'''{sky("#8ec5e8", "#eef6f8", 640)}{vesuvius(1350, 640, 1100, "#7a8a5a", "#5a6a3a", False)}<rect x="0" y="640" width="{W}" height="440" fill="#bdb29a"/>
{column(260, 360, 300, 50, "#d8ccb4", True)}{column(420, 400, 260, 50, "#d8ccb4")}<path d="M0 1080 L700 700 L1220 700 L1920 1080 Z" fill="#8a8478" stroke="{INK}" stroke-width="6"/>
{"".join(f'<ellipse cx="{820+i*140}" cy="{860}" rx="50" ry="30" fill="#c9bea6" stroke="{INK}" stroke-width="5"/>' for i in range(3))}
{"".join(person(600 + i * 200, 620 + (i % 2) * 30, 0.65, ["#e23b3b", "#2E86C1", "#f2b705", "#2EC4B6", "#8e44ad"][i], "walk", i % 2 == 1) for i in range(5))}''')
S[44] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0f1426"/>{vesuvius(960, 760, 1700, "#1e2840", "#141c30", False)}<rect x="0" y="760" width="{W}" height="320" fill="#101828"/>
{"".join(f'<circle cx="{random.Random(i).uniform(0,W):.0f}" cy="{random.Random(i+5).uniform(780,900):.0f}" r="{random.Random(i+9).uniform(2,5):.1f}" fill="#ffd27a" opacity="0.85"/>' for i in range(260))}
<rect x="0" y="920" width="{W}" height="160" fill="#0a1220"/>{text(960, 220, "STILL ACTIVE. STILL WATCHING.", 76, 900, "#efe8dc", "middle", 2)}''')
S[45] = lambda: svg(f'''{sky("#f2c27b", "#d9643a")}{vesuvius(1500, 860, 900)}<rect x="0" y="840" width="{W}" height="240" fill="{OCHRE}"/>
<ellipse cx="660" cy="560" rx="600" ry="500" fill="url(#ylamp)"/>{ava_r(240, 160, 1.8, "smile", 6)}
{bigtext(1360, 340, "I'M AVA.", 120)}{bigtext(1360, 480, "AND I WAS THERE.", 84, TEAL)}''')
S[46] = lambda: svg(f'''{text(960, 220, "WHERE SHOULD I GO NEXT?", 100, 900, "#f4f1ea", "middle", -2)}
{"".join(f'<rect x="{240+i*370}" y="320" width="330" height="300" rx="24" fill="#1b1d23" stroke="{TEAL}" stroke-width="6"/>' + text(405+i*370, 520, ic, 140, 900, TEAL, "middle") for i, ic in enumerate(["?", "?", "?", "?"]))}
{text(960, 760, "Write it in the comments. The best idea might be my next story.", 44, 500, "#cfd3da", "middle")}
<rect x="760" y="860" width="400" height="100" rx="50" fill="#e23b3b"/>{text(960, 928, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}''', "#14110e")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
