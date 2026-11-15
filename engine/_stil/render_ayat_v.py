# -*- coding: utf-8 -*-
"""Причины ниспослания — стиль «NUR» (вертикальный 9:16, 1080x1920, 25 fps, для Shorts / Reels / TikTok).
Видео-фон на весь экран (тёплый, тёмный, медленное приближение), золотая пыль, мягкий свет,
крупный текст по предложениям (слова загораются вслед за голосом, текущее слово золотое),
золотой арабский аят, кнопки ПОДПИСАТЬСЯ / ПОДЕЛИТЬСЯ, золотая полоса прогресса.
Запуск: python render_nur_v.py "<папка серии>" [--preview]
В папке: ssenari.txt ([1]..[12]) или Ssenari_ozvucka.txt (абзацы), meta.json, voice\\*.wav (самый новый),
_nur\\ar_N.png (арабский текст блока N), kadr.txt (поиск видео-фона, скачивает footage.py)."""
import sys, os, re, json, math, random, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
for _tp in (os.path.join(HERE, '..', '_toolkit'),):
    if os.path.exists(os.path.join(_tp, 'infographics.py')): sys.path.insert(0, os.path.abspath(_tp)); break
import infographics as IG
W, H, FPS = 1080, 1920, 25
GOLD = (247, 201, 102); CREAM = (255, 249, 238); RED = (214, 40, 52)
XF = 0.6
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = 'ffmpeg'

def log(*a): print('»', *a, flush=True)

def _find(name, extra=()):
    for c in (os.path.join(HERE, 'fonts', name),) + tuple(extra):
        if os.path.exists(c): return c
    raise SystemExit('Нет шрифта ' + name)
P_SERIF = _find('CormorantGaramond-Italic[wght].ttf', (r'D:\gemini\az\RuhunQidasi\Arxiv_stil\fonts\CormorantGaramond-Italic[wght].ttf',))
P_MONT = _find('Montserrat.ttf', (r'D:\gemini\_doc_engine\fonts\Montserrat.ttf',))
P_AMIRI = _find('Amiri-Regular.ttf', (r'D:\gemini\az\RuhunQidasi\Arxiv_stil\fonts\Amiri-Regular.ttf',))
_FC = {}
def _var(path, size, w):
    k = (path, size, w)
    if k not in _FC:
        f = ImageFont.truetype(path, size)
        if w:
            try: f.set_variation_by_axes([w])
            except Exception: pass
        _FC[k] = f
    return _FC[k]
SERIF = lambda s: _var(P_SERIF, s, 620)
MONT = lambda s, w=700: _var(P_MONT, s, w)
FA = lambda s: _var(P_AMIRI, int(s * 0.9), None)

# ---------------- input ----------------
def find_audio(d):
    c = []
    for p in (os.path.join(d, 'voice'), d, os.path.join(d, 'audio')):
        c += [f for f in glob.glob(os.path.join(p, '*')) if f.lower().endswith(('.wav', '.mp3', '.m4a', '.flac', '.ogg'))]
    if not c: raise SystemExit('Нет озвучки: положите .wav в папку voice')
    return max(c, key=os.path.getmtime)

