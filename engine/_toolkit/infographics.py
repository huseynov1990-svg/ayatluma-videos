# -*- coding: utf-8 -*-
"""Инфографика вместо случайных роликов: анимированные карты, флаги, счётчики дат и чисел.
Используется в render_doc.py (документальные серии) и в исламских стилях NUR.

spec (dict):
  {"type": "map", "focus": ["TR"], "hl": ["TR"], "pins": [{"name": "Istanbul", "lat": 41.01, "lon": 28.98}],
   "route": [[lat, lon], ...], "flags": ["tr"], "cap": "текст внизу"}
  {"type": "number", "value": "1453", "cap": "текст", "focus": ["TR"], "flags": ["tr"]}
  {"type": "flags", "flags": ["no", "se", "dk"], "cap": "..."}
Данные: assets/countries.json, cities.json, water.json, flags/*.png (Natural Earth — public domain; flag-icons — MIT)."""
import os, re, json, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets')
_C = {}
def _unpack():
    z = os.path.join(HERE, 'infographics_assets.zip')
    if not os.path.exists(os.path.join(A, 'countries.json')) and os.path.exists(z):
        import zipfile; zipfile.ZipFile(z).extractall(HERE)
_unpack()
def data(name):
    if name not in _C: _C[name] = json.load(open(os.path.join(A, name), encoding='utf-8'))
    return _C[name]

THEMES = {
    'doc': dict(sea_top=(22, 38, 62), sea_bot=(12, 22, 40), land=(226, 218, 198), land2=(208, 199, 177), border=(132, 120, 100),
                hl=(214, 48, 49), text=(255, 255, 255), outline=(20, 16, 40), accent=(214, 48, 49), grat=(255, 255, 255, 18),
                river=(60, 110, 170), lake=(40, 74, 112), cap_bg=(214, 48, 49), cap_fg=(255, 255, 255), num=(214, 48, 49)),
    'nur': dict(sea_top=(20, 15, 11), sea_bot=(8, 6, 5), land=(66, 50, 34), land2=(56, 42, 29), border=(170, 135, 70),
                hl=(247, 201, 102), text=(255, 246, 228), outline=(10, 6, 2), accent=(247, 201, 102), grat=(247, 201, 102, 16),
                river=(110, 90, 55), lake=(26, 20, 14), cap_bg=(247, 201, 102), cap_fg=(40, 24, 10), num=(247, 201, 102)),
}

# названия стран по-азербайджански (Natural Earth не содержит az)
AZ = {'TR': 'Türkiyə', 'AZ': 'Azərbaycan', 'RU': 'Rusiya', 'IR': 'İran', 'GE': 'Gürcüstan', 'AM': 'Ermənistan', 'IQ': 'İraq',
      'SY': 'Suriya', 'SA': 'Səudiyyə Ərəbistanı', 'AE': 'BƏƏ', 'EG': 'Misir', 'GR': 'Yunanıstan', 'BG': 'Bolqarıstan', 'IT': 'İtaliya',
      'FR': 'Fransa', 'DE': 'Almaniya', 'GB': 'Britaniya', 'NO': 'Norveç', 'SE': 'İsveç', 'DK': 'Danimarka', 'IS': 'İslandiya',
      'FI': 'Finlandiya', 'PL': 'Polşa', 'UA': 'Ukrayna', 'KZ': 'Qazaxıstan', 'UZ': 'Özbəkistan', 'TM': 'Türkmənistan', 'KG': 'Qırğızıstan',
      'TJ': 'Tacikistan', 'AF': 'Əfqanıstan', 'PK': 'Pakistan', 'IN': 'Hindistan', 'CN': 'Çin', 'MN': 'Monqolustan', 'KP': 'Şimali Koreya',
      'KR': 'Cənubi Koreya', 'JP': 'Yaponiya', 'US': 'ABŞ', 'CA': 'Kanada', 'MX': 'Meksika', 'BR': 'Braziliya', 'ES': 'İspaniya',
      'PT': 'Portuqaliya', 'JO': 'İordaniya', 'IL': 'İsrail', 'PS': 'Fələstin', 'LB': 'Livan', 'YE': 'Yəmən', 'OM': 'Oman', 'QA': 'Qətər',
      'KW': 'Küveyt', 'BH': 'Bəhreyn', 'LY': 'Liviya', 'SD': 'Sudan', 'ET': 'Efiopiya', 'TN': 'Tunis', 'DZ': 'Əlcəzair', 'MA': 'Mərakeş',
      'IE': 'İrlandiya', 'NL': 'Niderland', 'BE': 'Belçika', 'AT': 'Avstriya', 'CH': 'İsveçrə', 'HU': 'Macarıstan', 'RO': 'Rumıniya',
      'CY': 'Kipr', 'BY': 'Belarus', 'TW': 'Tayvan', 'VN': 'Vyetnam', 'TH': 'Tailand', 'ID': 'İndoneziya', 'PH': 'Filippin', 'AU': 'Avstraliya'}

def cname(iso, lang):
    c = data('countries.json').get(iso)
    if not c: return iso
    if lang == 'az' and iso in AZ: return AZ[iso]
    return c['name'].get(lang) or c['name']['en']

