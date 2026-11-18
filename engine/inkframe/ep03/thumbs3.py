import sys; sys.path.insert(0, "/home/claude/work/iwt3")
from iwt_scenes_ep3 import *
from PIL import Image
A = svg(f'''{sky("#3a2a2a", "#e0703a")}<ellipse cx="1350" cy="380" rx="700" ry="420" fill="{EMBER}" opacity="0.5" filter="url(#b30)"/>{pine_cloud(1400, 560, 520, 900)}{vesuvius(1400, 1080, 1300, "#3a3a22", "#2a2a18", False, False)}
<ellipse cx="430" cy="560" rx="460" ry="460" fill="url(#ylamp)"/>{ava_r(-120, 140, 2.6, "scared", 10)}
{bigtext(1380, 190, "I WAS IN", 120, "#ffffff")}{bigtext(1380, 340, "POMPEII", 150, OCHRE)}''')
B = svg(f'''{sky("#4a4440", "#7a6a5a")}{pumice_fall(600, 5)}{"".join(rhouse(20 + i * 320, 760, 280, 220, "#bba98a", "#7a2a22") for i in range(6))}
{bigtext(960, 300, "THE SKY", 200, "#ffffff")}{bigtext(960, 520, "FELL", 230, EMBER)}''')
C = svg(f'''<rect width="{W}" height="{H}" fill="#f1e8d6"/>{vesuvius(1450, 1080, 1100, OLIVE, "#56632c", False)}
<g transform="translate(160 300)"><rect width="560" height="520" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="10"/><rect width="560" height="130" rx="30" fill="{PRED}" stroke="{INK}" stroke-width="10"/>{text(280, 95, "AUGUST", 70, 900, "#ffffff", "middle")}{text(280, 400, "24", 230, 900, "#2a1a10", "middle")}<path d="M40 160 L520 490" stroke="{PRED}" stroke-width="30" stroke-linecap="round"/></g>
{bigtext(1250, 230, "WRONG DATE?", 150, PRED)}''')
for n, s in (("A", A), ("B", B), ("C", C)):
    out = f"/home/claude/work/iwt3/thumb_{n}.jpg"; render(s, out, scale=1.0, grain=4, vignette=0.25)
    Image.open(out).resize((1280, 720), Image.LANCZOS).save(out, quality=90); print("ok", n)
