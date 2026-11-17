import sys; sys.path.insert(0, "/home/claude/wn")
from scenes_ep2 import *
from PIL import Image
A = svg(f'''<ellipse cx="560" cy="560" rx="600" ry="560" fill="{ACC}" opacity="0.18"/>{eli(-60, 30, 2.9, "face_close", "scared", 10)}
{photo_eli(1060, 330, 1.05, 6)}{big(1420, 200, "IT WAS ME", 150, ACC)}''', "#0b0c10")
B = svg(f'''<rect width="{W}" height="{H}" fill="#241a12"/><ellipse cx="560" cy="400" rx="600" ry="560" fill="#ffd36a" opacity="0.22"/>{woman(160, 40, 1.6, "cold", True)}
{key(1250, 640, 1.2, -20)}{big(1420, 220, "DON'T GIVE", 140, "#ffffff")}{big(1420, 380, "HER THE KEY", 130, RED)}''')
C = svg(f'''<rect width="{W}" height="{H}" fill="#0d0f14"/>{stranger(120, -260, 2.6)}{eli(1180, 380, 1.5, "face_close", "surprised", -14)}
{big(1340, 220, "MY FATHER?", 150, ACC)}{rain(0, 0, W, H, 300, 5)}''')
for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/wn/ep2/thumb_{n}.jpg"; render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=90); print("ok", n)
