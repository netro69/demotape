"""Session 33 — YouTube results dedupe/relevance + Italian magazine/fanzine coverage search via web."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"

with open(BASE + "s33_yt_all.json", encoding="utf-8") as f:
    all_results = json.load(f)

# --- Dedupe by videoId, classify ---
videos = {}
for q, items in all_results.items():
    for it in items:
        vid = it.get("videoId")
        if not vid:
            continue
        e = videos.setdefault(vid, {"title": it.get("title", ""), "author": it.get("author", ""),
                                    "length": it.get("lengthSeconds", 0), "published": it.get("publishedText", ""),
                                    "views": it.get("viewCount", 0), "queries": []})
        e["queries"].append(q)

print("=== %d unique videos ===" % len(videos))
# relevance scoring: live/rare > official
for vid, e in sorted(videos.items(), key=lambda kv: -kv[1]["length"]):
    t = e["title"]
    print("  %s | %4ds | %s | %s" % (vid, e["length"], t[:85], e["author"][:25]))

with open(BASE + "s33_yt_dedup.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=1)
print("saved s33_yt_dedup.json")
