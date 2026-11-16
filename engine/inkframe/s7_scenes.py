import os, sys, math, random
sys.path.insert(0, "/home/claude/wn")
import kit
kit.ACC = "#FF7A1A"            # Signal 7 accent: warning orange
from kit import svg, text, render, rain, INK, W, H
ACC = kit.ACC
ICE = "#7fd6ff"
SUIT = "#e8e4dc"
SKIN2 = "#c9a58a"
OUT = "ep1/scenes"
os.makedirs(OUT, exist_ok=True)

def mara(x, y, s=1.0, mood="calm", look=0, pose="bust", headset=True):
    brow = {"calm": "M162 108 L188 106 M212 106 L238 108", "worried": "M160 102 Q175 110 190 108 M210 108 Q225 110 240 102",
            "scared": "M160 100 Q175 90 190 104 M210 104 Q225 90 240 100", "smile": "M162 104 Q175 98 188 104 M212 104 Q225 98 238 104"}[mood]
    mouth = {"calm": f'<path d="M190 184 L214 184" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "worried": f'<path d="M188 188 Q202 178 216 188" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "scared": f'<ellipse cx="202" cy="186" rx="9" ry="11" fill="{INK}"/>',
             "smile": f'<path d="M186 180 Q202 196 218 180" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'}[mood]
    e = look
    head = f'''
  <path d="M118 150 Q110 40 200 34 Q292 40 284 150 L290 230 Q250 214 240 170 L160 170 Q150 214 110 230 Z" fill="#2a2320" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <ellipse cx="200" cy="146" rx="66" ry="78" fill="{SKIN2}" stroke="{INK}" stroke-width="7"/>
  <path d="M134 120 Q150 60 214 64 Q262 70 268 120 Q230 92 196 98 Q160 100 134 120 Z" fill="#2a2320" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
  <path d="{brow}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="{176+e}" cy="140" rx="7" ry="10" fill="{INK}"/><ellipse cx="{226+e}" cy="140" rx="7" ry="10" fill="{INK}"/>
  <path d="M{202+e/2} 146 Q{196+e/2} 162 {206+e/2} 164" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  {mouth}'''
    hs = f'''<path d="M128 146 Q130 60 200 56 Q272 60 274 146" fill="none" stroke="#3b3f47" stroke-width="10"/>
  <rect x="112" y="128" width="26" height="46" rx="10" fill="#3b3f47" stroke="{INK}" stroke-width="5"/>
  <path d="M126 172 Q140 210 182 206" fill="none" stroke="#3b3f47" stroke-width="6"/><circle cx="184" cy="206" r="7" fill="{ACC}"/>''' if headset else ""
    torso = f'''<path d="M108 248 Q200 222 292 248 Q326 320 318 440 L82 440 Q74 320 108 248 Z" fill="#3c4a5a" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M150 240 L200 300 L250 240" fill="none" stroke="{INK}" stroke-width="6"/>
  <rect x="236" y="300" width="50" height="30" rx="5" fill="{ACC}" stroke="{INK}" stroke-width="4"/>
  <rect x="112" y="300" width="60" height="16" rx="4" fill="#d8dde3" stroke="{INK}" stroke-width="3"/>'''
    if pose == "suit":
        return f'''<g transform="translate({x} {y}) scale({s})">
  <path d="M70 250 Q200 200 330 250 Q360 340 350 470 L50 470 Q40 340 70 250 Z" fill="{SUIT}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
  <rect x="150" y="300" width="100" height="70" rx="10" fill="#9aa3ad" stroke="{INK}" stroke-width="6"/>
  <circle cx="175" cy="335" r="9" fill="{ACC}"/><circle cx="205" cy="335" r="9" fill="{ICE}"/>
  <path d="M60 330 L120 330 M280 330 L340 330" stroke="{ACC}" stroke-width="12"/>
  {head}
  <circle cx="200" cy="140" r="122" fill="{ICE}" opacity="0.12" stroke="{INK}" stroke-width="9"/>
  <path d="M120 80 Q150 50 190 44" fill="none" stroke="#ffffff" stroke-width="10" opacity="0.5" stroke-linecap="round"/>
  <rect x="96" y="240" width="208" height="30" rx="12" fill="#9aa3ad" stroke="{INK}" stroke-width="7"/></g>'''
    return f'<g transform="translate({x} {y}) scale({s})">{torso}{head}{hs}</g>'

