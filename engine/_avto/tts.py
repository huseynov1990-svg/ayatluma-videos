# Gemini 3.8 TTS: tekst = tolko slova; stil -> speech_metadata.style (ne chitaetsya vslukh)
import json,sys,base64,urllib.request,subprocess
import os
key=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','.secrets','gemini_key.txt')).read().strip()
model,voice,style,text,out=sys.argv[1:6]
part={"text":text}
if style.strip(): part["speech_metadata"]={"style":style}
body={"contents":[{"role":"user","parts":[part]}],
 "generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"voice":voice}}}}
req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":key})
d=json.load(urllib.request.urlopen(req,timeout=180))
b=base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
tmp=out+'.raw'; open(tmp,'wb').write(b)
src=["-i",tmp] if b[:4]==b'RIFF' else ["-f","s16le","-ar","24000","-ac","1","-i",tmp]
subprocess.run(["ffmpeg","-y","-loglevel","error",*src,out],check=True,stdin=subprocess.DEVNULL)
import os; os.remove(tmp)
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True)
print("ok",float(r.stdout),"sec",d.get("usageMetadata",{}).get("candidatesTokenCount"))
