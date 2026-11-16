# INKFRAME STORIES — ежедневная задача (облако, без компьютера пользователя)

Канал YouTube **Inkframe Stories** (@inkframe.stories, channelId UC-3TZ_7BHntBBmOcdjKdKVQ), английский.
Два сериала, **по одной новой серии каждый день**, плюс Shorts из них. Пользователь в процессе не участвует.
Старая инструкция (ПК + uguu + vidIQ с подтверждением «да») — `PIPELINE_staryy.md`: оттуда брать ТОЛЬКО описание движка, сериалов и правил сценария. Загрузка и публикация теперь — как у остальных каналов (GitHub + Metricool).

| Сериал | Герой | Голос ElevenLabs (voice_id) | Акцент | Длина | Публикация (МСК) |
|---|---|---|---|---|---|
| **I WAS THERE** — Ava проживает реальное историческое событие от первого лица | Ava (`ava.py`, костюм/головной убор по эпохе) | Sarah `EXAVITQu4vr4xnSDxMaL` | teal #2EC4B6 | 5–7 мин (900–1000 слов) | 20:00 |
| **WRONG NUMBER** — нуар-сериал про курьера Eli Brooks | Eli (`kit.py`) | Eric `cjVigY5qzO86Huf0OWal` | yellow #F2B705 | ~4 мин (~650 слов) | 23:00 |

## 0. Подготовка
```
add_repo huseynov1990-svg/ayatluma-videos (push); git clone --depth 1 … /home/claude/ayatluma-videos
E=/home/claude/ayatluma-videos/engine; I=$E/inkframe
pip install --break-system-packages numpy scipy pillow faster-whisper
which rsvg-convert || apt-get install -y librsvg2-bin    # нужно kit.py
fc-list | grep -i inter || (шрифт Inter: pip download / положить в ~/.fonts — см. kit.py)
```
Ключ ElevenLabs: Google Drive → папка AUTO_VIDEO → `eleven_key.txt` (read_file_content) → записать в `~/.eleven_key` (chmod 600). НИКОГДА не коммитить ключ.

## 1. Состояние
`$I/state.json` — номера следующих серий, краткое содержание прошлых, очередь тем I Was There, id видео. Читать в начале, обновлять и коммитить в конце.

## 2. Сценарии (каждый день новые)
- **I WAS THERE**: следующая тема из `topic_queue` (если в комментариях/описании канала нет лучшей). Факты проверить веб-поиском. Старая история в приоритете; недавние трагедии — бережно, без натурализма. Формат как `primery/IWT_E01_script.txt`: хук в первых 3 строках («My name is Ava…»), середина — призыв подписаться и вопрос в комментарии, конец — вопрос «куда Аве отправиться дальше?».
- **WRONG NUMBER**: продолжение по `state.json` (summary прошлой серии). Голосование зрителей НЕ проводим (читать комментарии нечем): серия 2 разрешает выбор из серии 1 так, как сильнее для сюжета, без слов «вы проголосовали». Каждая серия заканчивается клиффхэнгером и вопросом зрителям «What would you do?». Хук в первых 2 строках, призыв подписаться в середине и в конце. Формат как `primery/WN_S01E01_script.txt`.
- Текст для озвучки: только слова, без [тегов], без «[MIDDLE]» и «---» (их убрать перед TTS).

## 3. Сборка (по `PIPELINE_staryy.md`, разделы Files и Daily steps 3–7)
1. `python3 $I/tts.py say <voice_id> narration.txt <epdir>/voice` → voice.mp3 + voice.json.
2. Нарисовать 35–50 сцен (`scenes/NN.jpg`, 2304×1296) по образцу `ep1_scenes.py` / `scenes_ep1.py` — **каждая серия с новыми композициями** (YouTube не монетизирует однотипный контент). Посмотреть контакт-лист.
3. `python3 $I/build_iwt.py <epdir>` / `build_ep.py <epdir>` (поправить ANCHORS и блок SFX) → `episode.mp4` (~20–25 мин рендер).
4. 3 обложки (большое эмоциональное лицо, 2–4 слова, контраст) по `thumbs_ep1.py`; главная — A.
5. SEO: title (интрига + сериал + Ep N), описание с хуком, главы из voice.json, хэштеги, «Voice: AI narration (ElevenLabs)», 10–15 тегов. Образцы `primery/*_SEO.txt`.
6. Проверить: длительность, 5 кадров, звук (распознать первые 30 с — голос читает текст, без лишнего).

## 4. Публикация (Metricool, БЕЗ подтверждения пользователя)
- Бренд Metricool: **Inkframe Stories, id 8160878** (YouTube `UC-3TZ_7BHntBBmOcdjKdKVQ`, подключён 17.11.2026). **Если его нет** — собрать серии, загрузить на GitHub, ничего не публиковать и написать пользователю одной строкой: «Inkframe Stories не виден в Metricool аккаунта huseynovaamina2017@gmail.com — добавьте бренд туда».
- Файл ≤ 95 МБ: `ffmpeg -i episode.mp4 -c:v libx264 -preset faster -crf 26 -maxrate 6M -bufsize 12M -c:a aac -b:a 160k -movflags +faststart up.mp4`.
- `python3 $E/upload.py /home/claude/ayatluma-videos inkframe up.mp4 thumb_A.jpg` (имена файлов уникальные: `IWT_E02_*.mp4`, `WN_S01E02_*.mp4`) → raw-ссылки.
- `createScheduledPost`: providers youtube, youtubeData {title, type "video", privacy public, madeForKids false, category ENTERTAINMENT, tags, isAiGeneratedContent true}, videoThumbnailUrl = обложка A, text = описание. Время: I Was There 20:00 МСК, Wrong Number 23:00 МСК, ближайший будущий свободный слот.
- **Shorts**: по 2 на каждую серию (`make_short.py`, самые сильные 25–55-секундные моменты: хук и клиффхэнгер), youtubeData.type "short", title с «#shorts», в описании — «Full episode on the channel». Слоты (МСК): 15:00, 17:00, 19:00, 21:30, чередуя сериалы.
- Без повторов: перед публикацией проверить запланированные посты бренда и state.json.

## 5. В конце
- `state.json`: next_episode +1, добавить серию (title, summary, published, planner url). Коммит в main (без видео и ключей).
- Отчёт пользователю по-русски (SendUserMessage + push): обе серии (название, длина, время выхода, ссылки planner), Shorts, остаток символов ElevenLabs если виден в ответе API / ошибка 401-quota. Если ElevenLabs вернул ошибку лимита — НЕ подменять голос молча: собрать без публикации и написать пользователю «лимит ElevenLabs закончился, меняем голоса?».
