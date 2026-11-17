"""Generic Inkframe builder. usage: python3 build_gen.py EPDIR   (EPDIR/cfg.json)
cfg: anchors[], sets{rain,rain_muf,sea,room,wind}, shake{k:amp}, tense[a,b], sfx[[name,scene,offset,gain]], tail
"""
import sys, json, subprocess, os
import numpy as np
from PIL import Image
from scipy.signal import butter, sosfilt
import scipy.io.wavfile as wf
D = sys.argv[1]; C = json.load(open(f"{D}/cfg.json"))
SR, FPS, W, H = 44100, 30, 1920, 1080
LEAD, TAIL = 0.6, C.get("tail", 5.0)
ANCHORS = C["anchors"]; S = {k: set(v) for k, v in C.get("sets", {}).items()}
SHAKE = {int(k): v for k, v in C.get("shake", {}).items()}
al = json.load(open(f"{D}/voice.json"))
chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
full = "".join(chars); pos, times = 0, []
for a in ANCHORS:
    i = full.find(a, pos)
    assert i >= 0, a
    times.append(starts[i] + LEAD); pos = i + 1
times[0] = 0.0
T = ends[-1] + LEAD + TAIL; bounds = times + [T]
print("duration %.1f s, scenes %d" % (T, len(ANCHORS)), flush=True)
def load(path):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.float32).copy()
N = int(T * SR); rng = np.random.default_rng(5); t = np.arange(N) / SR
def sos(k, f, o=2): return butter(o, f, btype=k, fs=SR, output="sos")
def env_seg(a, b, fade=0.8):
    e = np.zeros(N, np.float32); i0, i1 = int(a * SR), min(N, int(b * SR)); f = int(fade * SR)
    if i1 <= i0: return e
    e[i0:i1] = 1; r = np.arange(f) / f
    if i1 - i0 >= 2 * f: e[i0:i0 + f] *= r; e[i1 - f:i1] *= r[::-1]
    return e
def ranges(name): return [(bounds[k - 1], bounds[k]) for k in sorted(S.get(name, ()))]
mix = np.zeros(N, np.float32)
voice = load(f"{D}/voice.mp3"); v0 = int(LEAD * SR); mix[v0:v0 + len(voice)] += voice[:N - v0]
noise = rng.standard_normal(N).astype(np.float32)
rain = sosfilt(sos("bandpass", [500, 8000]), noise); rain /= rain.std()
rain_muf = sosfilt(sos("lowpass", 700), noise); rain_muf /= rain_muf.std()
room = sosfilt(sos("lowpass", 180), rng.standard_normal(N).astype(np.float32)); room /= room.std()
wind = sosfilt(sos("bandpass", [150, 1200]), noise); wind /= wind.std(); wind *= (0.6 + 0.4 * np.sin(2 * np.pi * t / 7.3) * np.sin(2 * np.pi * t / 3.1))
seaw = sosfilt(sos('lowpass', 500), rain).astype(np.float32) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 6.5))
for a, b in ranges("rain"): mix += rain * env_seg(a, b) * 0.035
for a, b in ranges("rain_muf"): mix += rain_muf * env_seg(a, b) * 0.03
for a, b in ranges("sea"): mix += seaw * env_seg(a, b) * 0.035
for a, b in ranges("room"): mix += (room * 0.03 + 0.004 * np.sin(2 * np.pi * 100 * t)) * env_seg(a, b)
for a, b in ranges("wind"): mix += wind * env_seg(a, b) * 0.02
md = C.get("drone", [55, 82.4, 110.3])
drone = (np.sin(2 * np.pi * md[0] * t) + 0.6 * np.sin(2 * np.pi * (md[0] + 0.4) * t) + 0.4 * np.sin(2 * np.pi * md[1] * t) + 0.25 * np.sin(2 * np.pi * md[2] * t)) * (0.75 + 0.25 * np.sin(2 * np.pi * t / 9))
drone = sosfilt(sos("lowpass", 300), drone.astype(np.float32))
mix += drone * 0.018 * np.clip(t / 3, 0, 1) * np.clip((T - t) / 3, 0, 1)
if C.get("tense"):
    ta, tb = bounds[C["tense"][0]], bounds[C["tense"][1]]; beat = np.zeros(N, np.float32)
    for bt in np.arange(ta, tb, C.get("beat", 0.92)):
        i = int(bt * SR); n = int(0.35 * SR)
        if i + n < N:
            tt = np.arange(n) / SR; beat[i:i + n] += np.sin(2 * np.pi * 52 * tt) * np.exp(-tt / 0.09)
    mix += beat * 0.09 * np.clip((t - ta) / 20, 0, 1) * np.clip((tb - t) / 3, 0, 1)
