# -*- coding: utf-8 -*-
"""Скачивает бесплатные видеоролики (Pixabay, Pexels) в максимальном качестве для серии.
Usage:
  python footage.py "<папка серии>" [--per 2] [--out montaj\\video] [--size 1920x1080] [--nopeople] [--keep-raw]
Читает kadr.txt в папке серии: строки  "N | первые слова | english search words".
ГЛАВНОЕ (с 13.11.2026): строка  "@topic: istanbul, bosphorus, constantinople"  — тема серии.
  КАЖДЫЙ ролик обязан иметь в тегах хотя бы одно слово темы. Ролики не по теме не берутся никогда
  (лучше повторить кадр той же серии, чем показать Рим вместо Стамбула).
Слово с + (например +ankara) в строке = для этого абзаца вместо темы обязательны эти слова.
--check : проверить уже скачанные ролики (теги через API), ролики не по теме удалить и скачать замену.
Ключи: D:\\gemini\\_toolkit\\pixabay_key.txt (есть), pexels_key.txt (необязательно).
Ролики не повторяются: все использованные ID пишутся в _toolkit\\used_videos.txt.
Результат: <out>\\pNN_a.mp4 ... + <out>\\footage.json + credits.txt (+ montaj\\img\\cover_bg.jpg)."""
import os, sys, re, json, time, shutil, subprocess, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    import imageio_ffmpeg; FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = 'ffmpeg'
UA = {'User-Agent': 'Mozilla/5.0 (footage.py for personal video projects)'}
MAX_BYTES = 450 * 1024 * 1024
PEOPLE = {'person', 'people', 'man', 'men', 'woman', 'women', 'girl', 'boy', 'child', 'children', 'kid', 'kids', 'face',
          'portrait', 'couple', 'family', 'crowd', 'human', 'lady', 'baby', 'worker', 'tourist', 'model', 'selfie', 'hand', 'hands',
          # фигуры, персонажи и чужие религиозные символы — для исламских роликов недопустимы
          'statue', 'figure', 'character', 'fantasy', 'monk', 'wizard', 'warrior', 'soldier', 'knight', 'silhouette', 'pilgrim',
          'angel', 'god', 'jesus', 'christ', 'church', 'cross', 'buddha', 'buddhist', 'christmas', 'santa', 'halloween', 'hanukkah',
          'menorah', 'idol', 'sculpture', 'mannequin', 'dancer', 'dance', 'party', 'bikini', 'animation', 'cartoon', 'skull', 'witch', 'ghost'}

def log(*a): print('>>', *a, flush=True)

def key(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p): p = os.path.join(HERE, '..', '.secrets', name)
    if not os.path.exists(p): return None
    k = open(p, encoding='utf-8-sig').read().strip()
    return k or None

def get_json(url, headers=None):
    req = urllib.request.Request(url, headers=dict(UA, **(headers or {})))
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            log('  retry', i + 1, e); time.sleep(2 + 3 * i)
    return None

def download(url, dst):
    req = urllib.request.Request(url, headers=UA)
    tmp = dst + '.part'
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, 'wb') as f:
        shutil.copyfileobj(r, f, 1 << 20)
    os.replace(tmp, dst)

# ---------------------------------------------------------------- providers
def pixabay(q, k):
    u = 'https://pixabay.com/api/videos/?' + urllib.parse.urlencode(dict(key=k, q=q[:100], per_page=40, safesearch='true', order='popular'))
    d = get_json(u)
    out = []
    for h in (d or {}).get('hits', []):
        if h.get('isAiGenerated'): continue
        vs = [v for v in h.get('videos', {}).values() if v.get('url') and v.get('width')]
        vs = [v for v in vs if (v.get('size') or 0) <= MAX_BYTES] or vs
        if not vs: continue
        best = max(vs, key=lambda v: v['width'])
        if best['width'] < best['height']: continue
        out.append(dict(id='pixabay:%s' % h['id'], url=best['url'], w=best['width'], h=best['height'], dur=h.get('duration', 0),
                        tags=h.get('tags', ''), pop=h.get('downloads', 0), credit='Pixabay — %s — %s' % (h.get('user', ''), h.get('pageURL', ''))))
    return out

