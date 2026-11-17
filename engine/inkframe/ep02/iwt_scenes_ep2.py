"""I WAS THERE Ep2 - Building the Great Pyramid. Desert palette: sand, gold, deep blue night, Nile green."""
import os, sys, math, random
sys.path.insert(0, "/home/claude/iwt")
import kit
kit.ACC = "#2EC4B6"
from kit import svg, text, render, INK, W, H
from ava import ava, TEAL
OUT = "/home/claude/iwt/ep2/scenes"; os.makedirs(OUT, exist_ok=True)
SAND = "#d9b26f"; SAND2 = "#c4964f"; SKY = "#f2c27b"; DUSK = "#e0875a"; NIGHT = "#0d1530"; NILE = "#2f6f73"; LIME = "#efe6d2"
GOLD = "#e8b94a"; RED = "#b8432f"; LINEN = "#ece2cc"; SKINW = "#b07a52"

def stars(n, seed, y1=H):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,y1):.0f}" r="{r.uniform(1,2.8):.1f}" fill="#fff" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(n))

def ava_eg(x, y, s=1.0, mood="calm", look=0):
    band = f'''<g transform="translate({x} {y}) scale({s})"><path d="M136 118 Q200 98 264 118" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round"/>
    <circle cx="200" cy="104" r="9" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>
    <circle cx="132" cy="176" r="8" fill="{GOLD}" stroke="{INK}" stroke-width="4"/></g>'''
    return ava(x, y, s, mood, look, coat=LINEN, scarf=TEAL) + band

def sky(top, bot, y1=760):
    return f'''<defs><linearGradient id="sk{top[1:]}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>
<rect width="{W}" height="{y1}" fill="url(#sk{top[1:]})"/>'''

def dunes(y=760, c1=SAND, c2=SAND2):
    return (f'<path d="M0 {y} Q300 {y-60} 620 {y-10} T1280 {y-20} T1920 {y-40} L1920 {H} L0 {H} Z" fill="{c2}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M0 {y+80} Q400 {y+20} 800 {y+70} T1920 {y+60} L1920 {H} L0 {H} Z" fill="{c1}" stroke="{INK}" stroke-width="6"/>')

def pyramid(cx, base_y, w, prog=1.0, col=LIME, shade="#cdbd98", lines=True):
    h = w * 0.64; top_y = base_y - h * prog; half = w / 2; th = half * (1 - prog)
    pts = f"{cx-half},{base_y} {cx+half},{base_y} {cx+th},{top_y} {cx-th},{top_y}"
    sh = f"{cx},{base_y} {cx+half},{base_y} {cx+th},{top_y} {cx if prog>=1 else cx+th*0.1},{top_y}"
    ls = ""
    if lines:
        for i in range(1, int(18 * prog)):
            yy = base_y - h * i / 18; hw = half * (1 - i / 18)
            ls += f'<path d="M{cx-hw:.0f} {yy:.0f} L{cx+hw:.0f} {yy:.0f}" stroke="{INK}" stroke-width="2" opacity="0.35"/>'
    return f'<polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/><polygon points="{sh}" fill="{shade}" opacity="0.7"/>{ls}'

def worker(x, y, s=1.0, pose="stand", flip=False, skin=SKINW, kilt=LINEN):
    fl = " translate(120 0) scale(-1 1)" if flip else ""
    arms = {"stand": "M30 120 L10 210 M90 120 L110 210", "pull": "M30 120 L-30 150 M90 120 L40 150",
            "up": "M30 120 L10 30 M90 120 L110 30", "chisel": "M30 120 L70 170 M90 120 L130 150"}[pose]
    lean = -14 if pose == "pull" else 0
    return f'''<g transform="translate({x} {y}) scale({s}){fl}"><g transform="rotate({lean} 60 300)">
  <path d="M40 230 L30 330 M80 230 L95 330" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M40 230 L30 330 M80 230 L95 330" stroke="{skin}" stroke-width="12" stroke-linecap="round"/>
  <path d="{arms}" stroke="{INK}" stroke-width="22" stroke-linecap="round" fill="none"/><path d="{arms}" stroke="{skin}" stroke-width="12" stroke-linecap="round" fill="none"/>
  <path d="M28 110 Q60 96 92 110 L88 200 L32 200 Z" fill="{skin}" stroke="{INK}" stroke-width="6"/>
  <path d="M28 196 L92 196 L100 252 L20 252 Z" fill="{kilt}" stroke="{INK}" stroke-width="6"/>
  <circle cx="60" cy="70" r="34" fill="{skin}" stroke="{INK}" stroke-width="6"/>
  <path d="M26 66 Q30 30 60 32 Q92 30 94 66 Q80 50 60 52 Q40 50 26 66 Z" fill="#1d1a18" stroke="{INK}" stroke-width="4"/>
  <circle cx="50" cy="74" r="4" fill="{INK}"/><circle cx="72" cy="74" r="4" fill="{INK}"/></g></g>'''

def block(x, y, w=160, h=100, col=LIME):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="{INK}" stroke-width="6"/><path d="M{x+10} {y+18} L{x+w-30} {y+14}" stroke="#bfb08f" stroke-width="4"/>'

