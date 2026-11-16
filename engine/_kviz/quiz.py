# -*- coding: utf-8 -*-
"""
VIKTORINA 1080x1920 (shorts/reels), bez avtorskikh prav.
  python3 quiz.py <papka>        (v papke quiz.json)
Tipy voprosov (items[].mode):
  shape  — kontur strany (iso = ADM0_A3, napr. ITA, AZE)
  flag   — flag strany (iso2 = 'az')
  text   — vopros tekstom + 3–4 varianta (options, correct = indeks), source = istochnik
Ozvuchka: ODIN zapros Gemini TTS na ves tekst (stroki razdeleny pustoy strokoy),
potom rezka po pauzam; esli ne sovpalo — ozvuchka gruppami po neskolko strok.
Vykhod: output/<out>_PUBLISH.mp4 (≤ 175 s), COVER.jpg
"""
import os, sys, json, math, subprocess, re, wave, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, '..')
FONTS = os.path.join(ENG, '_stil', 'fonts')
W, H, SR = 1080, 1920, 48000
GOLD = (247, 201, 102); CREAM = (255, 249, 238); ORANGE = (255, 140, 40)
GREEN = (72, 200, 120); RED = (235, 80, 80); NAVY = (14, 18, 44)
LEVEL_COL = {'easy': GREEN, 'medium': (250, 190, 40), 'hard': RED}
SAW = 'ﷺ'

def run(*a, **k):
    return subprocess.run(list(a), check=True, stdin=subprocess.DEVNULL, **k)

def mont(sz, w=800):
    f = ImageFont.truetype(os.path.join(FONTS, 'Montserrat.ttf'), sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
AMIRI = lambda sz: ImageFont.truetype(os.path.join(FONTS, 'Amiri-Regular.ttf'), sz)

def UPP(s, lang):
    return (s.replace('i', 'İ') if lang == 'az' else s).upper()

# ---------- tekst s ﷺ ----------
def tlen(d, s, f):
    parts = s.split(SAW); am = AMIRI(int(f.size * 1.05))
    return sum(d.textlength(p, font=f) for p in parts) + (len(parts) - 1) * d.textlength(SAW, font=am)

def tdraw(d, xy, s, f, fill, anchor='l'):
    x, y = xy; parts = s.split(SAW); am = AMIRI(int(f.size * 1.05))
    if anchor == 'm': x -= tlen(d, s, f) / 2
    for k, p in enumerate(parts):
        d.text((x, y), p, font=f, fill=fill, anchor='lm'); x += d.textlength(p, font=f)
        if k < len(parts) - 1:
            d.text((x, y + f.size * 0.08), SAW, font=am, fill=fill, anchor='lm'); x += d.textlength(SAW, font=am)

def wrap(d, s, f, maxw):
    lines, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if tlen(d, t, f) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def shadow_text(im, xy, s, f, fill, anchor='m', blur=8):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); tdraw(ImageDraw.Draw(sh), (xy[0] + 3, xy[1] + 5), s, f, (0, 0, 0, 220), anchor)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    tdraw(ImageDraw.Draw(im), xy, s, f, fill, anchor)

# ---------- figury stran ----------
CDATA = None
def country(a3):
    global CDATA
    if CDATA is None: CDATA = json.load(open(os.path.join(HERE, 'data', 'countries.json'), encoding='utf-8'))
    return CDATA[a3]

def ring_area(r):
    a = 0
    for i in range(len(r)):
        x1, y1 = r[i]; x2, y2 = r[(i + 1) % len(r)]; a += x1 * y2 - x2 * y1
    return abs(a) / 2