def put(sig, at, gain):
    i = int(at * SR); n = min(len(sig), N - i)
    if n > 0: mix[i:i + n] += sig[:n] * gain
def ring(dur=2.6):
    out = np.zeros(int(dur * SR), np.float32)
    for k, f in enumerate([880, 1318.5, 1046.5, 1568] * 6):
        i = int(k * 0.11 * SR) + (int(0.7 * SR) if k >= 12 else 0); n = int(0.18 * SR)
        if i + n < len(out):
            tt = np.arange(n) / SR; out[i:i + n] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.06)
    return out
def click():
    n = int(0.25 * SR); tt = np.arange(n) / SR
    x = sosfilt(sos("bandpass", [1500, 6000]), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.006)
    return x * 3 + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt / 0.05)
def hum(dur=4):
    tt = np.arange(int(dur * SR)) / SR
    x = (np.sin(2 * np.pi * 110 * tt) + 0.5 * np.sin(2 * np.pi * 165.5 * tt) + 0.3 * np.sin(2 * np.pi * 221 * tt))
    return (x * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * tt)) * np.clip(tt / 0.8, 0, 1) * np.clip((dur - tt) / 0.8, 0, 1)).astype(np.float32)
def thud():
    n = int(1.2 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 58 * tt) * np.exp(-tt / 0.18) * 1.5 + sosfilt(sos("lowpass", 400), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.05)).astype(np.float32)
def buzz():
    n = int(1.3 * SR); tt = np.arange(n) / SR; g = ((tt % 0.65) < 0.35).astype(np.float32)
    return np.sign(np.sin(2 * np.pi * 150 * tt)) * sosfilt(sos("lowpass", 600), np.ones(n, np.float32)) * g * 0.5
def ticks(dur=4):
    out = np.zeros(int(dur * SR), np.float32)
    for k, st in enumerate(np.arange(0, dur - 0.1, 0.5)):
        c = click()[:int(0.05 * SR)] * (1.0 if k % 2 == 0 else 0.7); i = int(st * SR); out[i:i + len(c)] += c
    return out
def sting():
    n = int(3.0 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 45 * tt) * np.exp(-tt / 0.6) * 1.4 + sosfilt(sos("bandpass", [200, 2000]), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.4) * 0.3).astype(np.float32)
def scrape(d=3.0):
    n = int(d * SR); tt = np.arange(n) / SR
    x = sosfilt(sos("bandpass", [60, 900]), rng.standard_normal(n).astype(np.float32))
    return (x / x.std() * np.minimum(1, tt / 0.3) * np.exp(-tt / 1.4)).astype(np.float32)
def chisel(d=4.0):
    out = np.zeros(int(d * SR), np.float32)
    for st in np.arange(0.1, d - 0.3, 0.62):
        c = click(); i = int(st * SR); out[i:i + len(c)] += c[:len(out) - i]
    return out
def splash():
    n = int(1.5 * SR); tt = np.arange(n) / SR
    return (sosfilt(sos("bandpass", [300, 5000]), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.35)).astype(np.float32)