def pexels(q, k):
    u = 'https://api.pexels.com/videos/search?' + urllib.parse.urlencode(dict(query=q[:100], per_page=40, orientation='landscape'))
    d = get_json(u, {'Authorization': k})
    out = []
    for v in (d or {}).get('videos', []):
        fs = [f for f in v.get('video_files', []) if f.get('link') and f.get('width') and f.get('width') <= 4096]
        if not fs: continue
        best = max(fs, key=lambda f: f['width'])
        if best['width'] < best['height']: continue
        tags = ' '.join(re.split(r'[-/]', v.get('url', '')))
        out.append(dict(id='pexels:%s' % v['id'], url=best['link'], w=best['width'], h=best['height'], dur=v.get('duration', 0),
                        tags=tags, pop=0, credit='Pexels — %s — %s' % (v.get('user', {}).get('name', ''), v.get('url', ''))))
    return out

def has_people(c):
    words = set(re.findall(r'[a-z]+', c['tags'].lower()))
    return bool(words & PEOPLE)

def tier(w): return 3 if w >= 3800 else 2 if w >= 2500 else 1 if w >= 1900 else 0

def tag_ok(c, need, topic):
    t = ' ' + re.sub(r'[^a-z0-9ğüşöçıə ]', ' ', c['tags'].lower()) + ' '
    if need: return all(n in t for n in need)
    if topic: return any(' ' + x + ' ' in t or (' ' in x and x in t) for x in topic)
    return True

def relevance(c, q):
    t = c['tags'].lower(); w = [x for x in q.replace('+', '').lower().split() if len(x) > 2]
    return sum(1 for x in w if x in t)

def search(q, used, nopeople, keys, need=(), topic=()):
    cands = []
    if keys['pixabay']: cands += pixabay(q, keys['pixabay'])
    if keys['pexels']: cands += pexels(q, keys['pexels'])
    cands = [c for c in cands if c['id'] not in used and c['dur'] >= 5 and tier(c['w']) >= 1]
    if nopeople: cands = [c for c in cands if not has_people(c)]
    cands = [c for c in cands if tag_ok(c, need, topic)]
    cands.sort(key=lambda c: (-relevance(c, q), -tier(c['w']), -c['pop']))
    return cands

def pixabay_tags(vid, k):
    d = get_json('https://pixabay.com/api/videos/?' + urllib.parse.urlencode(dict(key=k, id=vid)))
    h = (d or {}).get('hits') or []
    return h[0].get('tags', '') if h else None

def queries(q):
    q = q.replace('+', ''); w = q.split(); out = [q]
    while len(w) > 2: w = w[:-1]; out.append(' '.join(w))
    # одно последнее слово не берём: «bow arrow» -> «arrow»/«bow» давало скрипку, «writing» -> девочку с тетрадью
    return out

