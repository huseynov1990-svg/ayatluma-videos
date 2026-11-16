import os, sys
from kit import *

OUT = "ep1/scenes"
os.makedirs(OUT, exist_ok=True)

def big_phone(cx, cy, screen, rot=-4, ring=False, s=1.0):
    rings = ""
    if ring:
        rings = "".join(f'<path d="M{-60-i*40} {120+i*10} Q{-90-i*45} 400 {-60-i*40} {680-i*10}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.7-i*0.2}" stroke-linecap="round"/>'
                        f'<path d="M{480+i*40} {120+i*10} Q{510+i*45} 400 {480+i*40} {680-i*10}" fill="none" stroke="{ACC}" stroke-width="8" opacity="{0.7-i*0.2}" stroke-linecap="round"/>' for i in range(3))
    return f'''<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-210 -400)">
  <ellipse cx="210" cy="400" rx="420" ry="520" fill="url(#ylamp)"/>{rings}
  <rect x="0" y="0" width="420" height="800" rx="56" fill="#0b0b0d" stroke="{INK}" stroke-width="12"/>
  <rect x="22" y="22" width="376" height="756" rx="40" fill="#15161b"/>
  <rect x="160" y="40" width="100" height="22" rx="11" fill="#0b0b0d"/>
  {screen}</g>'''

def screen_call(name, sub, timer=None):
    t = text(210, 600, timer, 34, 500, "#cfd3da", "middle") if timer else ""
    return f'''<circle cx="210" cy="250" r="86" fill="#2a2c33" stroke="#3a3c44" stroke-width="4"/>
  <path d="M170 280 Q210 190 250 280 M185 240 A25 25 0 1 1 235 240 A25 25 0 1 1 185 240" fill="#6b7079"/>
  {text(210, 400, name, 46, 800, "#f4f1ea", "middle")}
  {text(210, 450, sub, 28, 500, "#9aa0a8", "middle")}{t}'''

def screen_msg(lines, big=None):
    y = 300; out = ""
    for ln in lines:
        out += text(70, y, ln, 30, 500, "#e8e6e0"); y += 42
    bubble = f'<rect x="46" y="250" width="330" height="{len(lines)*42+40}" rx="22" fill="#2a2c33"/>'
    b = text(210, 560, big, 88, 900, ACC, "middle", 10) if big else ""
    return f'''{text(210, 140, "Unknown", 34, 800, "#f4f1ea", "middle")}{text(210, 180, "Text message · 1:13 AM", 22, 500, "#8a9098", "middle")}{bubble}{out}{b}'''

def card(lines, bg="#101114", extra=""):
    out = ""
    for (x, y, s, size, w, fill, anc) in lines:
        out += text(x, y, s, size, w, fill, anc, -1)
    return svg(extra + out, bg)

def street(eli_g, seed=1):
    return svg(f'''
<rect x="0" y="0" width="{W}" height="700" fill="#151821"/>
<path d="M0 640 L300 520 L300 120 L0 60 Z" fill="#1d2029" stroke="{INK}" stroke-width="8"/>
<path d="M1920 640 L1560 520 L1560 100 L1920 30 Z" fill="#1d2029" stroke="{INK}" stroke-width="8"/>
<rect x="420" y="220" width="1020" height="300" fill="#191c25"/>
{bokeh([(520,300,60,"#d9475c",.5),(800,260,45,ACC,.4),(1100,330,70,"#3d7bd9",.45),(1350,280,50,"#d9475c",.35),(150,250,40,ACC,.4),(1750,260,55,"#3d7bd9",.4)])}
<path d="M0 700 L1920 700 L1920 1080 L0 1080 Z" fill="#1b1d23"/>
<path d="M0 700 L1920 700" stroke="{INK}" stroke-width="8"/>
<g opacity="0.5" filter="url(#b8)"><rect x="480" y="760" width="40" height="300" fill="#d9475c" opacity=".4"/><rect x="900" y="740" width="30" height="320" fill="{ACC}" opacity=".35"/><rect x="1300" y="760" width="50" height="300" fill="#3d7bd9" opacity=".4"/></g>
<path d="M0 880 L1920 880" stroke="#3a3c44" stroke-width="6" stroke-dasharray="80 60"/>
{eli_g}
{rain(0, 0, W, H, 420, seed)}''', "#14161c")

