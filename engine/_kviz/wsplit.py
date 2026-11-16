import re, difflib, numpy as np
NUM = {'az': ['sıfır','bir','iki','üç','dörd','beş','altı','yeddi','səkkiz','doqquz','on','on bir','on iki','on üç','on dörd','on beş'],
       'en': ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen'],
       'ru': ['ноль','один','два','три','четыре','пять','шесть','семь','восемь','девять','десять','одиннадцать','двенадцать','тринадцать','четырнадцать','пятнадцать']}
def _norm(s, lang):
    s = s.lower().replace('ё','е').replace('ﷺ',' ').replace('ı','i').replace('ə','e')
    nums = NUM.get(lang, NUM['en'])
    f = lambda k: nums[k].replace('ı','i').replace('ə','e')
    s = re.sub(r'\d+', lambda m: (f(int(m.group())) if int(m.group()) < len(nums) else ''.join(f(int(c)) for c in m.group())), s)
    return re.sub(r'[^\w]+', '', s)
def split_by_wordstamps(a, SR, lines, lang, model):
    """a: mono float32 at SR. Returns list of arrays (one per line) or None."""
    a16 = a[::3].astype(np.float32) if SR == 48000 else a
    # rezhem po pauzam (>=0.3 s) na kuski ~ do 12 s i raspoznaem kazhdyy kusok otdelno (whisper ne «uplyvaet»)
    sr16 = 16000; fr = int(sr16 * 0.02)
    e = np.sqrt(np.mean(a16[:len(a16) // fr * fr].reshape(-1, fr) ** 2, 1))
    thr = max(1e-3, np.percentile(e, 30) * 1.5, e.max() * 0.02); sil = e < thr
    cuts = [0]; runlen = 0
    for i, sl in enumerate(sil):
        runlen = runlen + 1 if sl else 0
        if runlen == 15 and (i - cuts[-1]) * 0.02 > 2.0: cuts.append(i - 7)
    cuts.append(len(e))
    W = []
    for c0, c1 in zip(cuts[:-1], cuts[1:]):
        x = a16[c0 * fr:c1 * fr]
        if len(x) < sr16 * 0.2: continue
        segs, _ = model.transcribe(x, language=lang, word_timestamps=True, vad_filter=False, condition_on_previous_text=False, beam_size=5)
        off = c0 * 0.02
        W += [(w.start + off, w.end + off, _norm(w.word, lang)) for s in segs for w in s.words]
    W = [w for w in W if w[2]]
    m, n = len(W), len(lines)
    if m < n: return None
    L = [_norm(x, lang) for x in lines]
    # prefix strings for speed
    def sim(i, k, j):
        g = ''.join(w[2] for w in W[k:j])
        return difflib.SequenceMatcher(None, L[i], g, autojunk=False).ratio() * max(len(L[i]), 1)
    NEG = -1e18; best = np.full((n + 1, m + 1), NEG); arg = np.zeros((n + 1, m + 1), int); best[0][0] = 0
    MAXW = 25
    for i in range(1, n + 1):
        for j in range(i, m - (n - i) + 1):
            for k in range(max(i - 1, j - MAXW), j):
                if best[i - 1][k] == NEG: continue
                v = best[i - 1][k] + sim(i - 1, k, j)
                if v > best[i][j]: best[i][j] = v; arg[i][j] = k
    if best[n][m] == NEG: return None
    cuts = []; j = m
    for i in range(n, 0, -1): k = arg[i][j]; cuts.append((k, j)); j = k
    cuts.reverse()
    score = best[n][m] / max(1, sum(len(x) for x in L))
    st = [W[k][0] for k, j in cuts]; en = [W[j - 1][1] for k, j in cuts]
    bnd = [0.0] + [(en[i] + st[i + 1]) / 2 for i in range(n - 1)] + [len(a) / SR]
    out = []
    fr = int(SR * 0.01)
    for i in range(n):
        x = a[int(bnd[i] * SR):int(bnd[i + 1] * SR)]
        # trim silence at edges (keep 80 ms)
        e = np.sqrt(np.mean(x[:len(x) // fr * fr].reshape(-1, fr) ** 2, 1)) if len(x) >= fr else np.zeros(1)
        thr = max(1e-3, e.max() * 0.04); nz = np.where(e > thr)[0]
        if len(nz): x = x[max(0, (nz[0] - 8) * fr):min(len(x), (nz[-1] + 12) * fr)]
        out.append(x.copy())
        r = difflib.SequenceMatcher(None, L[i], ''.join(w[2] for w in W[cuts[i][0]:cuts[i][1]]), autojunk=False).ratio()
        if r < 0.5: print(f'» VNIMANIE stroka {i}: «{lines[i][:40]}» ~ «{" ".join(w[2] for w in W[cuts[i][0]:cuts[i][1]])[:40]}» ({r:.2f})')
    print(f'» slova-razrez: {m} slov, kachestvo {score:.2f}')
    return out if score >= 0.6 else None
