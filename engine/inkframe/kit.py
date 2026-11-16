"""Wrong Number - drawing kit (SVG -> PNG). Noir ink style, one accent colour."""
import random, subprocess, os
import numpy as np
from PIL import Image

W, H = 1920, 1080
INK = "#121214"
ACC = "#F2B705"
SKIN = "#d6c6b2"
HOOD = "#3a3b42"
JEANS = "#24262c"
FONT = "Inter Display"

# ---------------- character ----------------
def _face(mood, look=0):
    brow = {"surprised": "M160 104 Q175 94 190 102 M210 102 Q225 94 240 104",
            "worried":   "M160 100 Q175 108 190 106 M210 106 Q225 108 240 100",
            "calm":      "M162 106 L188 106 M212 106 L238 106",
            "scared":    "M160 98 Q175 90 190 104 M210 104 Q225 90 240 98",
            "determined":"M160 100 L190 110 M210 110 L240 100"}[mood]
    mouth = {"surprised": f'<ellipse cx="203" cy="182" rx="8" ry="10" fill="{INK}"/>',
             "scared":    f'<ellipse cx="203" cy="184" rx="11" ry="9" fill="{INK}"/>',
             "worried":   f'<path d="M188 186 Q203 176 218 186" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "calm":      f'<path d="M190 182 L216 182" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>',
             "determined":f'<path d="M188 184 L218 180" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'}[mood]
    e = look
    return f'''
  <ellipse cx="200" cy="140" rx="70" ry="80" fill="{SKIN}" stroke="{INK}" stroke-width="7"/>
  <path d="M134 128 Q118 108 138 92 M266 128 Q284 110 262 92" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
  <path d="M126 112 Q128 46 200 42 Q272 46 274 112 Z" fill="#26272c" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <rect x="122" y="96" width="156" height="26" rx="11" fill="#1d1e22" stroke="{INK}" stroke-width="6"/>
  <path d="{brow}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="{176+e}" cy="134" rx="7" ry="10" fill="{INK}"/>
  <ellipse cx="{226+e}" cy="134" rx="7" ry="10" fill="{INK}"/>
  <path d="M{202+e/2} 140 Q{196+e/2} 158 {206+e/2} 160" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
  {mouth}'''

def _bag(x=58, y=210):
    return f'''<rect x="{x}" y="{y}" width="96" height="150" rx="22" fill="{ACC}" stroke="{INK}" stroke-width="7"/>
  <path d="M{x+18} {y+30} L{x+78} {y+30}" stroke="{INK}" stroke-width="5"/>'''

def _torso():
    return f'''<path d="M112 232 Q200 206 290 232 Q324 300 318 430 L82 430 Q76 300 112 232 Z" fill="{HOOD}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M150 226 Q200 262 250 226" fill="none" stroke="{INK}" stroke-width="6"/>
  <path d="M184 250 L180 300 M216 250 L220 300" stroke="#d8d8d8" stroke-width="4" stroke-linecap="round"/>
  <path d="M200 262 L200 430" stroke="{INK}" stroke-width="4" opacity="0.6"/>'''

def _legs_stand():
    return f'''<path d="M100 425 L96 610 L170 610 L190 440 L210 440 L232 610 L306 610 L300 425 Z" fill="{JEANS}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M84 600 Q86 640 176 640 L178 604 Z M226 604 L228 640 Q318 640 318 600 Z" fill="#e9e6e0" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'''