def read_ep(d):
    f = os.path.join(d, 'Ssenari_ozvucka.txt')
    if not os.path.exists(f): f = os.path.join(d, 'ssenari.txt')
    body = open(f, encoding='utf-8-sig').read().replace('\r', '').split('------')[0]
    if re.search(r'^\[\d+\]\s*$', body, re.M):
        blocks = [re.sub(r'\s+', ' ', m.group(2)).strip() for m in re.finditer(r'\[(\d+)\]\n([\s\S]*?)(?=\n\s*\n|\n\[|$)', body)]
    else:
        paras = [re.sub(r'\s+', ' ', p).strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
        blocks = [p for p in paras if not (p.startswith('[') and p.endswith(']'))]
    meta = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8-sig'))
    return blocks, meta, find_audio(d)

def audio_info(a):
    e = subprocess.run([FF, '-hide_banner', '-nostats', '-i', a, '-af', 'silencedetect=n=-35dB:d=0.35', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace').stderr
    dm = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', e)
    return int(dm.group(1)) * 3600 + int(dm.group(2)) * 60 + float(dm.group(3))

def norm(w): return re.sub(r'[\W_]', '', w.lower().replace('ё', 'е'))
def find_model_dir():
    for c in (os.path.join(HERE, '.models', 'faster-whisper-small'), r'D:\gemini\azcity\.models\faster-whisper-small'):
        if os.path.exists(os.path.join(c, 'model.bin')): return c
def asr_words(voice, epdir, lang):
    cache = os.path.join(epdir, '_nur', 'asr_words.json')
    if os.path.exists(cache): return json.load(open(cache, encoding='utf-8'))
    from faster_whisper import WhisperModel
    log('Распознавание речи (несколько минут)...')
    m = WhisperModel(find_model_dir() or 'small', device='cpu', compute_type='int8', download_root=os.path.join(HERE, '.models'))
    raw = subprocess.run([FF, '-v', 'error', '-i', voice, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.float32), language=lang, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
    out = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in (s.words or [])]
    os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(out, open(cache, 'w', encoding='utf-8'), ensure_ascii=False)
    return out
def align(blocks, voice, epdir, dur, lang):
    import difflib
    words = [w for b in blocks for w in b.split()]
    try: aw = asr_words(voice, epdir, lang)
    except Exception as e: log('ASR не удалось (%s)' % e); aw = []
    A = [norm(w) for w in words]; B = [norm(w[0]) for w in aw]; t = [None] * len(words)
    if aw:
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                for k in range(i2 - i1): t[i1 + k] = aw[j1 + k][1]
            elif op == 'replace':
                for k in range(i2 - i1):
                    jj = j1 + int(k * (j2 - j1) / max(1, i2 - i1))
                    if jj < j2: t[i1 + k] = aw[jj][1]
    known = [(i, x) for i, x in enumerate(t) if x is not None] or [(0, 0.3), (len(words) - 1, dur - 0.8)]
    xs = np.array([k for k, _ in known], float); ys = np.maximum.accumulate(np.array([v for _, v in known], float))
    full = np.interp(np.arange(len(words)), xs, ys)
    log('Совпадение текста и голоса: %d / %d слов' % (sum(x is not None for x in t), len(words)))
    res = []; k = 0
    for b in blocks:
        n = len(b.split()); res.append(full[k:k + n]); k += n
    return res

class VideoReader:
    def __init__(self, path):
        self.n = W * H * 3; self.last = None
        vf = 'scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos,crop=%d:%d,fps=%d' % (W, H, W, H, FPS)
        self.p = subprocess.Popen([FF, '-v', 'error', '-stream_loop', '-1', '-i', path, '-an', '-vf', vf, '-f', 'rawvideo',
                                   '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.n * 2)
    def next(self):
        b = self.p.stdout.read(self.n)
        if len(b) == self.n: self.last = Image.frombytes('RGB', (W, H), b)
        return self.last if self.last is not None else Image.new('RGB', (W, H))
    def close(self):
        try: self.p.kill(); self.p.stdout.close()
        except Exception: pass

# ---------------- layers ----------------
def vignette_arr():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.6)) ** 2)
    v = np.clip(1.1 - 0.8 * r ** 1.7, 0.15, 1.0)
    # тёмные полосы сверху и снизу (под интерфейс Shorts)
    v *= np.clip(0.35 + y / 260.0, 0, 1) * np.clip(0.35 + (H - y) / 380.0, 0, 1)
    return v[..., None]
def glow_img():
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([-W * 0.5, -H * 0.25, W * 0.7, H * 0.45], fill=255)
    g = g.filter(ImageFilter.GaussianBlur(200))
    return np.asarray(g, np.float32)[..., None] / 255.0 * np.array([255, 170, 90], np.float32)
VIG = GLOW = None

def sprite(r):
    s = Image.new('RGBA', (r * 6, r * 6), (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse([r * 2, r * 2, r * 4, r * 4], fill=GOLD + (255,))
    return s.filter(ImageFilter.GaussianBlur(r * 0.9))
class Dust:
    def __init__(self, n=80, seed=7):
        R = random.Random(seed); self.sp = {r: sprite(r) for r in (2, 3, 4, 6)}
        self.p = [[R.uniform(0, W), R.uniform(0, H), R.choice((2, 2, 3, 3, 4, 6)), R.uniform(8, 26), R.uniform(-6, 6), R.uniform(0, 6.28), R.uniform(0.25, 0.8)] for _ in range(n)]
    def draw(self, im, t):
        for x0, y0, r, vy, vx, ph, a in self.p:
            x = (x0 + vx * t + 12 * math.sin(t * 0.4 + ph)) % W; y = (y0 - vy * t) % H
            al = a * (0.55 + 0.45 * math.sin(t * 1.3 + ph)); s = self.sp[r]
            sx, sy = int(x - s.width / 2), int(y - s.height / 2)
            if 0 <= sx < W - s.width and 0 <= sy < H - s.height:
                tmp = s.copy(); tmp.putalpha(s.split()[3].point(lambda v: int(v * al))); im.alpha_composite(tmp, (sx, sy))

def grade(fr, p, t, i):
    p = min(1.2, max(0.0, p)); z = 1.0 + 0.08 * p; cw, ch = W / z, H / z
    ox = (W - cw) / 2 + (1 if i % 2 else -1) * 14 * p; oy = (H - ch) / 2
    ox = min(max(0.0, ox), W - cw); oy = min(max(0.0, oy), H - ch)
    fr = fr.resize((W, H), Image.BILINEAR, box=(ox, oy, ox + cw, oy + ch))
    a = np.asarray(fr, np.float32); lum = a.mean(axis=2, keepdims=True)
    a = (a * 0.72 + lum * 0.28) * np.array([1.06, 0.97, 0.84], np.float32) * 0.6 * VIG
    a = a + GLOW * (0.16 + 0.08 * math.sin(t * 0.35 + i))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def fallback_bg():
    a = np.asarray(Image.new('RGB', (W, H), (18, 12, 8)), np.float32) * VIG + GLOW * 0.3
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------------- text ----------------
def sentences(words):
    out = []; cur = []
    for k, w in enumerate(words):
        cur.append(k)
        if (re.search(r'[.!?…]["”»)]*$', w) and len(cur) >= 4) or (re.search(r'[,:;]["”»)]*$', w) and len(cur) >= 8) or len(cur) >= 14: out.append(cur); cur = []
    if cur:
        if out and len(cur) < 4: out[-1] += cur
        else: out.append(cur)
    return out
def wrap(dr, words, f, maxw):
    lines, cur = [], []
    for w in words:
        if cur and dr.textlength(' '.join(cur + [w]), font=f) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    if cur: lines.append(cur)
    return lines
LANG = ['ru']
def UP(s): return (s.replace('i', 'İ') if LANG[0] == 'az' else s).upper()
def spaced(s): return '  '.join(UP(s)) if len(s) < 12 else ' '.join(UP(s))

TX = {'ru': ('ПОДПИСАТЬСЯ', 'ПОДЕЛИСЬ — НАГРАДА И ТЕБЕ', 'ПРИЧИНЫ НИСПОСЛАНИЯ'),
      'en': ('SUBSCRIBE', 'SHARE IT — SHARE THE REWARD', 'AYAT LUMA'),
      'az': ('ABUNƏ OL', 'PAYLAŞ — SAVABA ORTAQ OL', 'RUHUN QİDASI')}
TY = 940          # центр текста

class Block:
    def __init__(self, i, n, text, bm, epdir):
        self.i, self.text = i, text
        self.words = text.split(); self.sents = sentences(self.words)
        label = (bm.get('label') or '').strip()
        if i == 0: kind = 'title'
        elif bm.get('cta') or i == n - 1: kind = 'share'
        elif re.search(r'ПОДПИШ|ABUN|SUBSCRIB', label.upper()) or re.search(r'подпиш|abunə ol|subscribe', text.lower()): kind = 'subscribe'
        else: kind = 'story'
        self.ar = None
        for sub in ('_nur', '_arxiv'):
            arp = os.path.join(epdir, sub, 'ar_%d.png' % (i + 1))
            if os.path.exists(arp) and kind in ('story', 'share'):
                a = Image.open(arp).convert('RGBA'); al = a.split()[3]
                hgt = 150 if a.height > 200 else 110
                al = al.resize((max(1, int(a.width * hgt / a.height)), hgt), Image.LANCZOS)
                if al.width > 960: al = al.resize((960, max(1, int(al.height * 960 / al.width))), Image.LANCZOS)
                g = Image.new('RGBA', al.size, GOLD + (0,)); g.putalpha(al)
                gl = Image.new('RGBA', (g.width + 120, g.height + 120), (0, 0, 0, 0)); gl.paste(g, (60, 60), g)
                gl = gl.filter(ImageFilter.GaussianBlur(16)); o = Image.new('RGBA', gl.size, (0, 0, 0, 0))
                o.alpha_composite(gl); o.alpha_composite(gl); o.alpha_composite(g, (60, 60)); self.ar = o
                if kind == 'story': kind = 'ayah'
                break
        self.kind, self.label, self.ref = kind, label, (bm.get('ref') or '').strip()
        self.cache = {}
        st = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
        ly = 560 if kind != 'ayah' else 400
        if label and kind != 'subscribe':
            f = MONT(28, 650); s = spaced(label)
            while d.textlength(s, font=f) > 860 and f.size > 18: f = MONT(f.size - 2, 650)
            tw = d.textlength(s, font=f)
            d.text((W / 2, ly), s, font=f, fill=GOLD + (235,), anchor='mm')
            d.line([(W / 2 - tw / 2 - 80, ly), (W / 2 - tw / 2 - 20, ly)], fill=GOLD + (170,), width=2)
            d.line([(W / 2 + tw / 2 + 20, ly), (W / 2 + tw / 2 + 80, ly)], fill=GOLD + (170,), width=2)
        if self.ref and kind != 'share':
            d.text((W / 2, 1370), '— ' + self.ref + ' —', font=MONT(26, 600), fill=GOLD + (200,), anchor='mm')
        self.static = st
        self.size = 70 if kind == 'title' else 60
        self.ty = {'ayah': 1000, 'subscribe': 820, 'share': 860}.get(kind, TY)

    def text_layer(self, si, k_in, cur):
        key = (si, k_in, cur)
        if key in self.cache: return self.cache[key]
        if len(self.cache) > 40: self.cache.clear()
        idx = self.sents[si]; ws = [self.words[j] for j in idx]
        tmp = ImageDraw.Draw(Image.new('RGBA', (8, 8))); size = self.size
        while True:
            f = MONT(size, 850); lines = wrap(tmp, [UP(x) for x in ws], f, 950)
            if len(lines) <= (5 if self.kind != 'ayah' else 4) or size <= 44: break
            size -= 4
        lh = int(size * 1.25); hh = lh * len(lines) + 40
        lay = Image.new('RGBA', (W, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        sh = Image.new('RGBA', (W, hh), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        n = 0
        for li, ln in enumerate(lines):
            lw = d.textlength(' '.join(ln), font=f); x = (W - lw) / 2; y = 20 + li * lh
            for w in ln:
                w = UP(w)
                j = idx[n]; n += 1
                fw = FA(size) if '\ufdfa' in w else f
                col = (GOLD + (255,) if (j == k_in - 1 and cur) else CREAM + (255,)) if j < k_in else (255, 255, 255, 62)
                ds.text((x + 3, y + 4), w, font=fw, fill=(0, 0, 0, 210 if j < k_in else 60))
                d.text((x, y), w, font=fw, fill=col)
                x += d.textlength(w, font=fw) + d.textlength(' ', font=f)
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        out = Image.new('RGBA', (W, hh), (0, 0, 0, 0)); out.alpha_composite(sh); out.alpha_composite(sh); out.alpha_composite(lay)
        if cur: out.alpha_composite(Image.eval(lay.filter(ImageFilter.GaussianBlur(10)), lambda v: int(v * 0.35)))
        self.cache[key] = out
        return out

def pill(im, cx, cy, text, bg, fg, scale=1.0, bell=False):
    f = MONT(int(36 * scale), 800); d = ImageDraw.Draw(im); tw = d.textlength(text, font=f)
    w = tw + (115 if bell else 75) * scale; h = 84 * scale; x0, y0 = cx - w / 2, cy - h / 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 6, y0 + 10, x0 + w + 6, y0 + h + 10], int(h / 2), fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(h / 2), fill=bg)
    tx = x0 + (78 if bell else 37) * scale
    if bell:
        bx, by, r = x0 + 42 * scale, cy, 16 * scale
        d.pieslice([bx - r, by - r * 1.3, bx + r, by + r * 0.9], 180, 360, fill=fg)
        d.rectangle([bx - r, by - r * 0.2, bx + r, by + r * 0.6], fill=fg)
        d.ellipse([bx - r * 0.3, by + r * 0.55, bx + r * 0.3, by + r * 1.1], fill=fg)
    d.text((tx, cy), text, font=f, fill=fg, anchor='lm')

def chrome(meta, lang):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    s = meta.get('series', '') or TX[lang][2]
    f = MONT(26, 650)
    d.text((W / 2, 250), UP(s), font=f, fill=GOLD + (220,), anchor='mm')
    d.line([(W / 2 - 60, 285), (W / 2 + 60, 285)], fill=GOLD + (150,), width=2)
    return c

# ---------------- render ----------------
def render(epdir, preview=False):
    global VIG, GLOW
    epdir = os.path.abspath(epdir)
    kf = os.path.join(epdir, 'kadr.txt')
    tool = next((c for c in (os.path.join(HERE, '..', '_toolkit', 'footage.py'),) if os.path.exists(c)), None)
    blocks, meta, voice = read_ep(epdir)
    lang = meta.get('lang', 'ru') if meta.get('lang', 'ru') in TX else 'ru'
    LANG[0] = lang
    NB = IG.NurBackground(epdir, blocks, W, H, lang)
    log('Фон блоков: ' + ', '.join('%d:%s' % (k + 1, v) for k, v in sorted(NB.kinds().items())))
    if NB.video and os.path.exists(kf) and tool:
        log('Видео (только строки VIDEO:) ...')
        subprocess.run([sys.executable, tool, epdir, '--per', '1', '--out', os.path.join('_nur', 'video'), '--nopeople', '--size', '%dx%d' % (W, H), '--only-video'])
    VIG = vignette_arr(); GLOW = glow_img()
    dur = audio_info(voice)
    WT = align(blocks, voice, epdir, dur, lang)
    n = len(blocks)
    # голос сначала прочитал название серии (старые серии) — показываем его крупно как первое предложение
    t0 = float(WT[0][0]) if len(WT[0]) else 0.0
    if t0 > 2.5 and meta.get('title'):
        tw = meta['title'].split()
        if not re.search(r'[.!?…]["”»)]*$', tw[-1]): tw[-1] += '.'
        if len(tw) < 4: tw = ['—'] * (4 - len(tw)) + tw
        blocks[0] = ' '.join(tw) + ' ' + blocks[0]
        WT[0] = np.concatenate([np.linspace(0.15, max(0.5, t0 - 0.5), len(tw)), WT[0]])
        log('Название озвучено в начале — добавлено на экран')
    edges = [0.0] + [max(0.0, WT[i][0] - 0.4) for i in range(1, n)] + [dur + 1.2]
    B = [Block(i, n, blocks[i], meta.get('blocks', {}).get(str(i + 1), {}), epdir) for i in range(n)]
    log('Голос: %.1f с, блоки: %s' % (dur, ', '.join(b.kind for b in B)))
    wt = [np.array(WT[i]) - 0.06 for i in range(n)]
    VIDS = {}
    fj = os.path.join(epdir, '_nur', 'video', 'footage.json')
    if os.path.exists(fj):
        base = epdir
        for kk, vv in json.load(open(fj, encoding='utf-8')).items():
            vv = [os.path.join(base, x) for x in vv if os.path.exists(os.path.join(base, x))]
            if vv: VIDS[int(kk) - 1] = vv[0]
    log('Видео-фон: %d / %d' % (len(VIDS), n))
    RD = {}
    def vframe(i):
        if i not in VIDS: return None
        if i not in RD: RD[i] = VideoReader(VIDS[i])
        for j in [j for j in RD if j < i - 1]: RD.pop(j).close()
        return RD[i].next()
    dust = Dust(); CH = chrome(meta, lang)
    od = os.path.join(epdir, 'output'); os.makedirs(od, exist_ok=True)
    name = meta.get('out') or ('Nuzul_' + os.path.basename(epdir))
    out = os.path.join(od, name + ('_PREVIEW' if preview else '') + '.mp4')
    total = edges[-1]; nf = int(total * FPS)
    sc = 0.5 if preview else 1.0; OW, OH = int(W * sc) // 2 * 2, int(H * sc) // 2 * 2
    cmd = [FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (OW, OH), '-r', str(FPS), '-i', '-',
           '-i', voice, '-filter_complex', '[0:v]noise=alls=4:allf=t,format=yuv420p[v];[1:a]highpass=f=70,acompressor=threshold=-18dB:ratio=3,'
           'aecho=0.8:0.5:60:0.12,loudnorm=I=-14:TP=-1.5,apad[a]',
           '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '28' if preview else '19',
           '-c:a', 'aac', '-b:a', '192k', '-t', '%.2f' % total, '-movflags', '+faststart', out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    VF = {}; SHOT = {}; PAT = {}
    def frame(i, t, fi):
        b = B[i]; a0, a1 = edges[i], edges[i + 1]; p = (t - a0) / max(1.0, a1 - a0)
        if (i, fi) not in VF:
            v = vframe(i); VF.clear(); VF[(i, fi)] = v
        v = VF[(i, fi)]
        bgi = NB.frame(i, t - a0, a1 - a0)
        if bgi is not None: im = Image.blend(bgi.convert('RGB'), Image.new('RGB', (W, H)), 0.22).convert('RGBA')
        elif v is not None: im = grade(v, p, t, i).convert('RGBA')
        else: im = PAT.setdefault(i, IG.make({'type': 'pattern', 'seed': i}, W, H, 'nur')).frame(t - a0, a1 - a0)
        dust.draw(im, t)
        fa = min(1.0, (t - a0) / 0.7)
        im.alpha_composite(b.static if fa >= 1 else Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 0)), b.static, fa))
        if b.ar is not None:
            ay = 470 if b.kind == 'ayah' else 1150
            ar = b.ar if fa >= 1 else Image.blend(Image.new('RGBA', b.ar.size, (0, 0, 0, 0)), b.ar, fa)
            im.alpha_composite(ar, (int((W - ar.width) / 2), ay))
        k = int(np.searchsorted(wt[i], t, side='right')); si = 0
        for s_i, sidx in enumerate(b.sents):
            if wt[i][sidx[0]] <= t + 0.15: si = s_i
        cur = k > 0 and (t - wt[i][k - 1]) < 0.45
        lay = b.text_layer(si, k, cur)
        st = wt[i][b.sents[si][0]] - 0.15
        sa = 1.0 if si == 0 and t - a0 < 0.4 else min(1.0, max(0.0, (t - st) / 0.28))
        ty = b.ty - lay.height // 2 + int(14 * (1 - sa))
        if sa < 1: lay = Image.blend(Image.new('RGBA', lay.size, (0, 0, 0, 0)), lay, sa)
        im.alpha_composite(lay, (0, ty))
        if b.kind == 'subscribe' and t - a0 > 0.6:
            q = min(1.0, (t - a0 - 0.6) / 0.35); s = 0.6 + 0.4 * q + 0.03 * math.sin(t * 5)
            pill(im, W / 2, 1250, TX[lang][0], RED + (255,), (255, 255, 255, 255), s, bell=True)
        if b.kind == 'share' and t - a0 > 0.8:
            q = min(1.0, (t - a0 - 0.8) / 0.35); s = 0.6 + 0.4 * q + 0.025 * math.sin(t * 4)
            pill(im, W / 2, 1300, TX[lang][1], GOLD + (255,), (40, 24, 10, 255), s)
        im.alpha_composite(CH)
        d = ImageDraw.Draw(im); d.rectangle([0, H - 8, int(W * t / total), H], fill=GOLD + (220,))
        return im.convert('RGB')
    last = -1
    for fi in range(nf):
        t = fi / FPS
        i = min(n - 1, int(np.searchsorted(edges, t, side='right')) - 1)
        im = frame(i, t, fi)
        if i > 0 and t - edges[i] < XF:
            im = Image.blend(frame(i - 1, t, fi), im, (t - edges[i]) / XF)
        if i == 0 and 'hook' not in SHOT and t > min(edges[1] - 0.3, 6.0): SHOT['hook'] = im.copy()
        if t < 0.4: im = Image.blend(Image.new('RGB', (W, H)), im, t / 0.4)
        if t > total - 0.8: im = Image.blend(Image.new('RGB', (W, H)), im, max(0.0, (total - t) / 0.8))
        if sc != 1.0: im = im.resize((OW, OH), Image.BILINEAR)
        pr.stdin.write(im.tobytes())
        if fi * 10 // nf != last: last = fi * 10 // nf; log('кадр %d / %d' % (fi, nf))
    pr.stdin.close(); pr.wait()
    for r in RD.values(): r.close()
    # обложка: готовая от Claude или кадр с хуком
    import shutil
    oc = os.path.join(epdir, 'OBLOZHKA_1080x1920.jpg')
    if os.path.exists(oc): shutil.copy(oc, os.path.join(od, 'OBLOZHKA_1080x1920.jpg'))
    elif 'hook' in SHOT: SHOT['hook'].save(os.path.join(od, 'OBLOZHKA_1080x1920.jpg'), quality=92)
    for f in ('youtube.txt',):
        if os.path.exists(os.path.join(epdir, f)): shutil.copy(os.path.join(epdir, f), os.path.join(od, f))
    log('ГОТОВО:', out)
    return out

if __name__ == '__main__':
    render(sys.argv[1], preview='--preview' in sys.argv)