def station_hall(extra, light=True):
    return svg(f'''
<path d="M0 0 L1920 0 L1920 120 L0 120 Z" fill="#101116"/>
<path d="M0 120 L1920 120 L1920 860 L0 860 Z" fill="#1c1e24"/>
{"".join(f'<rect x="{x}" y="120" width="40" height="740" fill="#17191e" stroke="{INK}" stroke-width="6"/>' for x in (240, 760, 1280, 1800))}
<path d="M0 860 L1920 860 L1920 1080 L0 1080 Z" fill="#26282e"/>
<path d="M0 860 L1920 860" stroke="{INK}" stroke-width="8"/>
{"".join(f'<path d="M{x} 860 L{x*1.4-380:.0f} 1080" stroke="#1f2126" stroke-width="5"/>' for x in range(0, 1921, 160))}
{'<ellipse cx="960" cy="160" rx="700" ry="420" fill="url(#lamp)"/>' if light else ''}
<rect x="900" y="120" width="120" height="16" fill="#e9e3d6" opacity="{0.9 if light else 0.25}"/>
{extra}''', "#121318")

S = {}
# 1 phone ringing at 1:12
S[1] = lambda: svg(f'''
<rect x="0" y="640" width="{W}" height="440" fill="#2b2c33"/><rect x="0" y="620" width="{W}" height="30" fill="#cfc9bd" stroke="{INK}" stroke-width="8"/>
{bokeh([(300,250,90,"#d9475c",.35),(1600,200,110,"#3d7bd9",.35),(1000,150,70,ACC,.25)])}
{big_phone(960, 560, screen_call("Unknown", "incoming call...", "1:12 AM"), -8, True, 0.9)}''')
# 2 title card
S[2] = lambda: svg(f'''
{stranger(1480, 260, 0.75, 0.55)}{stranger(1240, 300, 0.7, 0.4)}{stranger(1700, 320, 0.68, 0.35)}
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#fadeB)"/>
{text(150, 470, "WRONG", 190, 900, "#f4f1ea", "start", -4)}
{text(150, 650, "NUMBER", 190, 900, ACC, "start", -4)}
{text(158, 740, "EPISODE 1  ·  LOCKER 14", 38, 600, "#b9bec7", "start", 8, "Inter")}''', "#0f1013")
# 3 Eli on bike
S[3] = lambda: street(eli(640, 240, 1.0, "bike", "calm"), 3)
# 4 diner, Eli with letter
def diner(e, clock="1:12"):
    return svg(f'''
<rect x="0" y="0" width="{W}" height="620" fill="#1f2026"/>
<rect x="150" y="90" width="1060" height="520" fill="#0e1420" stroke="{INK}" stroke-width="10"/>
{bokeh([(380,300,70,"#d9475c",.55),(720,230,55,ACC,.45),(980,360,80,"#3d7bd9",.45)])}
{rain(160, 100, 1040, 500, 260, 1)}
<path d="M680 90 L680 610" stroke="{INK}" stroke-width="10"/>
<circle cx="1560" cy="200" r="78" fill="#e9e3d6" stroke="{INK}" stroke-width="9"/>
<path d="M1560 200 L1560 142 M1560 200 L1580 210" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
<ellipse cx="1560" cy="120" rx="420" ry="300" fill="url(#lamp)"/>
<path d="M1180 300 Q1180 250 1240 250 L1840 250 Q1890 250 1890 300 L1890 820 L1180 820 Z" fill="#5a1f2a" stroke="{INK}" stroke-width="10"/>
<path d="M1300 260 L1300 800 M1460 260 L1460 800 M1620 260 L1620 800 M1780 260 L1780 800" stroke="#43161f" stroke-width="10"/>
{e}
<rect x="0" y="790" width="{W}" height="300" fill="#2b2c33"/>
<rect x="0" y="770" width="{W}" height="34" fill="#cfc9bd" stroke="{INK}" stroke-width="9"/>
<path d="M1060 720 L1150 720 L1140 790 L1070 790 Z" fill="#efe9dc" stroke="{INK}" stroke-width="8"/>
<path d="M1150 735 Q1185 745 1145 772" fill="none" stroke="{INK}" stroke-width="8"/>
<rect x="760" y="740" width="210" height="44" rx="6" fill="#efe9dc" stroke="{INK}" stroke-width="7" transform="rotate(-6 860 760)"/>
{text(780, 772, "FINAL NOTICE", 22, 700, "#b3263b", "start", 0, "Inter").replace("<text", '<text transform="rotate(-6 860 760)"')}''', "#17181c")
S[4] = lambda: diner(eli(1250, 330, 1.25, "sit_letter", "worried", -4))
# 5 letter close-up
S[5] = lambda: svg(f'''
<rect x="0" y="0" width="{W}" height="{H}" fill="#2b2c33"/>
<g transform="rotate(-4 960 540)">
<rect x="520" y="90" width="880" height="900" fill="#efe9dc" stroke="{INK}" stroke-width="10"/>
{text(600, 220, "FINAL NOTICE", 84, 900, "#b3263b", "start", 2)}
<path d="M600 260 L1320 260" stroke="{INK}" stroke-width="5"/>
{text(600, 340, "Tenant: Eli Brooks", 36, 600, "#2a2a2a", "start", 0, "Inter")}
{text(600, 400, "Unit 4B, 211 Mercer St.", 36, 500, "#2a2a2a", "start", 0, "Inter")}
{text(600, 520, "Amount due:", 40, 600, "#2a2a2a", "start", 0, "Inter")}
{text(600, 640, "$1,800", 130, 900, INK)}
{text(600, 760, "Pay by Friday or vacate the unit.", 36, 500, "#2a2a2a", "start", 0, "Inter")}
<ellipse cx="1180" cy="880" rx="120" ry="60" fill="none" stroke="#8a5a3a" stroke-width="10" opacity="0.4"/>
</g>''')
# 6 phone rings on table (diner)
S[6] = lambda: svg(f'''
{bokeh([(400,260,90,"#d9475c",.4),(1500,230,100,"#3d7bd9",.4)])}
<rect x="0" y="560" width="{W}" height="520" fill="#2b2c33"/><rect x="0" y="540" width="{W}" height="30" fill="#cfc9bd" stroke="{INK}" stroke-width="8"/>
<path d="M300 520 L420 520 L408 600 L312 600 Z" fill="#efe9dc" stroke="{INK}" stroke-width="8"/>
{big_phone(980, 640, screen_call("Unknown", "incoming call..."), 76, True, 0.75)}''')
# 7 diner, phone at ear, surprised
S[7] = lambda: diner(eli(1250, 330, 1.25, "sit_phone", "surprised"))
# 8 the voice - shadow caller
S[8] = lambda: svg(f'''
<rect x="0" y="0" width="{W}" height="{H}" fill="#0c0d10"/>
<ellipse cx="1250" cy="480" rx="700" ry="600" fill="url(#blue)" opacity="0.6"/>
{stranger(1050, 160, 1.15, 1)}
<rect x="1300" y="330" width="60" height="110" rx="10" fill="#0b0b0d" stroke="{INK}" stroke-width="6"/>
<path d="M1150 900 L1150 1080" stroke="#0c0d10" stroke-width="400"/>
{text(150, 470, '"You\'re the', 96, 300, "#f4f1ea")}{text(150, 590, 'courier?"', 96, 300, "#f4f1ea")}''')
# 9 route map
def route():
    return svg(f'''
<rect x="0" y="0" width="{W}" height="{H}" fill="#121318"/>
{"".join(f'<path d="M{x} 0 L{x} {H}" stroke="#1d1f26" stroke-width="3"/>' for x in range(0, W, 80))}
{"".join(f'<path d="M0 {y} L{W} {y}" stroke="#1d1f26" stroke-width="3"/>' for y in range(0, H, 80))}
<path d="M0 820 Q600 760 1100 900 T1920 840 L1920 1080 L0 1080 Z" fill="#14233a"/>
{text(1500, 1000, "EAST RIVER", 30, 700, "#3d5c86", "middle", 10, "Inter")}
<path d="M430 360 C700 360 820 600 1060 620 S1420 760 1480 780" fill="none" stroke="{ACC}" stroke-width="9" stroke-dasharray="26 20" stroke-linecap="round"/>
<circle cx="430" cy="360" r="26" fill="{ACC}" stroke="{INK}" stroke-width="6"/>
<rect x="1450" y="740" width="60" height="84" fill="#2f6fd6" stroke="{INK}" stroke-width="6"/>
{text(430, 300, "GRAND ST. STATION", 40, 800, "#f4f1ea", "middle", 2)}{text(430, 440, "LOCKER 14", 34, 600, ACC, "middle", 6, "Inter")}
{text(1480, 700, "PIER 9 · BLUE DOOR", 40, 800, "#f4f1ea", "middle", 2)}
<rect x="120" y="80" width="420" height="110" rx="14" fill="#1b1d23" stroke="#2c2f37" stroke-width="4"/>
{text(150, 150, "BEFORE 2:00 AM", 44, 900, "#f4f1ea")}
<rect x="1380" y="80" width="420" height="110" rx="14" fill="{ACC}"/>
{text(1590, 157, "$5,000", 64, 900, INK, "middle")}''')
S[9] = route
# 10 don't open it
S[10] = lambda: card([(960, 520, "DON'T OPEN IT.", 170, 900, "#f4f1ea", "middle"),
                      (960, 650, "DON'T CALL THIS NUMBER.", 60, 700, ACC, "middle")], "#0e0f12")