# ---------------- fonts
_F = {}
def font(size, w=800):
    k = (size, w)
    if k not in _F:
        for p in (os.path.join(HERE, 'fonts', 'Montserrat.ttf'), r'D:\gemini\_doc_engine\fonts\Montserrat.ttf',
                  os.path.join(HERE, '..', '_doc_engine', 'fonts', 'Montserrat.ttf')):
            if os.path.exists(p):
                f = ImageFont.truetype(p, size)
                try: f.set_variation_by_axes([w])
                except Exception: pass
                _F[k] = f; break
        else: _F[k] = ImageFont.load_default()
    return _F[k]

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def pop(t, d=0.3):
    if t <= 0: return 0.0
    x = min(1.0, t / d); return 1 + 0.12 * math.sin(x * math.pi) if x < 1 else 1.0

# ---------------- projection (Mercator)
def merc(lon, lat):
    lat = max(-80, min(80, lat)); return lon, -math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))

_BB = {}
def country_bbox(iso):
    if iso not in _BB:
        xs, ys = [], []
        for r in data('countries.json')[iso]['rings']:
            for lon, lat in r:
                x, y = merc(lon, lat); xs.append(x); ys.append(y)
        _BB[iso] = (min(xs), min(ys), max(xs), max(ys))
    return _BB[iso]

def main_bbox(iso):
    """bbox самой большой части страны (без далёких островов)"""
    rings = data('countries.json')[iso]['rings']
    best = max(rings, key=len)
    pts = [merc(*p) for p in best]
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

