"""Build an episode: scenes + ElevenLabs voice (with timestamps) -> mp4.
usage: python3 build_ep.py ep1
"""
import sys, json, subprocess, os
import numpy as np
from PIL import Image
from scipy.signal import butter, sosfilt

EP = sys.argv[1]
D = EP
SR, FPS, W, H = 44100, 30, 1920, 1080
LEAD = 0.6          # silence before the first word
TAIL = 5.0          # hold on the last card

ANCHORS = ["My name is Ava.", "And tonight, I'm going to tell you", "April fourteenth, 1912.", "I was nineteen.",
 "She had found me a job", "And what a ship to cross it on.", "Longer than four city blocks.", "Electric lights, a swimming pool",
 "Even in third class", "We left Southampton", "That Sunday, the air turned sharp.", "The sea was perfectly flat.",
 "What I didn't know", "If you want to know what it was really like", "At 11:40 at night", "I felt it before I heard it.",
 "Up in the crow's nest", "The officers turned the ship", "At first, nobody was scared.", "But the man who designed her",
 "Just after midnight, the order came.", "Here is the part that still makes me angry.", "The Titanic had twenty lifeboats.",
 "The rule was women and children first.", "For people in third class", "A steward I had never met",
 "When I finally reached the boat deck", "And the band was still playing.", "At five past two", "I watched the lights of the Titanic",
 "At 2:18, the lights went out.", "At 2:20, she was gone.", "And then came the sound", "Most of the boats did not go back.",
 "Little by little, the voices stopped.", "We sat in that boat for hours.", "Then, a little after three thirty",
 "The Carpathia had heard the distress call", "About seven hundred people were saved.", "Three days later",
 "After that night, the world changed the rules.", "So that no one would ever have to hear", "I'm Ava. And I was there.",
 "Tomorrow, I will be somewhere else in history."]
EXTERIOR = set()
INTERIOR_RAIN = set()
STATION = {4, 5, 8, 9, 13, 15, 16, 20, 21, 25, 26}
SEA = {3, 6, 11, 12, 17, 19, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 42}
SHAKE = {16: 8, 31: 3}

# ---------- timing ----------
al = json.load(open(f"{D}/voice.json"))
chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
full = "".join(chars)
pos, times = 0, []
for a in ANCHORS:
    i = full.find(a, pos)
    if i < 0:
        i = full.lower().find(a.lower().strip('"'), pos)
    assert i >= 0, a
    times.append(starts[i] + LEAD); pos = i + 1
times[0] = 0.0
voice_end = ends[-1] + LEAD
T = voice_end + TAIL
bounds = times + [T]
print("duration %.1f s" % T)

# ---------- audio ----------
def load(path):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True)
    return np.frombuffer(p.stdout, np.float32).copy()
N = int(T * SR)
rng = np.random.default_rng(5)
def sos(k, f, o=2): return butter(o, f, btype=k, fs=SR, output="sos")
def env_seg(a, b, fade=0.8):
    e = np.zeros(N, np.float32); i0, i1 = int(a * SR), min(N, int(b * SR)); f = int(fade * SR)
    e[i0:i1] = 1
    r = np.arange(f) / f
    e[i0:i0 + f] *= r[:max(0, min(f, i1 - i0))] if i1 - i0 >= f else 1
    e[max(i0, i1 - f):i1] *= r[::-1][-(i1 - max(i0, i1 - f)):]
    return e
def ranges(ids):
    return [(bounds[k - 1], bounds[k]) for k in sorted(ids)]

mix = np.zeros(N, np.float32)
voice = load(f"{D}/voice.mp3")
v0 = int(LEAD * SR); mix[v0:v0 + len(voice)] += voice[:N - v0] * 1.0

