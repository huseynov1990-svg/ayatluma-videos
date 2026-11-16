"""ElevenLabs TTS with character timestamps.
usage: python3 tts.py voices               -> list voices available to this key
       python3 tts.py say VOICE_ID text.txt out_prefix [model]
Key is read from env ELEVEN_KEY or file ~/.eleven_key
"""
import sys, os, json, base64, urllib.request

def key():
    k = os.environ.get("ELEVEN_KEY")
    if not k:
        k = open(os.path.expanduser("~/.eleven_key")).read().strip()
    return k

def req(path, body=None):
    url = "https://api.elevenlabs.io" + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                               headers={"xi-api-key": key(), "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=300) as f:
        return json.loads(f.read())

if sys.argv[1] == "voices":
    v = req("/v1/voices")
    for x in v["voices"]:
        l = x.get("labels", {})
        print(x["voice_id"], "|", x["name"], "|", x.get("category"), "|", l.get("gender"), l.get("age"), l.get("accent"), l.get("description") or l.get("descriptive"), l.get("use_case"))
    u = req("/v1/user/subscription")
    print("credits:", u.get("character_count"), "/", u.get("character_limit"), "tier:", u.get("tier"))
elif sys.argv[1] == "say":
    vid, txtfile, out = sys.argv[2], sys.argv[3], sys.argv[4]
    model = sys.argv[5] if len(sys.argv) > 5 else "eleven_multilingual_v2"
    text = open(txtfile).read().strip()
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}
    r = req(f"/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", body)
    open(out + ".mp3", "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump(r.get("alignment") or r.get("normalized_alignment"), open(out + ".json", "w"))
    print("ok", out)