class Map:
    def __init__(self, spec, W, H, theme='doc', lang='en', ss=1.0):
        self.s = spec; self.W, self.H = W, H; self.th = THEMES[theme]; self.lang = lang
        C = data('countries.json')
        self.hl = [c for c in spec.get('hl', spec.get('focus', [])) if c in C]
        focus = [c for c in spec.get('focus', self.hl) if c in C]
        boxes = [main_bbox(c) for c in focus]
        for p in spec.get('pins', []): x, y = merc(p['lon'], p['lat']); boxes.append((x - 1.5, y - 1.5, x + 1.5, y + 1.5))
        for lat, lon in spec.get('route', []): x, y = merc(lon, lat); boxes.append((x - 1, y - 1, x + 1, y + 1))
        if not boxes: boxes = [(-20, -60, 60, -20)]
        x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes); x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
        pad = spec.get('pad', 0.35)
        bw, bh = max(x1 - x0, 2.5), max(y1 - y0, 2.5)
        self.cx, self.cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.s1 = min(W * (1 - pad) / bw, H * (1 - pad - 0.1) / bh)
        self.s1 = min(self.s1, spec.get('maxzoom', 420))
        self.s0 = self.s1 / spec.get('zoomfrom', 2.6)
        self.zoom_t = spec.get('zoom_t', 2.4)
        self._static = None
        self.flags = {}
        for f in spec.get('flags', []):
            p = os.path.join(A, 'flags', f.lower() + '.png')
            if os.path.exists(p): self.flags[f.lower()] = flag_disc(Image.open(p), 54, self.th)

    def to_px(self, x, y, cx, cy, s): return (x - cx) * s + self.W / 2, (y - cy) * s + self.H / 2

    def draw_base(self, cx, cy, s, scale=1.0):
        W, H = int(self.W * scale), int(self.H * scale); th = self.th
        img = Image.new('RGB', (W, H), th['sea_bot'])
        g = Image.linear_gradient('L').resize((W, H))
        img = Image.composite(Image.new('RGB', (W, H), th['sea_bot']), Image.new('RGB', (W, H), th['sea_top']), g)
        d = ImageDraw.Draw(img, 'RGBA'); ss = s * scale
        P = lambda x, y: ((x - cx) * ss + W / 2, (y - cy) * ss + H / 2)
        vx0, vx1 = cx - W / 2 / ss, cx + W / 2 / ss; vy0, vy1 = cy - H / 2 / ss, cy + H / 2 / ss
        # graticule
        step = 10 if ss < 60 else 5 if ss < 160 else 2
        for lon in range(-180, 181, step):
            if vx0 - step <= lon <= vx1 + step: d.line([P(lon, vy0), P(lon, vy1)], fill=th['grat'], width=max(1, int(scale)))
        for lat in range(-80, 81, step):
            y = merc(0, lat)[1]
            if vy0 - step <= y <= vy1 + step: d.line([P(vx0, y), P(vx1, y)], fill=th['grat'], width=max(1, int(scale)))
        C = data('countries.json'); lw = max(1, int(1.6 * scale))
        for iso, c in C.items():
            b = country_bbox(iso)
            if b[2] < vx0 or b[0] > vx1 or b[3] < vy0 or b[1] > vy1: continue
            col = th['land'] if (hash(iso) % 2) else th['land2']
            for r in c['rings']:
                pts = [P(*merc(lon, lat)) for lon, lat in r]
                if len(pts) > 2: d.polygon(pts, fill=col, outline=th['border'])
        W2 = data('water.json')
        for r in W2['lakes']:
            pts = [P(*merc(lon, lat)) for lon, lat in r]
            if len(pts) > 2 and any(0 <= x <= W and 0 <= y <= H for x, y in pts[::5]): d.polygon(pts, fill=th['lake'])
        if ss > 40:
            for r in W2['rivers']:
                pts = [P(*merc(lon, lat)) for lon, lat in r]
                if len(pts) > 1 and any(0 <= x <= W and 0 <= y <= H for x, y in pts[::4]): d.line(pts, fill=th['river'], width=max(1, int(2 * scale)))
        return img

    def hl_layer(self, cx, cy, s, a):
        lay = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        C = data('countries.json')
        for iso in self.hl:
            for r in C[iso]['rings']:
                pts = [self.to_px(*merc(lon, lat), cx, cy, s) for lon, lat in r]
                if len(pts) > 2: d.polygon(pts, fill=self.th['hl'] + (int(150 * a),), outline=self.th['hl'] + (int(255 * a),))
        glow = lay.filter(ImageFilter.GaussianBlur(10))
        out = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0)); out.alpha_composite(glow); out.alpha_composite(lay)
        return out

    def labels(self, img, cx, cy, s, t):
        d = ImageDraw.Draw(img); C = data('countries.json'); th = self.th
        vx0, vx1 = cx - self.W / 2 / s, cx + self.W / 2 / s; vy0, vy1 = cy - self.H / 2 / s, cy + self.H / 2 / s
        placed = [(0, 0, 150 + 140 * len(self.flags), 200)] if self.flags else []
        cand = []
        for iso, c in C.items():
            lx, ly = c['label']
            if lx is None: continue
            x, y = merc(lx, ly)
            if not (vx0 < x < vx1 and vy0 < y < vy1): continue
            b = country_bbox(iso); area = (b[2] - b[0]) * (b[3] - b[1]) * s * s
            if iso in self.hl or area > 26000: cand.append((iso in self.hl, area, iso, x, y))
        cand.sort(reverse=True)
        for is_hl, area, iso, x, y in cand[:14]:
            px, py = self.to_px(x, y, cx, cy, s)
            if any(math.dist((px, py), self.to_px(*merc(p['lon'], p['lat']), cx, cy, s)) < 260 for p in self.s.get('pins', [])):
                if not is_hl: continue
                py += 120
            nm = cname(iso, self.lang).upper()
            f = font(44 if is_hl else 24, 850 if is_hl else 700)
            tw = d.textlength(nm, font=f)
            box = (px - tw / 2 - 8, py - 26, px + tw / 2 + 8, py + 26)
            if any(not (box[2] < q[0] or box[0] > q[2] or box[3] < q[1] or box[1] > q[3]) for q in placed): continue
            if box[0] < 20 or box[2] > self.W - 20 or box[1] < 20 or box[3] > self.H - 170: continue
            placed.append(box)
            a = int(255 * ease((t - (0.6 if is_hl else 1.0)) / 0.4))
            if a <= 0: continue
            col = th['text'] if is_hl else (th['outline'] if self.th is THEMES['doc'] else th['border'])
            if is_hl:
                for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3), (2, 2), (-2, 2)): d.text((px + ox, py + oy), nm, font=f, fill=th['outline'] + (a,), anchor='mm')
            d.text((px, py), nm, font=f, fill=col + (int(a * (1 if is_hl else 0.75)),), anchor='mm')

    def frame(self, t, d):
        th = self.th
        z = ease(t / self.zoom_t); s = self.s0 + (self.s1 - self.s0) * z
        s *= 1 + 0.05 * max(0.0, t - self.zoom_t) / max(1.0, d)
        yc = self.s.get('ycenter', 0.5)
        cx, cy = self.cx, self.cy - (yc - 0.5) * self.H / s
        if t < self.zoom_t + 0.05 or self._static is None:
            if t >= self.zoom_t:
                self._static = (self.draw_base(cx, self.cy - (yc - 0.5) * self.H / self.s1, self.s1, 1.08), self.s1)
            base = self.draw_base(cx, cy, s).convert('RGBA') if t < self.zoom_t else None
        if t >= self.zoom_t:
            big, s1 = self._static; k = s / s1
            cw, ch = big.width / k / 1.08, big.height / k / 1.08
            bx, by = (big.width - cw) / 2, (big.height - ch) / 2
            base = big.resize((self.W, self.H), Image.BILINEAR, box=(bx, by, bx + cw, by + ch)).convert('RGBA')
        pulse = 0.75 + 0.25 * math.sin(t * 3)
        if self.hl: base.alpha_composite(self.hl_layer(cx, cy, s, ease((t - 0.3) / 0.6) * pulse))
        self.labels(base, cx, cy, s, t)
        dr = ImageDraw.Draw(base)
        # route
        rt = self.s.get('route')
        if rt and len(rt) > 1:
            pts = [self.to_px(*merc(lon, lat), cx, cy, s) for lat, lon in rt]
            prog = ease((t - 1.2) / 2.2)
            seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; L = sum(seg) * prog; acc = 0; dl = [pts[0]]
            for (a, b), sl in zip(zip(pts, pts[1:]), seg):
                if acc + sl <= L: dl.append(b); acc += sl
                else:
                    f = (L - acc) / sl if sl else 0; dl.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)); break
            if prog > 0 and len(dl) > 1:
                dr.line(dl, fill=(0, 0, 0, 110), width=14); dr.line(dl, fill=th['accent'] + (255,), width=8, joint='curve')
                (ax, ay), (bx2, by2) = dl[-2], dl[-1]; an = math.atan2(by2 - ay, bx2 - ax)
                dr.polygon([(bx2 + 26 * math.cos(an), by2 + 26 * math.sin(an)), (bx2 + 22 * math.cos(an + 2.5), by2 + 22 * math.sin(an + 2.5)),
                            (bx2 + 22 * math.cos(an - 2.5), by2 + 22 * math.sin(an - 2.5))], fill=th['accent'] + (255,))
        # pins
        for j, p in enumerate(self.s.get('pins', [])):
            tt = t - 0.9 - 0.35 * j
            if tt < 0: continue
            x, y = self.to_px(*merc(p['lon'], p['lat']), cx, cy, s); sc = pop(tt)
            rr = 22 + 26 * ((t * 0.8 + j * 0.3) % 1.0)
            dr.ellipse([x - rr, y - rr, x + rr, y + rr], outline=th['accent'] + (int(200 * (1 - ((t * 0.8 + j * 0.3) % 1.0))),), width=4)
            r = 15 * sc; dr.ellipse([x - r, y - r, x + r, y + r], fill=th['accent'] + (255,), outline=(255, 255, 255, 255), width=4)
            if tt > 0.2 and p.get('name'):
                f = font(p.get('size', 42), 850); side = p.get('side', 'r')
                tx = x + (30 if side == 'r' else -30); anc = 'lm' if side == 'r' else 'rm'
                tw = dr.textlength(p['name'], font=f)
                bx0 = tx - 14 if side == 'r' else tx - tw - 14
                a = int(235 * ease((tt - 0.2) / 0.3))
                dr.rounded_rectangle([bx0, y - 32, bx0 + tw + 28, y + 32], 10, fill=th['outline'] + (int(a * 0.85),))
                dr.text((tx, y), p['name'], font=f, fill=th['text'] + (a,), anchor=anc)
        # flags (top-left stack)
        for j, (k2, fl) in enumerate(self.flags.items()):
            sc = pop(t - 0.5 - 0.25 * j)
            if sc > 0: paste_scaled(base, fl, 110 + j * 140, 115, sc)
        cap = self.s.get('cap')
        if cap: caption(base, cap, t - 0.4, th)
        return base