def shape_img(a3, box=780, col=CREAM, glow=ORANGE):
    c = country(a3); rings = c['rings']
    big = max(rings, key=ring_area); ba = ring_area(big)
    bx = [p[0] for p in big]; by = [p[1] for p in big]; cx0, cy0 = (min(bx) + max(bx)) / 2, (min(by) + max(by)) / 2
    keep = []
    for r in rings:
        rx = sum(p[0] for p in r) / len(r); ry = sum(p[1] for p in r) / len(r)
        if ring_area(r) >= ba * 0.004 and abs(rx - cx0) < 25 and abs(ry - cy0) < 18: keep.append(r)
    lat0 = math.radians(sum(p[1] for p in big) / len(big)); kx = math.cos(lat0)
    pts = [(x * kx, -y) for r in keep for x, y in r]
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts); miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    s = box / max(maxx - minx, maxy - miny)
    ww, hh = int((maxx - minx) * s) + 80, int((maxy - miny) * s) + 80
    m = Image.new('L', (ww, hh), 0); d = ImageDraw.Draw(m)
    for r in keep:
        d.polygon([((x * kx - minx) * s + 40, (-y - miny) * s + 40) for x, y in r], fill=255)
    out = Image.new('RGBA', (ww + 160, hh + 160), (0, 0, 0, 0))
    gl = Image.new('RGBA', out.size, glow + (0,)); gm = Image.new('L', out.size, 0); gm.paste(m, (80, 80))
    gl.putalpha(gm.filter(ImageFilter.GaussianBlur(26)).point(lambda v: min(255, int(v * 1.6))))
    out.alpha_composite(gl)
    fill = Image.new('RGBA', (ww, hh), col + (255,)); fill.putalpha(m)
    out.alpha_composite(fill, (80, 80))
    return out

def flag_img(iso2, width=760):
    import cairosvg, urllib.request
    cache = os.path.join(HERE, 'data', 'flags'); os.makedirs(cache, exist_ok=True)
    svg = os.path.join(cache, iso2 + '.svg')
    if not os.path.exists(svg):
        urllib.request.urlretrieve(f'https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{iso2}.svg', svg)
    png = svg[:-4] + f'_{width}.png'
    if not os.path.exists(png): cairosvg.svg2png(url=svg, write_to=png, output_width=width)
    f = Image.open(png).convert('RGBA')
    mask = Image.new('L', f.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, f.width - 1, f.height - 1), 26, fill=255)
    f.putalpha(mask)
    out = Image.new('RGBA', (f.width + 120, f.height + 120), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((60, 75, 60 + f.width, 75 + f.height), 26, fill=(0, 0, 0, 200))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20))); out.alpha_composite(f, (60, 60))
    return out

# ---------- fon ----------
def make_bg(cfg, ep):
    p = os.path.join(ep, '_q', 'bg.png')
    if cfg.get('bg_prompt'):
        if not os.path.exists(p):
            pr = cfg['bg_prompt'] + ' Vertical 9:16, no people, no faces, no animals, no text, no letters. Dark, calm, cinematic, soft light.'
            run('python3', os.path.join(ENG, '_avto', 'img.py'), 'gemini-3.1-flash-image', pr, p, '9:16')
        bg = Image.open(p).convert('RGB'); s = max(W / bg.width, H / bg.height)
        bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
        x = (bg.width - W) // 2; y = (bg.height - H) // 2; bg = bg.crop((x, y, x + W, y + H))
        bg = bg.filter(ImageFilter.GaussianBlur(3)).convert('RGBA')
        dark = Image.new('RGBA', (W, H), (8, 10, 24, 150)); bg.alpha_composite(dark)
        return bg
    # tyomno-siniy gradient + slabaya karta mira
    a = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H)[:, None]; xx = np.linspace(-1, 1, W)[None, :]
    r = np.sqrt(xx ** 2 + (yy - 0.42) ** 2 * 1.4)
    base = np.array(NAVY, np.float32); hi = np.array((34, 44, 96), np.float32)
    k = np.clip(1 - r, 0, 1)[..., None]
    a[:] = base * (1 - k) + hi * k
    return Image.fromarray(a.astype(np.uint8)).convert('RGBA')

