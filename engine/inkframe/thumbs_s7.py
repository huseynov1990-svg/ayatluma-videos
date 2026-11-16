import sys
sys.path.insert(0, "/home/claude/s7"); sys.path.insert(0, "/home/claude/wn")
from s7_scenes import *
from PIL import Image

def big_text(x, y, s, size, fill, stroke=INK, sw=14, anchor="start"):
    s = s.replace("&", "&amp;").replace("'", "&#39;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-3">{s}</text>')
HAND = f'''<g fill="#d8f3ff" stroke="{INK}" stroke-width="5"><ellipse cx="0" cy="40" rx="70" ry="85"/>
<rect x="-70" y="-120" width="26" height="120" rx="13" transform="rotate(-12 -57 0)"/><rect x="-36" y="-150" width="26" height="150" rx="13"/>
<rect x="-2" y="-160" width="26" height="160" rx="13"/><rect x="32" y="-140" width="26" height="140" rx="13" transform="rotate(8 45 0)"/>
<rect x="60" y="-20" width="26" height="100" rx="13" transform="rotate(50 73 30)"/></g>'''

A = svg(f'''<rect width="{W}" height="{H}" fill="#14354a"/>
{"".join(f'<path d="M{i*130} 0 L{i*130+90} 1080" stroke="#1f4a63" stroke-width="6"/>' for i in range(16))}
<ellipse cx="1350" cy="560" rx="520" ry="460" fill="{ICE}" opacity="0.35" filter="url(#b30)"/>
<g transform="translate(1350 600) scale(2.6)">{HAND}</g>
{mara(-60, 300, 1.9, "scared", 16, pose="suit")}
{big_text(60, 200, "SOMETHING", 150, "#ffffff")}{big_text(60, 350, "KNOCKED BACK", 150, ACC)}''', "#14354a")

B = svg(f'''<rect width="{W}" height="{H}" fill="#06080c"/>{stars(160, 9)}{jupiter(1500, 300, 330)}
{mara(-80, 160, 2.4, "scared", 10)}
{wave(820, 760, 1050, 120, "speech", ACC)}
{big_text(820, 600, "MY OWN", 170, "#ffffff")}{big_text(820, 960, "VOICE?!", 170, ACC)}''', "#06080c")

C = svg(f'''<rect width="{W}" height="{H}" fill="#0b0e12"/>
<rect width="{W}" height="{H}" fill="#ff2a2a" opacity="0.18"/>
{big_text(960, 420, "DO NOT", 260, "#ffffff", INK, 16, "middle")}{big_text(960, 700, "RESPOND", 260, "#ff3b3b", INK, 16, "middle")}
<g transform="translate(1700 860) scale(1.1)">{HAND}</g>
{wave(120, 930, 1300, 70, "speech", ACC)}''', "#0b0e12")

for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/s7/ep1/thumb_{n}.jpg"
    render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=92); print("ok", n)
