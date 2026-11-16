import os, sys, math, random
sys.path.insert(0, "/home/claude/wn")
import kit
kit.ACC = "#2EC4B6"
from kit import svg, text, render, INK, W, H
from ava import ava, TEAL
OUT = "ep1/scenes"; os.makedirs(OUT, exist_ok=True)
SEPIA = "#e9dcc3"; NIGHT = "#0b1220"; GOLD = "#e8c37a"

def stars(n, seed, y1=H, op=(0.3, 0.9)):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,y1):.0f}" r="{r.uniform(1,2.8):.1f}" fill="#fff" opacity="{r.uniform(*op):.2f}"/>' for _ in range(n))

def ship(x, y, s=1.0, tilt=0, lights=True, dark=False):
    hull = "#15171c"; sup = "#e9e4d8" if not dark else "#2a2c33"; fun = "#d99a3a" if not dark else "#2a2c33"
    win = "".join(f'<rect x="{60+i*26}" y="{150 + (i%3)*0}" width="12" height="7" fill="#ffe7a3" opacity="0.9"/>' for i in range(36)) if lights else ""
    win2 = "".join(f'<rect x="{80+i*30}" y="{118}" width="12" height="7" fill="#ffe7a3" opacity="0.9"/>' for i in range(30)) if lights else ""
    funnels = "".join(f'''<g transform="translate({250+i*170} 0)"><path d="M0 92 L10 -20 L70 -20 L80 92 Z" fill="{fun}" stroke="{INK}" stroke-width="6"/>
      <path d="M8 -20 L72 -20 L70 4 L10 4 Z" fill="{INK}"/></g>''' for i in range(4))
    return f'''<g transform="translate({x} {y}) rotate({tilt}) scale({s})">
  {funnels}
  <path d="M120 92 L1000 92 L990 132 L130 132 Z" fill="{sup}" stroke="{INK}" stroke-width="6"/>
  <path d="M0 132 L1150 132 L1110 230 Q600 250 60 230 Z" fill="{hull}" stroke="{INK}" stroke-width="7"/>
  <path d="M10 140 L1140 140" stroke="#b33" stroke-width="0" />
  {win}{win2}
  <path d="M30 200 L1120 200" stroke="#7a1f1f" stroke-width="10" opacity="0.8"/>
  <path d="M200 92 L200 -60 M980 92 L980 -50" stroke="{INK}" stroke-width="5"/>
  <path d="M200 -60 L980 -50" stroke="{INK}" stroke-width="2" opacity="0.6"/></g>'''

def sea(y=760, col="#0e1a2c", lines=True):
    l = "".join(f'<path d="M{random.Random(i).uniform(0,W):.0f} {y+20+(i*13)%300} l{random.Random(i+5).uniform(40,140):.0f} 0" stroke="#2b3d58" stroke-width="3" opacity="0.6"/>' for i in range(60)) if lines else ""
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{col}"/>{l}'

def lifeboat(x, y, s=1.0, people=6, ava_in=False):
    heads = "".join(f'<circle cx="{40+i*38}" cy="-6" r="16" fill="#cdb79c" stroke="{INK}" stroke-width="4"/><path d="M{26+i*38} 10 Q{40+i*38} -2 {54+i*38} 10 L{56+i*38} 30 L{24+i*38} 30 Z" fill="#3a3b42" stroke="{INK}" stroke-width="4"/>' for i in range(people))
    return f'''<g transform="translate({x} {y}) scale({s})">{heads}
  <path d="M-20 20 L{60+people*38} 20 Q{40+people*38} 70 {people*19+20} 72 Q0 70 -20 20 Z" fill="#e9e4d8" stroke="{INK}" stroke-width="6"/>
  <path d="M-10 34 L{50+people*38} 34" stroke="{INK}" stroke-width="3" opacity="0.5"/></g>'''

