"""Session 30 — check IA item metadata + YouTube rips for Massimo Volume."""
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


# 1. IA item metadata
for ident in ["massimo-volume-vittoria-burattini", "42IlNuotatoreCheever", "Roxyto2406.04.2011"]:
    j = fetch("https://archive.org/metadata/%s" % ident)
    print("=== IA: %s ===" % ident)
    if j.startswith("__FETCH_ERROR__"):
        print(j)
    else:
        try:
            meta = json.loads(j)
            m = meta.get("metadata", {})
            print("title:", m.get("title"))
            print("desc:", str(m.get("description"))[:400])
            print("creator:", m.get("creator"))
            files = meta.get("files", [])
            print("files (%d):" % len(files))
            for f in files[:10]:
                print("  -", f.get("name"), "|", f.get("format"), "|", f.get("size"))
        except Exception as e:
            print("parse error:", e)
    print()

# 2. YouTube search via piped/invidious API
for q in ["massimo volume demo nero", "massimo volume stanze full album", "massimo volume lungo i bordi"]:
    print("=== YouTube search: %s ===" % q)
    qe = urllib.parse.quote(q)
    j = fetch("https://pipedapi.kavin.rocks/search?q=%s&filter=music_songs" % qe)
    if j.startswith("__FETCH_ERROR__"):
        j = fetch("https://pipedapi.kavin.rocks/search?q=%s&filter=videos" % qe)
    if j.startswith("__FETCH_ERROR__"):
        print(j)
    else:
        try:
            items = json.loads(j).get("items", [])[:8]
            for it in items:
                print("  YT:", it.get("title", "")[:80], "|", it.get("url"), "|", it.get("uploaderName"))
        except Exception as e:
            print("parse error:", e, "|", j[:200])
    print()