def phone_svg(x, y, rot=0, s=1.0, glow=True):
    g = f'<ellipse cx="17" cy="33" rx="60" ry="70" fill="{ACC}" opacity="0.18"/>' if glow else ""
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})">{g}
    <rect x="0" y="0" width="34" height="66" rx="7" fill="#0c0c0e" stroke="{INK}" stroke-width="5"/>
    <rect x="5" y="7" width="24" height="50" rx="3" fill="{ACC}" opacity="0.92"/></g>'''

def eli(x, y, s=1.0, pose="stand", mood="calm", look=0, flip=False):
    fl = f" translate(400 0) scale(-1 1)" if flip else ""
    if pose == "sit_phone":
        body = _bag() + _torso() + _face(mood, look) + f'''
  <path d="M282 238 Q338 290 318 338 Q300 362 276 330 Q262 260 268 196" fill="{HOOD}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  {phone_svg(252, 128, -14)}
  <ellipse cx="270" cy="196" rx="20" ry="17" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'''
    elif pose == "sit_letter":
        body = _bag() + _torso() + _face(mood, look) + f'''
  <path d="M110 300 Q90 380 150 420 L250 420 Q310 380 290 300" fill="none" stroke="{INK}" stroke-width="7"/>'''
    elif pose == "stand":
        body = _bag() + _legs_stand() + _torso() + _face(mood, look)
    elif pose == "stand_phone":
        body = _bag() + _legs_stand() + _torso() + _face(mood, look) + f'''
  <path d="M286 250 Q330 330 290 360 Q250 330 236 296" fill="{HOOD}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>
  {phone_svg(208, 262, 8, 1.15)}
  <ellipse cx="236" cy="300" rx="20" ry="17" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'''
    elif pose == "hold_case":
        body = _bag() + _legs_stand() + _torso() + _face(mood, look) + f'''
  <path d="M112 250 Q80 330 140 360 M288 250 Q320 330 260 360" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>
  <path d="M112 250 Q80 330 140 360 M288 250 Q320 330 260 360" fill="none" stroke="{HOOD}" stroke-width="18" stroke-linecap="round"/>
  {case_svg(118, 330, 0.9)}
  <ellipse cx="140" cy="362" rx="18" ry="16" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>
  <ellipse cx="260" cy="362" rx="18" ry="16" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'''
    elif pose == "run":
        body = f'''<g transform="rotate(10 200 400)">
  <path d="M150 420 L60 560 L20 540 M250 420 L300 530 L380 600" fill="none" stroke="{INK}" stroke-width="58" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M150 420 L60 560 L20 540 M250 420 L300 530 L380 600" fill="none" stroke="{JEANS}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <ellipse cx="22" cy="548" rx="34" ry="20" fill="#e9e6e0" stroke="{INK}" stroke-width="7"/>
  <ellipse cx="392" cy="604" rx="34" ry="20" fill="#e9e6e0" stroke="{INK}" stroke-width="7"/>
  {_bag(40, 220)}{_torso()}
  <path d="M120 250 L60 330 M280 250 L350 300" fill="none" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>
  <path d="M120 250 L60 330 M280 250 L350 300" fill="none" stroke="{HOOD}" stroke-width="28" stroke-linecap="round"/>
  {_face(mood, look)}</g>
  <path d="M-80 250 L-10 250 M-120 330 L-30 330 M-60 410 L0 410" stroke="#cfd3da" stroke-width="7" stroke-linecap="round" opacity="0.6"/>'''
    elif pose == "bike":
        body = f'''
  <circle cx="20" cy="560" r="110" fill="none" stroke="{INK}" stroke-width="14"/>
  <circle cx="20" cy="560" r="110" fill="none" stroke="#5b5e66" stroke-width="5"/>
  <circle cx="420" cy="560" r="110" fill="none" stroke="{INK}" stroke-width="14"/>
  <circle cx="420" cy="560" r="110" fill="none" stroke="#5b5e66" stroke-width="5"/>
  <path d="M20 560 L170 560 L330 420 L420 560 M170 560 L130 420 L330 420 M110 410 L160 410 M330 420 L350 340 L400 330" fill="none" stroke="{INK}" stroke-width="13" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M20 560 L170 560 L330 420 L420 560 M170 560 L130 420 L330 420" fill="none" stroke="#8a3b3b" stroke-width="6" stroke-linejoin="round"/>
  <path d="M150 420 L200 500 L170 560 M190 420 L250 480 L230 540" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M150 420 L200 500 L170 560 M190 420 L250 480 L230 540" fill="none" stroke="{JEANS}" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
  <g transform="translate(10 0) rotate(18 200 400)">{_bag(30, 200)}{_torso()}
  <path d="M260 260 L370 340" stroke="{INK}" stroke-width="40" stroke-linecap="round"/>
  <path d="M260 260 L370 340" stroke="{HOOD}" stroke-width="28" stroke-linecap="round"/>
  {_face(mood, look)}</g>'''
    elif pose == "face_close":
        body = f'''{_torso()}{_face(mood, look)}
  <ellipse cx="200" cy="240" rx="90" ry="60" fill="{ACC}" opacity="0.10"/>'''
    else:
        raise ValueError(pose)
    return f'<g transform="translate({x} {y}) scale({s}){fl}">{body}</g>'

def stranger(x, y, s=1.0, opacity=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})" opacity="{opacity}">
  <path d="M30 900 L40 300 Q80 230 150 230 Q220 230 260 300 L272 900 Z" fill="#4b4e55" stroke="{INK}" stroke-width="8"/>
  <path d="M150 240 L150 900" stroke="{INK}" stroke-width="5" opacity="0.6"/>
  <path d="M90 250 L150 380 L210 250" fill="none" stroke="{INK}" stroke-width="6"/>
  <ellipse cx="150" cy="170" rx="62" ry="72" fill="#2e3035" stroke="{INK}" stroke-width="8"/>
  <path d="M60 140 L240 140 L222 100 Q150 66 78 100 Z" fill="#1b1c20" stroke="{INK}" stroke-width="7"/>
  <rect x="40" y="132" width="220" height="16" rx="6" fill="#1b1c20" stroke="{INK}" stroke-width="6"/>
  <path d="M118 180 L138 180 M162 180 L182 180" stroke="#cfd3da" stroke-width="6" stroke-linecap="round"/>
</g>'''

