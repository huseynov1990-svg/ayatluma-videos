# Arabskiy tekst v PNG dlya bloka N: python arabic.py <papka serii> <N> "<arabskiy tekst s kharakatami>"
import sys, os
from PIL import Image, ImageDraw, ImageFont
ep, n, t = sys.argv[1], int(sys.argv[2]), sys.argv[3]
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_stil', 'fonts', 'Amiri-Regular.ttf')
f = ImageFont.truetype(F, 110, layout_engine=ImageFont.Layout.RAQM)
b = ImageDraw.Draw(Image.new('L', (10, 10))).textbbox((0, 0), t, font=f, direction='rtl', language='ar')
im = Image.new('RGBA', (b[2] - b[0] + 40, b[3] - b[1] + 60), (0, 0, 0, 0))
ImageDraw.Draw(im).text((20 - b[0], 30 - b[1]), t, font=f, fill=(255, 255, 255, 255), direction='rtl', language='ar')
os.makedirs(os.path.join(ep, '_nur'), exist_ok=True); im.save(os.path.join(ep, '_nur', 'ar_%d.png' % n)); print('OK', im.size)
