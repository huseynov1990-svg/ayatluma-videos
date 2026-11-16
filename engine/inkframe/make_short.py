"""Make a vertical 1080x1920 Short from a finished episode.
usage: python3 make_short.py EPDIR "start phrase" "end phrase" "HOOK LINE 1|HOOK LINE 2" ACCENT_HEX OUT.mp4 ["CTA text"]
Times come from EPDIR/voice.json (+0.6 s lead, as in the build scripts).
"""
import sys, json, subprocess, os, re

LEAD = 0.6
ep, p0, p1, hook, acc, out = sys.argv[1:7]
cta = sys.argv[7] if len(sys.argv) > 7 else "FULL EPISODE ON THE CHANNEL"
a = json.load(open(f"{ep}/voice.json"))
ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
full = "".join(ch)
i0 = full.find(p0); i1 = full.find(p1, i0)
assert i0 >= 0 and i1 >= 0, (p0, p1)
i1e = i1 + len(p1) - 1
t0 = max(0.0, st[i0] + LEAD - 0.25)
t1 = en[i1e] + LEAD + 0.6
dur = t1 - t0

# words with times (relative to t0)
words, cur, ws = [], "", None
for k in range(i0, i1e + 1):
    c = ch[k]
    if c.isspace():
        if cur: words.append((cur, ws, en[k - 1])); cur = ""
    else:
        if not cur: ws = st[k]
        cur += c
if cur: words.append((cur, ws, en[i1e]))
words = [(w, s + LEAD - t0, e + LEAD - t0) for w, s, e in words]

def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def bgr(hexc):
    hexc = hexc.lstrip("#"); return f"&H00{hexc[4:6]}{hexc[2:4]}{hexc[0:2]}&"
A = bgr(acc)
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Inter Display Black,96,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H80000000&,1,0,0,0,100,100,0,0,1,8,3,8,60,60,190,1
Style: Hook2,Inter Display Black,96,{A},{A},&H00000000&,&H80000000&,1,0,0,0,100,100,0,0,1,8,3,8,60,60,310,1
Style: Cap,Inter Display Black,78,&H00FFFFFF&,{A},&H00000000&,&H80000000&,1,0,0,0,100,100,0,0,1,7,2,2,60,60,520,1
Style: Cta,Inter Display Black,58,{A},{A},&H00000000&,&H80000000&,1,0,0,0,100,100,0,0,1,6,2,2,60,60,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
h = hook.split("|")
ass += f"Dialogue: 1,{ts(0)},{ts(dur)},Hook,,0,0,0,,{{\\fad(150,0)}}{h[0]}\n"
if len(h) > 1:
    ass += f"Dialogue: 1,{ts(0.2)},{ts(dur)},Hook2,,0,0,0,,{{\\fad(150,0)}}{h[1]}\n"
# captions: chunks of up to 3 words, current word in accent colour
chunks, c = [], []
for w in words:
    c.append(w)
    if len(c) == 3 or re.search(r"[.,!?;:]$", w[0]):
        chunks.append(c); c = []
if c: chunks.append(c)
for chunk in chunks:
    for j, (w, s, e) in enumerate(chunk):
        endt = chunk[j + 1][1] if j + 1 < len(chunk) else e + 0.15
        txt = " ".join((f"{{\\c{A}}}{x[0].upper()}{{\\c&H00FFFFFF&}}" if k == j else x[0].upper()) for k, x in enumerate(chunk))
        ass += f"Dialogue: 0,{ts(s)},{ts(endt)},Cap,,0,0,0,,{txt}\n"
ass += f"Dialogue: 2,{ts(dur-3.2)},{ts(dur)},Cta,,0,0,0,,{{\\fad(200,0)}}{cta} ▲\n"
assf = out + ".ass"
open(assf, "w").write(ass)

vf = (f"[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.28[bg];"
      f"[b]scale=1080:-2[fg];[bg][fg]overlay=0:620,ass='{assf}',fade=t=in:d=0.25,format=yuv420p[v]")
af = f"afade=t=in:d=0.2,afade=t=out:st={dur-0.8:.2f}:d=0.8"
tmp = out.replace(".mp4", "._tmp.mp4")
r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", f"{ep}/episode.mp4",
    "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", af, "-c:v", "libx264", "-preset", "faster", "-crf", "22",
    "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp])
if r.returncode == 0:
    os.replace(tmp, out); os.remove(assf); print(f"ok {out} {dur:.1f}s")
