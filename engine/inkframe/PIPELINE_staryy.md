# Inkframe Stories — daily production pipeline (for Claude)

Channel: Inkframe Stories, @inkframe.stories, channelId UC-3TZ_7BHntBBmOcdjKdKVQ (vidIQ platformAccountId the same).
Everything lives on the user's PC in D:\youtube\mult. Engine code: D:\youtube\mult\_engine (this folder).
Two series, one new episode of each per day, English:

| Series | Folder | Hero | Voice (ElevenLabs voice_id) | Accent | Length | Publish (Moscow) |
|---|---|---|---|---|---|---|
| WRONG NUMBER — interactive noir, viewers vote in comments | WrongNumber\S01E0X | Eli Brooks, courier (kit.eli) | Eric cjVigY5qzO86Huf0OWal | yellow #F2B705 | 4 min (~650 words) | 23:00 (15:00 New York) |
| I WAS THERE — Ava lives through a real historical event, first person | IWasThere\E0X | Ava (ava.ava, change costume/hat per era) | Sarah EXAVITQu4vr4xnSDxMaL | teal #2EC4B6 | 5–7 min (~900–1000 words) | 20:00 (12:00 New York) |

Reserve pilot (not scheduled): SIGNAL 7 (s7_*.py), voice Lily pFZP5JQG7iQjIQuC4Bku.

## Files
- kit.py — SVG drawing kit (Eli, stranger, case, phone, render() with grain/vignette, svg() defs). Set kit.ACC before calling svg() for a series accent.
- ava.py — Ava character (moods calm/worried/scared/smile/determined, hat None/"1912"/"helmet", coat & scarf colours).
- tts.py — ElevenLabs TTS with timestamps: `python3 tts.py say VOICE_ID narration.txt out_prefix` -> out_prefix.mp3 + .json. Key: ~/.eleven_key (copy from _engine\keys\eleven_key.txt). Model eleven_multilingual_v2.
- build_ep.py (Wrong Number), build_iwt.py (I Was There), build_s7.py — `python3 build_X.py <epdir>`; epdir has scenes/NN.jpg (2304x1296), voice.mp3, voice.json. Edit ANCHORS (first words of each scene, in order, unique), scene-type sets and the SFX block for each new episode. Output epdir/episode.mp4.
- ep1_scenes.py / scenes_ep1.py / s7_scenes.py — examples of a full episode's scenes. thumbs*.py — thumbnail examples. brand.py — channel avatar/banner.
- deps: pip install --break-system-packages numpy scipy pillow; apt has ffmpeg + rsvg-convert; fonts Inter / Inter Display.

## Daily steps (per series)
1. Read state.json (next episode numbers, story so far, last video ids, chosen topics).
2. WRONG NUMBER: read comments of the last episode (vidiq_video_comments), count OPEN/DELIVER-style votes, the winner decides the next episode. Write the next ~650-word script: hook in first 2 lines, subscribe+bell+comment call in the middle and at the end, a new two-option vote at the end.
   I WAS THERE: pick the next topic (viewer suggestions in comments first, then the topic list in state.json). Verify facts with web search. Old history first; recent disasters only respectfully, no graphic detail.
3. TTS -> voice.mp3/json. 4. Draw ~35-50 scenes (new compositions every episode — never repeat an episode's look; YouTube demonetises repetitive/mass-produced content). Check a contact sheet.
5. Build (render ~20-25 min). 6. 3 thumbnails: huge emotional face, 2–4 words, high contrast. 7. SEO: title (curiosity + series + Ep N), description with hook, chapters from voice.json, hashtags, "Voice: AI narration (ElevenLabs)", 10-15 tags.
8. Upload: re-encode `ffmpeg -i episode.mp4 -c:v libx264 -preset faster -crf 27 -c:a copy -movflags +faststart up.mp4` (must be < 120 MB), `curl -F "files[]=@up.mp4" https://uguu.se/upload` -> url, vidiq_video_upload(url) -> uploadId; thumbnail: upload jpg to uguu, vidiq_upload_image(url) -> imageId.
9. vidiq_social_post_draft_create: YOUTUBE, platformAccountId UC-3TZ_7BHntBBmOcdjKdKVQ, privacyStatus public, publishAt (UTC), categoryId 1, tags, thumbnailImageId. Then ASK THE USER for "да" (vidIQ requires the user's approval of each draft). After "да": vidiq_social_post_publish, check vidiq_social_post_status.
10. After upload, in the built-in browser open studio.youtube.com/video/<id>/edit and set "Нет, это видео не для детей", Save (vidIQ leaves it unset). Add to the series playlist.
11. Save to PC: episode folder (FINAL mp4, script, 3 thumbs, SEO.txt) + updated state.json.
12. Every 2–3 weeks: vidiq_channel_analytics_extended report=audience (when viewers are online) and move publish times.

## Shorts (3 per episode, 6 per day)
make_short.py EPDIR "first words" "last words" "HOOK LINE 1|HOOK LINE 2" ACCENT OUT.mp4 ["CTA"] -> 1080x1920 Short cut from episode.mp4: blurred background, the 16:9 picture in the middle, big 2-line hook on top, word-by-word captions, CTA at the end. Pick 3 self-contained 25-55 s moments with the strongest hooks (opening hook, mid-episode reveal, the cliffhanger/vote). Schedule with Metricool youtubeData.type "short", title ending "#shorts", description pointing to the full episode. Slots (Moscow): 15:00, 17:00, 19:00, 21:30, 01:00, 03:00, alternating series.