def case_svg(x, y, s=1.0, sticker=True, glow=False):
    gl = f'<ellipse cx="82" cy="60" rx="150" ry="110" fill="{ACC}" opacity="0.16"/>' if glow else ""
    st = (f'<rect x="56" y="44" width="56" height="22" rx="3" fill="{ACC}" stroke="{INK}" stroke-width="3"/>'
          f'<text x="84" y="61" font-family="Inter" font-weight="800" font-size="13" text-anchor="middle" fill="{INK}">FRAGILE</text>') if sticker else ""
    return f'''<g transform="translate({x} {y}) scale({s})">{gl}
  <path d="M60 10 Q60 -14 84 -14 Q108 -14 108 10" fill="none" stroke="{INK}" stroke-width="9"/>
  <rect x="0" y="8" width="168" height="104" rx="12" fill="#a7adb5" stroke="{INK}" stroke-width="8"/>
  <path d="M0 40 L168 40" stroke="{INK}" stroke-width="5"/>
  <rect x="14" y="16" width="16" height="16" rx="3" fill="#6e747c" stroke="{INK}" stroke-width="3"/>
  <rect x="138" y="16" width="16" height="16" rx="3" fill="#6e747c" stroke="{INK}" stroke-width="3"/>
  {st}</g>'''

# ---------------- backgrounds / helpers ----------------
def rain(x0, y0, w, h, n, seed, op=(0.2, 0.55), col="#9fb3c8"):
    r = random.Random(seed); out = []
    for _ in range(n):
        x = r.uniform(x0, x0 + w); y = r.uniform(y0, y0 + h); l = r.uniform(20, 70)
        out.append(f'<path d="M{x:.0f} {y:.0f} l{-l*0.12:.1f} {l:.0f}" stroke="{col}" stroke-width="2" opacity="{r.uniform(*op):.2f}"/>')
    return "\n".join(out)

def bokeh(items):
    return '<g filter="url(#b30)">' + "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"/>' for x, y, r, c, o in items) + "</g>"

def text(x, y, s, size, weight=800, fill="#f4f1ea", anchor="start", ls=0, family=FONT, op=1):
    s = s.replace("&", "&amp;")
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{s}</text>')

def svg(body, bg="#14151a"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <filter id="b30"><feGaussianBlur stdDeviation="30"/></filter>
 <filter id="b8"><feGaussianBlur stdDeviation="8"/></filter>
 <filter id="b3"><feGaussianBlur stdDeviation="3"/></filter>
 <radialGradient id="lamp" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#f6e7c4" stop-opacity="0.35"/><stop offset="1" stop-color="#f6e7c4" stop-opacity="0"/></radialGradient>
 <radialGradient id="ylamp" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{ACC}" stop-opacity="0.35"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
 <radialGradient id="blue" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#3d7bd9" stop-opacity="0.45"/><stop offset="1" stop-color="#3d7bd9" stop-opacity="0"/></radialGradient>
 <linearGradient id="fadeB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.7"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>'''

def render(svgtext, path, scale=1.2, grain=7, vignette=0.45):
    tmp = path + ".svg"
    open(tmp, "w").write(svgtext)
    w, h = int(W * scale), int(H * scale)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), tmp, "-o", path + ".raw.png"], check=True)
    a = np.asarray(Image.open(path + ".raw.png").convert("RGB")).astype(np.float32)
    r = np.random.default_rng(abs(hash(path)) % 2**32)
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - vignette * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = a * vig[..., None] + r.normal(0, grain, (h, w, 1))
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path, quality=93)
    os.remove(tmp); os.remove(path + ".raw.png")