def iceberg(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M0 200 L60 60 L110 100 L170 0 L240 90 L300 70 L360 200 Z" fill="#dff3fb" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M170 0 L190 120 L240 90 M60 60 L80 150" fill="none" stroke="#9fc8da" stroke-width="5"/></g>'''

def card(lines, bg="#0e1015", extra=""):
    return svg(extra + "".join(text(x, y, s, size, w, fill, anc, ls) for (x, y, s, size, w, fill, anc, ls) in lines), bg)

def clock_card(t, sub):
    return card([(960, 560, t, 280, 900, "#f4f1ea", "middle", -6), (960, 690, sub, 50, 800, TEAL, "middle", 10)], "#0b0f16")

def person(x, y, s=1.0, coat="#3a3b42", hatc="#1b1c20", skin="#cdb79c"):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M10 330 L20 120 Q60 90 100 120 L110 330 Z" fill="{coat}" stroke="{INK}" stroke-width="6"/>
  <ellipse cx="60" cy="70" rx="38" ry="44" fill="{skin}" stroke="{INK}" stroke-width="6"/>
  <path d="M18 46 L102 46 L92 24 Q60 6 28 24 Z" fill="{hatc}" stroke="{INK}" stroke-width="5"/>
  <path d="M46 72 L54 72 M68 72 L76 72" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'''

S = {}
S[1] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#151820"/><ellipse cx="960" cy="560" rx="700" ry="520" fill="url(#ylamp)"/>{ava(760, 160, 1.8, "calm", 0, hat="1912")}''')
S[2] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0e1118"/>{stars(120, 2)}{ava(500, 40, 2.6, "worried", 8)}''')
S[3] = lambda: svg(f'''{stars(160, 3, 700)}{sea(720)}{ship(380, 420, 1.0, 0)}
{text(960, 190, "I WAS THERE", 150, 900, "#f4f1ea", "middle", 6)}{text(960, 270, "THE NIGHT THE TITANIC SANK  ·  APRIL 14, 1912", 40, 700, TEAL, "middle", 8, "Inter")}''', NIGHT)
S[4] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/><rect x="0" y="820" width="{W}" height="260" fill="#3a3329"/>
{ava(560, 240, 1.4, "smile", 0, hat="1912")}
<g transform="translate(1100 640)"><rect x="0" y="0" width="300" height="200" rx="16" fill="#7a4a2a" stroke="{INK}" stroke-width="8"/><path d="M110 0 Q150 -50 190 0" fill="none" stroke="{INK}" stroke-width="10"/><path d="M0 70 L300 70" stroke="{INK}" stroke-width="5"/></g>
<g transform="translate(1200 300) rotate(8)"><rect width="360" height="200" fill="{SEPIA}" stroke="{INK}" stroke-width="6"/>{text(180, 60, "WHITE STAR LINE", 30, 800, "#7a1f1f", "middle", 2, "Inter")}{text(180, 120, "THIRD CLASS", 44, 900, INK, "middle")}{text(180, 170, "SOUTHAMPTON → NEW YORK", 22, 600, "#333", "middle", 2, "Inter")}</g>''')
S[5] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/><g transform="rotate(-3 960 540)"><rect x="520" y="100" width="880" height="880" fill="{SEPIA}" stroke="{INK}" stroke-width="10"/>
{text(600, 220, "Dear Ava,", 64, 400, "#3a2b20", "start", 0, "Inter")}
{text(600, 330, "I have found you a position", 44, 400, "#3a2b20", "start", 0, "Inter")}{text(600, 400, "with a family in New York.", 44, 400, "#3a2b20", "start", 0, "Inter")}
{text(600, 470, "Come as soon as you can.", 44, 400, "#3a2b20", "start", 0, "Inter")}{text(600, 620, "A new life is waiting.", 52, 700, "#7a1f1f", "start", 0, "Inter")}
{text(1300, 860, "- Aunt Margaret", 44, 400, "#3a2b20", "end", 0, "Inter")}</g>''')
S[6] = lambda: svg(f'''<rect width="{W}" height="700" fill="#c9d6dc"/>{sea(720, "#2f4656")}<rect x="0" y="690" width="{W}" height="60" fill="#6b5a46" stroke="{INK}" stroke-width="6"/>
{ship(260, 380, 1.25, 0, False)}{"".join(person(200+i*120, 560, 0.45, ["#3a3b42","#5a3a2a","#2f4a3f"][i%3]) for i in range(10))}''', "#c9d6dc")
S[7] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#101520"/>{ship(320, 260, 1.12, 0)}
{"".join(f'<rect x="{320+i*322}" y="660" width="300" height="160" fill="#2a3040" stroke="{INK}" stroke-width="6"/>' for i in range(4))}
{"".join(text(470+i*322, 760, f"BLOCK {i+1}", 34, 800, "#9fb3c8", "middle", 4, "Inter") for i in range(4))}
{text(960, 940, "269 METERS  ·  LONGER THAN FOUR CITY BLOCKS", 46, 800, TEAL, "middle", 4, "Inter")}''')
S[8] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a2a1e"/>
<path d="M560 1080 L760 520 L1160 520 L1360 1080 Z" fill="#6b4a2e" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{760-i*28} {560+i*60} L{1160+i*28} {560+i*60}" stroke="{INK}" stroke-width="5"/>' for i in range(9))}
<ellipse cx="960" cy="200" rx="160" ry="60" fill="{GOLD}" stroke="{INK}" stroke-width="6"/><ellipse cx="960" cy="260" rx="500" ry="300" fill="url(#lamp)"/>
{"".join(f'<circle cx="{830+i*52}" cy="250" r="12" fill="#fff3c4"/>' for i in range(6))}
<rect x="160" y="200" width="300" height="420" fill="#2a1e14" stroke="{GOLD}" stroke-width="10"/><rect x="1460" y="200" width="300" height="420" fill="#2a1e14" stroke="{GOLD}" stroke-width="10"/>
{text(960, 1010, "ELECTRIC LIGHTS · A SWIMMING POOL · A GYM", 40, 800, "#f4f1ea", "middle", 4, "Inter")}''')
S[9] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#d9cdb4"/><rect x="0" y="760" width="{W}" height="320" fill="#a9967a"/>
<rect x="200" y="680" width="1520" height="40" fill="#f4efe4" stroke="{INK}" stroke-width="7"/>
{"".join(person(260+i*200, 440, 0.7, ["#3a3b42","#5a3a2a","#4a4f5a"][i%3]) for i in [0,1,2,5,6])}
{ava(820, 330, 0.95, "smile", 0)}
{"".join(f'<ellipse cx="{360+i*260}" cy="690" rx="60" ry="14" fill="#fff" stroke="{INK}" stroke-width="4"/>' for i in range(6))}''')
S[10] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#cbb994"/><rect x="0" y="0" width="{W}" height="{H}" fill="#1f4a66" opacity="0.35"/>
<path d="M120 300 Q220 250 300 330 Q260 420 160 400 Z" fill="#a8b089" stroke="{INK}" stroke-width="6"/>
<path d="M1500 200 Q1700 260 1760 480 Q1700 700 1580 820 L1920 820 L1920 200 Z" fill="#a8b089" stroke="{INK}" stroke-width="6"/>
<path d="M260 340 C320 360 300 420 250 430 C600 500 1100 560 1560 520" fill="none" stroke="#7a1f1f" stroke-width="8" stroke-dasharray="22 16"/>
{"".join(f'<circle cx="{x}" cy="{y}" r="14" fill="#7a1f1f" stroke="{INK}" stroke-width="4"/>' + text(x, y-30, n, 30, 800, INK, "middle", 2, "Inter") for x, y, n in [(260,340,"SOUTHAMPTON"),(300,420,"CHERBOURG"),(240,470,"QUEENSTOWN"),(1580,520,"NEW YORK")])}
<g transform="translate(1040 540)">{iceberg(0, -60, 0.35)}</g><path d="M960 520 L1060 520" stroke="{TEAL}" stroke-width="0"/>
<circle cx="1000" cy="545" r="20" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>{text(1000, 620, "APRIL 14", 40, 900, INK, "middle", 4, "Inter")}''')
S[11] = lambda: svg(f'''{stars(240, 11, 760)}{sea(760)}<rect x="0" y="700" width="{W}" height="80" fill="#3a3329" stroke="{INK}" stroke-width="6"/>
<path d="M0 690 L{W} 690" stroke="#e9e4d8" stroke-width="14"/>{ava(640, 260, 1.2, "worried", -6, hat="1912")}
<path d="M1040 420 Q1080 400 1110 420 Q1140 440 1170 420" fill="none" stroke="#cfe6f2" stroke-width="6" opacity="0.7"/>
<g transform="translate(1500 300)"><rect x="0" y="0" width="60" height="320" rx="30" fill="#e9e4d8" stroke="{INK}" stroke-width="6"/><circle cx="30" cy="330" r="50" fill="#c33" stroke="{INK}" stroke-width="6"/><rect x="20" y="230" width="20" height="100" fill="#c33"/>{text(90, 240, "31°F", 50, 900, "#f4f1ea", "start")}</g>''', NIGHT)
S[12] = lambda: svg(f'''{stars(420, 12, 700)}<rect x="0" y="700" width="{W}" height="380" fill="#05070c"/>
{stars(160, 99, 0)}<path d="M0 700 L{W} 700" stroke="#1b2536" stroke-width="3"/>{ship(420, 520, 0.8, 0)}
<rect x="420" y="740" width="920" height="120" fill="#ffe7a3" opacity="0.06"/>''', "#05070c")
S[13] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2a24"/><rect x="200" y="620" width="1520" height="60" fill="#6b5a46" stroke="{INK}" stroke-width="7"/>
{person(420, 330, 1.0, "#1b2236", "#1b2236")}<path d="M560 520 L720 600" stroke="{INK}" stroke-width="14"/>
<rect x="700" y="560" width="260" height="70" fill="#3a3329" stroke="{INK}" stroke-width="6"/>
{"".join(f'<g transform="translate({1080+(i%2)*280} {150+i*130}) rotate({-6+i*4})"><rect width="420" height="110" fill="{SEPIA}" stroke="{INK}" stroke-width="5"/>{text(210, 72, t, 46, 900, "#7a1f1f", "middle", 4, "Inter")}</g>' for i, t in enumerate(["ICE AHEAD", "ICEBERGS SEEN", "FIELD ICE", "ICE WARNING"]))}''')
S[14] = lambda: svg(f'''{text(960, 290, "WHAT WAS IT REALLY LIKE?", 96, 900, "#f4f1ea", "middle", -2)}
<rect x="610" y="420" width="420" height="120" rx="60" fill="#e23b3b"/>{text(820, 500, "SUBSCRIBE", 52, 900, "#ffffff", "middle")}
<circle cx="1150" cy="480" r="60" fill="#1d1f26" stroke="{TEAL}" stroke-width="6"/>
<path d="M1120 500 Q1120 440 1150 438 Q1180 440 1180 500 L1188 510 L1112 510 Z M1140 516 Q1150 530 1160 516" fill="{TEAL}"/>
{text(960, 740, "What would you have done that night?", 66, 700, TEAL, "middle")}{text(960, 820, "Tell me in the comments.", 44, 500, "#cfd3da", "middle")}''', "#101114")
S[15] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1c1a17"/><rect x="200" y="520" width="1100" height="240" fill="#4a3f33" stroke="{INK}" stroke-width="8"/>
<rect x="240" y="470" width="1020" height="80" rx="20" fill="#e9e4d8" stroke="{INK}" stroke-width="6"/>{ava(260, 160, 0.9, "calm", 6)}
<circle cx="1560" cy="300" r="140" fill="#e9e3d6" stroke="{INK}" stroke-width="10"/><path d="M1560 300 L1560 190 M1560 300 L1500 270" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>
{text(1560, 520, "11:40 PM", 70, 900, "#f4f1ea", "middle", 4)}''')
S[16] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1c1a17"/>{ava(560, 60, 2.4, "scared", 0)}
{"".join(f'<path d="M{100+i*30} {200+i*120} l60 0" stroke="#e9e4d8" stroke-width="8" opacity="0.5"/><path d="M{1700-i*30} {220+i*120} l60 0" stroke="#e9e4d8" stroke-width="8" opacity="0.5"/>' for i in range(6))}''')
S[17] = lambda: svg(f'''{stars(260, 17, 900)}{sea(860, "#05070c")}{iceberg(1280, 540, 1.3)}
<g transform="translate(200 360)"><rect x="0" y="0" width="240" height="140" fill="#e9e4d8" stroke="{INK}" stroke-width="8"/><path d="M120 140 L120 720" stroke="{INK}" stroke-width="14"/>
{person(20, -200, 0.6, "#1b2236", "#1b2236")}{person(120, -200, 0.6, "#1b2236", "#1b2236")}</g>
{text(1460, 470, "!", 140, 900, "#ff3b3b", "middle")}''', "#05070c")
S[18] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b1220"/>{sea(520, "#0e1a2c", False)}
<g transform="translate(200 260)"><path d="M0 120 L1300 120 L1260 380 Q650 410 60 380 Z" fill="#20242c" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{120+i*110} 120 L{120+i*110} 380" stroke="#6b7079" stroke-width="5"/>' for i in range(11))}
{"".join(f'<rect x="{1150-i*110}" y="{380-(5-i)*45}" width="106" height="{(5-i)*45}" fill="#3d7bd9" opacity="0.7"/>' for i in range(5))}
<path d="M780 300 L1240 340" stroke="#ff3b3b" stroke-width="10" stroke-dasharray="20 14"/></g>
{iceberg(1440, 300, 1.0)}{text(960, 960, "THE ICE CUT ALONG HER SIDE, BELOW THE WATERLINE", 42, 800, "#f4f1ea", "middle", 4, "Inter")}''')
S[19] = lambda: svg(f'''{stars(200, 19, 700)}<rect x="0" y="700" width="{W}" height="380" fill="#3a3329"/><path d="M0 700 L{W} 700" stroke="#e9e4d8" stroke-width="14"/>
{person(500, 380, 1.0, "#3a3b42", "#2a2c33")}{person(760, 400, 0.95, "#5a3a2a", "#3a2b2b")}{person(1100, 390, 1.0, "#2f4a3f", "#1b1c20")}
{"".join(f'<path d="M{600+i*170} {840+(i%2)*40} l40 -30 l40 30 l-40 20 Z" fill="#dff3fb" stroke="{INK}" stroke-width="5"/>' for i in range(5))}''', NIGHT)
S[20] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/><rect x="760" y="300" width="1000" height="600" fill="#1f4a66" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{820+i*90} 360 L{820+i*90} 840" stroke="#9fc4d6" stroke-width="3" opacity="0.6"/>' for i in range(11))}
<path d="M800 600 L1720 600" stroke="#9fc4d6" stroke-width="5"/>{person(260, 380, 1.4, "#2a2c33", "#2a2c33")}
<rect x="900" y="120" width="720" height="140" rx="16" fill="#7a1f1f"/>{text(1260, 220, "TWO HOURS LEFT", 80, 900, "#f4f1ea", "middle", 4)}''')
S[21] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1c1a17"/>{person(300, 300, 1.5, "#1b2236", "#1b2236")}
{"".join(f'<g transform="translate({900+i*260} 420)"><rect width="200" height="300" rx="30" fill="#e9e4d8" stroke="{INK}" stroke-width="7"/><path d="M0 100 L200 100 M0 200 L200 200" stroke="{INK}" stroke-width="5"/></g>' for i in range(3))}
{text(1250, 260, "TO THE BOATS!", 110, 900, "#f4f1ea", "middle", 2)}''')
S[22] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#140f0f"/><ellipse cx="960" cy="560" rx="700" ry="500" fill="#7a1f1f" opacity="0.25"/>{ava(560, 40, 2.4, "determined", 0)}''')
def boats_vs_people():
    boats = "".join(f'<rect x="{180+(i%10)*70}" y="{300+(i//10)*70}" width="56" height="30" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>' for i in range(20))
    ppl = "".join(f'<circle cx="{1040+(i%22)*34}" cy="{280+(i//22)*34}" r="11" fill="{"#e9e4d8" if i<53 else "#5a5f69"}"/>' for i in range(110))
    return svg(f'''{text(520, 200, "20 LIFEBOATS", 70, 900, TEAL, "middle")}{boats}{text(520, 560, "1,178 SEATS", 90, 900, "#f4f1ea", "middle")}
{text(1400, 200, "2,200+ PEOPLE", 70, 900, "#f4f1ea", "middle")}{ppl}{text(1400, 560, "1 dot = 20 people", 34, 500, "#9aa0a8", "middle", 2, "Inter")}
{text(960, 860, "NOT ENOUGH SEATS FOR EVERYONE", 70, 900, "#ff6b6b", "middle", 2)}''', "#0e1015")
S[23] = boats_vs_people
S[24] = lambda: svg(f'''{stars(200, 24, 600)}{sea(860)}<path d="M0 0 L1500 0 L1500 760 L0 760 Z" fill="#15171c" stroke="{INK}" stroke-width="8"/>
{"".join(f'<rect x="{80+i*90}" y="120" width="40" height="22" fill="#ffe7a3" opacity="0.8"/>' for i in range(16))}
<path d="M1100 300 L1100 560 M1340 300 L1340 560" stroke="#cfcfcf" stroke-width="4"/>{lifeboat(1080, 580, 1.2, 3)}
{text(1700, 300, "HALF", 90, 900, "#f4f1ea", "middle")}{text(1700, 390, "EMPTY", 90, 900, TEAL, "middle")}''', NIGHT)
S[25] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/>
{"".join(f'<rect x="{100+i*140}" y="{100+i*70}" width="{1720-i*280}" height="{880-i*140}" fill="none" stroke="#6b5a46" stroke-width="22"/>' for i in range(6))}
<g transform="translate(860 340)">{"".join(f'<path d="M{i*40} 0 L{i*40} 400" stroke="{INK}" stroke-width="10"/>' for i in range(6))}<path d="M-10 20 L210 20 M-10 380 L210 380" stroke="{INK}" stroke-width="10"/></g>
{ava(1260, 520, 0.8, "worried", -10)}''')
S[26] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#1c1a17"/>
{"".join(f'<rect x="{300+i*150}" y="{900-i*120}" width="900" height="30" fill="#6b4a2e" stroke="{INK}" stroke-width="5"/>' for i in range(7))}
{person(900, 260, 1.3, "#e9e4d8", "#1b2236")}{ava(420, 300, 1.2, "worried", 10)}
<ellipse cx="860" cy="620" rx="30" ry="24" fill="#cdb79c" stroke="{INK}" stroke-width="5"/>''')
def boat_deck(rockets=True):
    rk = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff"/>' + "".join(f'<path d="M{x} {y} l{70*math.cos(a):.0f} {70*math.sin(a):.0f}" stroke="#fff6c8" stroke-width="4" opacity="0.8"/>' for a in [k*0.785 for k in range(8)]) for x, y in [(600, 160), (1300, 120)]) if rockets else ""
    return f'''{stars(180, 27, 700)}{rk}<g transform="rotate(6 960 700)"><rect x="-100" y="640" width="2200" height="500" fill="#3a3329" stroke="{INK}" stroke-width="8"/>
<path d="M-100 630 L2100 630" stroke="#e9e4d8" stroke-width="14"/></g>'''
S[27] = lambda: svg(f'''{boat_deck()}{ava(700, 300, 1.2, "scared", 0, hat="1912")}{person(1200, 370, 1.0, "#3a3b42")}{person(1400, 380, 1.0, "#5a3a2a")}''', NIGHT)
S[28] = lambda: svg(f'''{boat_deck(False)}
{"".join(person(420+i*280, 360, 1.1, "#1b1c20", "#1b1c20") + f'<path d="M{470+i*280} 560 L{620+i*280} 470" stroke="#8a4a2a" stroke-width="16"/><path d="M{560+i*280} 520 L{680+i*280} 420" stroke="#ddd" stroke-width="3"/>' for i in range(4))}
{"".join(text(300+i*360, 220-(i%2)*60, "♪", 90, 400, TEAL, "middle") for i in range(5))}''', NIGHT)
S[29] = lambda: svg(f'''{stars(160, 29, 500)}{sea(900)}<path d="M0 0 L1920 0 L1920 520 L0 520 Z" fill="#15171c"/>
<path d="M760 520 L760 700 M1160 520 L1160 700" stroke="#cfcfcf" stroke-width="5"/>{lifeboat(740, 720, 1.4, 9)}
<rect x="80" y="120" width="420" height="150" rx="14" fill="#0b0f16" stroke="{TEAL}" stroke-width="6"/>{text(290, 225, "2:05 AM", 80, 900, "#f4f1ea", "middle")}
{text(1600, 240, "COLLAPSIBLE D", 50, 900, TEAL, "middle", 4, "Inter")}{text(1600, 300, "the last boat lowered", 36, 500, "#cfd3da", "middle", 2, "Inter")}''', NIGHT)
S[30] = lambda: svg(f'''{stars(260, 30, 640)}{sea(640, "#05070c")}{ship(360, 470, 1.0, -9)}{lifeboat(160, 900, 1.6, 6)}''', "#05070c")
S[31] = lambda: svg(f'''{stars(320, 31, 640)}{ship(560, 760, 0.85, -32, False, True)}{sea(700, "#05070c")}{text(1600, 200, "2:18", 140, 900, "#f4f1ea", "middle")}''', "#05070c")
S[32] = lambda: svg(f'''{stars(360, 32, 640)}{sea(640, "#05070c")}{text(960, 420, "2:20 AM", 170, 900, "#f4f1ea", "middle")}{text(960, 520, "SHE WAS GONE.", 60, 800, TEAL, "middle", 12, "Inter")}''', "#05070c")
S[33] = lambda: svg(f'''{stars(300, 33, 640)}{sea(640, "#05070c")}
{"".join(f'<ellipse cx="{200+i*180}" cy="{760+(i%3)*60}" rx="{60+(i%4)*20}" ry="8" fill="none" stroke="#2b3d58" stroke-width="4"/>' for i in range(10))}
{text(960, 330, "28°F", 160, 900, "#cfe6f2", "middle")}{text(960, 420, "BELOW FREEZING", 50, 800, TEAL, "middle", 10, "Inter")}''', "#05070c")
S[34] = lambda: svg(f'''{stars(300, 34, 640)}{sea(640, "#05070c")}{lifeboat(300, 700, 0.8, 5)}{lifeboat(900, 660, 0.6, 6)}{lifeboat(1400, 720, 0.9, 4)}''', "#05070c")
S[35] = lambda: svg(f'''{stars(500, 35, H, (0.15, 0.6))}''', "#020306")
S[36] = lambda: svg(f'''{stars(200, 36, 560)}{sea(560, "#0b1525")}
<path d="M200 760 L1720 760 Q1500 1000 960 1010 Q420 1000 200 760 Z" fill="#e9e4d8" stroke="{INK}" stroke-width="8"/>
{person(300, 470, 1.0, "#5a5f69")}{person(1400, 470, 1.0, "#3a3b42")}{ava(620, 300, 1.15, "worried", 0, coat="#6b6f78", scarf="#9aa0a8")}''', "#0b1525")
S[37] = lambda: svg(f'''{stars(160, 37, 700, (0.2, 0.5))}<rect x="0" y="0" width="{W}" height="700" fill="#1a2a44" opacity="0.4"/>{sea(700, "#0b1525")}
<ellipse cx="1500" cy="700" rx="300" ry="60" fill="#ffd27a" opacity="0.35" filter="url(#b30)"/><circle cx="1500" cy="560" r="10" fill="#fff"/>
{"".join(f'<path d="M1500 560 l{60*math.cos(a):.0f} {60*math.sin(a):.0f}" stroke="#fff6c8" stroke-width="4"/>' for a in [k*0.785 for k in range(8)])}
{lifeboat(200, 780, 1.3, 7)}{text(700, 300, "A LIGHT ON THE HORIZON", 64, 900, "#f4f1ea", "middle", 4)}''', "#0b1525")
S[38] = lambda: svg(f'''<rect width="{W}" height="700" fill="#33465e"/>{sea(700, "#1c2c40")}
<g transform="translate(400 380)"><path d="M0 120 L900 120 L870 230 Q450 250 40 230 Z" fill="#20242c" stroke="{INK}" stroke-width="7"/>
<path d="M120 120 L760 120 L740 60 L140 60 Z" fill="#e9e4d8" stroke="{INK}" stroke-width="6"/><path d="M400 60 L420 -60 L480 -60 L500 60 Z" fill="#c8562e" stroke="{INK}" stroke-width="6"/>
{text(450, 200, "CARPATHIA", 44, 900, "#e9e4d8", "middle", 6, "Inter")}</g>
{iceberg(1450, 520, 0.6)}{iceberg(120, 560, 0.4)}{text(960, 960, "SHE RACED THROUGH THE ICE IN THE DARK", 46, 800, "#f4f1ea", "middle", 4, "Inter")}''', "#33465e")
def saved():
    a = "".join(f'<circle cx="{220+(i%25)*26}" cy="{420+(i//25)*26}" r="9" fill="{TEAL}"/>' for i in range(35))
    b = "".join(f'<circle cx="{1050+(i%25)*26}" cy="{420+(i//25)*26}" r="9" fill="#6b7079"/>' for i in range(75))
    return svg(f'''{text(540, 300, "ABOUT 700 SAVED", 70, 900, TEAL, "middle")}{a}{text(1380, 300, "ABOUT 1,500 LOST", 70, 900, "#cfd3da", "middle")}{b}
{text(960, 900, "1 dot = 20 people", 34, 500, "#9aa0a8", "middle", 2, "Inter")}''', "#0e1015")
S[39] = saved
S[40] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3a3f48"/>
{"".join(f'<path d="M{(i*53)%1920} {(i*97)%600} l-12 60" stroke="#9fb3c8" stroke-width="3" opacity="0.5"/>' for i in range(160))}
<rect x="0" y="780" width="{W}" height="300" fill="#4a4036" stroke="{INK}" stroke-width="7"/>
{"".join(person(80+i*150, 520, 0.8, ["#1b1c20","#3a3b42","#4a3a2a"][i%3]) + f'<path d="M{100+i*150} 520 Q{130+i*150} 460 {160+i*150} 520 Z" fill="#111" stroke="{INK}" stroke-width="4"/>' for i in range(12))}
{text(960, 160, "NEW YORK · APRIL 18, 1912", 60, 900, "#f4f1ea", "middle", 6, "Inter")}''')
S[41] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2a2620"/><g transform="rotate(-2 960 540)"><rect x="460" y="90" width="1000" height="900" fill="{SEPIA}" stroke="{INK}" stroke-width="10"/>
{text(960, 230, "NEW RULES AT SEA", 72, 900, "#7a1f1f", "middle", 4)}<path d="M560 270 L1360 270" stroke="{INK}" stroke-width="5"/>
{text(580, 420, "✓  Lifeboats for every person", 46, 700, "#2a2a2a", "start", 0, "Inter")}
{text(580, 540, "✓  Radio watch day and night", 46, 700, "#2a2a2a", "start", 0, "Inter")}
{text(580, 660, "✓  Ice patrol in the North Atlantic", 46, 700, "#2a2a2a", "start", 0, "Inter")}</g>''')
S[42] = lambda: svg(f'''<rect width="{W}" height="700" fill="#e8b98a"/><ellipse cx="1400" cy="700" rx="500" ry="200" fill="#ffd9a0" opacity="0.8"/>{sea(700, "#4a6680")}
<rect x="0" y="760" width="{W}" height="40" fill="#e9e4d8" stroke="{INK}" stroke-width="6"/>{ava(420, 300, 1.2, "calm", 12, coat="#6b6f78", scarf="#9aa0a8")}''', "#e8b98a")
S[43] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#151820"/><ellipse cx="760" cy="560" rx="600" ry="500" fill="url(#ylamp)"/>{ava(360, 160, 1.8, "smile", 6, hat="1912")}
{text(1400, 480, "I'M AVA.", 120, 900, "#f4f1ea", "middle")}{text(1400, 620, "AND I WAS THERE.", 80, 900, TEAL, "middle")}''')
S[44] = lambda: svg(f'''{text(960, 220, "WHERE SHOULD I GO NEXT?", 100, 900, "#f4f1ea", "middle", -2)}
{"".join(f'<rect x="{240+i*370}" y="320" width="330" height="300" rx="24" fill="#1b1d23" stroke="{TEAL}" stroke-width="6"/>' + text(405+i*370, 500, "?", 160, 900, TEAL, "middle") for i in range(4))}
{text(960, 760, "Write it in the comments. The best idea might be my next story.", 44, 500, "#cfd3da", "middle")}
<rect x="760" y="860" width="400" height="100" rx="50" fill="#e23b3b"/>{text(960, 928, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}''', "#101114")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
