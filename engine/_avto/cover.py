# Oblozhka 1080x1920: risuet fon po opisaniyu (Gemini) i kladet krupnye stroki khuka.
# python cover.py <papka serii>   (chitaet cover.json: {"prompt": "...", "lines": [["TEKST", razmer, "gold|cream", y], ...]})
import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ep = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, '..', '_stil', 'fonts')
cfg = json.load(open(os.path.join(ep, 'cover.json'), encoding='utf-8'))
bgp = os.path.join(ep, '_nur', 'cover_bg.png'); os.makedirs(os.path.dirname(bgp), exist_ok=True)
if not os.path.exists(bgp):
    pr = cfg['prompt'] + ' Vertical 9:16 photograph, no people, no faces, no animals, no text, no letters, no logos. Dark cinematic, warm gold light, high detail, empty space at top and bottom for large text.'
    subprocess.run(['python3', os.path.join(HERE, 'img.py'), 'gemini-3.1-flash-image', pr, bgp, '9:16'], check=True, stdin=subprocess.DEVNULL)
W, H = 1080, 1920; GOLD = (247, 201, 102); CREAM = (255, 249, 238)
bg = Image.open(bgp).convert('RGB'); s = max(W / bg.width, H / bg.height)
bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS); x = (bg.width - W) // 2; y = (bg.height - H) // 2
im = bg.crop((x, y, x + W, y + H)).convert('RGBA')
g = Image.new('L', (1, H))
for yy in range(H): g.putpixel((0, yy), int(175 * max(0, 1 - yy / 720)) if yy < 720 else int(200 * max(0, (yy - 1300) / 620)))
im.alpha_composite(Image.merge('RGBA', [Image.new('L', (W, H), 0)] * 3 + [g.resize((W, H))]))
def mont(sz, w=850):
    f = ImageFont.truetype(os.path.join(F, 'Montserrat.ttf'), sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
AM = ImageFont.truetype(os.path.join(F, 'Amiri-Regular.ttf'), 70)
def draw_line(dr, parts, f, c, cy, x0, shadow=False):
    xx = x0
    for k, p in enumerate(parts):
        dr.text((xx + (4 if shadow else 0), cy + (6 if shadow else 0)), p, font=f, fill=c, anchor='lm'); xx += dr.textlength(p, font=f)
        if k < len(parts) - 1: dr.text((xx, cy + 4), '\ufdfa', font=AM, fill=c, anchor='lm'); xx += dr.textlength('\ufdfa', font=AM)
for t, sz, col, cy in cfg['lines']:
    c = (GOLD if col == 'gold' else CREAM) + (255,); f = mont(sz, 900 if sz >= 90 else 800)
    d = ImageDraw.Draw(im); parts = t.split('\ufdfa')
    tw = lambda: sum(d.textlength(p, font=f) for p in parts) + (len(parts) - 1) * d.textlength('\ufdfa', font=AM)
    while tw() > 1000 and f.size > 30: f = mont(f.size - 4)
    x0 = (W - tw()) / 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_line(ImageDraw.Draw(sh), parts, f, (0, 0, 0, 235), cy, x0, True)
    sh = sh.filter(ImageFilter.GaussianBlur(9)); im.alpha_composite(sh); im.alpha_composite(sh)
    draw_line(ImageDraw.Draw(im), parts, f, c, cy, x0)
im.convert('RGB').save(os.path.join(ep, 'OBLOZHKA_1080x1920.jpg'), quality=93)
print('OK oblozhka')
