"""WRONG NUMBER S01E02 - 'Door Number Nine'. Pier at 1:55 AM, open case, the woman in red."""
import os, sys, random, math
sys.path.insert(0, "/home/claude/wn")
from kit import *
from phone_helpers import big_phone, screen_call, screen_msg
OUT = "/home/claude/wn/ep2/scenes"; os.makedirs(OUT, exist_ok=True)
RED = "#c8303a"; BLUE = "#2f6fd6"; BRASS = "#c9a24a"; SEPIA = "#d9c7a4"

def big(x, y, s, size, fill="#f4f1ea", anchor="middle", sw=12):
    s = s.replace("&", "&amp;").replace("'", "&#39;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-2">{s}</text>')

def water(y=780, seed=1):
    r = random.Random(seed)
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="#0a1220"/>' + "".join(
        f'<path d="M{r.uniform(0,W):.0f} {r.uniform(y+10,H):.0f} l{r.uniform(30,120):.0f} 0" stroke="#2a3c58" stroke-width="3" opacity="0.7"/>' for _ in range(70))

def boards(y=700, col="#2b2620"):
    return (f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{col}"/>' +
            "".join(f'<path d="M0 {yy} L{W} {yy}" stroke="#1a1612" stroke-width="5"/>' for yy in range(y + 40, H, 52)) +
            f'<path d="M0 {y} L{W} {y}" stroke="{INK}" stroke-width="8"/>')

