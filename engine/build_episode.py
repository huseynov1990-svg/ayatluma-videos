# Sobrat odin rolik AYAT LUMA iz papki serii.
# V papke zaranee: Ssenari_ozvucka.txt, meta.json, kadr.txt, cover.json, (_nur/ar_N.png dlya arabskogo teksta)
# python build_episode.py <papka serii> <golos> "<stil golosa>" [muzyka.mp3] [--lang ru]
# Kod vykhoda: 0 = gotovo, 3 = ozvuchka dlinnee 2:55 (sokrati tekst i zapusti snova), inoe = oshibka.
import sys, os, glob, subprocess, json
E = os.path.dirname(os.path.abspath(__file__)); ep = os.path.abspath(sys.argv[1]); voice, style = sys.argv[2], sys.argv[3]
music = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith('--') else os.path.join(E, 'zvuki', 'muzyka', 'Desert-Fox-Underscore.mp3')
lang = sys.argv[sys.argv.index('--lang') + 1] if '--lang' in sys.argv else 'ru'
MAXDUR = 175.0
# PRAVILO POLZOVATELYA (16.11.2026): v religii (AYAT LUMA, Ruhun Qidasi) MUZYKI NET — tolko golos i zvuki
_meta = json.load(open(os.path.join(ep, 'meta.json'), encoding='utf-8'))
if _meta.get('religion') or any(k in _meta.get('out', '').upper() for k in ('AYAT', 'RUHUN')): music = 'none'
def run(c): print('>>', ' '.join(c[:3]), flush=True); subprocess.run(c, check=True, stdin=subprocess.DEVNULL)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
vo = os.path.join(ep, 'voice', 'voiceover.wav')
if not os.path.exists(vo):
    run(['python3', os.path.join(E, '_avto', 'ozvuchka.py'), ep, voice, style, lang])
d = dur(vo); print('Ozvuchka: %.1f s' % d)
if d > MAXDUR:
    os.rename(vo, vo + '.dlinno_%.0fs.wav' % d)
    print('SLISHKOM DLINNO (%.0f s > %.0f s): sokrati Ssenari_ozvucka.txt i zapusti snova' % (d, MAXDUR)); sys.exit(3)
if not os.path.exists(os.path.join(ep, 'OBLOZHKA_1080x1920.jpg')):
    run(['python3', os.path.join(E, '_avto', 'cover.py'), ep])
od = os.path.join(ep, 'output')
for f in glob.glob(os.path.join(od, '*.mp4')): os.remove(f)
run(['python3', os.path.join(E, '_stil', 'render_ayat_v.py'), ep])
run(['python3', os.path.join(E, '_avto', 'mix.py'), ep, music, os.path.join(E, 'zvuki', 'effekty', 'swoosh_01.mp3'), os.path.join(E, 'zvuki', 'effekty', 'boom-intro.mp3'), '-24'])
fin = [f for f in glob.glob(os.path.join(od, '*_FINAL.mp4'))][0]
name = json.load(open(os.path.join(ep, 'meta.json'), encoding='utf-8')).get('out', os.path.basename(ep))
out = os.path.join(od, name + '_PUBLISH.mp4')
run(['ffmpeg', '-y', '-loglevel', 'error', '-i', fin, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-maxrate', '7M', '-bufsize', '14M', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out])
sz = os.path.getsize(out) / 1e6; dd = dur(out)
print('GOTOVO %s  %.1f MB  %.1f s' % (out, sz, dd))
if dd > 180 or sz > 95: print('VNIMANIE: dlinnee 3:00 ili bolshe 95 MB'); sys.exit(4)