def flag_disc(fl, r, th):
    fl = fl.convert('RGB'); w, h = fl.size; k = 2 * r / min(w, h)
    fl = fl.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
    fl = fl.crop(((fl.width - 2 * r) // 2, (fl.height - 2 * r) // 2, (fl.width - 2 * r) // 2 + 2 * r, (fl.height - 2 * r) // 2 + 2 * r)).convert('RGBA')
    m = Image.new('L', (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255); fl.putalpha(m)
    d = Image.new('RGBA', (2 * r + 14, 2 * r + 14), (0, 0, 0, 0))
    ImageDraw.Draw(d).ellipse([0, 0, 2 * r + 13, 2 * r + 13], fill=(255, 255, 255, 255) if th is THEMES['doc'] else th['accent'] + (255,))
    d.alpha_composite(fl, (7, 7)); return d

def paste_scaled(img, im, cx, cy, sc):
    if sc <= 0.01: return
    w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc)); im2 = im.resize((w, h), Image.LANCZOS)
    img.alpha_composite(im2, (int(cx - w / 2), int(cy - h / 2)))

def caption(img, text, t, th):
    if t < 0: return
    W, H = img.size; a = ease(t / 0.35); f = font(46, 800)
    d = ImageDraw.Draw(img)
    words = text.split(); lines = []; cur = []
    for w in words:
        if cur and d.textlength(' '.join(cur + [w]), font=f) > W - 360: lines.append(' '.join(cur)); cur = [w]
        else: cur.append(w)
    if cur: lines.append(' '.join(cur))
    lines = lines[:2]
    tw = max(d.textlength(l, font=f) for l in lines); hh = 64 * len(lines) + 28
    x0 = W / 2 - tw / 2 - 30; y0 = H - 70 - hh + 30 * (1 - a)
    d.rounded_rectangle([x0, y0, x0 + tw + 60, y0 + hh], 14, fill=th['cap_bg'] + (int(235 * a),))
    for i, l in enumerate(lines): d.text((W / 2, y0 + 14 + 32 + i * 64), l, font=f, fill=th['cap_fg'] + (int(255 * a),), anchor='mm')

class Number:
    def __init__(self, spec, W, H, theme='doc', lang='en'):
        self.s = spec; self.W, self.H = W, H; self.th = THEMES[theme]
        m = dict(spec); m['cap'] = None; m.setdefault('zoomfrom', 1.0); m['pins'] = spec.get('pins', [])
        self.bg = None; self.mp = Map(m, W, H, theme, lang) if (spec.get('focus') or spec.get('pins')) else None
        self.flags = [flag_disc(Image.open(os.path.join(A, 'flags', f.lower() + '.png')), 46, self.th)
                      for f in spec.get('flags', []) if os.path.exists(os.path.join(A, 'flags', f.lower() + '.png'))]

    def frame(self, t, d):
        th = self.th
        if self.bg is None:
            if self.mp: base = self.mp.draw_base(self.mp.cx, self.mp.cy, self.mp.s1 * 0.8).convert('RGBA'); base.alpha_composite(self.mp.hl_layer(self.mp.cx, self.mp.cy, self.mp.s1 * 0.8, 0.8))
            elif self.th is THEMES['nur']:
                self.pat = Pattern({}, self.W, self.H, 'nur'); base = None
            else:
                g = Image.linear_gradient('L').resize((self.W, self.H))
                base = Image.composite(Image.new('RGB', (self.W, self.H), th['sea_bot']), Image.new('RGB', (self.W, self.H), th['sea_top']), g).convert('RGBA')
            if base is None: self.bg = 'pattern'
            else: base = base.filter(ImageFilter.GaussianBlur(6))
            if base is not None:
                dark = Image.new('RGBA', base.size, (0, 0, 0, 140)); base.alpha_composite(dark); self.bg = base
        if self.bg == 'pattern': img = self.pat.frame(t, d)
        else:
            k = 1 + 0.04 * t / max(1.0, d); cw, ch = self.W / k, self.H / k
            img = self.bg.resize((self.W, self.H), Image.BILINEAR, box=((self.W - cw) / 2, (self.H - ch) / 2, (self.W + cw) / 2, (self.H + ch) / 2))
        dr = ImageDraw.Draw(img)
        v = str(self.s['value']); prog = ease(t / 1.1)
        def cnt(m):
            s = m.group(0); c = s.replace(',', '').replace(' ', '')
            try: x = float(c.replace(',', '.'))
            except ValueError: return s
            if prog >= 1: return s
            if '.' in c: return ('%.1f' % (x * prog))
            n = int(x * prog)
            return '{:,}'.format(n).replace(',', ' ') if (' ' in s or ',' in s) else str(n)
        num = re.sub(r'\d[\d ,\.]*\d|\d', cnt, v) if self.s.get('count', True) else v
        top = self.s.get('layout') == 'top'
        f = font((150 if top else 250) if len(v) <= 5 else (120 if top else 190) if len(v) <= 9 else (95 if top else 140), 900)
        y = self.H * (0.2 if top else 0.5) - (0 if top else 70)
        for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)):
            dr.text((self.W / 2 + ox, y + oy), num, font=f, fill=th['outline'] + (255,), anchor='mm')
        dr.text((self.W / 2, y), num, font=f, fill=th['num'] + (255,), anchor='mm')
        if self.s.get('unit') and t > 0.4 and not top:
            a = int(255 * ease((t - 0.4) / 0.4)); fu = font(62, 800)
            dr.text((self.W / 2, y + 165), self.s['unit'], font=fu, fill=th['text'] + (a,), anchor='mm')
        if not top:
            for j, fl in enumerate(self.flags): paste_scaled(img, fl, self.W / 2 + (j - (len(self.flags) - 1) / 2) * 120, y - 230, pop(t - 0.3 - 0.2 * j))
        if self.s.get('cap') and not top: caption(img, self.s['cap'], t - 0.6, th)
        return img

