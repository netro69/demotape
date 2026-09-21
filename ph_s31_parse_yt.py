"""Session 31 — parse YouTube HTML search results + mvstanze blog + DDG results."""
import html
import json
import re


def yt_videos(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", raw)
    if not m:
        m = re.search(r"ytInitialData\s*=\s*(\{.*?\});", raw)
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


for q in ["massimo_volume_stanze_1993", "massimo_volume_demo_nero",
          "massimo_volume_radio_blackout", "massimo_volume_il_primo_dio_live"]:
    print("=" * 15, q, "=" * 15)
    for vid, title, ch, views, length in yt_videos("/tmp/s31_yth_%s.txt" % q)[:10]:
        print(f"  {vid} | {title[:70]} | {ch[:25]} | {views} | {length}")

print()
print("=" * 15, "mvstanze blog", "=" * 15)
raw = open("/tmp/s31_mvstanze.txt", encoding="utf-8", errors="ignore").read()
urls = re.findall(r'href=["\x27](https?://[^"\x27]+)["\x27]', raw)
keep = [u for u in urls if any(k in u.lower() for k in ["mediafire", "mega", "rapidshare", "zippy", "send", "4shared", "deposit", "download", ".rar", ".zip", ".mp3"])]
for u in sorted(set(keep))[:15]:
    print("LINK:", u)
txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
txt = re.sub(r"\s+", " ", txt)
m = re.search(r"Demo", txt)
if m:
    print("TXT:", txt[max(0, m.start() - 100):m.start() + 500])

print()
print("=" * 15, "DDG rutracker", "=" * 15)
raw = open("/tmp/s31_ddg_rutracker.txt", encoding="utf-8", errors="ignore").read()
for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S):
    u = html.unescape(m.group(1))
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
    print(" ", u[:110], "|", t[:70])

print()
print("=" * 15, "DDG archive.org", "=" * 15)
raw = open("/tmp/s31_ddg_ia.txt", encoding="utf-8", errors="ignore").read()
for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, re.S):
    u = html.unescape(m.group(1))
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
    print(" ", u[:110], "|", t[:70])