def crates(x, y, s=1.0):
    def c(cx, cy, w, h):
        return (f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" fill="#5a4630" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M{cx} {cy} L{cx+w} {cy+h} M{cx+w} {cy} L{cx} {cy+h}" stroke="{INK}" stroke-width="5" opacity="0.6"/>')
    return f'<g transform="translate({x} {y}) scale({s})">{c(0,200,260,220)}{c(260,240,220,180)}{c(60,0,220,200)}</g>'

def lamp(x, y, c="#f6e7c4"):
    return (f'<path d="M{x} {y} L{x} {y+600}" stroke="{INK}" stroke-width="14"/><path d="M{x} {y} L{x+60} {y}" stroke="{INK}" stroke-width="10"/>'
            f'<ellipse cx="{x+70}" cy="{y+14}" rx="30" ry="14" fill="{c}"/><path d="M{x+40} {y+20} L{x-80} {y+640} L{x+220} {y+640} Z" fill="{c}" opacity="0.08"/>')

def watch(cx, cy, s=1.0, glow=True):
    hands = f'<path d="M0 0 L0 -70" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M0 0 L0 -100" stroke="{INK}" stroke-width="5" stroke-linecap="round" transform="rotate(2)"/>'
    ticks_ = "".join(f'<path d="M0 -112 L0 -96" stroke="{INK}" stroke-width="6" transform="rotate({i*30})"/>' for i in range(12))
    g = f'<circle r="260" fill="{ACC}" opacity="0.12"/>' if glow else ""
    return f'''<g transform="translate({cx} {cy}) scale({s})">{g}<path d="M-30 -150 L30 -150 L22 -128 L-22 -128 Z" fill="{BRASS}" stroke="{INK}" stroke-width="6"/>
  <circle cx="0" cy="-168" r="22" fill="none" stroke="{BRASS}" stroke-width="10"/>
  <circle r="138" fill="{BRASS}" stroke="{INK}" stroke-width="9"/><circle r="120" fill="#f1e9d4" stroke="{INK}" stroke-width="5"/>{ticks_}
  {text(0, -60, "XII", 26, 800, INK, "middle", 0, "Inter")}{hands}<circle r="10" fill="{INK}"/>
  <path d="M-80 -60 L-40 -90 M60 70 L90 40" stroke="#8a7a5a" stroke-width="3" opacity="0.6"/></g>'''

def key(cx, cy, s=1.0, rot=0):
    return f'''<g transform="translate({cx} {cy}) rotate({rot}) scale({s})"><circle r="60" fill="none" stroke="{INK}" stroke-width="26"/><circle r="60" fill="none" stroke="{BRASS}" stroke-width="16"/>
  <path d="M60 0 L320 0" stroke="{INK}" stroke-width="30"/><path d="M60 0 L320 0" stroke="{BRASS}" stroke-width="18"/>
  <path d="M250 0 L250 50 L280 50 L280 20 L300 20 L300 50 L320 50 L320 0" fill="{BRASS}" stroke="{INK}" stroke-width="6"/>
  <path d="M-40 40 Q-90 120 -60 170" fill="none" stroke="#cfd3da" stroke-width="4"/>
  <g transform="translate(-110 170) rotate(-10)"><rect width="110" height="70" rx="10" fill="#efe6cf" stroke="{INK}" stroke-width="5"/>{text(55, 54, "9", 54, 900, INK, "middle")}</g></g>'''

def woman(x, y, s=1.0, mood="smile", arm=False):
    mouth = {"smile": f'<path d="M180 186 Q203 204 226 186" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>',
             "cold": f'<path d="M184 190 L222 186" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'}[mood]
    a = (f'<path d="M290 260 Q400 300 470 270" stroke="{INK}" stroke-width="54" fill="none" stroke-linecap="round"/><path d="M290 260 Q400 300 470 270" stroke="{RED}" stroke-width="40" fill="none" stroke-linecap="round"/>'
         f'<ellipse cx="500" cy="262" rx="40" ry="28" fill="#141416" stroke="{INK}" stroke-width="6"/>') if arm else ""
    return f'''<g transform="translate({x} {y}) scale({s})">
  <path d="M110 240 Q200 214 290 240 Q340 500 360 900 L40 900 Q60 500 110 240 Z" fill="{RED}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>
  <path d="M200 250 L200 900" stroke="{INK}" stroke-width="5" opacity="0.5"/><path d="M150 236 L200 330 L250 236" fill="#7a1a20" stroke="{INK}" stroke-width="6"/>
  <path d="M120 150 Q100 40 200 34 Q300 40 282 150 L300 250 Q260 230 250 170 L150 170 Q140 230 100 250 Z" fill="#141414" stroke="{INK}" stroke-width="7"/>
  <ellipse cx="200" cy="146" rx="62" ry="76" fill="#e8d2bf" stroke="{INK}" stroke-width="7"/>
  <path d="M140 120 Q170 70 262 110 Q220 90 170 104 Z" fill="#141414"/>
  <path d="M160 116 L190 112 M212 112 L242 116" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="177" cy="140" rx="7" ry="8" fill="{INK}"/><ellipse cx="225" cy="140" rx="7" ry="8" fill="{INK}"/>
  <path d="M200 148 Q195 164 205 166" fill="none" stroke="{INK}" stroke-width="4"/>{mouth}
  <path d="M182 186 Q203 196 224 186" stroke="{RED}" stroke-width="6" fill="none" opacity="0.8"/>{a}</g>'''

def photo_eli(x, y, s=1.0, rot=0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-20" y="-20" width="740" height="560" fill="#efeadf" stroke="{INK}" stroke-width="7"/>
  <rect x="10" y="10" width="680" height="440" fill="#2a2018"/><rect x="10" y="10" width="680" height="440" fill="#d9a85a" opacity="0.25"/>
  <rect x="40" y="40" width="620" height="60" fill="#3a2e22"/>{text(350, 82, "DINER · FIFTH ST", 34, 900, "#e8b04a", "middle", 6, "Inter")}
  <rect x="10" y="330" width="680" height="30" fill="#5a3f2a" stroke="{INK}" stroke-width="5"/>
  {eli(180, 70, 0.75, "sit_letter", "worried", -4)}<rect x="470" y="300" width="40" height="30" fill="#efe6cf" stroke="{INK}" stroke-width="4"/>
  {text(640, 500, "01:04", 30, 700, "#ff8a3a", "end", 2, "Inter")}</g>'''

def subscribe(x=960, y=930):
    return f'<rect x="{x-200}" y="{y-60}" width="400" height="100" rx="50" fill="#e23b3b"/>{text(x, y+8, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}'

S = {}
S[1] = lambda: svg(f'''{boards(620)}<ellipse cx="960" cy="640" rx="760" ry="420" fill="url(#ylamp)"/>{case_svg(620, 560, 4.0, True, False)}
<g transform="translate(560 260)">{eli(0, 0, 0.7, "face_close", "scared", 6)}</g>{text(1840, 120, "1:55 AM", 80, 900, ACC, "end", 4)}''', "#0d1016")
S[2] = lambda: svg(f'''<ellipse cx="960" cy="540" rx="900" ry="520" fill="{ACC}" opacity="0.10"/>{photo_eli(610, 260, 1.0, -4)}{big(960, 170, "HIS OWN FACE", 120, ACC)}''', "#0b0c10")
S[3] = lambda: svg(f'''{bokeh([(400,300,140,"#3d7bd9",.25),(1500,700,120,"#d9475c",.2)])}{big_phone(960, 540, screen_call("Unknown", "Last night · 1:12 AM"), -6, True, 1.0)}
{text(300, 980, "PREVIOUSLY", 54, 900, "#9aa0a8", "start", 14)}''', "#111216")
S[4] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1a1c22"/>{"".join(f'<rect x="{180+i*320}" y="{180+j*260}" width="290" height="230" fill="#2a2d35" stroke="{INK}" stroke-width="7"/>' for i in range(5) for j in range(3))}
<rect x="820" y="440" width="290" height="230" fill="#0c0d10" stroke="{ACC}" stroke-width="8"/>{text(965, 410, "14", 60, 900, ACC, "middle")}{case_svg(880, 540, 1.0, True, True)}
{big(960, 1000, "$5,000", 110, ACC)}''')
S[5] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121318"/><rect x="0" y="820" width="{W}" height="260" fill="#202228"/>
<path d="M760 0 L1160 0 L1500 1080 L420 1080 Z" fill="#f6e7c4" opacity="0.06"/>{stranger(820, 120, 1.0, 0.9)}<path d="M0 820 L{W} 820" stroke="{INK}" stroke-width="8"/>''')
S[6] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0e0f13"/>{case_svg(560, 380, 4.4, True, True)}
{"".join(f'<path d="M{1500+i*40} {300+i*10} q50 120 0 240" stroke="{ACC}" stroke-width="8" fill="none" opacity="{0.8-i*0.2:.1f}"/>' for i in range(3))}{big(1600, 860, "TICK", 140, ACC)}''')
S[7] = lambda: svg(f'''<rect width="{W}" height="780" fill="#0b0f18"/>{water(700, 7)}
<path d="M0 700 L1380 700 L1380 760 L0 760 Z" fill="#2b2620" stroke="{INK}" stroke-width="7"/>{"".join(f'<rect x="{80+i*200}" y="760" width="26" height="320" fill="#1a1612" stroke="{INK}" stroke-width="5"/>' for i in range(7))}
<rect x="1000" y="300" width="340" height="400" fill="#23262f" stroke="{INK}" stroke-width="8"/><rect x="1110" y="460" width="120" height="240" fill="{BLUE}" stroke="{INK}" stroke-width="7"/>
{lamp(1360, 220)}<ellipse cx="1170" cy="560" rx="200" ry="180" fill="url(#blue)"/>{text(1170, 280, "PIER 9", 46, 900, "#9aa0a8", "middle", 8)}
{rain(0, 0, W, H, 420, 7)}''', "#0b0f18")
S[8] = lambda: svg(f'''<rect width="{W}" height="700" fill="#10141d"/>{boards(700)}<rect x="1400" y="260" width="120" height="440" fill="{BLUE}" stroke="{INK}" stroke-width="8" opacity="0.8"/>
{eli(560, 420, 0.95, "face_close", "worried", 14)}{crates(80, 420, 1.3)}{crates(1100, 520, 0.9)}{case_svg(780, 820, 1.2, True, False)}{rain(0, 0, W, H, 300, 8)}''', "#10141d")
S[9] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#16181d"/><g transform="translate(960 560) scale(2.2) translate(-84 -60)">{case_svg(0, 0, 1.0, True, False)}</g>
<circle cx="680" cy="470" r="70" fill="none" stroke="{ACC}" stroke-width="8"/><circle cx="1240" cy="470" r="70" fill="none" stroke="{ACC}" stroke-width="8"/>{text(960, 900, "TWO LATCHES. NO LOCK.", 64, 900, "#cfd3da", "middle", 6)}''')
S[10] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0f1218"/><ellipse cx="960" cy="560" rx="600" ry="460" fill="url(#lamp)"/>{eli(560, 60, 2.4, "face_close", "worried", -8)}{rain(0, 0, W, H, 260, 10, (0.1, 0.3))}''')
S[11] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121318"/>{big(560, 600, "CLICK.", 220, "#f4f1ea")}{big(1380, 700, "CLICK.", 220, ACC)}''')
S[12] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0c10"/><ellipse cx="960" cy="560" rx="700" ry="300" fill="{ACC}" opacity="0.22" filter="url(#b30)"/>
<path d="M360 620 L1560 620 L1500 920 L420 920 Z" fill="#a7adb5" stroke="{INK}" stroke-width="10"/><path d="M360 620 L520 220 L1400 220 L1560 620 Z" fill="#8f959d" stroke="{INK}" stroke-width="10"/>
<path d="M420 640 L1500 640 L1470 760 L450 760 Z" fill="#141416"/>''')
S[13] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0e0e10"/><rect x="260" y="160" width="1400" height="780" rx="30" fill="#141416" stroke="#2a2a2e" stroke-width="10"/>
{"".join(f'<circle cx="{300+(i%14)*100}" cy="{200+(i//14)*100}" r="10" fill="#1d1d21"/>' for i in range(14*8))}{watch(960, 560, 2.0)}{big(1620, 1010, "NO BOMB.", 90, "#f4f1ea", "end")}''')
S[14] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0c0c0e"/>{watch(560, 560, 2.6, True)}{big(1400, 420, "2:00", 200, ACC)}{text(1400, 560, "the hands had stopped", 50, 700, "#cfd3da", "middle", 0, "Inter")}
{big(1400, 800, "TICK... TICK...", 100, "#f4f1ea")}''')
S[15] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#141416"/><ellipse cx="960" cy="540" rx="700" ry="400" fill="{BRASS}" opacity="0.12"/>{key(700, 480, 1.9, -8)}''')
S[16] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#141416"/><g transform="translate(560 300) rotate(6)"><rect width="740" height="560" fill="#efeadf" stroke="{INK}" stroke-width="8"/>
{text(370, 300, "?", 220, 900, "#c9c2b2", "middle")}</g>{text(1840, 1010, "and under the key...", 50, 700, "#9aa0a8", "end", 2, "Inter")}''')
S[17] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#101114"/>{photo_eli(560, 240, 1.05, 4)}
<ellipse cx="520" cy="820" rx="110" ry="80" fill="#d6c6b2" stroke="{INK}" stroke-width="8"/><ellipse cx="1400" cy="300" rx="110" ry="80" fill="#d6c6b2" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{380-i*20} {760+i*30} l-40 0" stroke="#cfd3da" stroke-width="5" opacity="0.6"/>' for i in range(3))}''')
S[18] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2018"/>{photo_eli(260, 160, 1.9, 0)}''')
S[19] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121520"/><rect x="200" y="200" width="900" height="520" fill="#e8b04a" opacity="0.85" stroke="{INK}" stroke-width="10"/>
{eli(560, 300, 0.9, "sit_letter", "worried", -4)}<rect x="200" y="200" width="900" height="70" fill="#3a2e22"/>{text(650, 252, "DINER", 46, 900, "#e8b04a", "middle", 8)}
<rect x="0" y="720" width="{W}" height="360" fill="#1b1d23"/>{stranger(1500, 260, 0.8, 0.95)}
<rect x="1520" y="420" width="90" height="60" rx="8" fill="#0c0c0e" stroke="{INK}" stroke-width="5"/><circle cx="1565" cy="450" r="20" fill="#3a3f4c"/>
{big(1500, 140, "BEFORE THE CALL", 70, ACC, "middle")}{rain(0, 0, W, H, 300, 19)}''')
S[20] = lambda: svg(f'''{big_phone(700, 540, screen_call("Unknown", "Incoming call"), -4, True, 0.95)}{big(1380, 470, "NOT THE", 140, "#f4f1ea")}{big(1380, 640, "WRONG NUMBER", 120, ACC)}''', "#111216")
S[21] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#101114"/>{photo_eli(120, 220, 0.9, -6)}
<rect x="900" y="200" width="900" height="420" rx="30" fill="#1b1d23" stroke="{ACC}" stroke-width="6"/>{text(1350, 330, "WHO TOOK THIS PHOTO?", 52, 900, "#f4f1ea", "middle")}
{text(1350, 420, "Tell me in the comments", 42, 600, ACC, "middle", 0, "Inter")}{subscribe(1350, 540)}''')
S[22] = lambda: svg(f'''<rect width="{W}" height="700" fill="#10141d"/>{boards(700)}{crates(1300, 420, 1.2)}{eli(700, 260, 1.1, "hold_case", "scared", -10)}{rain(0, 0, W, H, 320, 22)}''', "#10141d")
S[23] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0d1016"/>{boards(520, "#24201b")}
<ellipse cx="900" cy="900" rx="300" ry="40" fill="#3a4a66" opacity="0.5"/>
<path d="M800 0 L800 860 L900 860 L920 0 Z M1000 0 L1020 860 L1120 860 L1110 0 Z" fill="#4b4e55" stroke="{INK}" stroke-width="8"/>
<path d="M760 860 L920 860 L930 900 L740 900 Z M1000 860 L1160 860 L1180 900 L990 900 Z" fill="#141416" stroke="{INK}" stroke-width="6"/>{rain(0, 0, W, H, 320, 23)}''')
S[24] = lambda: svg(f'''<rect width="{W}" height="700" fill="#0d1016"/>{boards(700)}{lamp(1500, 120)}<ellipse cx="960" cy="560" rx="500" ry="500" fill="url(#lamp)"/>{stranger(800, 60, 1.15)}{rain(0, 0, W, H, 420, 24)}''', "#0d1016")
S[25] = lambda: svg(f'''<rect width="{W}" height="700" fill="#0d1016"/>{boards(700)}{stranger(1420, 360, 0.7)}{eli(180, 300, 1.05, "hold_case", "scared", 14)}
<path d="M640 980 L1420 980" stroke="{ACC}" stroke-width="6" stroke-dasharray="30 20" opacity="0.7"/>{text(1030, 1040, "10 STEPS", 44, 900, ACC, "middle", 6)}{rain(0, 0, W, H, 380, 25)}''', "#0d1016")
S[26] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#14161c"/>{stranger(260, -80, 2.4)}
<rect x="1020" y="300" width="760" height="260" rx="40" fill="#f4f1ea" stroke="{INK}" stroke-width="8"/><path d="M1060 560 L1000 640 L1140 560 Z" fill="#f4f1ea" stroke="{INK}" stroke-width="6"/>
{text(1400, 410, "Don't knock on", 64, 900, INK, "middle")}{text(1400, 500, "that door, son.", 64, 900, INK, "middle")}{rain(0, 0, W, H, 260, 26)}''')
S[27] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121520"/><ellipse cx="760" cy="560" rx="600" ry="500" fill="url(#ylamp)"/>{eli(260, 80, 2.2, "face_close", "surprised", 10)}{big(1500, 560, "WHO ARE YOU?", 110, "#f4f1ea")}''')
S[28] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a3024"/><rect width="{W}" height="{H}" fill="{SEPIA}" opacity="0.18"/>{boards(720, "#4a3e30")}
<rect x="1200" y="260" width="140" height="460" fill="#6a6a6a" stroke="{INK}" stroke-width="8"/>{stranger(600, 200, 0.95, 0.8)}{case_svg(780, 640, 1.0, True, False)}
{big(1500, 160, "22 YEARS AGO", 100, SEPIA)}{rain(0, 0, W, H, 300, 28, (0.15, 0.35), "#d9c7a4")}''', "#3a3024")
S[29] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0d12"/><rect x="700" y="80" width="520" height="900" fill="{BLUE}" stroke="{INK}" stroke-width="12"/>
<path d="M1220 80 L1460 160 L1460 900 L1220 980 Z" fill="#1f4f9e" stroke="{INK}" stroke-width="10"/><rect x="700" y="80" width="40" height="900" fill="#ffd36a"/>
<path d="M740 980 L540 1080 L1300 1080 L740 980 Z" fill="#ffd36a" opacity="0.5"/>{door_light}''' if False else f'''<rect width="{W}" height="{H}" fill="#0b0d12"/>
<rect x="700" y="80" width="520" height="900" fill="#ffd36a" stroke="{INK}" stroke-width="12"/><path d="M1220 80 L1460 160 L1460 900 L1220 980 Z" fill="{BLUE}" stroke="{INK}" stroke-width="10"/>
<path d="M700 980 L300 1080 L1700 1080 L1220 980 Z" fill="#ffd36a" opacity="0.45"/><ellipse cx="960" cy="540" rx="800" ry="600" fill="#ffd36a" opacity="0.10"/>''')
S[30] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0d12"/><rect x="620" y="60" width="680" height="960" fill="#ffd36a" stroke="{INK}" stroke-width="12"/>
<g opacity="0.95">{woman(760, 180, 1.0, "cold").replace(RED, "#1a1416")}</g><path d="M620 1020 L200 1080 L1720 1080 L1300 1020 Z" fill="#ffd36a" opacity="0.45"/>''')
S[31] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2214"/><ellipse cx="960" cy="400" rx="700" ry="500" fill="#ffd36a" opacity="0.25"/>{woman(700, 40, 1.5, "smile")}
{big(1560, 300, "“ELI BROOKS.”", 90, "#f4f1ea")}''')
S[32] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0f1218"/><ellipse cx="960" cy="560" rx="600" ry="480" fill="{RED}" opacity="0.12"/>{eli(540, 40, 2.5, "face_close", "scared", 0)}{big(960, 1000, "SHE KNEW HIS NAME", 100, RED)}''')
S[33] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a2e1c"/><ellipse cx="960" cy="400" rx="800" ry="400" fill="#ffd36a" opacity="0.2"/>
<path d="M200 640 L1720 640 L1820 860 L100 860 Z" fill="#5a3f2a" stroke="{INK}" stroke-width="10"/>
{"".join(f'<g transform="translate({600+i*150} {560-(i%2)*20})"><rect width="130" height="70" fill="#7fa36a" stroke="{INK}" stroke-width="6"/><rect x="50" y="0" width="30" height="70" fill="#efe6cf"/></g>' for i in range(5))}
{big(960, 300, "$5,000", 200, "#9fd36a")}''')
S[34] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#17181c"/><g transform="rotate(-4 960 540)"><rect x="560" y="140" width="800" height="800" fill="#efeadf" stroke="{INK}" stroke-width="10"/>
{text(960, 290, "FINAL NOTICE", 80, 900, "#2a2a2e", "middle", 4)}{text(960, 400, "Rent due: $1,800", 50, 600, "#2a2a2e", "middle", 0, "Inter")}
<g transform="rotate(-14 960 650)"><rect x="660" y="540" width="600" height="220" rx="20" fill="none" stroke="{RED}" stroke-width="18"/>{text(960, 700, "PAID", 160, 900, RED, "middle", 10)}</g></g>
{text(960, 1040, "Nobody knew about the rent.", 48, 700, "#cfd3da", "middle", 0, "Inter")}''')
S[35] = lambda: svg(f'''<rect width="{W}" height="700" fill="#0d1016"/>{boards(700)}{stranger(1100, 120, 1.0)}
<rect x="160" y="200" width="820" height="260" rx="40" fill="#f4f1ea" stroke="{INK}" stroke-width="8"/><path d="M940 460 L1080 520 L900 440 Z" fill="#f4f1ea" stroke="{INK}" stroke-width="6"/>
{text(570, 310, "She's paying you for", 54, 900, INK, "middle")}{text(570, 390, "what the key opens.", 54, 900, INK, "middle")}{rain(0, 0, W, H, 300, 35)}''', "#0d1016")
S[36] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#241a12"/><ellipse cx="1300" cy="400" rx="600" ry="500" fill="#ffd36a" opacity="0.18"/>{woman(1080, 120, 1.25, "smile")}
<rect x="120" y="260" width="860" height="300" rx="40" fill="#f4f1ea" stroke="{INK}" stroke-width="8"/>{text(550, 370, "He's been lying", 64, 900, INK, "middle")}{text(550, 460, "for twenty-two years.", 56, 900, INK, "middle")}''')
S[37] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#08080a"/>{watch(960, 560, 3.2, True)}<circle cx="960" cy="560" r="560" fill="none" stroke="{ACC}" stroke-width="6" opacity="0.4"/>
<circle cx="960" cy="560" r="640" fill="none" stroke="{ACC}" stroke-width="4" opacity="0.2"/>''')
S[38] = lambda: svg(f'''<rect width="{W}" height="700" fill="#0d1016"/>{boards(700)}<rect x="40" y="80" width="420" height="640" fill="#ffd36a" opacity="0.6"/>
{woman(60, 200, 0.85, "smile")}{stranger(1520, 200, 0.85)}{eli(760, 340, 0.95, "hold_case", "scared", 0)}{rain(0, 0, W, H, 300, 38)}''', "#0d1016")
S[39] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121318"/><path d="M0 760 Q500 640 900 620" stroke="{INK}" stroke-width="150" fill="none" stroke-linecap="round"/>
<path d="M0 760 Q500 640 900 620" stroke="{HOOD}" stroke-width="128" fill="none" stroke-linecap="round"/><ellipse cx="960" cy="610" rx="120" ry="95" fill="{SKIN}" stroke="{INK}" stroke-width="9"/>
{key(1060, 560, 1.3, -20)}{big(1500, 220, "NUMBER NINE", 110, BRASS)}''')
S[40] = lambda: svg(f'''{bokeh([(300,300,140,"#3d7bd9",.2),(1600,800,160,"#d9475c",.2)])}{big_phone(960, 540, screen_msg(["1 new message"]), 8, True, 1.0)}''', "#0e0f13")
S[41] = lambda: svg(f'''{big_phone(960, 540, screen_msg(["Whatever she says,", "don't give her the key.", "It opens the door", "to your father."]), -3, False, 1.05)}''', "#0e0f13")
S[42] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0d12"/><ellipse cx="960" cy="640" rx="500" ry="400" fill="{ACC}" opacity="0.16"/>{eli(620, 140, 1.9, "face_close", "surprised", 0)}{phone_svg(900, 780, 0, 2.4)}''')
S[43] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/><g transform="rotate(-5 960 540)"><rect x="520" y="120" width="880" height="760" fill="#efeadf" stroke="{INK}" stroke-width="10"/>
<rect x="560" y="160" width="800" height="600" fill="{SEPIA}"/>{stranger(780, 200, 0.62, 1).replace("#4b4e55", "#6b604e").replace("#2e3035", "#8a7a62")}
<ellipse cx="1080" cy="560" rx="70" ry="60" fill="#e9dcc8" stroke="{INK}" stroke-width="6"/>{text(960, 840, "...and Eli, age 2", 44, 600, "#3a2e22", "middle", 0, "Inter")}</g>
{big(1540, 1000, "22 YEARS AGO", 90, SEPIA)}''')
S[44] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0d0f14"/><g transform="translate(960 560) scale(5) translate(-150 -175)">
<ellipse cx="150" cy="170" rx="62" ry="72" fill="#2e3035" stroke="{INK}" stroke-width="5"/><path d="M60 140 L240 140 L222 100 Q150 66 78 100 Z" fill="#1b1c20" stroke="{INK}" stroke-width="5"/>
<rect x="40" y="132" width="220" height="16" rx="6" fill="#1b1c20" stroke="{INK}" stroke-width="4"/>
<ellipse cx="128" cy="180" rx="9" ry="6" fill="#cfd3da"/><ellipse cx="172" cy="180" rx="9" ry="6" fill="#cfd3da"/><circle cx="128" cy="180" r="3" fill="{INK}"/><circle cx="172" cy="180" r="3" fill="{INK}"/></g>
{rain(0, 0, W, H, 260, 44)}''')
S[45] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1a1410"/><ellipse cx="760" cy="500" rx="700" ry="500" fill="#ffd36a" opacity="0.16"/>{woman(-120, 60, 1.6, "cold", True)}
{text(1700, 980, "2:00", 160, 900, RED, "end", 4)}''')
S[46] = lambda: svg(f'''{text(960, 190, "WHAT WOULD YOU DO?", 110, 900, "#f4f1ea", "middle", -2)}
<rect x="240" y="280" width="640" height="420" rx="28" fill="#1b1d23" stroke="{RED}" stroke-width="8"/>{key(420, 400, 0.6, 0)}{text(560, 650, "GIVE THE KEY", 64, 900, RED, "middle", 4)}
<rect x="1040" y="280" width="640" height="420" rx="28" fill="#1b1d23" stroke="{ACC}" stroke-width="8"/><rect x="1270" y="330" width="180" height="260" fill="{BLUE}" stroke="{INK}" stroke-width="7"/>{text(1360, 480, "9", 120, 900, "#f4f1ea", "middle")}
{text(1360, 650, "KEEP IT", 64, 900, ACC, "middle", 4)}{text(960, 800, "Tell me in the comments.", 44, 500, "#cfd3da", "middle")}{subscribe(960, 920)}''', "#101114")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