def door():
    n = int(1.8 * SR); tt = np.arange(n) / SR
    f = 180 + 90 * np.sin(2 * np.pi * 0.8 * tt)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip(tt / 0.2, 0, 1) * np.exp(-tt / 0.9) * 0.5).astype(np.float32)
def chime():
    n = int(3 * SR); tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 1.2) for f in (523.3, 659.3, 784)).astype(np.float32) / 3
FX = dict(ring=ring, click=click, hum=hum, thud=thud, buzz=buzz, ticks=ticks, sting=sting, scrape=scrape, chisel=chisel, splash=splash, door=door, chime=chime)
for name, k, off, g, *arg in C.get("sfx", []):
    put(FX[name](*arg), bounds[k - 1] + off, g)
mix *= 0.9 / (np.abs(mix).max() + 1e-9)
wf.write(f"{D}/mix.wav", SR, (mix * 32767).astype(np.int16))
# rain overlay frames (uint8)
RAINK = S.get("rain", set())
rainov = None
if RAINK:
    rr = np.random.default_rng(3); rainov = np.zeros((48, H, W), np.uint8)
    xs = rr.uniform(0, W, 900); ys = rr.uniform(0, H, 900); ls = rr.uniform(20, 70, 900); al_ = rr.uniform(40, 120, 900)
    for f in range(48):
        im = Image.new("L", (W, H)); from PIL import ImageDraw; dr = ImageDraw.Draw(im)
        for x, y, l, a in zip(xs, ys, ls, al_):
            yy = (y + f * 38) % H; dr.line([(x, yy), (x - l * 0.12, yy + l)], fill=int(a), width=2)
        rainov[f] = np.asarray(im)
imgs = {}
def get(k):
    if k not in imgs:
        for old in [x for x in imgs if x < k - 1 or x > k + 1]: del imgs[old]
        imgs[k] = Image.open(f"{D}/scenes/{k:02d}.jpg").convert("RGB")
    return imgs[k]
tmp = f"{D}/_video.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
    "-r", str(FPS), "-i", "-", "-i", f"{D}/mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
    "-shortest", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
nf = int(T * FPS); XF = 0.35
def frame(k, ts):
    a, b = bounds[k - 1], bounds[k]; u = (ts - a) / max(b - a, 0.01)
    im = get(k); iw, ih = im.size
    mode = k % 4
    z = 1.0 + 0.08 * u if mode in (0, 2) else 1.08 - 0.08 * u
    cw = iw / z; s = cw / W
    px = (iw - cw) / 2 + (0.3 if mode == 1 else -0.3 if mode == 3 else 0) * (iw - cw) * (u - 0.5)
    py = (ih - cw * H / W) / 2 + (0.2 * (ih - cw * H / W) * (u - 0.5) if mode == 2 else 0)
    if k in SHAKE: px += SHAKE[k] * np.sin(ts * 47); py += SHAKE[k] * np.cos(ts * 39)
    return np.asarray(im.transform((W, H), Image.AFFINE, (s, 0, px, 0, s, py), resample=Image.BILINEAR)).astype(np.float32)
for f in range(nf):
    ts = f / FPS
    k = max(i for i in range(len(times)) if times[i] <= ts) + 1
    arr = frame(k, ts)
    if k > 1 and ts - bounds[k - 1] < XF:   # short crossfade from previous scene
        w = (ts - bounds[k - 1]) / XF
        pa = frame(k - 1, ts)
        arr = arr * w + pa * (1 - w)
    if k in RAINK: arr += rainov[f % 48][..., None].astype(np.float32) * np.array([0.35, 0.4, 0.5], np.float32)
    if ts < 0.6: arr *= ts / 0.6
    if ts > T - 1.0: arr *= max(0, (T - ts) / 1.0)
    p.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
    if f % 1500 == 0: print("frame", f, "/", nf, flush=True)
p.stdin.close()
if p.wait() == 0: os.replace(tmp, f"{D}/episode.mp4"); print("done", f"{D}/episode.mp4")