# 11 call ended
S[11] = lambda: svg(f'''{bokeh([(500,300,120,"#3d7bd9",.25)])}{big_phone(960, 540, screen_call("Unknown", "Call ended", "00:21"), 0, False, 1.0)}''', "#111216")
# 12 text code
S[12] = lambda: svg(f'''{big_phone(960, 540, screen_msg(["Locker 14. Code:"], "7319"), 3, False, 1.0)}''', "#111216")
# 13 Eli face close lit by phone
S[13] = lambda: svg(f'''
<rect x="0" y="0" width="{W}" height="{H}" fill="#101116"/>
{bokeh([(300,300,120,"#d9475c",.3),(1650,250,140,"#3d7bd9",.3)])}
{eli(560, 40, 2.4, "face_close", "worried", 4)}
{text(1500, 980, "WRONG NUMBER.", 44, 800, ACC, "middle", 6, "Inter")}''')
# 14 $5,000 = 3 months
S[14] = lambda: svg(f'''
{text(960, 230, "$5,000", 170, 900, ACC, "middle")}
{text(960, 320, "almost three months of rent", 50, 500, "#cfd3da", "middle")}
{"".join(f'<rect x="{560+i*290}" y="{620-150}" width="220" height="300" rx="16" fill="#1d1f26" stroke="{ACC}" stroke-width="6"/>' + text(670+i*290, 640, m, 40, 800, "#f4f1ea", "middle") + text(670+i*290, 700, "$1,800", 34, 500, "#9aa0a8", "middle") for i, m in enumerate(["DEC", "JAN", "FEB"]))}
{text(960, 880, "...or out by Friday.", 46, 600, "#b3263b", "middle")}''', "#101114")
# 15 rides into the rain (wide)
S[15] = lambda: street(eli(1100, 300, 0.9, "bike", "determined"), 15)
# 16 middle CTA
S[16] = lambda: svg(f'''
{text(960, 300, "WHAT'S IN LOCKER 14?", 100, 900, "#f4f1ea", "middle", -2)}
<rect x="610" y="420" width="420" height="120" rx="60" fill="#e23b3b"/>{text(820, 500, "SUBSCRIBE", 52, 900, "#ffffff", "middle")}
<circle cx="1150" cy="480" r="60" fill="#1d1f26" stroke="{ACC}" stroke-width="6"/>
<path d="M1120 500 Q1120 440 1150 438 Q1180 440 1180 500 L1188 510 L1112 510 Z M1140 516 Q1150 530 1160 516" fill="{ACC}"/>
{text(960, 740, "Would you have gone?", 70, 700, ACC, "middle")}
{text(960, 820, "Tell me in the comments.", 44, 500, "#cfd3da", "middle")}''', "#101114")
# 17 empty station, guard asleep
S[17] = lambda: station_hall(f'''
<rect x="1360" y="560" width="380" height="300" fill="#2e3138" stroke="{INK}" stroke-width="8"/>
<rect x="1390" y="590" width="320" height="130" fill="#0e1015" stroke="{INK}" stroke-width="6"/>
<g transform="translate(1470 520) scale(0.5)">
 <ellipse cx="200" cy="190" rx="70" ry="80" fill="{SKIN}" stroke="{INK}" stroke-width="10" transform="rotate(30 200 190)"/>
 <path d="M126 150 Q130 90 200 86 Q270 90 280 150 Z" fill="#23324d" stroke="{INK}" stroke-width="10" transform="rotate(30 200 190)"/>
 <path d="M168 190 L188 190 M218 200 L238 200" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
</g>
{text(1560, 470, "Z z z", 50, 700, "#9aa0a8", "middle", 6)}
{text(150, 1010, "GRAND ST. STATION · 1:31 AM", 30, 700, "#7f858e", "start", 8, "Inter")}''')
# lockers
def lockers(e="", open14=False, glow=False, highlight=False):
    cells = []
    for c in range(9):
        for r in range(3):
            x = 260 + c * 150; y = 230 + r * 190; num = c * 3 + r + 1
            if num == 14 and open14:
                cells.append(f'<rect x="{x}" y="{y}" width="140" height="180" fill="#07080a" stroke="{INK}" stroke-width="8"/>'
                             + case_svg(x + 14, y + 96, 0.67, True, glow)
                             + f'<path d="M{x} {y} L{x-100} {y-20} L{x-100} {y+200} L{x} {y+180} Z" fill="#9aa0a6" stroke="{INK}" stroke-width="8"/>')
            else:
                hl = f'stroke="{ACC}" stroke-width="10"' if (num == 14 and highlight) else f'stroke="{INK}" stroke-width="8"'
                cells.append(f'<rect x="{x}" y="{y}" width="140" height="180" fill="#8d939a" {hl}/>'
                             f'<rect x="{x+22}" y="{y+22}" width="96" height="10" fill="#6c7178"/><rect x="{x+22}" y="{y+40}" width="96" height="10" fill="#6c7178"/>'
                             f'<circle cx="{x+112}" cy="{y+110}" r="8" fill="{INK}"/>' + text(x + 16, y + 164, f"{num:02d}", 22, 700, ACC if (num == 14 and highlight) else "#2a2c30", "start", 0, "Inter"))
    return svg(f'''<rect x="0" y="880" width="{W}" height="200" fill="#202228"/><path d="M0 880 L{W} 880" stroke="{INK}" stroke-width="8"/>
{"".join(cells)}<rect x="230" y="200" width="1420" height="18" fill="#2a2c32" stroke="{INK}" stroke-width="6"/>
<ellipse cx="900" cy="530" rx="520" ry="420" fill="url(#lamp)"/>{e}''')
S[18] = lambda: lockers(highlight=True)
# 19 keypad
S[19] = lambda: svg(f'''
<rect x="560" y="80" width="800" height="920" rx="30" fill="#8d939a" stroke="{INK}" stroke-width="12"/>
<rect x="640" y="160" width="640" height="170" rx="14" fill="#0c0d10" stroke="{INK}" stroke-width="8"/>
{text(960, 285, "7 3 1 9", 110, 800, ACC, "middle", 10, "Inter")}
{"".join(f'<rect x="{660+(i%3)*210}" y="{380+(i//3)*150}" width="180" height="120" rx="14" fill="#c9ced4" stroke="{INK}" stroke-width="7"/>' + text(750+(i%3)*210, 462+(i//3)*150, k, 60, 800, INK, "middle") for i, k in enumerate("123456789"))}
<circle cx="1300" cy="940" r="18" fill="#5fe08a"/>{text(1260, 952, "OPEN", 30, 800, "#5fe08a", "end", 4, "Inter")}''', "#15161b")
# 20 open locker w/ case close
S[20] = lambda: svg(f'''
<rect x="360" y="60" width="1200" height="960" fill="#07080a" stroke="{INK}" stroke-width="14"/>
<path d="M360 60 L80 0 L80 1080 L360 1020 Z" fill="#9aa0a6" stroke="{INK}" stroke-width="12"/>
<ellipse cx="960" cy="640" rx="560" ry="360" fill="url(#lamp)"/>
{case_svg(660, 520, 3.6, True, True)}
{text(1520, 140, "14", 80, 900, "#2a2c30", "end")}''', "#0d0e11")
# 21 Eli holds case, humming
def hum(cx, cy, r0=180):
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{r0+i*70}" fill="none" stroke="{ACC}" stroke-width="5" opacity="{0.5-i*0.12:.2f}" stroke-dasharray="14 18"/>' for i in range(4))
S[21] = lambda: station_hall(f'''{hum(960, 760, 160)}{eli(760, 300, 1.15, "hold_case", "scared")}''')
# 22 door closing at end of hall
S[22] = lambda: svg(f'''
<path d="M0 0 L1920 0 L1240 380 L680 380 Z" fill="#101116"/>
<path d="M0 0 L680 380 L680 760 L0 1080 Z" fill="#1a1c22" stroke="{INK}" stroke-width="8"/>
<path d="M1920 0 L1240 380 L1240 760 L1920 1080 Z" fill="#1a1c22" stroke="{INK}" stroke-width="8"/>
<path d="M0 1080 L680 760 L1240 760 L1920 1080 Z" fill="#26282e" stroke="{INK}" stroke-width="8"/>
<rect x="680" y="380" width="560" height="380" fill="#0b0c0f" stroke="{INK}" stroke-width="8"/>
<rect x="860" y="470" width="200" height="290" fill="#2a2c33" stroke="{INK}" stroke-width="7"/>
<rect x="866" y="476" width="40" height="278" fill="#e9e3d6" opacity="0.5"/>
<circle cx="1036" cy="620" r="8" fill="{ACC}"/>
<ellipse cx="960" cy="420" rx="320" ry="200" fill="url(#lamp)"/>''', "#0e0f12")
# 23 man in grey coat watching
S[23] = lambda: station_hall(f'''<path d="M1040 860 L1500 1080 L1700 1080 L1160 860 Z" fill="#000" opacity="0.35"/>{stranger(960, 180, 0.95)}''', light=True)
# 24 phone: don't trust the man in grey
S[24] = lambda: svg(f'''{big_phone(960, 540, screen_msg(["Don't trust", "the man in grey."]), -3, True, 1.0)}''', "#111216")
# 25 Eli runs, stranger behind
S[25] = lambda: station_hall(f'''{stranger(1560, 380, 0.55, 0.8)}{eli(520, 300, 1.15, "run", "scared", -6)}''')
# 26 riding to river
S[26] = lambda: svg(f'''
<rect x="0" y="0" width="{W}" height="620" fill="#121722"/>
{"".join(f'<rect x="{x}" y="{620-h}" width="{w}" height="{h}" fill="#1a1f2b" stroke="{INK}" stroke-width="6"/>' for x, w, h in [(0,220,420),(240,160,300),(420,260,500),(700,180,360),(1300,240,460),(1560,200,320),(1780,180,420)])}
{bokeh([(300,300,40,ACC,.35),(520,220,30,ACC,.3),(1400,260,40,"#3d7bd9",.35),(1660,340,35,ACC,.3)])}
<path d="M0 620 L1920 620 L1920 1080 L0 1080 Z" fill="#0f1a2b"/>
{"".join(f'<path d="M{x} {660+(x%5)*60} L{x+120} {660+(x%5)*60}" stroke="{ACC}" stroke-width="4" opacity="0.25"/>' for x in range(0, 1920, 170))}
<path d="M0 760 L1920 760 L1920 820 L0 820 Z" fill="#2b2d33" stroke="{INK}" stroke-width="6"/>
{eli(600, 160, 0.95, "bike", "determined")}
<path d="M200 380 L460 380 M140 470 L420 470 M240 560 L480 560" stroke="#cfd3da" stroke-width="8" stroke-linecap="round" opacity="0.5"/>
{rain(0, 0, W, H, 500, 26)}''', "#101318")
# 27 pier 9 blue door
def pier(e=""):
    return svg(f'''
<rect x="0" y="0" width="{W}" height="700" fill="#0f131c"/>
<rect x="520" y="180" width="1100" height="520" fill="#2a2e38" stroke="{INK}" stroke-width="10"/>
<path d="M500 190 L1070 40 L1640 190" fill="#232731" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>
{text(1070, 150, "PIER 9", 64, 900, "#cfd3da", "middle", 8)}
<rect x="980" y="400" width="180" height="300" fill="#2f6fd6" stroke="{INK}" stroke-width="9"/>
<circle cx="1135" cy="560" r="10" fill="{INK}"/>
<path d="M1070 330 L1070 370" stroke="{INK}" stroke-width="6"/><ellipse cx="1070" cy="380" rx="34" ry="14" fill="#e9e3d6"/>
<ellipse cx="1070" cy="520" rx="380" ry="300" fill="url(#lamp)"/>
<ellipse cx="1070" cy="560" rx="260" ry="220" fill="url(#blue)"/>
<path d="M0 700 L1920 700 L1920 1080 L0 1080 Z" fill="#2b2620"/>
{"".join(f'<path d="M0 {y} L1920 {y}" stroke="#1d1a16" stroke-width="5"/>' for y in range(740, 1080, 50))}
<path d="M0 700 L1920 700" stroke="{INK}" stroke-width="8"/>
{e}{rain(0, 0, W, H, 380, 27)}''', "#0d1016")
S[27] = lambda: pier(eli(260, 420, 0.75, "stand", "worried", 6))
# 28 clock 1:54
S[28] = lambda: svg(f'''
{text(960, 560, "1:54", 300, 900, "#f4f1ea", "middle", -6)}
{text(960, 700, "SIX MINUTES LEFT", 56, 800, ACC, "middle", 12, "Inter")}''', "#0e0f12")
# 29 Eli with case in front of door
S[29] = lambda: pier(f'''{hum(1040, 840, 120)}{eli(840, 380, 1.0, "hold_case", "scared")}''')
# 30 ticking
S[30] = lambda: svg(f'''
<ellipse cx="960" cy="560" rx="700" ry="420" fill="url(#ylamp)"/>
{case_svg(660, 380, 3.6, True, False)}
{text(1560, 260, "tick", 70, 300, ACC, "middle", 4, "Inter")}{text(1650, 360, "tick", 54, 300, ACC, "middle", 4, "Inter")}{text(1720, 440, "tick", 40, 300, ACC, "middle", 4, "Inter")}''', "#0c0d10")
# 31 option OPEN
S[31] = lambda: svg(f'''
<ellipse cx="960" cy="600" rx="600" ry="420" fill="url(#ylamp)"/>
{"".join(f'<path d="M960 560 L{960+700*__import__("math").cos(a):.0f} {560-700*abs(__import__("math").sin(a)):.0f}" stroke="{ACC}" stroke-width="{18-abs(i-4)*3}" opacity="0.18"/>' for i, a in enumerate([0.5+0.27*k for k in range(9)]))}
<g transform="translate(660 520) scale(3.6)">
<path d="M0 40 L14 -30 L182 -30 L168 40 Z" fill="#8d939a" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<rect x="0" y="40" width="168" height="72" rx="10" fill="#a7adb5" stroke="{INK}" stroke-width="3"/>
<path d="M6 42 L162 42" stroke="{ACC}" stroke-width="5"/>
<rect x="56" y="64" width="56" height="22" rx="3" fill="{ACC}" stroke="{INK}" stroke-width="2"/></g>
{text(960, 220, "OPEN IT?", 130, 900, "#f4f1ea", "middle", -2)}''', "#0c0d10")
# 32 option DELIVER
S[32] = lambda: pier(f'''{text(1070, 330, "", 10)}<rect x="0" y="0" width="{W}" height="{H}" fill="#000" opacity="0.25"/>
{text(1070, 980, "OR KNOCK?", 130, 900, "#f4f1ea", "middle", -2)}''')
# 33 vote card
S[33] = lambda: svg(f'''
{text(960, 200, "WHAT SHOULD ELI DO?", 90, 900, "#f4f1ea", "middle", -2)}
<rect x="260" y="300" width="640" height="420" rx="28" fill="#1b1d23" stroke="{ACC}" stroke-width="8"/>
<rect x="1020" y="300" width="640" height="420" rx="28" fill="#1b1d23" stroke="#2f6fd6" stroke-width="8"/>
{case_svg(470, 380, 1.3, True, True)}
<rect x="1280" y="360" width="120" height="180" fill="#2f6fd6" stroke="{INK}" stroke-width="7"/>
{text(580, 660, "OPEN", 96, 900, ACC, "middle", 4)}{text(1340, 660, "DELIVER", 96, 900, "#5b9cff", "middle", 4)}
{text(960, 830, "Comment your answer. The most popular one decides Episode 2.", 40, 500, "#cfd3da", "middle")}
<rect x="760" y="900" width="400" height="100" rx="50" fill="#e23b3b"/>{text(960, 968, "SUBSCRIBE", 46, 900, "#ffffff", "middle")}''', "#101114")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg")
        print("ok", i, flush=True)