def sledge(x, y, s=1.0, col=LIME):
    return f'''<g transform="translate({x} {y}) scale({s})">{block(20, -110, 200, 120, col)}
  <path d="M0 10 L250 10 Q280 10 290 -10" fill="none" stroke="#6b4a2e" stroke-width="16" stroke-linecap="round"/><path d="M0 10 L250 10 Q280 10 290 -10" fill="none" stroke="{INK}" stroke-width="4"/>
  <path d="M40 -110 L120 10 M200 -110 L120 10" stroke="#8a6a3a" stroke-width="5" opacity="0.8"/></g>'''

def boat(x, y, s=1.0, cargo=True, sail=True):
    c = "".join(block(80 + i * 110, -84, 100, 64) for i in range(3)) if cargo else ""
    sl = f'<path d="M260 -100 L260 -420" stroke="{INK}" stroke-width="10"/><path d="M180 -400 L340 -400 L330 -150 L190 -150 Z" fill="{LINEN}" stroke="{INK}" stroke-width="6"/>' if sail else ""
    return f'''<g transform="translate({x} {y}) scale({s})">{sl}{c}
  <path d="M0 -30 Q260 30 520 -30 L560 -80 Q540 20 260 40 Q-20 20 -40 -80 Z" fill="#8a5a2e" stroke="{INK}" stroke-width="7"/>
  <path d="M40 -10 L480 -10" stroke="{INK}" stroke-width="3" opacity="0.5"/></g>'''

