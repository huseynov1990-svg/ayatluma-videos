import sys
sys.path.insert(0, "/home/claude/work/wn3")
from wn_scenes_ep3 import *
from PIL import Image
A = svg(f'''{iron_door(1420, 120, 560, 860)}<rect x="0" y="0" width="980" height="{H}" fill="#07080b" opacity="0.85"/>
<ellipse cx="520" cy="560" rx="560" ry="560" fill="url(#ylamp)"/><g transform="translate(-60 40)">{eli(0, 0, 3.1, "face_close", "scared", 22)}</g>
{big(1420, 300, "DON'T", 200, "#ffffff", "middle", 16)}{big(1420, 520, "OPEN IT", 180, ACC, "middle", 16)}''', "#07080b")
B = svg(f'''<rect width="{W}" height="{H}" fill="#0b0906"/>{watch2(620, 560, 3.0, back=True)}
{big(1450, 360, "HIS", 180, "#ffffff", "middle", 14)}{big(1450, 560, "FATHER'S", 160, ACC, "middle", 14)}{big(1450, 740, "WATCH", 180, "#ffffff", "middle", 14)}''')
C = svg(f'''{tunnel(red=True, light=False)}<g transform="translate(-40 300)">{eli(0, 0, 2.4, "face_close", "scared", -20, True)}</g>
{big(1380, 200, "SHE'S", 170, "#ffffff", "middle", 14)}{big(1380, 1000, "BEHIND YOU", 150, RED, "middle", 14)}''')
for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/work/wn3/thumb_{n}.jpg"; render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=90); print("ok", n)