class Flags:
    def __init__(self, spec, W, H, theme='doc', lang='en'):
        self.s = spec; self.W, self.H = W, H; self.th = THEMES[theme]; self.lang = lang
        self.items = []
        C = data('countries.json')
        for f in spec['flags']:
            p = os.path.join(A, 'flags', f.lower() + '.png')
            if os.path.exists(p): self.items.append((flag_disc(Image.open(p), 120, self.th), cname(f.upper(), lang) if f.upper() in C else f.upper()))
        self.n = Number(dict(value='', focus=[f.upper() for f in spec['flags'] if f.upper() in C]), W, H, theme, lang)
    def frame(self, t, d):
        self.n.s = dict(self.n.s, value=''); img = self.n.frame(t, d)
        dr = ImageDraw.Draw(img); n = len(self.items)
        for j, (fl, nm) in enumerate(self.items):
            cx = self.W / 2 + (j - (n - 1) / 2) * min(420, 1600 / max(n, 1)); cy = self.H / 2 - 60
            sc = pop(t - 0.2 - 0.3 * j); paste_scaled(img, fl, cx, cy, sc)
            if sc >= 1:
                f = font(52, 850); dr.text((cx, cy + 175), nm.upper(), font=f, fill=self.th['text'] + (255,), anchor='mm')
        if self.s.get('cap'): caption(img, self.s['cap'], t - 0.6, self.th)
        return img

def make(spec, W, H, theme='doc', lang='en'):
    T = spec.get('type', 'map')
    if T == 'number': return Number(spec, W, H, theme, lang)
    if T == 'flags': return Flags(spec, W, H, theme, lang)
    return Map(spec, W, H, theme, lang)

