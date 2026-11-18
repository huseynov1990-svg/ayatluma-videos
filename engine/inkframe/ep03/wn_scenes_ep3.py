"""WRONG NUMBER S01E03 - 'Under the Pier'. Keep the key, run, Walter, the watch, tunnel to door nine."""
import os, sys, random, math
E = "/home/claude/ayatluma-videos/engine/inkframe"
sys.path.insert(0, E); sys.path.insert(0, E + "/ep02")
from kit import *
from phone_helpers import big_phone
from wn_scenes_ep2 import water, boards, lamp, key, woman, big, subscribe, RED, BLUE, BRASS, SEPIA
OUT = "/home/claude/work/wn3/scenes"; os.makedirs(OUT, exist_ok=True)
BRICK = "#5a2f24"; BRICK2 = "#43231b"; IRON = "#1e2024"

def watch2(cx, cy, s=1.0, hh=2, mm=0, glow=True, back=False, open_=False):
    g = f'<circle r="280" fill="{ACC}" opacity="0.12"/>' if glow else ""
    if back:
        face = (f'<circle r="138" fill="{BRASS}" stroke="{INK}" stroke-width="9"/><circle r="118" fill="#d8b860" stroke="{INK}" stroke-width="4"/>'
                f'{text(0, -20, "To Daniel.", 34, 700, "#5a4310", "middle", 0, "Inter")}{text(0, 28, "Come home", 30, 700, "#5a4310", "middle", 0, "Inter")}'
                f'{text(0, 66, "before two.", 30, 700, "#5a4310", "middle", 0, "Inter")}')
    else:
        ticks_ = "".join(f'<path d="M0 -112 L0 -96" stroke="{INK}" stroke-width="6" transform="rotate({i*30})"/>' for i in range(12))
        ah = (hh % 12) * 30 + mm * 0.5; am = mm * 6
        face = (f'<circle r="138" fill="{BRASS}" stroke="{INK}" stroke-width="9"/><circle r="120" fill="#f1e9d4" stroke="{INK}" stroke-width="5"/>{ticks_}'
                f'{text(0, -60, "XII", 26, 800, INK, "middle", 0, "Inter")}'
                f'<path d="M0 0 L0 -66" stroke="{INK}" stroke-width="10" stroke-linecap="round" transform="rotate({ah})"/>'
                f'<path d="M0 0 L0 -100" stroke="{INK}" stroke-width="5" stroke-linecap="round" transform="rotate({am})"/><circle r="10" fill="{INK}"/>')
    lid = f'<ellipse cx="-250" cy="0" rx="40" ry="138" fill="{BRASS}" stroke="{INK}" stroke-width="8"/>' if open_ else ""
    return f'''<g transform="translate({cx} {cy}) scale({s})">{g}{lid}<path d="M-30 -150 L30 -150 L22 -128 L-22 -128 Z" fill="{BRASS}" stroke="{INK}" stroke-width="6"/>
  <circle cx="0" cy="-168" r="22" fill="none" stroke="{BRASS}" stroke-width="10"/>{face}</g>'''

def walter(x, y, s=1.0, hat=False, mood="tired"):
    eyes = {"tired": f'<path d="M118 180 Q128 172 140 180 M160 180 Q172 172 182 180" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>',
            "down": f'<path d="M118 186 L140 186 M160 186 L182 186" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>',
            "scared": f'<circle cx="128" cy="178" r="8" fill="{INK}"/><circle cx="172" cy="178" r="8" fill="{INK}"/>'}[mood]
    h = (f'<path d="M60 130 L240 130 L222 90 Q150 56 78 90 Z" fill="#1b1c20" stroke="{INK}" stroke-width="7"/>'
         f'<rect x="40" y="122" width="220" height="16" rx="6" fill="#1b1c20" stroke="{INK}" stroke-width="6"/>') if hat else \
        f'<path d="M86 150 Q84 96 150 92 Q216 96 214 150 Q200 118 150 116 Q100 118 86 150 Z" fill="#b9bcc2" stroke="{INK}" stroke-width="6"/>'
    return f'''<g transform="translate({x} {y}) scale({s})">
  <path d="M30 900 L40 300 Q80 240 150 240 Q220 240 260 300 L272 900 Z" fill="#4b4e55" stroke="{INK}" stroke-width="8"/>
  <path d="M150 250 L150 900" stroke="{INK}" stroke-width="5" opacity="0.6"/><path d="M90 260 L150 390 L210 260" fill="none" stroke="{INK}" stroke-width="6"/>
  <ellipse cx="150" cy="180" rx="66" ry="80" fill="#cbb8a2" stroke="{INK}" stroke-width="8"/>
  {eyes}<path d="M110 160 L130 158 M170 158 L190 160" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
  <path d="M150 186 Q144 206 156 208" fill="none" stroke="{INK}" stroke-width="4"/><path d="M128 230 Q150 222 172 230" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
  <path d="M176 196 L200 238" stroke="#8a4a3a" stroke-width="6" stroke-linecap="round"/>
  <path d="M106 214 Q112 236 130 244 M194 214 Q188 236 170 244" stroke="#8a7a6a" stroke-width="3" fill="none"/>{h}</g>'''