# ---------------------------------------------------------------- main
def main():
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    ep = os.path.abspath(a[0])
    per = int(a[a.index('--per') + 1]) if '--per' in a else 2
    outrel = a[a.index('--out') + 1] if '--out' in a else os.path.join('montaj', 'video')
    size = a[a.index('--size') + 1] if '--size' in a else '1920x1080'
    W, H = map(int, size.lower().split('x'))
    nopeople = '--nopeople' in a; keep = '--keep-raw' in a
    keys = dict(pixabay=key('pixabay_key.txt'), pexels=key('pexels_key.txt'))
    if not keys['pixabay'] and not keys['pexels']: sys.exit('Нет ключа: положите pixabay_key.txt в ' + HERE)
    kfile = os.path.join(ep, 'kadr.txt')
    if not os.path.exists(kfile): sys.exit('Нет kadr.txt в папке серии')
    lines = []; topic = []
    for ln in open(kfile, encoding='utf-8-sig'):
        ln = ln.strip()
        if not ln or ln.startswith('#'): continue
        if ln.startswith('@'):
            k2, _, v = ln[1:].partition(':')
            if k2.strip().lower() in ('topic', 'mavzu', 'tema', 'тема'): topic = [x.strip().lower() for x in v.split(',') if x.strip()]
            continue
        p = [x.strip() for x in ln.split('|')]
        if not p[0].isdigit(): continue
        q = (ln.split('|', 2)[-1] if ln.count('|') >= 2 else p[-1]).split('||')[0].strip()
        if not q or q.upper().startswith('INFO'): continue   # здесь будет карта/инфографика, ролик не нужен
        if q.upper().startswith('VIDEO:'): q = q[6:].strip()
        elif '--only-video' in sys.argv: continue          # исламские стили: видео только по строкам VIDEO:
        lines.append((p[0], q))
    check = '--check' in a
    if topic: log('Тема серии:', ', '.join(topic))
    out = os.path.join(ep, outrel); raw = os.path.join(out, '_raw'); os.makedirs(raw, exist_ok=True)
    regf = os.path.join(HERE, 'used_videos.txt')
    used = set(x.strip() for x in open(regf, encoding='utf-8')) if os.path.exists(regf) else set()
    fj = os.path.join(out, 'footage.json')
    res = json.load(open(fj, encoding='utf-8')) if os.path.exists(fj) else {}
    credits = []
    base = os.path.join(ep, 'montaj') if outrel.startswith('montaj') else ep  # пути в footage.json относительно base
    mjf = os.path.join(out, 'footage_meta.json')
    meta = json.load(open(mjf, encoding='utf-8')) if os.path.exists(mjf) else {}
    changed = False
    if check and (topic or any('+' in q for _, q in lines)):
        # id старых роликов — из credits.txt
        cid = {}
        for cf in (os.path.join(ep, 'montaj', 'credits.txt'), os.path.join(ep, 'credits.txt')):
            if os.path.exists(cf):
                for l2 in open(cf, encoding='utf-8'):
                    m = re.search(r'(p\d+_\w)\.mp4 — Pixabay .*?id-(\d+)', l2)
                    if m: cid[m.group(1)] = m.group(2)
        for n, q in lines:
            need_tags = [x[1:].lower() for x in q.split() if x.startswith('+')]
            keep_list = []
            for rel in res.get(str(int(n)), []):
                nm = os.path.splitext(os.path.basename(rel))[0]
                tg = (meta.get(rel) or {}).get('tags')
                if tg is None and nm in cid and keys['pixabay']:
                    tg = pixabay_tags(cid[nm], keys['pixabay']); time.sleep(0.4)
                    meta[rel] = dict(id='pixabay:' + cid[nm], tags=tg or '')
                if tg is not None and not tag_ok(dict(tags=tg), need_tags, topic):
                    log('   ✗ не по теме, удаляю %s  [%s]' % (nm, tg[:70]))
                    try: os.remove(os.path.join(base, rel))
                    except OSError: pass
                    changed = True; continue
                keep_list.append(rel)
            res[str(int(n))] = keep_list
        json.dump(meta, open(mjf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for n, q in lines:
        nn = '%02d' % int(n)
        have = [f for f in res.get(str(int(n)), []) if os.path.exists(os.path.join(base, f))]
        need = per - len(have)
        if need <= 0: log(nn, 'уже есть'); continue
        log(nn, q)
        got = []
        need_tags = [x[1:].lower() for x in q.split() if x.startswith('+')]
        words = [x for x in q.replace('+', '').split() if x.lower() not in need_tags and x.lower() not in topic]
        tries = [(qq, need_tags, topic) for qq in queries(q)]
        if need_tags: tries.append((' '.join(need_tags), need_tags, topic))
        if topic:  # запасной вариант — только ролики по теме серии
            for tw in topic[:3]:
                if words: tries.append((tw + ' ' + ' '.join(words[:2]), [], topic))
                tries.append((tw, [], topic))
        elif not need_tags:
            tries += [(qq, [], []) for qq in queries(q)[1:]]
        seen_q = set()
        for qq, nt, tp in tries:
            if qq in seen_q: continue
            seen_q.add(qq)
            for c in search(qq, used, nopeople, keys, nt, tp):
                if len(got) >= need: break
                letter = next(l for l in 'abcdefghij' if not os.path.exists(os.path.join(out, 'p%s_%s.mp4' % (nn, l))))
                rawf = os.path.join(raw, 'p%s_%s_%s.mp4' % (nn, letter, c['id'].replace(':', '_')))
                dst = os.path.join(out, 'p%s_%s.mp4' % (nn, letter))
                try:
                    log('   скачиваю %dx%d %s' % (c['w'], c['h'], c['id']))
                    if not os.path.exists(rawf): download(c['url'], rawf)
                    vf = 'scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos,crop=%d:%d,fps=25,format=yuv420p' % (W, H, W, H)
                    r = subprocess.run([FF, '-y', '-v', 'error', '-i', rawf, '-t', '30', '-an', '-vf', vf, '-c:v', 'libx264', '-preset', 'slow',
                                        '-crf', '16', dst], capture_output=True, text=True)
                    if r.returncode != 0 or not os.path.exists(dst): log('   ffmpeg error', r.stderr[-300:]); continue
                except Exception as e:
                    log('   ошибка:', e); continue
                finally:
                    if not keep and os.path.exists(rawf) and os.path.exists(dst): os.remove(rawf)
                used.add(c['id']); open(regf, 'a', encoding='utf-8').write(c['id'] + '\n')
                rel = os.path.relpath(dst, base).replace('\\', '/')
                got.append(rel); credits.append('%s — %s' % (os.path.basename(dst), c['credit']))
                meta[rel] = dict(id=c['id'], tags=c['tags']); changed = True
            if len(got) >= need: break
        res[str(int(n))] = have + got
        if len(got) < need: log('   !! по теме найдено меньше роликов (%d) — в этом месте повторится кадр серии' % (len(have) + len(got)))
        json.dump(res, open(fj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump(meta, open(mjf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if credits:
        cf = os.path.join(ep, 'montaj' if outrel.startswith('montaj') else '', 'credits.txt')
        with open(cf, 'a', encoding='utf-8') as f:
            f.write('\n# Видео (бесплатные лицензии Pixabay / Pexels):\n' + '\n'.join(credits) + '\n')
    # cover frame
    first = next((v for k in sorted(res, key=int) for v in res[k]), None)
    if first and outrel.startswith('montaj'):
        img = os.path.join(ep, 'montaj', 'img'); os.makedirs(img, exist_ok=True)
        subprocess.run([FF, '-y', '-v', 'error', '-ss', '2', '-i', os.path.join(ep, 'montaj', first), '-frames:v', '1', '-q:v', '2',
                        os.path.join(img, 'cover_bg.jpg')])
    try: os.rmdir(raw)
    except OSError: pass
    json.dump(res, open(fj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if changed:
        # автосцены ссылаются на старые ролики — пересоздать
        sj = os.path.join(ep, 'montaj', 'scenes.json')
        if os.path.exists(sj) and outrel.startswith('montaj'):
            try:
                txt = open(sj, encoding='utf-8-sig').read()
                if '"auto"' in txt or 'video/p' in txt: os.remove(sj); log('scenes.json будет создан заново')
            except OSError: pass
        open(os.path.join(out, 'CHANGED.txt'), 'w').write('footage changed')
    log('ГОТОВО: роликов %d' % sum(len(v) for v in res.values()), '->', out)

if __name__ == '__main__':
    main()
