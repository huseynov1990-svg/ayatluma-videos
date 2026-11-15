# Dobavlyaet k gotovomu video tikhuyu muzyku (pod golosom, s prigrusheniem) i zvuki perekhodov mezhdu abzatsami.
# python mix.py <papka serii> <muzyka.mp3> <swoosh.mp3> <boom.mp3> [muz_dB=-24]
import sys, os, re, json, glob, difflib, subprocess
ep, music, swoosh, boom = sys.argv[1:5]; mdb = float(sys.argv[5]) if len(sys.argv) > 5 else -24
od = os.path.join(ep, 'output'); vid = [f for f in glob.glob(os.path.join(od, '*.mp4')) if '_PREVIEW' not in f and not f.endswith('_FINAL.mp4')][0]
n = lambda w: re.sub(r'[\W_]', '', w.lower().replace('ё', 'е'))
paras = [p.split() for p in re.split(r'\n\s*\n', open(os.path.join(ep, 'Ssenari_ozvucka.txt'), encoding='utf-8-sig').read()) if p.strip()]
aw = json.load(open(os.path.join(ep, '_nur', 'asr_words.json'), encoding='utf-8'))
A = [n(w) for p in paras for w in p]; B = [n(w[0]) for w in aw]; t = [None] * len(A)
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1): t[i1 + k] = aw[j1 + k][1]
starts = []; k = 0
for p in paras:
    s = next((x for x in t[k:k + len(p)] if x is not None), None)
    if s is not None: starts.append(max(0, s - 0.45))
    k += len(p)
starts = starts[1:]  # pervyy abzats - boom v nachale
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid], capture_output=True, text=True).stdout)
inp = ['-i', vid, '-stream_loop', '-1', '-i', music, '-i', boom] + sum([['-i', swoosh] for _ in starts], [])
f = '[0:a]asplit=2[v][sc];[1:a]atrim=0:%.2f,volume=%.1fdB,afade=t=in:d=2,afade=t=out:st=%.2f:d=3[m0];' % (dur, mdb, max(0, dur - 3))
f += '[m0][sc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[m];[2:a]volume=-10dB[b];'
mix = ['[v]', '[m]', '[b]']
for i, s in enumerate(starts):
    f += '[%d:a]volume=-16dB,adelay=%d|%d[s%d];' % (3 + i, s * 1000, s * 1000, i); mix.append('[s%d]' % i)
f += ''.join(mix) + 'amix=inputs=%d:normalize=0:duration=first,alimiter=limit=0.95[a]' % len(mix)
out = vid[:-4] + '_FINAL.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', f, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', '%.2f' % dur, '-movflags', '+faststart', out], check=True)
print('OK', out, 'perekhodov:', len(starts))