def bricks(x0, y0, w, h, c=BRICK, seed=1, op=1):
    r = random.Random(seed); out = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{c}" opacity="{op}"/>'
    for j, yy in enumerate(range(int(y0), int(y0 + h), 46)):
        out += f'<path d="M{x0} {yy} L{x0+w} {yy}" stroke="{BRICK2}" stroke-width="5" opacity="{op}"/>'
        off = 0 if j % 2 else 50
        for xx in range(int(x0) + off, int(x0 + w), 100):
            out += f'<path d="M{xx} {yy} L{xx} {yy+46}" stroke="{BRICK2}" stroke-width="5" opacity="{op}"/>'
    return out

def tunnel(vx=960, vy=470, light=True, red=False, doors=True, nums=("5", "6", "7", "8")):
    """one-point perspective brick tunnel"""
    out = f'<rect width="{W}" height="{H}" fill="#0a0806"/>'
    out += f'<polygon points="0,0 {vx-140},{vy-110} {vx+140},{vy-110} {W},0" fill="#2a1712"/>'
    out += f'<polygon points="0,{H} {vx-140},{vy+110} {vx+140},{vy+110} {W},{H}" fill="#1c1410"/>'
    out += f'<polygon points="0,0 {vx-140},{vy-110} {vx-140},{vy+110} 0,{H}" fill="{BRICK}"/>'
    out += f'<polygon points="{W},0 {vx+140},{vy-110} {vx+140},{vy+110} {W},{H}" fill="{BRICK2}"/>'
    for k in range(1, 9):
        f = k / 9
        xl = f * (vx - 140); xr = W - f * (W - vx - 140); yt = f * (vy - 110); yb = H - f * (H - vy - 110)
        out += f'<path d="M{xl:.0f} {yt:.0f} L{xl:.0f} {yb:.0f} M{xr:.0f} {yt:.0f} L{xr:.0f} {yb:.0f}" stroke="#2a130e" stroke-width="{8-k*0.6:.1f}" opacity="0.7"/>'
    for k in range(1, 12):
        y1 = k * 90
        out += f'<path d="M0 {y1} L{vx-140} {vy-110+ (220*k/12):.0f}" stroke="#2a130e" stroke-width="3" opacity="0.5"/>'
        out += f'<path d="M{W} {y1} L{vx+140} {vy-110+ (220*k/12):.0f}" stroke="#1a0c08" stroke-width="3" opacity="0.5"/>'
    if doors:
        for i, (f, n) in enumerate(zip([0.12, 0.42, 0.62, 0.76], nums)):
            left = i % 2 == 0
            x = f * (vx - 140) if left else W - f * (W - vx - 140)
            dh = (1 - f) * 560; dw = (1 - f) * 150; yt = f * (vy - 110) + (1 - f) * 260
            xx = x + 10 if left else x - dw - 10
            out += f'<rect x="{xx:.0f}" y="{yt:.0f}" width="{dw:.0f}" height="{dh:.0f}" fill="{IRON}" stroke="{INK}" stroke-width="{max(3,8*(1-f)):.0f}"/>'
            out += text(xx + dw / 2, yt + dh * 0.22, n, max(18, 90 * (1 - f)), 900, BRASS, "middle")
    if light:
        out += f'<polygon points="960,1080 {vx-260},{vy-60} {vx+260},{vy-60}" fill="#f6e7c4" opacity="0.10"/>'
    if red:
        out += f'<ellipse cx="{vx}" cy="{vy+40}" rx="34" ry="80" fill="{RED}" opacity="0.85" filter="url(#b8)"/><ellipse cx="{vx}" cy="{vy-34}" rx="16" ry="18" fill="#141414"/>'
    return out