# ---------------- automatic spec from paragraph text
YEAR = re.compile(r'(?<![\d.,])(1[0-9]{3}|20[0-4][0-9]|[1-9][0-9]{2})(?:-?(?:ci|cı|cu|cü|ji|ий|го|м|year|s))?(?![\d])')
def find_place(name):
    for c in data('cities.json'):
        if c[0].lower() == name.lower(): return c
    return None

def auto_specs(text, ep_map, lang='en'):
    """ep_map: {'focus': [...], 'pins': [...], 'flags': [...]} — карта серии по умолчанию.
    Возвращает 1-2 spec: число/год (если есть) и карта."""
    out = []
    sents = re.split(r'(?<=[.!?])\s+', text)
    num = None
    for s in sents:
        m = re.search(r'(\d[\d ,\.]*\d|\d+)\s*(min|milyon|milyard|mln|thousand|million|billion|тысяч|миллион|миллиард|%|faiz|percent)?', s)
        if m and (m.group(2) or YEAR.fullmatch(m.group(1).strip())):
            val = m.group(1).strip(); unit = m.group(2) or ''
            words = s.split()
            cap = ' '.join(words[:9]) + ('…' if len(words) > 9 else '')
            num = dict(type='number', value=(val + (' ' + unit if unit else '')).strip(), cap=cap.rstrip(',;:'),
                       focus=ep_map.get('focus', []), flags=ep_map.get('flags', [])[:1])
            break
    mp = dict(type='map', focus=ep_map.get('focus', []), hl=ep_map.get('hl', ep_map.get('focus', [])), pins=ep_map.get('pins', []),
              flags=ep_map.get('flags', [])[:1], cap=None)
    if num: out.append(num)
    out.append(mp)
    return out

# ---------------- текстовый формат в kadr.txt
#  @map: focus=TR; pins=İstanbul@41.01,28.98; flags=tr
#  5 | начало | istanbul walls || num: 1453; cap=Константинополь пал
#  6 | начало | INFO || map: focus=GR,TR; pins=Byzantion@41.01,28.98/Athens@37.98,23.73@l; route=37.98,23.73/41.01,28.98; cap=...
def parse_spec(s, base=None):
    s = s.strip()
    if not s: return None
    typ, _, rest = s.partition(':') if re.match(r'^\s*(map|num|number|flags)\s*:', s) else ('map', '', s)
    typ = {'num': 'number'}.get(typ.strip(), typ.strip())
    sp = dict(base or {}); sp['type'] = typ
    if typ != 'map': sp.pop('route', None)
    for part in rest.split(';'):
        if '=' not in part: continue
        k, v = [x.strip() for x in part.split('=', 1)]
        if k in ('focus', 'hl'): sp[k] = [x.strip().upper() for x in v.split(',') if x.strip()]
        elif k == 'flags': sp['flags'] = [x.strip().lower() for x in v.split(',') if x.strip()]
        elif k == 'pins':
            pins = []
            for p in v.split('/'):
                q = p.split('@')
                if len(q) >= 2:
                    la, lo = [float(x) for x in q[1].split(',')]
                    pins.append(dict(name=q[0].strip(), lat=la, lon=lo, side=('l' if len(q) > 2 and q[2].strip() == 'l' else 'r')))
                else:
                    c = find_place(q[0].strip())
                    if c: pins.append(dict(name=q[0].strip(), lat=c[1], lon=c[2]))
            sp['pins'] = pins
        elif k == 'route': sp['route'] = [[float(a) for a in x.split(',')] for x in v.split('/') if ',' in x]
        elif k in ('value', 'cap', 'unit'): sp[k] = v
        elif k == 'zoomfrom': sp[k] = float(v)
    if typ == 'number' and 'value' not in sp:
        m = re.match(r'\s*([^;]+)', rest)
        if m and '=' not in m.group(1): sp['value'] = m.group(1).strip()
    keys = [x.split('=', 1)[0].strip() for x in rest.split(';') if '=' in x]
    if 'focus' in keys and 'hl' not in keys: sp['hl'] = sp['focus']
    elif 'focus' in sp and 'hl' not in sp: sp['hl'] = sp['focus']
    return sp

def read_kadr(path):
    """-> (topic list, ep_map dict, {N: (query, [specs])})"""
    topic, emap, lines = [], {}, {}
    if not os.path.exists(path): return topic, emap, lines
    for ln in open(path, encoding='utf-8-sig'):
        ln = ln.strip()
        if not ln or ln.startswith('#'): continue
        if ln.startswith('@'):
            k, _, v = ln[1:].partition(':'); k = k.strip().lower()
            if k in ('topic', 'mavzu', 'tema', 'тема'): topic = [x.strip().lower() for x in v.split(',') if x.strip()]
            elif k in ('map', 'xerite', 'карта'): emap = parse_spec('map: ' + v) or {}
            continue
        p = [x.strip() for x in ln.split('|')]
        try: n = int(p[0])
        except ValueError: continue
        tail = ln.split('|', 2)[-1] if ln.count('|') >= 2 else p[-1]
        q, _, sp = tail.partition('||')
        specs = [parse_spec(x, {k: v for k, v in emap.items() if k in ('focus', 'hl', 'flags', 'pins')}) for x in sp.split('&&') if x.strip()]
        lines[n] = (q.strip(), [x for x in specs if x])
    return topic, emap, lines

