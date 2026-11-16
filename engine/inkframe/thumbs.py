import sys
sys.path.insert(0, "/home/claude/wn")
from kit import *

def sweat(x, y, s=1):
    return f'<path d="M{x} {y} q{12*s} {26*s} 0 {38*s} q{-12*s} {-12*s} 0 {-38*s} Z" fill="#9fd3ff" stroke="{INK}" stroke-width="4"/>'

def big_text(x, y, s, size, fill, stroke=INK, sw=14, anchor="start"):
    s = s.replace("&", "&amp;").replace("'", "&#39;")
    return (f'<text x="{x}" y="{y}" font-family="Inter Display" font-weight="900" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" letter-spacing="-3">{s}</text>')

# A: huge scared face + glowing case
A = svg(f'''
<rect width="{W}" height="{H}" fill="#14151a"/>
<ellipse cx="1420" cy="640" rx="700" ry="560" fill="url(#ylamp)"/>
<ellipse cx="1420" cy="640" rx="420" ry="330" fill="url(#ylamp)"/>
{"".join(f'<path d="M1420 640 L{1420+900*__import__("math").cos(a):.0f} {640+900*__import__("math").sin(a):.0f}" stroke="{ACC}" stroke-width="22" opacity="0.13"/>' for a in [i*0.45 for i in range(14)])}
{eli(-120, 60, 2.6, "face_close", "scared", 8)}
<ellipse cx="420" cy="460" rx="420" ry="380" fill="url(#ylamp)"/>{sweat(575, 360, 1.6)}{sweat(250, 420, 1.2)}
{case_svg(1130, 560, 3.4, True, True)}

{big_text(1000, 250, "DON'T", 200, "#ffffff")}{big_text(1000, 440, "OPEN IT", 200, ACC)}
<path d="M1380 980 Q1300 900 1330 800" fill="none" stroke="#ff3b3b" stroke-width="22" stroke-linecap="round"/>
<path d="M1300 830 L1332 790 L1370 830" fill="none" stroke="#ff3b3b" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
''')

# B: giant phone "UNKNOWN" + $5,000
from ep1_scenes import big_phone, screen_call
B = svg(f'''
<rect width="{W}" height="{H}" fill="#121318"/>
<ellipse cx="560" cy="560" rx="600" ry="560" fill="url(#ylamp)"/>
{big_phone(560, 560, screen_call("UNKNOWN", "calling at 1:12 AM"), -10, True, 1.15)}
{big_text(1060, 330, "WRONG", 180, "#ffffff")}{big_text(1060, 520, "NUMBER", 180, ACC)}
<rect x="1090" y="640" width="640" height="190" rx="24" fill="#2bd46a" stroke="{INK}" stroke-width="12"/>
{big_text(1410, 785, "$5,000", 150, "#ffffff", INK, 10, "middle")}

''')

# C: man in grey looms behind Eli
C = svg(f'''
<rect width="{W}" height="{H}" fill="#101116"/>
<ellipse cx="1300" cy="300" rx="700" ry="500" fill="url(#blue)"/>
{stranger(980, -120, 2.4)}
<path d="M0 0 L{W} 0 L{W} {H} L0 {H} Z" fill="url(#fadeB)"/>
{eli(80, 160, 1.9, "face_close", "scared", 14)}
{sweat(590, 360, 1.4)}
{big_text(1900, 1010, "RUN.", 260, "#ff3b3b", INK, 14, "end")}
<circle cx="1410" cy="300" r="190" fill="none" stroke="#ff3b3b" stroke-width="16"/>
''')

for name, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/wn/ep1/thumb_{name}.jpg"
    render(s, out, scale=1.0, grain=4, vignette=0.25)
    from PIL import Image
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=92)
    print("ok", name)
