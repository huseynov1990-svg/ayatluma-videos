# Ozvuchka po abzatsam s proverkoy: python ozvuchka.py <papka serii> <golos> "<stil>" [yazyk=ru]
import sys, os, re, subprocess, difflib, numpy as np
ep, voice, style = sys.argv[1:4]; lang = sys.argv[4] if len(sys.argv) > 4 else 'ru'
from faster_whisper import WhisperModel
M = WhisperModel('small', device='cpu', compute_type='int8', download_root=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_stil', '.models'))
n = lambda w: re.sub(r'[\W_]', '', w.lower().replace('ё', 'е'))
def heard(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
    s, _ = M.transcribe(np.frombuffer(raw, np.float32), language=lang); return ' '.join(x.text for x in s)
paras = [p.strip() for p in re.split(r'\n\s*\n', open(os.path.join(ep, 'Ssenari_ozvucka.txt'), encoding='utf-8-sig').read()) if p.strip()]
# po 3 abzatsa v odnom zaprose (limit Gemini TTS ~100 zaprosov v den); pauza mezhdu abzatsami - pustaya stroka
GRP = 3
paras = ['\n\n'.join(paras[i:i + GRP]) for i in range(0, len(paras), GRP)]
os.makedirs(os.path.join(ep, 'voice'), exist_ok=True); parts = []
for i, p in enumerate(paras):
    out = os.path.join(ep, 'voice', 'p%02d.wav' % i); best = None
    for tr in range(3):
        r = subprocess.run(['python3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tts.py'), 'gemini-3.8-flash-tts', voice, style, p, out], stdin=subprocess.DEVNULL, capture_output=True, text=True)
        if r.returncode != 0: continue
        d = float(r.stdout.split()[1]); h = heard(out)
        A = [n(w) for w in p.split() if n(w) and 'ﷺ' not in w]; B = [n(w) for w in h.split() if n(w)]
        ratio = difflib.SequenceMatcher(None, A, B, autojunk=False).ratio(); wps = len(A) / d
        extra = len(B) - len(A) - p.count('ﷺ') * 4
        ok = ratio > 0.55 and 1.3 <= wps <= 3.0 and extra < 8
        print(i, 'popytka', tr + 1, 'sovpadenie %.2f' % ratio, 'temp %.2f sl/s' % wps, 'OK' if ok else 'PEREDELAT', flush=True)
        if ok: best = out; break
    if not best: sys.exit('Abzats %d ne udalos ozvuchit bez oshibok' % i)
    parts.append(out)
sil = os.path.join(ep, 'voice', '_sil.wav')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-t', '0.6', '-i', 'anullsrc=r=24000:cl=mono', sil], check=True)
lst = os.path.join(ep, 'voice', '_list.txt')
open(lst, 'w').write(''.join("file '%s'\nfile '%s'\n" % (q, sil) for q in parts))
final = os.path.join(ep, 'voice', 'voiceover.wav')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'pcm_s16le', '-ar', '24000', '-ac', '1', final], check=True)
for q in parts + [sil, lst]: os.remove(q)
print('GOTOVO', final)