class Pattern:
    """Анимированный исламский геометрический орнамент (8-конечные звёзды), золото на тёмном. Без людей и случайных кадров."""
    def __init__(self, spec, W, H, theme='nur', lang='en'):
        self.W, self.H = W, H; self.th = THEMES[theme]; self.seed = int(spec.get('seed', 0))
        cell = int(min(W, H) / 4.2)
        big = Image.new('RGBA', (W + 2 * cell, H + 2 * cell), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
        col = self.th['accent']
        for gy in range(-1, (H + 2 * cell) // cell + 2):
            for gx in range(-1, (W + 2 * cell) // cell + 2):
                cx, cy = gx * cell + (cell / 2 if gy % 2 else 0), gy * cell
                r1, r2 = cell * 0.42, cell * 0.30
                pts = []
                for k in range(16):
                    an = math.pi / 8 * k + math.pi / 16; r = r1 if k % 2 == 0 else r2
                    pts.append((cx + r * math.cos(an), cy + r * math.sin(an)))
                d.polygon(pts, outline=col + (105,), width=2)
                for k in range(8):
                    an = math.pi / 4 * k + math.pi / 16
                    d.line([(cx + r1 * math.cos(an), cy + r1 * math.sin(an)), (cx + cell * 0.5 * math.cos(an), cy + cell * 0.5 * math.sin(an))], fill=col + (60,), width=2)
                d.ellipse([cx - r2 * 0.35, cy - r2 * 0.35, cx + r2 * 0.35, cy + r2 * 0.35], outline=col + (80,), width=2)
        self.tile = big; self.cell = cell
        g = Image.linear_gradient('L').resize((W, H))
        self.bg = Image.composite(Image.new('RGB', (W, H), self.th['sea_bot']), Image.new('RGB', (W, H), self.th['sea_top']), g).convert('RGBA')
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([-W * 0.2, -H * 0.2, W * 1.2, H * 1.2], fill=255)
        self.mask = m.filter(ImageFilter.GaussianBlur(min(W, H) // 5))
        glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([W * 0.15, H * 0.2, W * 0.85, H * 0.8], fill=255)
        self.glow = glow.filter(ImageFilter.GaussianBlur(min(W, H) // 4))
    def frame(self, t, d):
        img = self.bg.copy()
        ox = int((t * 9 + self.seed * 37) % self.cell); oy = int((t * 5 + self.seed * 53) % self.cell)
        lay = self.tile.crop((ox, oy, ox + self.W, oy + self.H))
        a = lay.split()[3].point(lambda v: int(v * (0.75 + 0.25 * math.sin(t * 0.8))))
        lay.putalpha(Image.composite(a, Image.new('L', (self.W, self.H), 0), self.mask))
        img.alpha_composite(lay)
        gl = Image.new('RGBA', (self.W, self.H), self.th['accent'] + (0,)); gl.putalpha(self.glow.point(lambda v: int(v * (0.10 + 0.04 * math.sin(t * 0.5)))))
        img.alpha_composite(gl)
        return img

_make0 = make
def make(spec, W, H, theme='doc', lang='en'):
    if spec.get('type') == 'pattern': return Pattern(spec, W, H, theme, lang)
    return _make0(spec, W, H, theme, lang)


# ---------------- исламские серии: места и даты находятся в тексте автоматически
ISL = [  # (названия на разных языках, подпись en/az/ru, lat, lon, страна)
 (('mecca', 'makkah', 'məkkə', 'mekke', 'мекк', 'makka'), {'en': 'Makkah', 'az': 'Məkkə', 'ru': 'Мекка'}, 21.4225, 39.8262, 'SA'),
 (('medina', 'madinah', 'mədinə', 'medine', 'медин', 'yathrib', 'yəsrib', 'ясриб'), {'en': 'Madinah', 'az': 'Mədinə', 'ru': 'Медина'}, 24.4672, 39.6111, 'SA'),
 (('badr', 'bədr', 'бадр'), {'en': 'Badr', 'az': 'Bədr', 'ru': 'Бадр'}, 23.78, 38.79, 'SA'),
 (('uhud', 'ühud', 'ухуд'), {'en': 'Uhud', 'az': 'Ühud', 'ru': 'Ухуд'}, 24.50, 39.61, 'SA'),
 (('taif', 'таиф'), {'en': "Ta'if", 'az': 'Taif', 'ru': 'Таиф'}, 21.27, 40.42, 'SA'),
 (('abyssinia', 'ethiopia', 'habəş', 'həbəş', 'абиссин', 'эфиоп', 'negus', 'nəcaşi', 'najashi', 'негус'), {'en': 'Abyssinia', 'az': 'Həbəşistan', 'ru': 'Абиссиния'}, 14.13, 38.72, 'ET'),
 (('khaybar', 'xeybər', 'хайбар'), {'en': 'Khaybar', 'az': 'Xeybər', 'ru': 'Хайбар'}, 25.70, 39.29, 'SA'),
 (('jerusalem', 'al-aqsa', 'qüds', 'əqsa', 'иерусалим', 'аль-акс'), {'en': 'Jerusalem', 'az': 'Qüds', 'ru': 'Иерусалим'}, 31.78, 35.23, 'PS'),
 (('hudaybiy', 'hüdeybiy', 'hudeybiy', 'худайбий'), {'en': 'Hudaybiyyah', 'az': 'Hüdeybiyyə', 'ru': 'Худайбия'}, 21.44, 39.62, 'SA'),
 (('tabuk', 'təbuk', 'табук'), {'en': 'Tabuk', 'az': 'Təbuk', 'ru': 'Табук'}, 28.38, 36.57, 'SA'),
 (('damascus', 'dəməşq', 'дамаск'), {'en': 'Damascus', 'az': 'Dəməşq', 'ru': 'Дамаск'}, 33.51, 36.29, 'SY'),
 (('hira', 'хира'), {'en': 'Cave of Hira', 'az': 'Hira mağarası', 'ru': 'Пещера Хира'}, 21.457, 39.859, 'SA'),
]
HIJRA = ('hijra', 'hijrah', 'hicrət', 'hicret', 'хиджр', 'migrat', 'köç')
def islamic_specs(text, lang='en'):
    t = text.lower(); pins = []; hl = set()
    for keys, nm, la, lo, iso in ISL:
        if any(re.search(r'(?<![a-zəöüğışç])' + re.escape(k), t) for k in keys):
            pins.append(dict(name=nm.get(lang, nm['en']), lat=la, lon=lo)); hl.add(iso)
    specs = []
    m = re.search(r'(\d{1,2})\s*(?:-?(?:ci|cı|cu|cü|ji|й|го))?\s*(?:hicri|ah|г\.\s*х|hijri|хиджр)', t) or \
        re.search(r'(?<!\d)(5[7-9]\d|6[0-3]\d)(?!\d)', t)
    if pins:
        if len(pins) == 1 and pins[0]['name'] in ('Madinah', 'Mədinə', 'Медина', 'Makkah', 'Məkkə', 'Мекка', 'Cave of Hira', 'Hira mağarası', 'Пещера Хира'):
            pass
        sp = dict(type='map', hl=sorted(hl), pins=pins, maxzoom=260, zoomfrom=3.0)
        names = [p['name'] for p in pins]
        if any(h in t for h in HIJRA) and len(pins) >= 2 and any(n in ('Makkah', 'Məkkə', 'Мекка') for n in names) and any(n in ('Madinah', 'Mədinə', 'Медина') for n in names):
            sp['route'] = [[21.4225, 39.8262], [22.3, 39.2], [23.4, 39.1], [24.4672, 39.6111]]
        for j, p in enumerate(pins): p['side'] = 'l' if j % 2 else 'r'
        specs.append(sp)
    elif m:
        val = m.group(1) + (' AH' if 'hicri' not in t and 'хиджр' not in t and int(m.group(1)) < 100 else '')
        if lang == 'az' and int(m.group(1)) < 100: val = m.group(1) + ' h.'
        if lang == 'ru' and int(m.group(1)) < 100: val = m.group(1) + ' г.х.'
        specs.append(dict(type='number', value=val, layout='top'))
    else:
        specs.append(dict(type='pattern'))
    return specs

class NurBackground:
    """Фон блока в исламском стиле NUR: карта места / дата / орнамент. Видео — только если в kadr.txt строка «VIDEO: слова»."""
    def __init__(self, epdir, blocks, W, H, lang='en'):
        self.W, self.H, self.lang = W, H, lang
        topic, emap, L = read_kadr(os.path.join(epdir, 'kadr.txt'))
        self.video = set(); self.objs = {}; self.specs = {}
        for i, txt in enumerate(blocks):
            q, sp = L.get(i + 1, ('', []))
            if q.upper().startswith('VIDEO:'): self.video.add(i); continue
            sp = [dict(x, layout='top') if x.get('type') == 'number' else x for x in sp] or islamic_specs(txt, lang)
            for x in sp:
                if x.get('type') == 'map':
                    x.setdefault('maxzoom', 260); x['cap'] = None
                    x.setdefault('ycenter', 0.27 if H > W else 0.3); x.setdefault('pad', 0.4)
            self.specs[i] = sp
    def kinds(self): return {i: '+'.join(x['type'] for x in s) for i, s in self.specs.items()}
    def frame(self, i, t, d):
        if i in self.video or i not in self.specs: return None
        sp = self.specs[i]; k = min(len(sp) - 1, int(t / max(0.1, d) * len(sp)))
        key = (i, k)
        if key not in self.objs:
            for kk in [x for x in self.objs if x[0] < i - 1]: self.objs.pop(kk)
            self.objs[key] = make(sp[k], self.W, self.H, 'nur', self.lang)
        seg = d / len(sp)
        return self.objs[key].frame(t - k * seg, seg)