noise = rng.standard_normal(N).astype(np.float32)
rain = sosfilt(sos("bandpass", [500, 8000]), noise); rain /= rain.std()
rain_muf = sosfilt(sos("lowpass", 700), noise); rain_muf /= rain_muf.std()
room = sosfilt(sos("lowpass", 180), rng.standard_normal(N).astype(np.float32)); room /= room.std()
t = np.arange(N) / SR
for a, b in ranges(EXTERIOR): mix += rain * env_seg(a, b) * 0.035
for a, b in ranges(INTERIOR_RAIN): mix += rain_muf * env_seg(a, b) * 0.03
for a, b in ranges(SEA): mix += sosfilt(sos('lowpass', 500), rain).astype(np.float32) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 6.5)) * env_seg(a, b) * 0.03
for a, b in ranges(STATION): mix += (room * 0.03 + 0.004 * np.sin(2 * np.pi * 100 * t)) * env_seg(a, b)

# music: dark drone + slow pulse in the tense part
drone = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 55.4 * t) + 0.4 * np.sin(2 * np.pi * 82.4 * t)
         + 0.25 * np.sin(2 * np.pi * 110.3 * t)) * (0.75 + 0.25 * np.sin(2 * np.pi * t / 9))
drone = sosfilt(sos("lowpass", 300), drone.astype(np.float32))
mix += drone * 0.018 * np.clip(t / 3, 0, 1) * np.clip((T - t) / 3, 0, 1)
tense_a, tense_b = bounds[14], bounds[34]
beat = np.zeros(N, np.float32)
for bt in np.arange(tense_a, tense_b, 0.92):
    i = int(bt * SR); n = int(0.35 * SR)
    if i + n < N:
        tt = np.arange(n) / SR
        beat[i:i + n] += np.sin(2 * np.pi * 52 * tt) * np.exp(-tt / 0.09)
mix += beat * 0.09 * np.clip((t - tense_a) / 20, 0, 1)

def put(sig, at, gain):
    i = int(at * SR); n = min(len(sig), N - i)
    if n > 0: mix[i:i + n] += sig[:n] * gain
def ring(dur=2.6):
    out = np.zeros(int(dur * SR), np.float32)
    for k, f in enumerate([880, 1318.5, 1046.5, 1568] * 6):
        i = int(k * 0.11 * SR) + (int(0.7 * SR) if k >= 12 else 0); n = int(0.18 * SR)
        if i + n < len(out):
            tt = np.arange(n) / SR
            out[i:i + n] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.06)
    return out
def click():
    n = int(0.25 * SR); tt = np.arange(n) / SR
    x = sosfilt(sos("bandpass", [1500, 6000]), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.006)
    return x * 3 + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt / 0.05)
def hum(dur):
    tt = np.arange(int(dur * SR)) / SR
    x = (np.sin(2 * np.pi * 110 * tt) + 0.5 * np.sin(2 * np.pi * 165.5 * tt) + 0.3 * np.sin(2 * np.pi * 221 * tt))
    return (x * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * tt)) * np.clip(tt / 0.8, 0, 1) * np.clip((dur - tt) / 0.8, 0, 1)).astype(np.float32)
def thud():
    n = int(1.2 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 58 * tt) * np.exp(-tt / 0.18) * 1.5 + sosfilt(sos("lowpass", 400), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.05)).astype(np.float32)
def buzz():
    n = int(1.3 * SR); tt = np.arange(n) / SR
    g = ((tt % 0.65) < 0.35).astype(np.float32)
    return np.sign(np.sin(2 * np.pi * 150 * tt)) * sosfilt(sos("lowpass", 600), np.ones(n, np.float32)) * g * 0.5
def ticks(dur):
    out = np.zeros(int(dur * SR), np.float32)
    for k, st in enumerate(np.arange(0, dur - 0.1, 0.5)):
        c = click()[:int(0.05 * SR)] * (1.0 if k % 2 == 0 else 0.7); i = int(st * SR); out[i:i + len(c)] += c
    return out
def sting():
    n = int(3.0 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * 45 * tt) * np.exp(-tt / 0.6)
    sw = sosfilt(sos("bandpass", [200, 2000]), rng.standard_normal(n).astype(np.float32)) * np.exp(-tt / 0.4)
    return (boom * 1.4 + sw * 0.3).astype(np.float32)