def stars(n, seed, y1=H):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,y1):.0f}" r="{r.uniform(1,3):.1f}" fill="#fff" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(n))

def jupiter(cx, cy, r):
    bands = "".join(f'<rect x="{cx-r}" y="{cy-r+i*r*2/9:.0f}" width="{2*r}" height="{r*2/9:.0f}" fill="{c}"/>' for i, c in enumerate(
        ["#c9a27a", "#e3c9a3", "#b07a52", "#e9d6b6", "#a8683f", "#dcc19b", "#b8865c", "#e6cfaa", "#c39a72"]))
    return f'''<defs><clipPath id="jc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <radialGradient id="jsh" cx="0.35" cy="0.35" r="0.75"><stop offset="0.5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.75"/></radialGradient></defs>
  <g clip-path="url(#jc)">{bands}<ellipse cx="{cx+r*0.3}" cy="{cy+r*0.25}" rx="{r*0.16}" ry="{r*0.09}" fill="#b5532f"/></g>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#jsh)" stroke="{INK}" stroke-width="6"/>'''

def interior(extra, alarm=False, dim=1.0):
    return svg(f'''
<rect width="{W}" height="{H}" fill="#1a2028"/>
<path d="M0 0 L{W} 0 L{W} 140 Q960 220 0 140 Z" fill="#232b35" stroke="{INK}" stroke-width="8"/>
{"".join(f'<rect x="{x}" y="160" width="26" height="700" fill="#202832" stroke="{INK}" stroke-width="6"/>' for x in (180, 620, 1280, 1720))}
<path d="M0 860 L{W} 860 L{W} {H} L0 {H} Z" fill="#232a33"/><path d="M0 860 L{W} 860" stroke="{INK}" stroke-width="8"/>
{"".join(f'<rect x="{x}" y="176" width="140" height="10" rx="5" fill="{ICE}" opacity="{0.8*dim:.2f}"/>' for x in (300, 900, 1500))}
{'<rect width="1920" height="1080" fill="#ff2a2a" opacity="0.16"/>' if alarm else ''}
<rect width="1920" height="1080" fill="#000" opacity="{1-dim:.2f}"/>
{extra}''', "#161b22")

def console(x, y, w=620, h=380, inner=""):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#0d1218" stroke="{INK}" stroke-width="10"/>
  <rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" rx="10" fill="#0a1a24"/>{inner}'''

def orca_eye(cx, cy, r=120, col=None):
    col = col or ICE
    return f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0b0f14" stroke="{INK}" stroke-width="10"/>
  <circle cx="{cx}" cy="{cy}" r="{r*0.7:.0f}" fill="none" stroke="{col}" stroke-width="6" opacity="0.6"/>
  <circle cx="{cx}" cy="{cy}" r="{r*0.35:.0f}" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="{r*0.6:.0f}" fill="{col}" opacity="0.15"/>'''

def wave(x, y, w, h, kind="pulses", col=None):
    col = col or ACC
    pts = []
    r = random.Random(4)
    for i in range(0, w, 4):
        t = i / w
        if kind == "pulses":
            k = int(t * 14)
            amp = h * 0.9 if (k % 2 == 0 and abs((t * 14) % 1 - 0.5) < 0.25 and k < 14) else h * 0.05
        elif kind == "speech":
            amp = h * (0.2 + 0.8 * abs(math.sin(t * 9) * math.sin(t * 23))) * r.uniform(0.6, 1)
        else:
            amp = h * 0.08 * r.uniform(0, 1)
        pts.append(f"{x+i},{y - amp * (1 if (i//4) % 2 else -1):.0f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="4"/>'

def quote_card(lines, sub=None):
    out = "".join(text(960, 420 + i * 120, l, 92, 300, "#f4f1ea", "middle") for i, l in enumerate(lines))
    s = text(960, 420 + len(lines) * 120 + 40, sub, 40, 600, ACC, "middle", 8, "Inter") if sub else ""
    return svg(out + s, "#0b0e12")

def window_scene(e):
    return svg(f'''