# ---------- elementy kadra ----------
def ring(sec, total=5, size=150):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((8, 8, size - 8, size - 8), outline=(255, 255, 255, 60), width=10)
    if sec > 0:
        d.arc((8, 8, size - 8, size - 8), -90, -90 + 360 * sec / total, fill=ORANGE + (255,), width=10)
    f = mont(76, 900); d.text((size / 2, size / 2 + 2), str(sec) if sec > 0 else '', font=f, fill=CREAM + (255,), anchor='mm')
    return im

def header(im, cfg, n=None, total=None, level=None, done=0):
    d = ImageDraw.Draw(im); lang = cfg['lang']
    if cfg.get('brand'):
        f = mont(30, 700); d.text((W - 60, 70), cfg['brand'], font=f, fill=(255, 255, 255, 200), anchor='rm')
    f = mont(34, 800); tdraw(d, (W / 2, 140), UPP(cfg['header'], lang), f, GOLD + (255,), 'm')
    if n:
        f1 = mont(120, 900); f2 = mont(44, 700)
        s1 = str(n); s2 = f' / {total}'
        w1 = d.textlength(s1, font=f1); w2 = d.textlength(s2, font=f2); x0 = (W - w1 - w2) / 2
        d.text((x0, 255), s1, font=f1, fill=CREAM + (255,), anchor='lm'); d.text((x0 + w1 + 6, 275), s2, font=f2, fill=(255, 255, 255, 170), anchor='lm')
        if level:
            lab = UPP(cfg['levels'][level], lang); f3 = mont(30, 800); lw = d.textlength(lab, font=f3) + 44
            d.rounded_rectangle(((W - lw) / 2, 340, (W + lw) / 2, 386), 23, fill=LEVEL_COL[level] + (255,))
            d.text((W / 2, 364), lab, font=f3, fill=(20, 20, 30, 255), anchor='mm')
        y = 425; step = min(46, 900 / max(total, 1)); x0 = W / 2 - step * (total - 1) / 2
        for i in range(total):
            c = GOLD + (255,) if i < done else ((255, 255, 255, 255) if i == done else (255, 255, 255, 70))
            rr = 9 if i == done else 6; d.ellipse((x0 + i * step - rr, y - rr, x0 + i * step + rr, y + rr), fill=c)

def frame_intro(cfg, bg):
    im = bg.copy(); header(im, cfg)
    t1, t2 = cfg['intro_title']; lang = cfg['lang']
    f = mont(124, 900); d = ImageDraw.Draw(im)
    lines = wrap(d, UPP(t1, lang), f, 960)
    while len(lines) > 2: f = mont(f.size - 8, 900); lines = wrap(d, UPP(t1, lang), f, 960)
    y = 760 - (len(lines) - 1) * f.size * 0.6
    for ln in lines: shadow_text(im, (W / 2, y), ln, f, CREAM + (255,)); y += f.size * 1.15
    f2 = mont(60, 800); y += 20
    for ln in wrap(d, UPP(t2, lang), f2, 960): shadow_text(im, (W / 2, y), ln, f2, GOLD + (255,)); y += 76
    if cfg.get('intro_sub'):
        f3 = mont(44, 600); y += 40
        for ln in wrap(d, cfg['intro_sub'], f3, 900): shadow_text(im, (W / 2, y), ln, f3, (255, 255, 255, 230)); y += 58
    return im

def frame_outro(cfg, bg):
    im = bg.copy(); header(im, cfg); d = ImageDraw.Draw(im); lang = cfg['lang']
    f = mont(84, 900); y = 760
    for ln in wrap(d, UPP(cfg['outro_title'], lang), f, 960): shadow_text(im, (W / 2, y), ln, f, CREAM + (255,)); y += 100
    f2 = mont(52, 700); y += 30
    for ln in wrap(d, cfg['outro_sub'], f2, 940): shadow_text(im, (W / 2, y), ln, f2, GOLD + (255,)); y += 70
    lab = UPP(cfg['subscribe'], lang); f3 = mont(44, 800); lw = d.textlength(lab, font=f3) + 120
    d.rounded_rectangle(((W - lw) / 2, 1450, (W + lw) / 2, 1540), 45, fill=(230, 35, 45, 255))
    d.text((W / 2, 1495), lab, font=f3, fill=(255, 255, 255, 255), anchor='mm')
    return im

