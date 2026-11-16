import sys
sys.path.insert(0, "/home/claude/iwt"); sys.path.insert(0, "/home/claude/wn")
from scenes_ep1 import *
from PIL import Image

def big(x, y, s, size, fill, anchor="start", sw=14):
    s = s.replace("&", "&amp;").replace("'", "&#39;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-3">{s}</text>')
def sweat(x, y, s=1):
    return f'<path d="M{x} {y} q{12*s} {26*s} 0 {38*s} q{-12*s} {-12*s} 0 {-38*s} Z" fill="#9fd3ff" stroke="{INK}" stroke-width="4"/>'

A = svg(f'''{stars(200, 5, 700)}<ellipse cx="1400" cy="560" rx="700" ry="500" fill="#ffb35c" opacity="0.18"/>
{ship(980, 640, 0.95, -22)}{sea(760, "#05070c")}
<ellipse cx="430" cy="520" rx="420" ry="420" fill="url(#ylamp)"/>{ava(-120, 120, 2.6, "scared", 10, hat="1912")}{sweat(600, 420, 1.5)}
{big(1000, 220, "I WAS ON", 150, "#ffffff")}{big(1000, 380, "THE TITANIC", 150, TEAL)}''', "#05070c")

B = svg(f'''{stars(260, 6, 640)}{ship(700, 640, 0.95, -32, False, True)}{sea(700, "#05070c")}
{lifeboat(160, 860, 1.8, 6)}{big(1880, 230, "2:20 AM", 200, "#ffffff", "end")}{big(1880, 400, "SHE WAS GONE", 110, "#ff6b6b", "end")}''', "#05070c")

C = svg(f'''<rect width="{W}" height="{H}" fill="#0e1015"/>
{"".join(f'<rect x="{120+(i%10)*80}" y="{420+(i//10)*80}" width="64" height="34" rx="16" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>' for i in range(20))}
{"".join(f'<circle cx="{1060+(i%20)*40}" cy="{400+(i//20)*40}" r="13" fill="#e9e4d8"/>' for i in range(110))}
{big(520, 300, "20 BOATS", 150, TEAL, "middle")}{big(1440, 300, "2,200 PEOPLE", 120, "#ffffff", "middle")}
{ava(660, 640, 1.0, "scared", 0, hat="1912")}{big(1460, 1000, "WHO GOT A SEAT?", 90, "#ff6b6b", "middle")}''', "#0e1015")

for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/iwt/ep1/thumb_{n}.jpg"
    render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=92); print("ok", n)
