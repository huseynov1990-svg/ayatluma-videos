import sys; sys.path.insert(0, "/home/claude/iwt")
from scenes_ep2 import *
from PIL import Image
def sweat(x, y, s=1): return f'<path d="M{x} {y} q{12*s} {26*s} 0 {38*s} q{-12*s} {-12*s} 0 {-38*s} Z" fill="#9fd3ff" stroke="{INK}" stroke-width="4"/>'
A = svg(f'''{sky("#f7c06b", "#d9643a")}{sun(1450, 420, 200, "#fff0b0")}{pyramid(1400, 900, 1100, 1.0, "#fbf7ee", "#e2d6bb")}{dunes(900)}
<ellipse cx="430" cy="560" rx="460" ry="460" fill="url(#ylamp)"/>{ava_eg(-120, 140, 2.6, "scared", 10)}{sweat(620, 430, 1.5)}
{bigtext(1380, 200, "I WAS THERE", 120, "#ffffff")}{bigtext(1380, 340, "WHEN THEY BUILT IT", 96, TEAL)}''', SKY)
B = svg(f'''<rect width="{W}" height="{H}" fill="#1b1612"/>{block(160, 380, 900, 560, LIME)}{"".join(worker(220+i*170, 260, 0.9, "pull") for i in range(5))}
{bigtext(1460, 380, "2,300,000", 170, GOLD)}{bigtext(1460, 540, "STONES", 150, "#ffffff")}{bigtext(1460, 700, "NO MACHINES", 90, "#ff6b6b")}''')
C = svg(f'''{sky("#f7d79a", "#e9b06b", 720)}{pyramid(1500, 720, 700, 0.7)}<rect x="0" y="720" width="{W}" height="360" fill="{SAND}"/>
{"".join(worker(80 + i * 180, 520, 1.0, "up" if i % 2 else "stand") for i in range(5))}{ava_eg(1100, 380, 1.4, "determined", -10)}
{bigtext(560, 260, "NOT SLAVES?", 150, "#ffffff")}<path d="M120 300 L1000 300" stroke="#ff6b6b" stroke-width="0"/>''', SKY)
for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/iwt/ep2/thumb_{n}.jpg"; render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=90); print("ok", n)
