import json,sys,base64,urllib.request
import os
key=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','.secrets','gemini_key.txt')).read().strip()
model,prompt,out=sys.argv[1:4]; ar=sys.argv[4] if len(sys.argv)>4 else "9:16"
body={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":ar}}}
req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":key})
d=json.load(urllib.request.urlopen(req,timeout=180))
for p in d["candidates"][0]["content"]["parts"]:
    if "inlineData" in p: open(out,"wb").write(base64.b64decode(p["inlineData"]["data"])); print("ok",out); break
else: print("no image", json.dumps(d)[:500])
