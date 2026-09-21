"""Session 31 — parse ITA TAPES video page + new YT searches + DDG."""
import html
import json
import re


def yt_videos(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", raw)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except Exception:
        return []
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                vid = v.get("videoId")
                title = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
                ch = v.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
                views = v.get("viewCountText", {}).get("simpleText", "")
                length = v.get("lengthText", {}).get("simpleText", "")
                out.append((vid, title, ch, views, length))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return out


# ITA TAPES video page: description + channel
raw = open("/tmp/s31_yt_ita_tapes.txt", encoding="utf-8", errors="ignore").read()
m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', raw)
if m:
    desc = m.group(1).encode().decode("unicode_escape", errors="ignore")
    print("=== ITA TAPES qN-xpWFuL5I description ===")
    print(desc[:1200])
m = re.search(r'"ownerChannelName":"([^"]+)"', raw)
if m:
    print("CHANNEL:", m.group(1))
m = re.search(r'"publishDate":"([^"]+)"', raw)
if m:
    print("PUBLISHED:", m.group(1))
print()

for q in ["massimo_volume_club_privè_full_album", "massimo_volume_1994_live",
          "italian_tapes_archive_massimo_volume"]:
    print("=" * 15, q, "=" * 15)
    for vid, title, ch, views, length in yt_videos("/tmp/s31_yth_%s.txt" % q)[:10]:
        print(f"  {vid} | {title[:65]} | {ch[:25]} | {views} | {length}")
    print()

for name in ["ddg_rutracker2", "ddg_clubpriv"]:
    print("=" * 15, name, "=" * 15)
    raw = open("/tmp/s31_%s.txt" % name, encoding="utf-8", errors="ignore").read()
    for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S):
        u = html.unescape(m.group(1))
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        print(" ", u[:120], "|", t[:70])
