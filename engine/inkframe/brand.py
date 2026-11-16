import sys, subprocess
sys.path.insert(0, "/home/claude/wn")
from kit import eli, INK
from ava import ava
F = "'Segoe UI Black','Arial Black','Inter Display',sans-serif"
Y = "#F2B705"; T = "#2EC4B6"

def t(x, y, s, size, fill, anchor="middle", ls=0, w=900, op=1):
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-weight="{w}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{s}</text>')

avatar = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
<rect width="800" height="800" fill="#121318"/>
<circle cx="400" cy="400" r="330" fill="{Y}" opacity="0.10"/>
<rect x="150" y="170" width="500" height="460" rx="26" fill="none" stroke="{Y}" stroke-width="28"/>
<path d="M150 300 L90 300 M650 500 L710 500" stroke="{Y}" stroke-width="28" stroke-linecap="round"/>
{t(400, 390, "INK", 170, "#f4f1ea", ls=-4)}
{t(400, 530, "FRAME", 112, Y, ls=-4)}
</svg>'''

W, H = 2560, 1440
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><radialGradient id="g1" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{Y}" stop-opacity="0.30"/><stop offset="1" stop-color="{Y}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{T}" stop-opacity="0.30"/><stop offset="1" stop-color="{T}" stop-opacity="0"/></radialGradient>
<linearGradient id="split" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#101116"/><stop offset="0.5" stop-color="#15161c"/><stop offset="1" stop-color="#1a1712"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#split)"/>
<ellipse cx="580" cy="740" rx="520" ry="420" fill="url(#g1)"/><ellipse cx="1980" cy="740" rx="520" ry="420" fill="url(#g2)"/>

{eli(330, 480, 1.25, "face_close", "surprised", 10)}
{ava(1730, 480, 1.25, "smile", -10)}
{t(1280, 680, "INKFRAME", 150, "#f4f1ea", ls=-3)}
{t(1280, 790, "STORIES", 100, Y, ls=8)}
{t(1280, 848, "NEW ANIMATED EPISODES EVERY DAY", 32, "#b9bec7", ls=8, w=700)}
<rect x="780" y="868" width="460" height="56" rx="28" fill="{Y}"/>{t(1010, 906, "WRONG NUMBER", 30, INK, ls=4)}
<rect x="1320" y="868" width="460" height="56" rx="28" fill="{T}"/>{t(1550, 906, "I WAS THERE", 30, INK, ls=4)}
</svg>'''

open("/home/claude/wn/avatar.svg", "w").write(avatar)
open("/home/claude/wn/banner.svg", "w").write(banner)
for n in ("avatar", "banner"):
    subprocess.run(["rsvg-convert", f"/home/claude/wn/{n}.svg", "-o", f"/home/claude/wn/{n}_preview.png"], check=True)
print(len(avatar), len(banner))
