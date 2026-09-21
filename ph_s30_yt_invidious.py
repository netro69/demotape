"""Session 30 — YouTube rips via Invidious + Burattini IA item details."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# 1. Burattini item — full meta xml to understand what it is
j = fetch("https://archive.org/metadata/massimo-volume-vittoria-burattini")
try:
    meta = json.loads(j)
    print("=== Burattini item full metadata ===")
    print(json.dumps(meta.get("metadata", {}), indent=1, ensure_ascii=False)[:1200])
except Exception as e:
    print("err", e)

# 2. Invidious search (user's instance)
INV = "https://yt.chocolatemoo53.com"
for q in ["massimo volume demo nero", "massimo volume stanze 1993", "massimo volume live 1994", "massimo volume lungo i bordi full album"]:
    qe = urllib.parse.quote(q)
    j = fetch("%s/api/v1/search?q=%s&type=video" % (INV, qe))
    print()
    print("=== YT: %s ===" % q)
    if j.startswith("__FETCH_ERROR__"):
        print(j)
    else:
        try:
            items = json.loads(j)[:8]
            for it in items:
                secs = it.get("lengthSeconds", 0)
                print("  - %s | https://www.youtube.com/watch?v=%s | %ds | %s" % (
                    it.get("title", "")[:90], it.get("videoId"), secs, (it.get("author") or "")[:30]))
        except Exception as e:
            print("parse error:", e, "|", j[:150])