<rect width="{W}" height="{H}" fill="#151a21"/>
<rect x="250" y="100" width="1000" height="640" rx="60" fill="#05070c" stroke="{INK}" stroke-width="14"/>
<clipPath id="wc"><rect x="257" y="107" width="986" height="626" rx="54"/></clipPath>
<g clip-path="url(#wc)">{stars(160, 1)}{jupiter(820, 420, 300)}
<path d="M250 640 Q600 600 900 650 T1250 630 L1250 760 L250 760 Z" fill="#cfe9f5" stroke="{INK}" stroke-width="6"/></g>
<path d="M0 860 L{W} 860 L{W} {H} L0 {H} Z" fill="#232a33"/>
{e}
<rect x="1450" y="140" width="320" height="110" rx="12" fill="#0d1218" stroke="{INK}" stroke-width="7"/>
{text(1610, 215, "DAY 211", 56, 900, ACC, "middle", 4)}''')

S = {}
S[1] = lambda: window_scene(mara(1150, 420, 1.3, "calm", -10))
S[2] = lambda: svg(f'''{stars(120, 2)}
{text(960, 470, "SIGNAL 7", 230, 900, "#f4f1ea", "middle", 6)}
{wave(460, 640, 1000, 70, "speech", ACC)}
{text(960, 780, "EPISODE 1  ·  THE VOICE UNDER THE ICE", 38, 600, "#9fb3c8", "middle", 8, "Inter")}''', "#06080c")
S[3] = lambda: svg(f'''{stars(220, 3, 700)}{jupiter(1450, 330, 380)}
<path d="M0 720 Q500 660 960 700 T1920 690 L1920 1080 L0 1080 Z" fill="#cfe6f2" stroke="{INK}" stroke-width="8"/>
<path d="M200 800 L420 760 M900 850 L1200 820 M1400 760 L1700 790" stroke="#9fc4d6" stroke-width="6"/>
<g transform="translate(560 520)">
<rect x="0" y="80" width="420" height="140" rx="20" fill="#5b6672" stroke="{INK}" stroke-width="9"/>
<path d="M60 80 Q210 -20 360 80 Z" fill="#7b8792" stroke="{INK}" stroke-width="9"/>
<rect x="420" y="130" width="160" height="70" rx="10" fill="#4b5560" stroke="{INK}" stroke-width="8"/>
<path d="M500 130 L520 -60 L540 130" fill="#4b5560" stroke="{INK}" stroke-width="8"/>
{"".join(f'<rect x="{30+i*80}" y="120" width="50" height="30" rx="6" fill="{ICE}"/>' for i in range(5))}
<path d="M210 220 L210 300 M140 220 L120 300 M280 220 L300 300" stroke="{INK}" stroke-width="10"/></g>
{text(150, 1000, "HALCYON STATION · EUROPA", 38, 800, "#2a3644", "start", 8, "Inter")}''', "#04060a")
S[4] = lambda: svg(f'''
<rect x="0" y="0" width="{W}" height="150" fill="#05070c"/>{stars(40, 4, 150)}
<rect x="0" y="150" width="{W}" height="700" fill="#bfe1ef"/>
{"".join(f'<path d="M0 {y} L1920 {y+20}" stroke="#a6cfe0" stroke-width="5"/>' for y in range(220, 840, 70))}
<rect x="0" y="850" width="{W}" height="230" fill="#0b2340"/>
<rect x="820" y="80" width="280" height="80" rx="10" fill="#5b6672" stroke="{INK}" stroke-width="8"/>
<rect x="944" y="160" width="32" height="660" fill="#1b2430" stroke="{INK}" stroke-width="6"/>
<circle cx="960" cy="830" r="22" fill="{ACC}"/>
<path d="M1200 160 L1200 850 M1180 160 L1220 160 M1180 850 L1220 850" stroke="{INK}" stroke-width="6"/>
{text(1240, 520, "3 KM OF ICE", 60, 900, "#1d2a38", "start", 2)}
{text(1240, 980, "OCEAN?", 70, 900, ICE, "start", 4)}{text(700, 860, "10 m left", 40, 800, ACC, "end", 2, "Inter")}''', "#bfe1ef")
S[5] = lambda: svg(f'''
<rect width="{W}" height="{H}" fill="#03101f"/>
{"".join(f'<circle cx="{random.Random(i).uniform(0,W):.0f}" cy="{random.Random(i+99).uniform(200,H):.0f}" r="{random.Random(i+7).uniform(2,7):.1f}" fill="{ICE}" opacity="{random.Random(i+3).uniform(.2,.8):.2f}"/>' for i in range(140))}
<path d="M0 0 L{W} 0 L{W} 160 Q960 240 0 160 Z" fill="#bfe1ef" opacity="0.9"/>
<ellipse cx="960" cy="700" rx="700" ry="300" fill="url(#blue)"/>
{text(960, 960, "DARK. WARM. OLDER THAN ANYTHING ON EARTH.", 40, 700, "#9fc4d6", "middle", 6, "Inter")}''', "#03101f")
def crew_photo():
    people = "".join(f'<g transform="translate({560+i*140} 420) scale(0.32)"><path d="M90 240 Q200 200 310 240 L330 520 L70 520 Z" fill="#3c4a5a" stroke="{INK}" stroke-width="12"/><ellipse cx="200" cy="140" rx="70" ry="80" fill="{SKIN2 if i!=3 else "#d6c6b2"}" stroke="{INK}" stroke-width="12"/><path d="M180 140 L220 140" stroke="{INK}" stroke-width="10"/></g>' for i in range(6))
    return interior(f'''<g transform="rotate(-3 960 520)"><rect x="500" y="300" width="920" height="460" fill="#efe9dc" stroke="{INK}" stroke-width="12"/>