def iron_door(cx=960, top=120, w=560, h=860, knock=False):
    rivets = "".join(f'<circle cx="{cx-w/2+40+i*((w-80)/6):.0f}" cy="{top+40+j*((h-80)/8):.0f}" r="9" fill="#3a3d44" stroke="{INK}" stroke-width="3"/>'
                     for i in range(7) for j in (0, 8))
    kn = ""
    if knock:
        kn = "".join(f'<path d="M{cx-150-i*40} {top+330+i*30} q-60 40 0 80 M{cx+150+i*40} {top+330+i*30} q60 40 0 80" stroke="{ACC}" stroke-width="8" fill="none" opacity="{0.8-i*0.2}"/>' for i in range(3))
    return f'''{bricks(0, 0, W, H, BRICK, 3)}<rect x="{cx-w/2-30}" y="{top-30}" width="{w+60}" height="{h+60}" fill="#140c08"/>
  <rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}" fill="{IRON}" stroke="{INK}" stroke-width="12"/>
  <rect x="{cx-w/2+40}" y="{top+120}" width="{w-80}" height="{h-200}" fill="none" stroke="#2c2f35" stroke-width="10"/>{rivets}
  <rect x="{cx-70}" y="{top+30}" width="140" height="90" rx="10" fill="{BRASS}" stroke="{INK}" stroke-width="6"/>{text(cx, top+105, "9", 84, 900, INK, "middle")}
  <ellipse cx="{cx+w/2-90}" cy="{top+h/2}" rx="34" ry="44" fill="{BRASS}" stroke="{INK}" stroke-width="6"/>
  <circle cx="{cx+w/2-90}" cy="{top+h/2-8}" r="10" fill="{INK}"/><path d="M{cx+w/2-94} {top+h/2} L{cx+w/2-98} {top+h/2+24} L{cx+w/2-82} {top+h/2+24} L{cx+w/2-86} {top+h/2} Z" fill="{INK}"/>{kn}'''

def flashlight(x, y, ang=0, l=900, op=0.16):
    return f'<g transform="translate({x} {y}) rotate({ang})"><polygon points="0,0 {l},-240 {l},240" fill="#f6e7c4" opacity="{op}"/><rect x="-80" y="-18" width="90" height="36" rx="8" fill="#2a2c33" stroke="{INK}" stroke-width="5"/></g>'

def msg_screen(lines, stamp):
    y = 300; out = ""
    for ln in lines:
        out += text(70, y, ln, 31, 600, "#e8e6e0"); y += 44
    return (f'{text(210, 140, "Unknown", 34, 800, "#f4f1ea", "middle")}{text(210, 180, stamp, 22, 500, "#8a9098", "middle")}'
            f'<rect x="46" y="250" width="330" height="{len(lines)*44+40}" rx="22" fill="#2a2c33"/>{out}')