def frame_visual(cfg, bg, it, n, total, sec, reveal, cache):
    im = bg.copy(); header(im, cfg, n, total, it.get('level'), n - 1 + (1 if reveal else 0))
    lang = cfg['lang']; d = ImageDraw.Draw(im)
    key = (it['mode'], it.get('iso') or it.get('iso2'), reveal)
    if key not in cache:
        if it['mode'] == 'shape': cache[key] = shape_img(it['iso'], col=(GOLD if reveal else CREAM), glow=(ORANGE if not reveal else (255, 190, 60)))
        else: cache[key] = flag_img(it['iso2'])
    v = cache[key]; s = min(860 / v.width, 820 / v.height, 1.0)
    if s < 1: v = v.resize((int(v.width * s), int(v.height * s)), Image.LANCZOS)
    im.alpha_composite(v, (int((W - v.width) / 2), int(980 - v.height / 2)))
    if reveal:
        f = mont(40, 700); d.text((W / 2, 1480), UPP(cfg['answer_label'], lang), font=f, fill=(255, 255, 255, 190), anchor='mm')
        f2 = mont(96, 900); a = UPP(it['answer'], lang)
        while tlen(d, a, f2) > 980: f2 = mont(f2.size - 6, 900)
        shadow_text(im, (W / 2, 1580), a, f2, GOLD + (255,))
    else:
        r = ring(sec); im.alpha_composite(r, (int((W - r.width) / 2), 1490))
    return im

def frame_text(cfg, bg, it, n, total, sec, reveal):
    im = bg.copy(); header(im, cfg, n, total, it.get('level'), n - 1 + (1 if reveal else 0))
    d = ImageDraw.Draw(im); lang = cfg['lang']
    f = mont(60, 800); lines = wrap(d, it['q'], f, 940)
    while len(lines) > 5: f = mont(f.size - 4, 800); lines = wrap(d, it['q'], f, 940)
    lh = int(f.size * 1.28); y = 640 - (len(lines) - 1) * lh / 2
    for ln in lines: shadow_text(im, (W / 2, y), ln, f, CREAM + (255,)); y += lh
    opts = it['options']; fo = mont(50, 750); top = 900; bh = 120; gap = 34
    for i, o in enumerate(opts):
        y0 = top + i * (bh + gap); box = (90, y0, W - 90, y0 + bh)
        ok = reveal and i == it['correct']; bad = reveal and i != it['correct']
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle(box, 30, fill=(GREEN + (235,)) if ok else ((20, 24, 50, 120) if bad else (20, 24, 50, 200)),
                             outline=(GOLD + (255,)) if ok else (255, 255, 255, 90), width=4)
        im.alpha_composite(lay); d = ImageDraw.Draw(im)
        letter = 'ABCD'[i] if lang != 'ru' else 'АБВГ'[i]
        d.ellipse((115, y0 + 22, 191, y0 + 98), fill=(GOLD + (255,)) if not bad else (255, 255, 255, 60))
        d.text((153, y0 + 61), letter, font=mont(44, 900), fill=(20, 20, 30, 255), anchor='mm')
        ff = fo; ol = wrap(d, o, ff, 760)
        while len(ol) > 2 and ff.size > 30: ff = mont(ff.size - 4, 750); ol = wrap(d, o, ff, 760)
        yy = y0 + bh / 2 - (len(ol) - 1) * ff.size * 0.62
        for ln in ol:
            tdraw(d, (220, yy), ln, ff, (255, 255, 255, 120) if bad else (CREAM + (255,))); yy += ff.size * 1.24
    yb = top + len(opts) * (bh + gap) + 20
    if reveal:
        if it.get('source'):
            fs = mont(36, 600)
            for ln in wrap(d, it['source'], fs, 900): tdraw(d, (W / 2, yb + 40), ln, fs, GOLD + (255,), 'm'); yb += 50
    else:
        r = ring(sec); im.alpha_composite(r, (int((W - r.width) / 2), int(yb)))
    return im