def palm(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M0 0 Q10 -150 -10 -300" stroke="{INK}" stroke-width="26" fill="none"/><path d="M0 0 Q10 -150 -10 -300" stroke="#7a5a36" stroke-width="16" fill="none"/>
  {"".join(f'<path d="M-10 -300 Q{math.cos(a)*120:.0f} {-300+math.sin(a)*60-40:.0f} {math.cos(a)*190:.0f} {-300+math.sin(a)*120:.0f}" stroke="#2e5a33" stroke-width="22" fill="none" stroke-linecap="round"/>' for a in [-3.0,-2.3,-1.6,-0.8,-0.1])}</g>'''

def house(x, y, w=200, h=140, c="#c99a62"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="6"/><rect x="{x+w*0.4}" y="{y+h*0.45}" width="{w*0.2}" height="{h*0.55}" fill="#3a2a1e" stroke="{INK}" stroke-width="4"/>'

def bigtext(x, y, s, size, fill="#f4f1ea", anchor="middle", sw=12):
    s = s.replace("&", "&amp;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-2">{s}</text>')

def sun(cx, cy, r=110, c="#ffe39a"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r*2.6}" fill="{c}" opacity="0.18"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="6"/>'

def pot(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-50 0 Q-60 -110 0 -140 Q60 -110 50 0 Z" fill="#a0522d" stroke="{INK}" stroke-width="6"/><path d="M-40 -60 L40 -60" stroke="{INK}" stroke-width="3" opacity="0.5"/></g>'

def loaf(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-40 0 Q-36 -70 0 -80 Q36 -70 40 0 Z" fill="#d79a4a" stroke="{INK}" stroke-width="5"/><path d="M-14 -50 L14 -50" stroke="{INK}" stroke-width="3"/></g>'

S = {}
S[1] = lambda: svg(f'''{sky("#2a3b6b", DUSK)}{sun(1500, 700, 160, "#ffb36b")}{pyramid(1500, 760, 760, 0.7, "#8a6f4c", "#6b553a")}{dunes(760, "#a77d45", "#8c6537")}
<ellipse cx="560" cy="560" rx="560" ry="520" fill="url(#ylamp)"/>{ava_eg(300, 150, 1.85, "calm", 6)}''', NIGHT)
S[2] = lambda: svg(f'''{stars(260, 2, 700)}<circle cx="1550" cy="200" r="70" fill="#f4f1ea" stroke="{INK}" stroke-width="5"/>{pyramid(960, 820, 1100, 0.55, "#2b3350", "#1c2238")}
{dunes(820, "#20263c", "#171c2e")}{ava_eg(180, 640, 0.75, "determined", 10)}''', NIGHT)
S[3] = lambda: svg(f'''{sky("#f7d79a", "#e7a35c")}{sun(960, 520, 140)}{pyramid(960, 820, 900, 1.0)}{dunes(820)}
{bigtext(960, 190, "I WAS THERE", 150)}{text(960, 270, "BUILDING THE GREAT PYRAMID  ·  EGYPT, c. 2560 BC", 42, 800, "#4a2d14", "middle", 6, "Inter")}''', SKY)
S[4] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#5a3a22"/><rect x="0" y="780" width="{W}" height="300" fill="#7a5232" stroke="{INK}" stroke-width="6"/>
<rect x="1180" y="160" width="520" height="340" fill="#f2c27b" stroke="{INK}" stroke-width="8"/>{pyramid(1440, 500, 380, 0.35, LIME)}
{ava_eg(380, 230, 1.45, "smile", 4)}{"".join(loaf(1060 + i * 110, 800 - (i % 2) * 20, 1.1) for i in range(7))}''')
S[5] = lambda: svg(f'''{sky("#3b4f7a", "#f2a86b", 600)}<rect x="0" y="600" width="{W}" height="480" fill="#7a5232"/>
{"".join(f'<rect x="{80+i*300}" y="640" width="240" height="40" fill="#5a3a22" stroke="{INK}" stroke-width="5"/>' + "".join(loaf(110+i*300+j*58, 640, 0.65) for j in range(4)) for i in range(6))}
{"".join(f'<rect x="{80+i*300}" y="880" width="240" height="40" fill="#5a3a22" stroke="{INK}" stroke-width="5"/>' + "".join(loaf(110+i*300+j*58, 880, 0.65) for j in range(4)) for i in range(6))}
{text(960, 200, "THOUSANDS OF LOAVES. EVERY DAY.", 70, 900, "#fff3d6", "middle", 2)}''')
S[6] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#24140c"/><ellipse cx="960" cy="900" rx="1000" ry="300" fill="#ff7a2a" opacity="0.35" filter="url(#b30)"/>
<rect x="0" y="820" width="{W}" height="260" fill="#3a1e10"/>{"".join(f'<circle cx="{random.Random(i).uniform(0,W):.0f}" cy="{random.Random(i+9).uniform(820,1080):.0f}" r="{random.Random(i+3).uniform(4,12):.0f}" fill="#ff9a3a" opacity="0.8"/>' for i in range(120))}
{"".join(pot(260 + i * 280, 860, 1.6) for i in range(6))}
{"".join(f'<path d="M{300+i*280} 600 Q{280+i*280} 500 {310+i*280} 420" stroke="#9a8a7a" stroke-width="10" fill="none" opacity="0.4" stroke-linecap="round"/>' for i in range(6))}''')
S[7] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1a1410"/><ellipse cx="760" cy="540" rx="600" ry="520" fill="{GOLD}" opacity="0.12"/>
<g transform="translate(560 140)"><path d="M120 120 Q100 0 260 -10 Q420 0 400 120 L480 520 L40 520 Z" fill="{GOLD}" stroke="{INK}" stroke-width="10"/>
{"".join(f'<path d="M{60+i*30} {200+i*30} L{460-i*0} {200+i*30}" stroke="#2a5aa0" stroke-width="12" opacity="0.8"/>' for i in range(0,10,2))}
<ellipse cx="260" cy="230" rx="110" ry="140" fill="{SKINW}" stroke="{INK}" stroke-width="8"/><path d="M200 220 L235 220 M285 220 L320 220" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
<path d="M250 360 L270 360 L268 470 L252 470 Z" fill="#3a2a1e" stroke="{INK}" stroke-width="5"/></g>
{bigtext(1450, 520, "KHUFU", 220, GOLD)}{text(1450, 610, "PHARAOH OF EGYPT", 48, 800, "#f4f1ea", "middle", 8, "Inter")}''')
S[8] = lambda: svg(f'''{sky("#f5d49a", "#efb36e")}{pyramid(1300, 640, 900, 0.45, LIME)}
<rect x="0" y="640" width="{W}" height="440" fill="{SAND}"/>{"".join(house(40 + i * 260, 640 + (i % 3) * 60, 220, 160, ["#c99a62", "#b9874f", "#d6aa72"][i % 3]) for i in range(8))}
{palm(1780, 900, 1.0)}{ava_eg(100, 760, 0.7, "calm", 12)}''', SKY)
S[9] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1b1612"/>{bigtext(960, 520, "SLAVES?", 260, "#f4f1ea")}
<path d="M520 360 L1400 620" stroke="{RED}" stroke-width="38" stroke-linecap="round"/>{text(960, 760, "That is not what I saw.", 64, 700, GOLD, "middle", 0, "Inter")}''')
S[10] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#f0dfbd"/>{text(960, 170, "THE WAGES", 90, 900, "#4a2d14", "middle", 8)}
{loaf(330, 560, 2.6)}{pot(760, 600, 1.8)}
<g transform="translate(1180 470)">{"".join(f'<circle cx="{i*70}" cy="{(i%2)*40}" r="50" fill="#e9d8c8" stroke="{INK}" stroke-width="6"/><path d="M{i*70} {-50+(i%2)*40} q10 -40 30 -50" stroke="#4a8a3a" stroke-width="8" fill="none"/>' for i in range(3))}</g>
<g transform="translate(1550 500)"><path d="M-110 0 Q0 -80 110 0 Q0 80 -110 0 Z M110 0 L170 -50 L170 50 Z" fill="#8fb3c4" stroke="{INK}" stroke-width="6"/><circle cx="-60" cy="-10" r="8" fill="{INK}"/></g>
{"".join(text(x, 800, s, 48, 800, "#4a2d14", "middle", 4, "Inter") for x, s in ((330, "BREAD"), (760, "BEER"), (1250, "ONIONS"), (1550, "FISH")))}''', "#f0dfbd")
S[11] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b", 700)}<rect x="0" y="700" width="{W}" height="380" fill="{SAND}"/>
{block(300, 520, 520, 200)}{block(1100, 560, 420, 160)}{worker(380, 380, 1.0, "chisel")}{worker(640, 380, 1.0, "chisel", True)}{worker(1220, 420, 0.95, "chisel")}
{"".join(f'<path d="M{560+i*20} {470-i*14} l12 -10" stroke="#fff3c4" stroke-width="5"/>' for i in range(5))}''', SKY)
S[12] = lambda: svg(f'''{sky("#cfe3e6", "#f2d9a6", 560)}<rect x="0" y="560" width="{W}" height="520" fill="{NILE}"/>
{"".join(f'<path d="M{i*160} {620+(i%4)*90} l100 0" stroke="#9fd0cf" stroke-width="5" opacity="0.6"/>' for i in range(14))}
{"".join(palm(150 + i * 420, 600, 0.8) for i in range(5))}{worker(1300, 480, 1.1, "stand")}<path d="M1420 520 L1500 760" stroke="#6b4a2e" stroke-width="12"/>
{text(960, 140, "WHEN THE NILE FLOODED THE FIELDS", 62, 900, "#22404a", "middle", 2)}''')
S[13] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b", 720)}<rect x="0" y="720" width="{W}" height="360" fill="{SAND}"/>
{"".join(worker(160 + i * 200, 420 + (i % 2) * 20, 1.0, "up" if i % 3 == 0 else "stand", i % 2 == 1) for i in range(8))}
<rect x="560" y="140" width="800" height="150" fill="{RED}" stroke="{INK}" stroke-width="8"/>{text(960, 240, "ONE TEAM", 90, 900, "#fff3d6", "middle", 8)}''', SKY)
S[14] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2018"/>{block(160, 160, 1600, 760, "#cdbd98")}
<g transform="rotate(-4 960 540)"><text x="960" y="520" font-family="Inter Display" font-weight="900" font-size="150" text-anchor="middle" fill="{RED}" opacity="0.85">FRIENDS OF</text>
<rect x="560" y="580" width="800" height="220" rx="110" fill="none" stroke="{RED}" stroke-width="14" opacity="0.85"/>
<text x="960" y="745" font-family="Inter Display" font-weight="900" font-size="150" text-anchor="middle" fill="{RED}" opacity="0.85">KHUFU</text></g>
<ellipse cx="320" cy="300" rx="420" ry="380" fill="#ffcf7a" opacity="0.22"/>''')
S[15] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e8c890"/><path d="M0 300 L700 300 L760 1080 L0 1080 Z" fill="#d8b678" stroke="{INK}" stroke-width="8"/>
<path d="M1100 1080 L1180 260 L1920 260 L1920 1080 Z" fill="#cfa96a" stroke="{INK}" stroke-width="8"/>{block(700, 640, 480, 300, LIME)}
<path d="M700 640 L1180 640" stroke="{RED}" stroke-width="6" stroke-dasharray="20 14"/>{worker(760, 360, 1.0, "chisel")}{worker(1000, 360, 1.0, "chisel", True)}''')
S[16] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#161a24"/>
{"".join(f'<rect x="{180+(i%60)*26}" y="{520+(i//60)*26}" width="20" height="20" fill="{LIME}" opacity="{0.4+0.6*((i*37)%11)/11:.2f}"/>' for i in range(60*18))}
{bigtext(960, 300, "2,300,000", 220, GOLD)}{text(960, 420, "BLOCKS OF STONE", 60, 900, "#f4f1ea", "middle", 10)}''')
S[17] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#efe2c4"/><rect x="0" y="820" width="{W}" height="260" fill="{SAND2}"/>
{block(240, 480, 560, 340)}{text(520, 680, "2.5 TONS", 90, 900, INK, "middle")}
<g transform="translate(1100 600)"><path d="M0 220 L40 120 Q60 60 160 60 L420 60 Q500 60 540 120 L620 140 Q660 150 660 220 Z" fill="#7a8a99" stroke="{INK}" stroke-width="7"/>
<circle cx="140" cy="220" r="60" fill="#2a2c33" stroke="{INK}" stroke-width="7"/><circle cx="520" cy="220" r="60" fill="#2a2c33" stroke="{INK}" stroke-width="7"/></g>
{text(1430, 520, "HEAVIER THAN A CAR", 54, 900, RED, "middle", 4, "Inter")}''')
S[18] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#201812"/>
{"".join(f'<g transform="translate({300+i*660} 380)"><circle cx="0" cy="0" r="170" fill="#2e241c" stroke="{GOLD}" stroke-width="8"/>{ic}<path d="M-130 -130 L130 130" stroke="{RED}" stroke-width="22" stroke-linecap="round"/></g>' for i, ic in enumerate([
 f'<circle r="90" fill="none" stroke="#f4f1ea" stroke-width="16"/><path d="M0 -90 L0 90 M-90 0 L90 0" stroke="#f4f1ea" stroke-width="10"/>',
 f'<path d="M-90 40 L60 -80 L90 -50 L-60 70 Z" fill="#9aa0a8" stroke="#f4f1ea" stroke-width="6"/>',
 f'<rect x="-90" y="-50" width="180" height="100" fill="#e2b13a" stroke="#f4f1ea" stroke-width="6"/><circle cx="-50" cy="60" r="26" fill="#f4f1ea"/><circle cx="50" cy="60" r="26" fill="#f4f1ea"/>'])) }
{text(300, 640, "NO WHEELS", 54, 900, "#f4f1ea", "middle", 4)}{text(960, 640, "NO IRON", 54, 900, "#f4f1ea", "middle", 4)}{text(1620, 640, "NO MACHINES", 54, 900, "#f4f1ea", "middle", 4)}
{bigtext(960, 900, "SO HOW?", 160, GOLD)}''')
S[19] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b")}{pyramid(1420, 820, 800, 0.6)}{dunes(820)}{ava_eg(160, 200, 1.5, "smile", 8)}
<rect x="820" y="160" width="900" height="360" rx="30" fill="#1b1d23" opacity="0.92"/>{text(1270, 270, "HOW DID THEY LIFT THE STONES?", 46, 900, "#f4f1ea", "middle")}
{text(1270, 350, "Tell me in the comments", 40, 600, TEAL, "middle", 0, "Inter")}<rect x="1070" y="400" width="400" height="90" rx="45" fill="#e23b3b"/>{text(1270, 462, "SUBSCRIBE", 44, 900, "#ffffff", "middle")}''', SKY)
S[20] = lambda: svg(f'''{sky("#7a8fbf", "#f6b97a")}{sun(1700, 760, 90, "#ffd27a")}<rect x="0" y="760" width="{W}" height="320" fill="#b88a50"/>
{palm(260, 820, 1.2)}{palm(1500, 800, 0.9)}{"".join(house(600 + i * 230, 620, 200, 140) for i in range(3))}{ava_eg(860, 420, 1.0, "determined", 14)}''')
S[21] = lambda: svg(f'''{sky("#bfe0e8", "#f7d9a6", 640)}<rect x="0" y="640" width="{W}" height="440" fill="{NILE}"/>
{"".join(f'<path d="M{(i*137)%1900} {700+(i*53)%360} l90 0" stroke="#9fd0cf" stroke-width="5" opacity="0.6"/>' for i in range(30))}
{boat(520, 760, 1.3, False)}{ava_eg(820, 470, 0.7, "smile", 10)}{worker(1120, 500, 0.85, "stand", True)}''')
S[22] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9d8b0"/><path d="M1000 0 Q930 300 1010 540 Q1090 800 980 1080" fill="none" stroke="{NILE}" stroke-width="90"/>
<path d="M1010 600 Q800 640 640 700" fill="none" stroke="{NILE}" stroke-width="30" stroke-dasharray="40 20"/>
<circle cx="1260" cy="560" r="26" fill="{LIME}" stroke="{INK}" stroke-width="6"/>{text(1300, 545, "TURA", 64, 900, INK)}{text(1300, 600, "white limestone", 36, 600, "#4a2d14", "start", 0, "Inter")}
<polygon points="560,720 660,720 610,640" fill="{GOLD}" stroke="{INK}" stroke-width="6"/>{text(470, 800, "GIZA", 64, 900, INK, "middle")}
{text(820, 900, "CANAL", 36, 800, NILE, "middle", 6, "Inter")}{text(1100, 160, "THE NILE", 48, 900, NILE, "start", 8, "Inter")}''', "#e9d8b0")
S[23] = lambda: svg(f'''{sky("#f2c27b", "#e7895a", 600)}{pyramid(1500, 600, 600, 0.5, "#e9dcc0")}<rect x="0" y="600" width="{W}" height="480" fill="#3d7a78"/>
{boat(120, 820, 0.9)}{boat(860, 980, 1.0)}{boat(1380, 760, 0.6)}''')
S[24] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b", 760)}<rect x="0" y="760" width="{W}" height="320" fill="#3d7a78"/>
{worker(760, 300, 1.6, "stand")}<g transform="translate(1000 560) rotate(-10)"><rect width="160" height="110" fill="#efe0b8" stroke="{INK}" stroke-width="5"/></g>
{"".join(f'<circle cx="{120+(i%10)*56}" cy="{820+(i//10)*56}" r="18" fill="{SKINW}" stroke="{INK}" stroke-width="4"/>' for i in range(40))}
{text(1500, 300, "INSPECTOR", 60, 900, "#4a2d14", "middle", 8)}{bigtext(1500, 430, "MERER", 150, GOLD)}{text(1500, 520, "+ about 40 men", 46, 700, "#4a2d14", "middle", 0, "Inter")}''', SKY)
S[25] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2018"/><g transform="rotate(-3 960 540)"><rect x="300" y="160" width="1320" height="760" fill="#e9d6a6" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{380+(j%5)*240} {240+(j//5)*90} ' + " ".join(f'l{random.Random(j*9+k).uniform(10,30):.0f} {random.Random(j*7+k).uniform(-12,12):.0f} m8 0' for k in range(9)) + f'" stroke="#2a1a10" stroke-width="7" fill="none" stroke-linecap="round"/>' for j in range(40))}
{"".join(f'<path d="M{380+(j%5)*240} {240+(j//5)*90+40} l120 0" stroke="#a83a2a" stroke-width="6" opacity="0.6"/>' for j in range(0, 40, 7))}</g>
<path d="M1500 980 L1760 640" stroke="#6b4a2e" stroke-width="16" stroke-linecap="round"/>''')
S[26] = lambda: svg(f'''{sky("#9cc8e6", "#f2e0b8", 520)}<rect x="0" y="420" width="{W}" height="120" fill="#2f7fa8"/><rect x="0" y="540" width="{W}" height="540" fill="#d9bf8a"/>
{text(1700, 400, "RED SEA", 40, 900, "#0d3a52", "end", 8, "Inter")}
{"".join(f'<g transform="translate({300+i*300} {760+(i%2)*80}) rotate({(i*23)%30-15})"><rect width="{120+(i%3)*30}" height="70" fill="#e9d6a6" stroke="{INK}" stroke-width="4"/><path d="M14 24 l60 0 M14 44 l80 0" stroke="#2a1a10" stroke-width="5"/></g>' for i in range(5))}
<g transform="translate(1500 640) rotate(30)"><rect x="0" y="0" width="30" height="220" fill="#8a5a2e" stroke="{INK}" stroke-width="5"/><path d="M-20 220 L50 220 L40 300 L-10 300 Z" fill="#c9a36a" stroke="{INK}" stroke-width="5"/></g>
{text(960, 160, "WADI AL-JARF, 2013", 70, 900, "#1d2a3a", "middle", 4)}''')
S[27] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#14100c"/><ellipse cx="960" cy="540" rx="800" ry="400" fill="{GOLD}" opacity="0.10"/>
{text(960, 380, "THE DIARY OF MERER", 64, 800, GOLD, "middle", 12, "Inter")}{bigtext(960, 580, "THE OLDEST", 180, "#f4f1ea")}{bigtext(960, 760, "PAPYRUS IN EGYPT", 130, TEAL)}''')
S[28] = lambda: svg(f'''{sky("#f7d79a", "#eab06a", 600)}<rect x="0" y="600" width="{W}" height="480" fill="#c9a36a"/><rect x="0" y="600" width="600" height="140" fill="#3d7a78"/>
{boat(-60, 700, 0.8, False, False)}<path d="M620 520 L620 220 L980 220" fill="none" stroke="#6b4a2e" stroke-width="20"/><path d="M980 220 L980 420" stroke="{INK}" stroke-width="6"/>
{block(900, 420, 180, 110)}{sledge(860, 880, 1.2)}{worker(1300, 600, 0.9, "up")}''')
S[29] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9c88a"/><rect x="0" y="760" width="{W}" height="320" fill="{SAND}"/>
{sledge(80, 840, 1.4)}<path d="M480 830 L1900 560" stroke="#8a6a3a" stroke-width="10"/><path d="M480 860 L1900 640" stroke="#8a6a3a" stroke-width="10"/>
{"".join(worker(560 + i * 170, 430 - i * 32, 0.85, "pull") for i in range(8))}''')
S[30] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9c88a"/><rect x="0" y="720" width="{W}" height="360" fill="{SAND}"/>
<path d="M300 800 Q900 760 1500 820 L1500 900 Q900 870 300 900 Z" fill="#9a7a4a" opacity="0.7"/>{sledge(1200, 760, 1.2)}
{worker(420, 420, 1.2, "chisel")}<g transform="translate(560 520) rotate(40)">{pot(0, 0, 0.9)}</g>
{"".join(f'<path d="M{640+i*14} {600+i*6} q-6 {80+i*10} 10 {150+i*6}" stroke="#7ac0e8" stroke-width="7" fill="none" opacity="0.85"/>' for i in range(4))}''')
S[31] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#f2c27b"/><ellipse cx="900" cy="560" rx="700" ry="520" fill="#fff3d0" opacity="0.4"/>{ava_eg(560, 120, 2.0, "smile", -6)}
{text(1550, 300, "HA!", 160, 900, "#4a2d14", "middle")}{text(1550, 420, "water the sand?", 54, 700, "#4a2d14", "middle", 0, "Inter")}''', "#f2c27b")
S[32] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#191d26"/><path d="M960 120 L960 980" stroke="#3a3f4c" stroke-width="6"/>
{text(480, 200, "DRY SAND", 70, 900, "#f4f1ea", "middle", 4)}{text(1440, 200, "WET SAND", 70, 900, TEAL, "middle", 4)}
<rect x="80" y="760" width="800" height="200" fill="{SAND}"/>{sledge(220, 760, 1.0)}<path d="M170 760 Q250 700 300 760 Q350 690 420 760" fill="{SAND}" stroke="{INK}" stroke-width="5"/>
<rect x="1040" y="760" width="800" height="200" fill="#8a6a3a"/>{sledge(1180, 760, 1.0)}
<path d="M760 560 L860 560" stroke="#ff6b6b" stroke-width="40" stroke-linecap="round"/><path d="M1720 560 L1760 560" stroke="{TEAL}" stroke-width="40" stroke-linecap="round"/>
{bigtext(1480, 480, "ABOUT HALF THE FORCE", 64, "#f4f1ea")}''')
S[33] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b")}{pyramid(960, 900, 1300, 0.62)}
<polygon points="40,900 760,900 760,440 640,440" fill="#b98a52" stroke="{INK}" stroke-width="7"/>{"".join(block(150 + i * 120, 820 - i * 82, 70, 46) for i in range(5))}
<rect x="0" y="900" width="{W}" height="180" fill="{SAND}"/>''', SKY)
S[34] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#efe2c4"/>
{"".join(f'<g transform="translate({340+i*620} 0)">{pyramid(0, 760, 460, 0.8, LIME)}{rp}</g>' for i, rp in enumerate([
 '<path d="M-330 760 L-60 520" stroke="#8a5a2e" stroke-width="22"/>',
 '<path d="M-200 760 L120 680 L-150 600 L80 540" stroke="#8a5a2e" stroke-width="18" fill="none"/>',
 '<path d="M-230 740 L230 740 L150 620 L-150 620 L-90 520 L90 520" stroke="#8a5a2e" stroke-width="16" fill="none"/>']))}
{"".join(text(340+i*620, 880, s, 50, 900, "#4a2d14", "middle", 4) for i, s in enumerate(["STRAIGHT?", "ZIGZAG?", "SPIRAL?"]))}
{text(960, 170, "NOBODY KNOWS FOR SURE", 76, 900, RED, "middle", 4)}''', "#efe2c4")
S[35] = lambda: svg(f'''{sky("#f6c48a", "#d9734a", 640)}<rect x="0" y="640" width="{W}" height="440" fill="{NILE}"/>
<path d="M0 640 L300 420 L520 640 Z M1400 640 L1680 360 L1920 560 L1920 640 Z" fill="#9a4a3a" stroke="{INK}" stroke-width="7"/>
<g transform="translate(560 820)">{boat(0, 0, 1.2, False)}{block(130, -160, 340, 130, "#b8564a")}</g>
<path d="M200 200 L1720 200" stroke="#4a2d14" stroke-width="6" stroke-dasharray="24 14"/>{text(200, 170, "ASWAN", 54, 900, "#4a2d14")}{text(1720, 170, "GIZA", 54, 900, "#4a2d14", "end")}
{text(960, 290, "~800 KM UP THE NILE  ·  UP TO 80 TONS", 50, 900, "#fff3d6", "middle", 4)}''')
S[36] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a2418"/><ellipse cx="960" cy="600" rx="800" ry="420" fill="{DUSK}" opacity="0.22"/>
<rect x="420" y="640" width="1080" height="40" fill="#7a5a36" stroke="{INK}" stroke-width="6"/>{worker(360, 460, 1.0, "stand")}{worker(1440, 460, 1.0, "stand", True)}
<g transform="translate(700 520) rotate(90 120 120)">{worker(0, -60, 0.8, "stand")}</g>
<path d="M0 940 L{W} 940" stroke="{INK}" stroke-width="8"/>''')
S[37] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9dcc0"/><path d="M200 640 Q700 560 1500 620" stroke="{INK}" stroke-width="150" fill="none" stroke-linecap="round"/>
<path d="M200 640 Q700 560 1500 620" stroke="{SKINW}" stroke-width="130" fill="none" stroke-linecap="round"/>
{"".join(f'<rect x="{560+i*130}" y="520" width="40" height="220" rx="6" fill="#a37a4a" stroke="{INK}" stroke-width="5"/>' for i in range(4))}
{"".join(f'<path d="M{600+i*90} 520 Q{620+i*90} 640 {600+i*90} 740" stroke="{LINEN}" stroke-width="30" fill="none"/>' for i in range(6))}
{text(960, 260, "BONES WERE SET", 100, 900, RED, "middle", 4)}''', "#e9dcc0")
S[38] = lambda: svg(f'''{sky("#5a3f6b", "#e8875a", 700)}{pyramid(1250, 700, 1000, 1.0, "#c9a878", "#9a7a54")}<rect x="0" y="700" width="{W}" height="380" fill="#a77d45"/>
{"".join(f'<path d="M{100+i*170} {900+(i%2)*40} l60 -70 l60 70 Z" fill="#c4964f" stroke="{INK}" stroke-width="5"/>' for i in range(10))}
{loaf(400, 1000, 0.8)}{pot(520, 1010, 0.6)}''')
S[39] = lambda: svg(f'''{stars(320, 39)}<path d="M380 160 L1100 120" stroke="#f4f1ea" stroke-width="3" opacity="0.5"/>
<circle cx="1100" cy="120" r="10" fill="#fff"/><circle cx="380" cy="160" r="8" fill="#fff"/>
<rect x="0" y="860" width="{W}" height="220" fill="#1a1f33"/>{worker(1300, 450, 1.3, "up")}
{bigtext(560, 640, "HEMIUNU", 150, GOLD)}{text(560, 730, "THE KING'S ARCHITECT", 46, 800, "#f4f1ea", "middle", 6, "Inter")}''', NIGHT)
S[40] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9d8b0"/><g transform="translate(960 560) rotate(0)">
<polygon points="-340,-340 340,-340 340,340 -340,340" fill="{LIME}" stroke="{INK}" stroke-width="8"/><path d="M-340 -340 L340 340 M340 -340 L-340 340" stroke="{INK}" stroke-width="5" opacity="0.5"/></g>
<path d="M960 60 L960 190" stroke="{RED}" stroke-width="16"/><polygon points="960,30 930,90 990,90" fill="{RED}"/>
{text(1010, 110, "N", 70, 900, RED)}{text(1430, 580, "E", 70, 900, INK)}{text(470, 580, "W", 70, 900, INK)}{text(960, 1040, "S", 70, 900, INK, "middle")}''', "#e9d8b0")
S[41] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1b1612"/>{"".join(f'<circle cx="{180+i*82}" cy="760" r="28" fill="{GOLD}" opacity="{0.25+0.75*i/19:.2f}"/>' for i in range(20))}
{bigtext(960, 520, "20 YEARS", 260, "#f4f1ea")}''')
S[42] = lambda: svg(f'''{sky("#f7d79a", "#e9b06b", 620)}{pyramid(1350, 620, 820, 0.9)}<rect x="0" y="620" width="{W}" height="460" fill="{SAND}"/>
{"".join(house(30 + i * 300, 560, 240, 150) for i in range(3))}{worker(700, 720, 0.55, "up")}{worker(860, 740, 0.5, "stand", True)}{worker(1000, 720, 0.55, "up")}
<circle cx="800" cy="960" r="22" fill="#8a3b1e" stroke="{INK}" stroke-width="5"/>{ava_eg(1450, 640, 0.75, "smile", -8)}''', SKY)
S[43] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#9cc6e0"/>{sun(1560, 220, 120, "#fff7d6")}<ellipse cx="960" cy="500" rx="900" ry="500" fill="#fff" opacity="0.25"/>
{pyramid(960, 880, 1200, 1.0, "#fbf7ee", "#e9e0cc", False)}<path d="M420 880 L960 112" stroke="#ffffff" stroke-width="18" opacity="0.8"/>{dunes(880)}''', "#9cc6e0")
S[44] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#e9eef2"/><rect x="0" y="900" width="{W}" height="180" fill="{SAND}"/>
{pyramid(760, 900, 1000, 1.0, "#fbf7ee", "#e9e0cc", False)}<path d="M1380 900 L1380 260" stroke="{INK}" stroke-width="6"/><path d="M1350 260 L1410 260 M1350 900 L1410 900" stroke="{INK}" stroke-width="6"/>
{bigtext(1640, 540, "146 m", 160, RED)}{text(1640, 630, "about 481 feet", 46, 700, INK, "middle", 0, "Inter")}{worker(1500, 870, 0.1)}''', "#e9eef2")
S[45] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#141821"/><path d="M180 620 L1740 620" stroke="#f4f1ea" stroke-width="8"/>
<circle cx="180" cy="620" r="24" fill="{GOLD}"/><circle cx="1740" cy="620" r="24" fill="{TEAL}"/>{text(180, 700, "c. 2560 BC", 50, 900, GOLD, "middle")}{text(1740, 700, "1300s AD", 50, 900, TEAL, "middle")}
{pyramid(180, 590, 160, 1.0)}{bigtext(960, 420, "TALLEST ON EARTH", 120, "#f4f1ea")}{text(960, 820, "for almost 4,000 years", 60, 700, "#cfd3da", "middle", 0, "Inter")}''')
S[46] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#cfe2ee"/>{pyramid(960, 900, 1300, 1.0, "#c9a878", "#a88a5e")}
{"".join(f'<path d="M{960-650+i*30} {900-i*48} l{1300-i*60} 0" stroke="{INK}" stroke-width="4" opacity="0.4" stroke-dasharray="30 8"/>' for i in range(18))}
<polygon points="320,900 600,900 620,860 340,860" fill="#fbf7ee" stroke="{INK}" stroke-width="5"/>{dunes(900)}
{text(960, 160, "THE WHITE CASING IS GONE", 70, 900, "#2a3a4a", "middle", 4)}''', "#cfe2ee")
S[47] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0c0906"/><ellipse cx="1300" cy="520" rx="700" ry="480" fill="#ff9a3a" opacity="0.18"/>
{block(500, 300, 1100, 480, "#5a4a36")}<text x="1050" y="600" font-family="Inter Display" font-weight="900" font-size="110" text-anchor="middle" fill="{RED}" opacity="0.75">FRIENDS OF KHUFU</text>
<path d="M1700 900 L1640 520" stroke="#6b4a2e" stroke-width="20"/><path d="M1640 520 q-30 -60 0 -110 q30 50 0 110" fill="#ffb84a" stroke="{INK}" stroke-width="4"/>''')
S[48] = lambda: svg(f'''{sky("#f2c27b", "#e0875a")}{pyramid(1500, 820, 600, 1.0)}{dunes(820)}<ellipse cx="660" cy="560" rx="600" ry="500" fill="url(#ylamp)"/>{ava_eg(260, 160, 1.8, "smile", 6)}
{bigtext(1360, 380, "I'M AVA.", 120)}{bigtext(1360, 520, "AND I WAS THERE.", 84, TEAL)}''', SKY)
S[49] = lambda: svg(f'''{text(960, 220, "WHERE SHOULD I GO NEXT?", 100, 900, "#f4f1ea", "middle", -2)}
{"".join(f'<rect x="{240+i*370}" y="320" width="330" height="300" rx="24" fill="#1b1d23" stroke="{TEAL}" stroke-width="6"/>' + text(405+i*370, 520, ic, 140, 900, TEAL, "middle") for i, ic in enumerate(["?", "?", "?", "?"]))}
{text(960, 760, "Write it in the comments. The best idea might be my next story.", 44, 500, "#cfd3da", "middle")}
<rect x="760" y="860" width="400" height="100" rx="50" fill="#e23b3b"/>{text(960, 928, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}''', "#14110e")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