def crane(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})" opacity="0.9"><path d="M0 0 L40 -600 L80 0 M20 -300 L60 -300 M10 -150 L70 -150 M30 -450 L50 -450" stroke="#2a3346" stroke-width="12" fill="none"/>
  <path d="M40 -600 L520 -600 M40 -600 L-140 -600 M-140 -600 L-140 -540" stroke="#2a3346" stroke-width="14"/><path d="M400 -600 L400 -380" stroke="#2a3346" stroke-width="4"/><rect x="380" y="-380" width="40" height="30" fill="#2a3346"/></g>'''

def container(x, y, w=520, h=240, c="#7a3a2a"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="7"/>' + "".join(
        f'<path d="M{x+i} {y+10} L{x+i} {y+h-10}" stroke="{INK}" stroke-width="4" opacity="0.5"/>' for i in range(30, w, 40))

def boathouse_in(dark=False):
    sl = "".join(f'<rect x="{80+i*120}" y="80" width="100" height="760" fill="#3a2b1e" stroke="{INK}" stroke-width="5"/>' for i in range(15))
    gaps = "".join(f'<rect x="{180+i*120}" y="80" width="20" height="760" fill="#0a0c12"/>' for i in range(14))
    return f'''<rect width="{W}" height="{H}" fill="#0c0b0a"/>{sl}{gaps}<rect x="0" y="840" width="{W}" height="240" fill="#071018"/>
  {"".join(f'<path d="M{random.Random(i).uniform(0,W):.0f} {random.Random(i+5).uniform(860,1070):.0f} l90 0" stroke="#22344c" stroke-width="3"/>' for i in range(40))}
  <path d="M0 840 L{W} 840" stroke="{INK}" stroke-width="10"/><path d="M200 920 Q700 960 1100 920 L1150 880 Q700 900 160 880 Z" fill="#4a3220" stroke="{INK}" stroke-width="6"/>'''

S = {}
S[1] = lambda: svg(f'''<ellipse cx="960" cy="540" rx="900" ry="540" fill="{ACC}" opacity="0.08"/>{watch2(960, 560, 2.6, 2, 0)}
{"".join(f'<path d="M{960+math.cos(a)*470:.0f} {560+math.sin(a)*470:.0f} l{math.cos(a)*60:.0f} {math.sin(a)*60:.0f}" stroke="{ACC}" stroke-width="10" stroke-linecap="round"/>' for a in [i*0.785 for i in range(8)])}
{text(1840, 120, "2:00 AM", 80, 900, ACC, "end", 4)}''', "#07080b")
S[2] = lambda: svg(f'''{rain(0, 0, W, H, 160, 2)}<g transform="translate(560 260)"><path d="M0 200 Q120 60 330 120 Q520 160 560 320 Q560 520 330 560 Q100 560 40 420 Z" fill="{SKIN}" stroke="{INK}" stroke-width="12"/>
<path d="M120 160 Q260 220 330 120 M180 290 Q330 300 470 230 M200 420 Q340 420 500 360" stroke="{INK}" stroke-width="8" fill="none"/></g>{key(1250, 560, 0.9, -20)}
<path d="M0 600 Q300 560 560 560" stroke="{INK}" stroke-width="140"/><path d="M0 600 Q300 560 560 560" stroke="{HOOD}" stroke-width="116"/>''', "#0d1016")
S[3] = lambda: svg(f'''{text(120, 140, "PREVIOUSLY", 54, 900, "#9aa0a8", "start", 14)}
<g transform="translate(140 260) rotate(-4)"><rect width="520" height="560" fill="#1a1c22" stroke="{ACC}" stroke-width="6"/>{case_svg(140, 220, 1.4, True, True)}{text(260, 520, "THE CASE", 40, 900, ACC, "middle", 4)}</g>
<g transform="translate(700 240) rotate(2)"><rect width="520" height="560" fill="#1a1c22" stroke="{ACC}" stroke-width="6"/>{watch2(260, 240, 1.0, 2, 0, False)}{text(260, 520, "THE WATCH", 40, 900, ACC, "middle", 4)}</g>
<g transform="translate(1260 270) rotate(-2)"><rect width="520" height="560" fill="#1a1c22" stroke="{ACC}" stroke-width="6"/>{key(170, 240, 0.7)}{text(260, 520, "THE KEY", 40, 900, ACC, "middle", 4)}</g>''', "#101115")
S[4] = lambda: svg(f'''<rect x="0" y="0" width="640" height="{H}" fill="#2a0f12"/><rect x="640" y="0" width="640" height="{H}" fill="#1a1c22"/><rect x="1280" y="0" width="640" height="{H}" fill="#0f1420"/>
{woman(160, 200, 1.0, "smile")}{stranger(800, 200, 1.0)}{big_phone(1600, 560, msg_screen(["It opens the door", "to your father."], "Text · 1:59 AM"), 4, False, 0.95)}
<path d="M640 0 L640 {H} M1280 0 L1280 {H}" stroke="{INK}" stroke-width="14"/>''')
S[5] = lambda: svg(f'''{rain(0, 0, W, H, 140, 5)}<ellipse cx="700" cy="560" rx="600" ry="520" fill="url(#ylamp)"/><g transform="translate(260 120)">{eli(0, 0, 2.3, "face_close", "determined", 4)}</g>
{big(1450, 620, "“NO.”", 330, ACC)}''', "#0b0d12")
S[6] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#140808"/><ellipse cx="960" cy="420" rx="760" ry="520" fill="{RED}" opacity="0.18"/>
<g transform="translate(560 -60) scale(2.0)">{woman(0, 0, 1.0, "cold")}</g><rect x="0" y="380" width="{W}" height="70" fill="#000" opacity="0.0"/>''')
S[7] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0e0a0a"/><g transform="translate(80 140)">{woman(0, 0, 1.05, "smile")}</g>
{text(620, 420, "“That's a shame.", 92, 900, "#f4f1ea")}{text(620, 560, "Your father said", 92, 900, "#f4f1ea")}{text(620, 700, "no too.”", 92, 900, RED)}''')
S[8] = lambda: svg(f'''{water(820, 8)}{boards(760)}<rect x="1260" y="260" width="260" height="500" fill="#10151f" stroke="{INK}" stroke-width="10"/>
<path d="M1380 120 L1380 230 M1340 230 L1420 230" stroke="{INK}" stroke-width="12"/><ellipse cx="1380" cy="240" rx="40" ry="16" fill="#2a2c33" stroke="{INK}" stroke-width="5"/>
{"".join(f'<path d="M{1380+math.cos(a)*90:.0f} {240+math.sin(a)*90:.0f} l{math.cos(a)*40:.0f} {math.sin(a)*40:.0f}" stroke="#555" stroke-width="5" opacity="0.6"/>' for a in [i*0.9 for i in range(7)])}
{text(400, 300, "CLICK.", 140, 900, "#3a3d44", "middle")}''', "#030406")
S[9] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#020203"/><g transform="translate(560 140)">{eli(0, 0, 1.9, "face_close", "scared", -10)}</g><rect width="{W}" height="{H}" fill="#020203" opacity="0.55"/>
<path d="M1500 300 Q1300 330 1180 420 L1120 470" stroke="{INK}" stroke-width="80" stroke-linecap="round" fill="none"/><path d="M1500 300 Q1300 330 1180 420 L1120 470" stroke="#4b4e55" stroke-width="62" stroke-linecap="round" fill="none"/>
<ellipse cx="1110" cy="480" rx="50" ry="40" fill="#cbb8a2" stroke="{INK}" stroke-width="6"/>{big(1500, 880, "“RUN.”", 220, ACC)}''')
S[10] = lambda: svg(f'''<rect width="{W}" height="700" fill="#0d1422"/>{crane(1300, 700, 1.0)}{crane(300, 700, 0.7)}{rain(0, 0, W, H, 220, 10)}{boards(700)}
{eli(560, 300, 0.95, "run", "scared", 8)}<g transform="translate(260 260) scale(0.95)"><path d="M30 600 L60 200 Q150 140 240 200 L270 600 Z" fill="#4b4e55" stroke="{INK}" stroke-width="8"/>
<ellipse cx="150" cy="130" rx="62" ry="72" fill="#2e3035" stroke="{INK}" stroke-width="8"/><path d="M60 100 L240 100 L222 60 Q150 26 78 60 Z" fill="#1b1c20" stroke="{INK}" stroke-width="7"/></g>''', "#0d1422")
S[11] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#06080c"/>{container(-60, 360, 640, 300, "#5a2a22")}{container(1340, 330, 640, 330, "#2a4a5a")}
<polygon points="960,700 0,420 0,980" fill="#fff6d0" opacity="0.18"/><polygon points="960,700 1920,420 1920,980" fill="#fff6d0" opacity="0.18"/>
<circle cx="860" cy="700" r="40" fill="#fff6d0"/><circle cx="1060" cy="700" r="40" fill="#fff6d0"/><circle cx="960" cy="700" r="260" fill="#fff6d0" opacity="0.08"/>
{rain(0, 0, W, H, 300, 11, (0.3, 0.8), "#e8e6d0")}''')
S[12] = lambda: svg(f'''{boathouse_in()}{eli(520, 360, 0.8, "stand", "scared", 10)}{walter(980, 200, 0.75, True)}
<rect x="1500" y="200" width="220" height="640" fill="#2a2016" stroke="{INK}" stroke-width="8"/>{text(960, 1040, "THE OLD BOATHOUSE", 46, 900, "#9aa0a8", "middle", 10)}''')
S[13] = lambda: svg(f'''{boathouse_in()}{"".join(f'<rect x="{180+i*120}" y="80" width="20" height="760" fill="#fff6d0" opacity="{0.9 if 5<i<10 else 0.15}"/>' for i in range(14))}
<polygon points="780,80 1300,80 1500,840 600,840" fill="#fff6d0" opacity="0.08"/>{eli(300, 380, 0.7, "stand", "scared", 14)}''')
S[14] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0c0b0a"/><ellipse cx="560" cy="520" rx="560" ry="520" fill="url(#lamp)"/><g transform="translate(140 140)">{eli(0, 0, 2.1, "face_close", "worried", 10)}</g>
{text(1180, 460, "“You knew", 110, 900, "#f4f1ea")}{text(1180, 600, "my father.”", 110, 900, ACC)}''')
S[15] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#121010"/><ellipse cx="960" cy="420" rx="700" ry="500" fill="url(#lamp)"/><g transform="translate(600 -40) scale(2.1)">{walter(0, 0, 1.0, False, "tired")}</g>
<g transform="translate(1440 760) rotate(-15)"><path d="M60 130 L240 130 L222 90 Q150 56 78 90 Z" fill="#1b1c20" stroke="{INK}" stroke-width="7"/><rect x="40" y="122" width="220" height="16" rx="6" fill="#1b1c20" stroke="{INK}" stroke-width="6"/></g>''')
S[16] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#14161b"/><g transform="translate(160 160)">{walter(0, 0, 1.0, False)}</g>
{big(1180, 470, "WALTER", 260, "#f4f1ea")}{text(1180, 590, "twenty-two years on the pier", 54, 700, "#9aa0a8", "middle", 2, "Inter")}''')
S[17] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#3b3226"/><rect x="0" y="760" width="{W}" height="320" fill="#2a241c"/>
<rect x="1080" y="140" width="360" height="620" fill="#a9967a" stroke="#1a140e" stroke-width="10"/><rect x="1080" y="140" width="80" height="620" fill="#f0d9a0"/>
{stranger(1180, 250, 0.62)}<g transform="translate(260 200)">{walter(0, 0, 0.65, True)}</g>
{case_svg(1170, 700, 0.8, False)}<rect width="{W}" height="{H}" fill="{SEPIA}" opacity="0.28"/>{text(120, 140, "22 YEARS AGO", 70, 900, "#f4ead0", "start", 10)}''', "#3b3226")
S[18] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0a0a0c"/><ellipse cx="960" cy="200" rx="300" ry="900" fill="#f6e7c4" opacity="0.07"/><g transform="translate(810 160)">{walter(0, 0, 0.95, False, "down")}</g>
{text(960, 140, "“I was a coward, Eli.”", 74, 900, "#f4f1ea", "middle")}''')
S[19] = lambda: svg(f'''{rain(0, 0, W, H, 120, 19, (0.1, 0.3))}<g transform="translate(1100 160)">{eli(0, 0, 2.0, "face_close", "worried", -14)}</g>
{big(560, 560, "IS HE", 200, "#f4f1ea")}{big(560, 760, "ALIVE?", 200, ACC)}''', "#0c0d10")
S[20] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#120f0b"/><ellipse cx="960" cy="560" rx="700" ry="480" fill="{ACC}" opacity="0.1"/>
<path d="M300 1080 Q420 800 700 700" stroke="{INK}" stroke-width="150" fill="none"/><path d="M300 1080 Q420 800 700 700" stroke="#4b4e55" stroke-width="124" fill="none"/>
<ellipse cx="760" cy="690" rx="120" ry="90" fill="#cbb8a2" stroke="{INK}" stroke-width="8"/>{watch2(1000, 520, 1.8, 2, 0, False, False, True)}''')
S[21] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0906"/>{watch2(960, 560, 3.4, back=True)}''')
S[22] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#2b241b"/><g transform="translate(260 180) rotate(-5)"><rect width="560" height="700" fill="#efe6cf" stroke="{INK}" stroke-width="8"/>
<rect x="30" y="30" width="500" height="560" fill="#8a7a5e"/>{stranger(130, 140, 0.55)}<rect x="30" y="30" width="500" height="560" fill="{SEPIA}" opacity="0.35"/>{text(280, 660, "D. B. · 2004", 40, 700, "#4a3a22", "middle", 2, "Inter")}</g>
{big(1340, 470, "DANIEL", 190, "#f4f1ea")}{big(1340, 650, "BROOKS", 190, ACC)}{text(1340, 760, "Eli's father", 54, 700, "#cfc3a8", "middle", 2, "Inter")}''')
S[23] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#101116"/>{watch2(420, 520, 1.3, 2, 2)}
{text(1220, 380, "Find out what happened", 66, 900, "#f4f1ea", "middle")}{text(1220, 470, "to Daniel Brooks.", 66, 900, ACC, "middle")}
{text(1220, 620, "Can Eli trust Walter? Tell me in the comments.", 40, 600, "#cfd3da", "middle", 0, "Inter")}{subscribe(1220, 800)}
<path d="M1460 790 l40 -30 l0 60 z" fill="#ffffff" opacity="0"/>''')
S[24] = lambda: svg(f'''{boathouse_in()}{walter(1100, 180, 0.8, False)}<path d="M1300 520 Q1420 640 1420 820" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/>
<path d="M1300 520 Q1420 640 1420 820" stroke="#4b4e55" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M1420 860 l-30 -50 l60 0 z" fill="{ACC}"/>
{text(560, 300, "“It's not on the pier.", 70, 900, "#f4f1ea", "middle")}{text(560, 400, "It's UNDER it.”", 70, 900, ACC, "middle")}''')
S[25] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0b0a09"/><path d="M200 160 Q600 60 900 260 L760 520 Q500 360 160 420 Z" fill="#3a4a3a" stroke="{INK}" stroke-width="8"/>
{"".join(f'<polygon points="{560+i*40},{460+i*90} {1360-i*40},{460+i*90} {1330-i*44},{540+i*90} {590+i*44},{540+i*90}" fill="{["#4a4640","#3c3934","#2e2c28","#22201d","#171614","#0e0d0c","#070707"][i]}" stroke="{INK}" stroke-width="5"/>' for i in range(7))}
<rect x="440" y="440" width="1040" height="20" fill="#2a2620" stroke="{INK}" stroke-width="5"/>{"".join(f'<circle cx="{random.Random(i).uniform(600,1300):.0f}" cy="{random.Random(i+3).uniform(500,1000):.0f}" r="5" fill="#6a8aa8" opacity="0.6"/>' for i in range(20))}''')
S[26] = lambda: svg(f'''{tunnel(doors=False)}{flashlight(560, 820, -18, 1200, 0.18)}{eli(300, 520, 0.85, "stand", "worried", 10)}<g transform="translate(160 470) scale(0.9)">{walter(0, 0, 0.75, False)}</g>''')
S[27] = lambda: svg(f'''{tunnel(nums=("1", "2", "3", "4"))}{flashlight(960, 1100, -90, 800, 0.12)}''')
S[28] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#0a0806"/>{"".join(f'<g transform="translate({60+i*470} 180)"><rect width="390" height="720" fill="{IRON}" stroke="{INK}" stroke-width="10"/>{text(195, 200, n, 180, 900, BRASS, "middle")}</g>' for i, n in enumerate(["5", "6", "7", "8"]))}
<ellipse cx="1650" cy="540" rx="300" ry="400" fill="#f6e7c4" opacity="0.12"/>''')
S[29] = lambda: svg(f'''{tunnel(nums=("5", "6", "7", "8"))}<rect x="830" y="320" width="260" height="380" fill="{IRON}" stroke="{INK}" stroke-width="8"/>
<rect x="900" y="340" width="120" height="70" rx="8" fill="{BRASS}" stroke="{INK}" stroke-width="5"/>{text(960, 400, "9", 64, 900, INK, "middle")}<ellipse cx="960" cy="520" rx="400" ry="320" fill="#f6e7c4" opacity="0.08"/>''')
S[30] = lambda: svg(f'''{iron_door()}''')
S[31] = lambda: svg(f'''{bricks(0, 0, W, H, BRICK2, 31, 1)}<rect x="300" y="0" width="1100" height="{H}" fill="{IRON}" stroke="{INK}" stroke-width="12"/>
<ellipse cx="1100" cy="540" rx="150" ry="190" fill="{BRASS}" stroke="{INK}" stroke-width="10"/><circle cx="1100" cy="500" r="44" fill="{INK}"/><path d="M1080 530 L1066 640 L1134 640 L1120 530 Z" fill="{INK}"/>
<path d="M0 640 Q200 620 520 560" stroke="{INK}" stroke-width="120" fill="none"/><path d="M0 640 Q200 620 520 560" stroke="{HOOD}" stroke-width="96" fill="none"/>{key(620, 520, 1.2, 0)}
{"".join(f'<path d="M{560+i*14} {420-i*16} l20 -10" stroke="#cfd3da" stroke-width="5" opacity="0.6"/>' for i in range(3))}''')
S[32] = lambda: svg(f'''{iron_door(knock=True)}{big(960, 1020, "KNOCK.", 140, ACC)}''')
S[33] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#060505"/>{big(960, 330, "KNOCK.", 170, "#f4f1ea")}{big(960, 560, "KNOCK.", 170, "#cfc6b0")}{big(960, 790, "KNOCK.", 170, ACC)}
<path d="M120 700 L1800 700" stroke="#2a2c33" stroke-width="4"/>''')
S[34] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#030303"/><ellipse cx="760" cy="520" rx="520" ry="460" fill="#f6e7c4" opacity="0.10"/>
<g transform="translate(260 180)">{eli(0, 0, 1.7, "face_close", "scared", 16)}</g><g transform="translate(1180 120) scale(1.0)">{walter(0, 0, 1.0, False, "scared")}</g>
{flashlight(1500, 700, 200, 900, 0.10)}''')
S[35] = lambda: svg(f'''{tunnel(doors=False, light=False)}<rect width="{W}" height="{H}" fill="#000" opacity="0.5"/>{big_phone(960, 540, msg_screen([], "1 new message"), -4, True, 0.95)}''')
S[36] = lambda: svg(f'''<ellipse cx="960" cy="540" rx="900" ry="540" fill="{RED}" opacity="0.06"/>{big_phone(960, 560, msg_screen(["Don't open it yet.", "", "She's right", "behind you."], "Text · 2:03 AM"), 2, False, 1.15)}''', "#0b0b0e")
S[37] = lambda: svg(f'''{tunnel(red=True, light=False)}<g transform="translate(120 360)">{eli(0, 0, 1.6, "face_close", "scared", -18, True)}</g>''')
S[38] = lambda: svg(f'''<rect width="{W}" height="{H}" fill="#080706"/>{watch2(760, 560, 2.4, 2, 4)}{big(1520, 520, "2:04", 220, ACC)}{text(1520, 640, "AM", 70, 900, "#9aa0a8", "middle", 6)}''')
S[39] = lambda: svg(f'''{text(960, 190, "WHAT WOULD YOU DO?", 104, 900, "#f4f1ea", "middle", -2)}
<rect x="160" y="290" width="760" height="520" rx="30" fill="#1b1d23" stroke="{ACC}" stroke-width="8"/><g transform="translate(540 540) scale(0.42) translate(-960 -560)">{iron_door()}</g>{text(540, 760, "OPEN DOOR NINE", 56, 900, ACC, "middle")}
<rect x="1000" y="290" width="760" height="520" rx="30" fill="#1b1d23" stroke="{RED}" stroke-width="8"/><g transform="translate(1210 300) scale(0.48)">{woman(0, 0, 1.0, "cold")}</g>{text(1380, 760, "FACE HER", 56, 900, RED, "middle")}
{text(960, 920, "Tell me in the comments.", 46, 600, "#cfd3da", "middle")}''', "#0d0e12")
S[40] = lambda: svg(f'''{rain(0, 0, W, H, 120, 40, (0.1, 0.3))}<g transform="translate(140 200)">{eli(0, 0, 1.6, "face_close", "determined", 8)}</g>
{big(1260, 360, "WRONG", 170, "#f4f1ea")}{big(1260, 530, "NUMBER", 170, ACC)}{text(1260, 640, "New episode every day", 50, 700, "#cfd3da", "middle", 2, "Inter")}{subscribe(1260, 800)}''', "#0b0c10")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or sorted(S)
    for i in ids:
        render(S[i](), f"{OUT}/{i:02d}.jpg"); print("ok", i, flush=True)