# ---------- zvuk ----------
def read_audio(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True, stdin=subprocess.DEVNULL)
    return np.frombuffer(r.stdout, np.float32).copy()

def tone(freqs, dur, decay=8.0, vol=0.5):
    t = np.arange(int(SR * dur)) / SR; s = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    return (s * np.exp(-decay * t) * vol).astype(np.float32)

def sfx_tick(last=False): return tone([1800 if last else 1200], 0.06, 60, 0.35)
def sfx_ding(): return np.concatenate([tone([880, 1760], 0.25, 9, 0.35), tone([1320, 2640], 0.6, 6, 0.35)])
def sfx_whoosh():
    n = int(SR * 0.45); x = np.random.default_rng(1).standard_normal(n).astype(np.float32)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2; k = np.linspace(0.02, 0.3, n)
    y = np.zeros(n, np.float32); acc = 0.0
    for i in range(n): acc += k[i] * (x[i] - acc); y[i] = acc
    return (y * env * 0.5).astype(np.float32)
def sfx_boom(): t = np.arange(int(SR * 1.2)) / SR; return (np.sin(2 * np.pi * (55 + 40 * np.exp(-6 * t)) * t) * np.exp(-3.5 * t) * 0.8).astype(np.float32)

def put(buf, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    n = min(len(clip), len(buf) - i); buf[i:i + n] += clip[:n] * gain

# ---------- ozvuchka ----------
def tts(cfg, text, out):
    model = cfg.get('tts_model', 'gemini-2.5-flash-preview-tts')
    run('python3', os.path.join(ENG, '_avto', 'tts.py'), model, cfg['voice'], cfg['style'], text, out)

def split_by_silence(wav, n_expect):
    a = read_audio(wav); fr = int(SR * 0.02); e = np.sqrt(np.mean(a[:len(a) // fr * fr].reshape(-1, fr) ** 2, 1))
    thr = max(1e-3, np.percentile(e, 30) * 1.5, e.max() * 0.02)
    silent = e < thr
    # vse kuski rechi s pauzoy >= 0.16 s
    g = 8; segs = []; start = None; run_s = 0; last = 0
    for i, s in enumerate(silent):
        if not s:
            if start is None: start = i
            run_s = 0; last = i
        else:
            run_s += 1
            if start is not None and run_s == g: segs.append([start, last]); start = None
    if start is not None: segs.append([start, last])
    segs = [s for s in segs if (s[1] - s[0]) * 0.02 > 0.12]
    if len(segs) < n_expect: return None
    while len(segs) > n_expect:   # skleivaem samye korotkie pauzy (vnutri stroki)
        gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]
        k = int(np.argmin(gaps)); segs[k] = [segs[k][0], segs[k + 1][1]]; del segs[k + 1]
    gaps = sorted(segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1))
    out = []
    for s0, s1 in segs:
        i0 = max(0, s0 * fr - int(0.06 * SR)); i1 = min(len(a), (s1 + 1) * fr + int(0.12 * SR)); out.append(a[i0:i1])
    return out

_WM = None
def whisper():
    global _WM
    if _WM is None:
        from faster_whisper import WhisperModel
        _WM = WhisperModel('small', device='cpu', compute_type='int8')
    return _WM

def norm_words(s):
    s = s.lower().replace('ё', 'е').replace('\ufdfa', ' ')
    return [w[:5] for w in re.findall(r'\w+', s)]

def split_by_words(wav, lines, lang):
    """Rezhem po vsem pauzam na melkie kuski, raspoznaem kazhdyy kusok otdelno,
    zatem optimalno (DP) raskladyvaem kuski po strokam teksta."""
    import difflib
    a = read_audio(wav); fr = int(SR * 0.02)
    e = np.sqrt(np.mean(a[:len(a) // fr * fr].reshape(-1, fr) ** 2, 1))
    thr = max(1e-3, np.percentile(e, 30) * 1.5, e.max() * 0.02); silent = e < thr
    ch = []; start = None; run_s = 0; last = 0
    for i, sl in enumerate(silent):
        if not sl:
            if start is None: start = i
            run_s = 0; last = i
        else:
            run_s += 1
            if start is not None and run_s == 9: ch.append([start, last]); start = None
    if start is not None: ch.append([start, last])
    ch = [c for c in ch if (c[1] - c[0]) * 0.02 > 0.1]
    m, n = len(ch), len(lines)
    if m < n: return None
    texts = []
    for c0, c1 in ch:
        x = a[max(0, c0 * fr - 1600):(c1 + 1) * fr + 3200][::3].copy()
        sg, _ = whisper().transcribe(x, language=lang, vad_filter=False, condition_on_previous_text=False, beam_size=1)
        texts.append(norm_words(' '.join(q.text for q in sg)))
    L = [norm_words(x) for x in lines]
    def sim(i, j0, j1):
        g = sum(texts[j0:j1], []); 
        if not g: return 0.0
        return difflib.SequenceMatcher(None, L[i], g, autojunk=False).ratio() * max(len(L[i]), 1)
    NEG = -1e9; best = [[NEG] * (m + 1) for _ in range(n + 1)]; arg = [[0] * (m + 1) for _ in range(n + 1)]; best[0][0] = 0
    for i in range(1, n + 1):
        for j in range(i, m - (n - i) + 1):
            for k in range(i - 1, j):
                if best[i - 1][k] == NEG: continue
                v = best[i - 1][k] + sim(i - 1, k, j)
                if v > best[i][j]: best[i][j] = v; arg[i][j] = k
    if best[n][m] == NEG: return None
    cuts = []; j = m
    for i in range(n, 0, -1): k = arg[i][j]; cuts.append((k, j)); j = k
    cuts.reverse()
    tot = sum(len(x) for x in L); score = best[n][m] / max(1, tot)
    out = []
    for i, (k, j) in enumerate(cuts):
        s0 = ch[k][0]; s1 = ch[j - 1][1]
        i0 = max(0, s0 * fr - int(0.06 * SR)); i1 = min(len(a), (s1 + 1) * fr + int(0.15 * SR)); out.append(a[i0:i1].copy())
        got = ' '.join(sum(texts[k:j], []))
        r = difflib.SequenceMatcher(None, L[i], sum(texts[k:j], []), autojunk=False).ratio()
        if r < 0.35: print(f'» VNIMANIE stroka {i}: «{lines[i][:40]}» ~ «{got[:40]}» ({r:.2f})')
    print(f'» stroki razlozheny po kuskam: {m} kuskov, kachestvo {score:.2f}')
    if score < 0.5: return None
    return out

def voice_lines(cfg, ep, lines):
    vd = os.path.join(ep, '_q', 'voice'); os.makedirs(vd, exist_ok=True)
    cache = os.path.join(vd, 'segs.npz')
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=True)
        if list(z['lines']) == lines: print('» ozvuchka iz kesha'); return list(z['segs'])
    segs = None
    for att in range(2):
        w = os.path.join(vd, f'full_{att}.wav')
        if not os.path.exists(w): tts(cfg, '\n\n'.join(lines), w)
        segs = split_by_words(w, lines, cfg['lang'])
        if segs: break
    if not segs:
        segs = []; G = 6
        for g in range(0, len(lines), G):
            part = lines[g:g + G]; w = os.path.join(vd, f'grp_{g}.wav')
            if not os.path.exists(w): tts(cfg, '\n\n'.join(part), w)
            s = split_by_words(w, part, cfg['lang']) or split_by_silence(w, len(part))
            if not s: raise SystemExit(f'ozvuchka: ne razrezat gruppu {g}')
            segs += s
    np.savez(cache, lines=np.array(lines, dtype=object), segs=np.array(segs, dtype=object))
    return segs

def check_voice(cfg, segs, lines):
    m = whisper()
    a = np.concatenate([np.concatenate([s, np.zeros(int(SR * 0.4), np.float32)]) for s in segs])
    a16 = a[::3].astype(np.float32)
    seg, _ = m.transcribe(a16, language=cfg['lang'], vad_filter=False)
    got = ' '.join(s.text for s in seg).lower()
    norm = lambda s: re.findall(r'\w+', s.lower())
    exp = norm(' '.join(lines)); g = norm(got)
    import difflib
    r = difflib.SequenceMatcher(None, exp, g).ratio()
    print(f'» proverka ozvuchki: sovpadenie {r:.2f}')
    if r < 0.5: raise SystemExit('ozvuchka ne sovpadaet s tekstom — pereozvuchit')

# ---------- sborka ----------
def build(ep):
    cfg = json.load(open(os.path.join(ep, 'quiz.json'), encoding='utf-8'))
    items = cfg['items']; total = len(items); lang = cfg['lang']
    lines = [cfg['intro_voice']]
    for it in items: lines += [it['q_voice'], it['a_voice']]
    lines.append(cfg['outro_voice'])
    segs = voice_lines(cfg, ep, lines)
    check_voice(cfg, segs, lines)
    bg = make_bg(cfg, ep)
    fd = os.path.join(ep, '_q', 'frames'); shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
    seq = []; ev = []; t = 0.0; cache = {}
    def add(im, dur):
        nonlocal t
        p = os.path.join(fd, f'{len(seq):04d}.png'); im.convert('RGB').save(p); seq.append((p, dur)); t += dur
    dl = lambda s: len(s) / SR
    # intro
    ev.append(('boom', 0.0)); ev.append(('v', 0.25, segs[0]))
    add(frame_intro(cfg, bg), max(3.2, dl(segs[0]) + 0.9))
    CD = cfg.get('countdown', 5)
    for k, it in enumerate(items):
        qv, av = segs[1 + 2 * k], segs[2 + 2 * k]; n = k + 1
        ev.append(('whoosh', t)); ev.append(('v', t + 0.15, qv))
        read = dl(qv) + 0.35
        mk = (lambda s, r: frame_text(cfg, bg, it, n, total, s, r)) if it['mode'] == 'text' else (lambda s, r: frame_visual(cfg, bg, it, n, total, s, r, cache))
        if it['mode'] == 'text':
            add(mk(CD, False), read)  # chitaem vopros, kolco polnoe
        else:
            read = max(read, 0.6); add(mk(CD, False), read)
        for s in range(CD, 0, -1):
            ev.append(('tick', t, s == 1)); add(mk(s, False), 1.0)
        ev.append(('ding', t)); ev.append(('v', t + 0.25, av))
        add(mk(0, True), dl(av) + (1.6 if it['mode'] == 'text' else 1.0))
    ev.append(('v', t + 0.3, segs[-1]))
    add(frame_outro(cfg, bg), dl(segs[-1]) + 1.6)
    dur = t
    print(f'» dlitelnost {dur:.1f} s')
    if dur > 178: raise SystemExit(f'SLISHKOM DLINNO: {dur:.1f} s (nado ≤ 175) — ubrat voprosy')
    # zvuk
    vbuf = np.zeros(int(SR * (dur + 0.5)), np.float32); sbuf = np.zeros_like(vbuf)
    for e in ev:
        if e[0] == 'v': put(vbuf, e[2], e[1])
        elif e[0] == 'tick': put(sbuf, sfx_tick(e[2]), e[1])
        elif e[0] == 'ding': put(sbuf, sfx_ding(), e[1])
        elif e[0] == 'whoosh': put(sbuf, sfx_whoosh(), e[1], 0.6)
        elif e[0] == 'boom': put(sbuf, sfx_boom(), e[1])
    mus = np.zeros_like(vbuf)
    religion = cfg.get('religion') or any(k in cfg.get('out', '').upper() for k in ('AYAT', 'RUHUN'))
    if religion: print('» religiya: BEZ MUZYKI (pravilo polzovatelya)')
    if cfg.get('music') and os.path.exists(cfg['music']) and not religion:
        m = read_audio(cfg['music'])
        while len(m) < len(mus): m = np.concatenate([m, m])
        mus = m[:len(mus)] * 0.16
        env = np.abs(vbuf); k = int(SR * 0.25)
        env = np.convolve(env, np.ones(k) / k, 'same'); duck = 1 - 0.6 * np.clip(env / 0.05, 0, 1)
        mus *= duck
        fade = int(SR * 2); mus[-fade:] *= np.linspace(1, 0, fade)
    vpk = np.abs(vbuf).max() or 1; vbuf *= 0.85 / vpk
    mix = vbuf + sbuf * 0.8 + mus
    mix = np.tanh(mix * 1.1) * 0.95
    wav = os.path.join(ep, '_q', 'audio.wav')
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    lst = os.path.join(fd, 'list.txt')
    with open(lst, 'w') as f:
        for p, d in seq: f.write(f"file '{p}'\nduration {d:.3f}\n")
        f.write(f"file '{seq[-1][0]}'\n")
    os.makedirs(os.path.join(ep, 'output'), exist_ok=True)
    out = os.path.join(ep, 'output', cfg['out'] + '_PUBLISH.mp4')
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav,
        '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-tune', 'stillimage',
        '-c:a', 'aac', '-b:a', '192k', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-shortest', '-movflags', '+faststart', out)
    # oblozhka: esli net cover.json — kadr-vopros
    if os.path.exists(os.path.join(ep, 'cover.json')):
        run('python3', os.path.join(ENG, '_avto', 'cover.py'), ep)
        shutil.copy(os.path.join(ep, 'OBLOZHKA_1080x1920.jpg'), os.path.join(ep, 'output', cfg['out'] + '_cover.jpg'))
    else:
        cover_quiz(cfg, bg, items, os.path.join(ep, 'output', cfg['out'] + '_cover.jpg'), cache)
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True)
    print('GOTOVO', out, f'{os.path.getsize(out) / 1e6:.1f} MB', f'{float(r.stdout):.1f} s')

def cover_quiz(cfg, bg, items, out, cache):
    im = bg.copy(); lang = cfg['lang']; d = ImageDraw.Draw(im)
    it = items[-1] if items[-1]['mode'] != 'text' else None
    if it:
        v = shape_img(it['iso']) if it['mode'] == 'shape' else flag_img(it['iso2'])
        s = min(900 / v.width, 760 / v.height, 1.0); v = v.resize((int(v.width * s), int(v.height * s)))
        im.alpha_composite(v, (int((W - v.width) / 2), int(1000 - v.height / 2)))
        f = mont(260, 900); shadow_text(im, (W / 2, 1000), '?', f, (255, 255, 255, 235))
    cl = cfg.get('cover_lines') or [cfg['intro_title'][0], cfg['intro_title'][1]]
    f = mont(110, 900); y = 330
    for ln in wrap(d, UPP(cl[0], lang), f, 980): shadow_text(im, (W / 2, y), ln, f, CREAM + (255,)); y += 125
    f2 = mont(70, 900); y = 1560
    for ln in wrap(d, UPP(cl[1], lang), f2, 980): shadow_text(im, (W / 2, y), ln, f2, GOLD + (255,)); y += 86
    im.convert('RGB').save(out, quality=92)

if __name__ == '__main__':
    build(os.path.abspath(sys.argv[1]))
