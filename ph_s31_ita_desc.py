"""Session 31 — extract ITA TAPES video description via grep-style scan."""
import re

raw = open("/tmp/s31_yt_ita_tapes.txt", encoding="utf-8", errors="ignore").read()
# try multiple description patterns
for pat in [r'"shortDescription":"((?:[^"\\]|\\.)*)"',
            r'"description":\{"simpleText":"((?:[^"\\]|\\.)*)"']:
    m = re.search(pat, raw)
    if m:
        desc = m.group(1)
        desc = desc.replace("\\n", "\n").replace('\\"', '"')
        print("=== DESCRIPTION ===")
        print(desc[:1500])
        break
m = re.search(r'"ownerChannelName":"([^"]+)"', raw)
if m:
    print("CHANNEL:", m.group(1))
m = re.search(r'"publishDate":"([^"]+)"', raw)
if m:
    print("PUBLISHED:", m.group(1))
m = re.search(r'"channelId":"(UC[^"]+)"', raw)
if m:
    print("CHANNEL_ID:", m.group(1))
# title
m = re.search(r'"title":"((?:[^"\\]|\\.)*)"', raw)
if m:
    print("TITLE:", m.group(1)[:120])