<rect x="530" y="330" width="860" height="330" fill="#7d8a97"/>{people}
{text(960, 720, "HALCYON CREW · YEAR 1", 34, 700, "#333", "middle", 6, "Inter")}</g>''')
S[6] = crew_photo
S[7] = lambda: svg(f'''{stars(200, 7)}{jupiter(300, 260, 200)}
<g transform="translate(1100 380) rotate(-28)"><path d="M0 0 L260 40 L0 80 Z" fill="#9aa3ad" stroke="{INK}" stroke-width="8"/>
<path d="M-20 10 L-200 -10 L-200 90 L-20 70 Z" fill="{ACC}" opacity="0.7"/></g>
<path d="M0 820 Q960 760 1920 820 L1920 1080 L0 1080 Z" fill="#cfe6f2" stroke="{INK}" stroke-width="8"/>
<rect width="1920" height="1080" fill="#ff2a2a" opacity="0.12"/>
{text(150, 980, "5 WENT HOME", 70, 900, "#1d2a38")}''', "#04060a")
S[8] = lambda: svg(f'''{text(960, 520, "40", 330, 900, ACC, "middle")}
{text(960, 650, "DAYS UNTIL THE RELIEF SHIP", 56, 800, "#f4f1ea", "middle", 8, "Inter")}''', "#0b0e12")
S[9] = lambda: interior(f'''{console(1050, 300, 640, 420, orca_eye(1370, 510, 130))}{text(1370, 770, "ORCA", 50, 900, ICE, "middle", 12)}{mara(260, 360, 1.25, "calm", 10)}''')
S[10] = lambda: interior(f'''{console(360, 160, 1200, 700, "")}
{text(960, 300, "DRILL DEPTH", 50, 700, "#9fc4d6", "middle", 10, "Inter")}
{text(960, 480, "2,990 m", 180, 900, ICE, "middle")}
<rect x="560" y="560" width="800" height="40" rx="20" fill="#1b2a38"/><rect x="560" y="560" width="792" height="40" rx="20" fill="{ACC}"/>
{text(960, 700, "10 METERS TO OPEN WATER", 50, 800, ACC, "middle", 6, "Inter")}''')
S[11] = lambda: interior(f'''<ellipse cx="960" cy="560" rx="600" ry="500" fill="url(#ylamp)"/>{mara(560, 60, 2.3, "smile", 0, headset=False)}''')
S[12] = lambda: interior(f'''<rect x="300" y="620" width="1300" height="40" fill="#5b6672" stroke="{INK}" stroke-width="8"/>
<path d="M900 520 L1010 520 L1000 620 L910 620 Z" fill="#efe9dc" stroke="{INK}" stroke-width="8"/>
<path d="M1010 540 Q1050 560 1004 600" fill="none" stroke="{INK}" stroke-width="8"/>
<path d="M930 500 Q920 470 940 450 M960 505 Q950 475 970 455" stroke="#cfcfcf" stroke-width="5" fill="none" opacity="0.7"/>
{mara(1120, 300, 1.0, "calm", -14, headset=False)}''', dim=0.55)
S[13] = lambda: interior(f'''{console(560, 200, 800, 560, orca_eye(960, 470, 170, ACC))}
{text(960, 860, "SIGNAL DETECTED BELOW THE ICE", 46, 800, ACC, "middle", 6, "Inter")}''', alarm=True)
S[14] = lambda: svg(f'''{console(160, 260, 1600, 560, wave(260, 540, 1400, 200, "pulses"))}
{text(960, 200, "7 PULSES · SILENCE · 7 PULSES", 52, 800, "#f4f1ea", "middle", 6, "Inter")}''', "#0b0e12")
S[15] = lambda: interior(f'''{mara(560, 60, 2.3, "worried", 8, headset=False)}''', dim=0.7)
S[16] = lambda: interior(f'''<circle cx="960" cy="500" r="200" fill="#0d1218" stroke="{INK}" stroke-width="12"/>
<circle cx="960" cy="500" r="120" fill="#1b2430" stroke="{INK}" stroke-width="8"/><circle cx="960" cy="500" r="40" fill="{ACC}"/>
{"".join(f'<path d="M{1200+i*70} {340-i*20} Q{1260+i*80} 500 {1200+i*70} {660+i*20}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.8-i*0.2:.1f}"/><path d="M{720-i*70} {340-i*20} Q{660-i*80} 500 {720-i*70} {660+i*20}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.8-i*0.2:.1f}"/>' for i in range(4))}
{text(960, 880, "KNOCK  ·  KNOCK  ·  KNOCK", 48, 600, "#9fc4d6", "middle", 10, "Inter")}''', dim=0.6)
S[17] = lambda: svg(f'''{text(960, 500, "SIGNAL 7", 200, 900, ACC, "middle", 6)}
{text(960, 620, "REPEATS EVERY 7 MINUTES", 50, 700, "#f4f1ea", "middle", 10, "Inter")}{wave(560, 760, 800, 40, "pulses", ICE)}''', "#0b0e12")
S[18] = lambda: svg(f'''{text(960, 290, "WHAT'S UNDER THE ICE?", 96, 900, "#f4f1ea", "middle", -2)}
<rect x="610" y="420" width="420" height="120" rx="60" fill="#e23b3b"/>{text(820, 500, "SUBSCRIBE", 52, 900, "#ffffff", "middle")}
<circle cx="1150" cy="480" r="60" fill="#1d1f26" stroke="{ACC}" stroke-width="6"/>
<path d="M1120 500 Q1120 440 1150 438 Q1180 440 1180 500 L1188 510 L1112 510 Z M1140 516 Q1150 530 1160 516" fill="{ACC}"/>
{text(960, 740, "Would you stay on Halcyon alone?", 66, 700, ACC, "middle")}
{text(960, 820, "Tell me in the comments.", 44, 500, "#cfd3da", "middle")}''', "#101114")
S[19] = lambda: interior(f'''{console(1000, 260, 760, 460, wave(1060, 490, 640, 120, "pulses"))}
{text(1380, 790, "03:07", 80, 900, ACC, "middle", 4)}{mara(200, 360, 1.25, "worried", 14)}''', dim=0.6)
S[20] = lambda: svg(f'''{console(160, 260, 1600, 560, wave(260, 540, 700, 180, "pulses", ICE) + wave(960, 540, 700, 200, "speech", ACC))}
{text(960, 200, "THE PATTERN IS NOW SPEECH", 60, 900, "#f4f1ea", "middle", 4, "Inter")}''', "#0b0e12")
S[21] = lambda: quote_card(['"Mara... don\'t let them', 'take the drill up.', 'Please."'], "HER OWN VOICE")
S[22] = lambda: interior(f'''{mara(560, 60, 2.3, "scared", 0)}{wave(100, 980, 1720, 40, "speech", ACC)}''', dim=0.5)
S[23] = lambda: interior(f'''{console(460, 180, 1000, 640, "")}
{text(960, 380, "VOICE MATCH: MARA QUINN", 52, 800, ICE, "middle", 4, "Inter")}{text(960, 560, "99.8%", 170, 900, ACC, "middle")}
{text(960, 700, "RECORDINGS WITH THESE WORDS: 0", 44, 700, "#f4f1ea", "middle", 4, "Inter")}''')
S[24] = lambda: svg(f'''
<path d="M0 0 L760 0 L760 1080 L0 1080 Z" fill="#9fc8da"/><path d="M1160 0 L1920 0 L1920 1080 L1160 1080 Z" fill="#9fc8da"/>
<path d="M760 0 L1160 0 L1160 1080 L760 1080 Z" fill="#0b1a2a"/>
{"".join(f'<path d="M{760 if i%2 else 1160} {i*90} l{-40 if i%2 else 40} 30" stroke="#7fb0c6" stroke-width="6"/>' for i in range(12))}
<path d="M760 0 L760 1080 M1160 0 L1160 1080" stroke="{INK}" stroke-width="10"/>
<rect x="900" y="0" width="16" height="1080" fill="#2b3644"/><rect x="1004" y="0" width="16" height="1080" fill="#2b3644"/>
{mara(760, 380, 1.0, "worried", 0, pose="suit")}
<ellipse cx="960" cy="200" rx="300" ry="200" fill="url(#ylamp)"/>''', "#0b1a2a")
S[25] = lambda: svg(f'''{console(260, 160, 1400, 760, "")}
<rect x="300" y="200" width="1320" height="680" fill="#1d3a4e"/>
{"".join(f'<path d="M{300+i*150} 200 L{360+i*140} 880" stroke="#2b5068" stroke-width="5"/>' for i in range(9))}
{text(340, 250, "SHAFT CAM · 2,990 m", 32, 700, ICE, "start", 4, "Inter")}<circle cx="1560" cy="236" r="12" fill="#ff3b3b"/>''', "#0b0e12")
S[26] = lambda: svg(f'''
<rect width="{W}" height="{H}" fill="#14354a"/>
{"".join(f'<path d="M{i*130} 0 L{i*130+90} 1080" stroke="#1f4a63" stroke-width="5"/>' for i in range(16))}
<ellipse cx="960" cy="560" rx="420" ry="360" fill="{ICE}" opacity="0.18" filter="url(#b30)"/>
<g transform="translate(960 560) scale(1.6)" fill="#d8f3ff" opacity="0.85" stroke="{INK}" stroke-width="4">
<ellipse cx="0" cy="40" rx="70" ry="85"/>
<rect x="-70" y="-120" width="26" height="120" rx="13" transform="rotate(-12 -57 0)"/>
<rect x="-36" y="-150" width="26" height="150" rx="13"/><rect x="-2" y="-160" width="26" height="160" rx="13"/>
<rect x="32" y="-140" width="26" height="140" rx="13" transform="rotate(8 45 0)"/>
<rect x="60" y="-20" width="26" height="100" rx="13" transform="rotate(50 73 30)"/></g>
{text(960, 1000, "FROM BELOW.", 70, 900, "#f4f1ea", "middle", 8)}''', "#14354a")
S[27] = lambda: interior(f'''<rect x="760" y="300" width="400" height="520" rx="30" fill="#2b3644" stroke="{INK}" stroke-width="10"/>
<rect x="800" y="340" width="320" height="200" rx="10" fill="#0a1a24"/>{wave(820, 440, 280, 60, "speech", ICE)}
{"".join(f'<circle cx="{840+(i%5)*60}" cy="{620+(i//5)*60}" r="14" fill="#1b2430"/>' for i in range(15))}
{text(960, 940, "MISSION CONTROL · EARTH", 46, 800, ICE, "middle", 8, "Inter")}''', dim=0.7)
S[28] = lambda: svg(f'''{text(960, 470, "DO NOT", 200, 900, "#f4f1ea", "middle")}{text(960, 660, "RESPOND.", 200, 900, "#ff3b3b", "middle")}
{text(960, 780, "STOP DRILLING · SEAL THE SHAFT", 46, 700, "#9fc4d6", "middle", 8, "Inter")}''', "#0b0e12")
S[29] = lambda: svg(f'''{console(980, 200, 820, 620, "")}
<rect x="1010" y="230" width="760" height="560" fill="#14354a"/>
<g transform="translate(1390 520) scale(0.8)" fill="#d8f3ff" opacity="0.85" stroke="{INK}" stroke-width="4">
<ellipse cx="0" cy="40" rx="70" ry="85"/><rect x="-36" y="-150" width="26" height="150" rx="13"/><rect x="-2" y="-160" width="26" height="160" rx="13"/>
<rect x="32" y="-140" width="26" height="140" rx="13"/><rect x="-70" y="-120" width="26" height="120" rx="13"/></g>
{mara(160, 380, 1.15, "scared", 18, pose="suit")}''', "#0b1a2a")
S[30] = lambda: quote_card(['"Mara. Answer me.', 'I don\'t have much time."'])
S[31] = lambda: svg(f'''<circle cx="960" cy="560" r="330" fill="#5b6672" stroke="{INK}" stroke-width="16"/>
<circle cx="960" cy="560" r="250" fill="#4b5560" stroke="{INK}" stroke-width="10"/>
{"".join(f'<rect x="{940}" y="{230}" width="40" height="90" fill="{ACC}" transform="rotate({a} 960 560)"/>' for a in range(0, 360, 45))}
<path d="M760 560 L1160 560 M960 360 L960 760" stroke="{INK}" stroke-width="18"/>
{text(960, 160, "SEAL THE SHAFT?", 110, 900, "#f4f1ea", "middle", -2)}''', "#0b0e12")
S[32] = lambda: svg(f'''<rect x="760" y="300" width="400" height="520" rx="30" fill="#2b3644" stroke="{INK}" stroke-width="10"/>
<rect x="800" y="340" width="320" height="200" rx="10" fill="#0a1a24"/>{wave(820, 440, 280, 60, "speech", ACC)}
<circle cx="960" cy="680" r="70" fill="{ACC}" stroke="{INK}" stroke-width="8"/>{text(960, 698, "TALK", 40, 900, INK, "middle")}
{text(960, 200, "OR ANSWER?", 120, 900, "#f4f1ea", "middle", -2)}''', "#0b0e12")
S[33] = lambda: svg(f'''{text(960, 200, "WHAT SHOULD MARA DO?", 90, 900, "#f4f1ea", "middle", -2)}
<rect x="260" y="300" width="640" height="420" rx="28" fill="#1b1d23" stroke="{ACC}" stroke-width="8"/>
<rect x="1020" y="300" width="640" height="420" rx="28" fill="#1b1d23" stroke="{ICE}" stroke-width="8"/>
{wave(330, 460, 500, 60, "speech", ACC)}
<circle cx="1340" cy="460" r="110" fill="#5b6672" stroke="{INK}" stroke-width="10"/><path d="M1260 460 L1420 460 M1340 380 L1340 540" stroke="{INK}" stroke-width="12"/>
{text(580, 660, "ANSWER", 96, 900, ACC, "middle", 4)}{text(1340, 660, "SEAL", 96, 900, ICE, "middle", 4)}
{text(960, 830, "Comment your answer. The most popular one decides Episode 2.", 40, 500, "#cfd3da", "middle")}
<rect x="760" y="900" width="400" height="100" rx="50" fill="#e23b3b"/>{text(960, 968, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}''', "#101114")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