def scrape(d=3.0):
    n = int(d * SR); tt = np.arange(n) / SR
    x = sosfilt(sos("bandpass", [60, 900]), rng.standard_normal(n).astype(np.float32))
    return (x / x.std() * np.minimum(1, tt / 0.3) * np.exp(-tt / 1.4)).astype(np.float32)
def rocket():
    n = int(1.6 * SR); tt = np.arange(n) / SR
    whoosh = sosfilt(sos("bandpass", [800, 4000]), rng.standard_normal(n).astype(np.float32)) * np.clip(tt / 0.8, 0, 1) * (tt < 0.9)
    pop = np.zeros(n, np.float32); i = int(0.9 * SR); m = int(0.5 * SR); t2 = np.arange(m) / SR
    pop[i:i + m] = (np.sin(2 * np.pi * 70 * t2) * np.exp(-t2 / 0.15) + sosfilt(sos("lowpass", 2000), rng.standard_normal(m).astype(np.float32)) * np.exp(-t2 / 0.05))
    return (whoosh * 0.4 + pop).astype(np.float32)
def melody(d):
    notes = [392, 440, 392, 329.6, 293.7, 329.6, 392, 0, 349.2, 392, 349.2, 293.7, 261.6, 293.7, 329.6, 0]
    out = np.zeros(int(d * SR), np.float32); k = 0; tpos = 0.0
    while tpos < d - 1:
        f = notes[k % len(notes)]; n = int(0.55 * SR); i = int(tpos * SR); tt = np.arange(n) / SR
        if f and i + n < len(out):
            out[i:i + n] += (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.35)
        k += 1; tpos += 0.55
    return out
put(sting(), bounds[2], 0.35); put(sting(), bounds[43], 0.3)
put(scrape(), bounds[15] + 0.2, 0.06)
put(rocket(), bounds[26] + 0.5, 0.12); put(rocket(), bounds[26] + 2.6, 0.1); put(rocket(), bounds[36] + 1.0, 0.06)
put(melody(bounds[28] - bounds[27] + 1.5), bounds[27], 0.035)
mix *= 0.9 / (np.abs(mix).max() + 1e-9)
import scipy.io.wavfile as wf
wf.write(f"{D}/mix.wav", SR, (mix * 32767).astype(np.int16))

# ---------- video ----------
rainov = None
imgs = {}
def get(k):
    if k not in imgs:
        imgs.clear(); imgs[k] = Image.open(f"{D}/scenes/{k:02d}.jpg").convert("RGB")
    return imgs[k]
tmp = f"{D}/_video.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
    "-r", str(FPS), "-i", "-", "-i", f"{D}/mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
    "-shortest", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
nf = int(T * FPS)
for f in range(nf):
    ts = f / FPS
    k = max(i for i in range(len(times)) if times[i] <= ts) + 1
    a, b = bounds[k - 1], bounds[k]
    u = (ts - a) / max(b - a, 0.01)
    im = get(k); iw, ih = im.size
    z = 1.0 + 0.07 * u if k % 2 else 1.07 - 0.07 * u
    cw = iw / z; s = cw / W
    px = (iw - cw) / 2 + (0.25 if k % 3 == 0 else -0.25) * (iw - cw) * (u - 0.5)
    py = (ih - cw * H / W) / 2
    if k in SHAKE:
        px += SHAKE[k] * np.sin(ts * 47); py += SHAKE[k] * np.cos(ts * 39)
    fr = im.transform((W, H), Image.AFFINE, (s, 0, px, 0, s, py), resample=Image.BICUBIC)
    arr = np.asarray(fr).astype(np.float32)
    if k in EXTERIOR:
        arr += rainov[f % 300][..., None] * np.array([0.35, 0.4, 0.5], np.float32)
    if ts < 0.6: arr *= ts / 0.6
    if ts > T - 1.0: arr *= max(0, (T - ts) / 1.0)
    p.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes())
p.stdin.close()
if p.wait() == 0:
    os.replace(tmp, f"{D}/episode.mp4"); print("done", f"{D}/episode.mp4")
