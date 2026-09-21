"""Session 31 — fetch ITALIAN TAPES ARCHIVE video page + more YT searches."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=40):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# 1. ITALIAN TAPES ARCHIVE video page -> channel + description
raw = fetch("https://www.youtube.com/watch?v=qN-xpWFuL5I")
open("/tmp/s31_yt_ita_tapes.txt", "w").write(raw)
print("ita tapes video:", len(raw))

# 2. more YT searches
for q in ["massimo volume club privè full album", "massimo volume 1994 live",
          "italian tapes archive massimo volume"]:
    u = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
    raw = fetch(u)
    open("/tmp/s31_yth_%s.txt" % q.replace(" ", "_"), "w").write(raw)
    print("yt", q, len(raw))

# 3. DDG: rutracker lungo i bordi
for name, q in [("ddg_rutracker2", '"massimo volume" rutracker lungo'),
                ("ddg_clubpriv", '"massimo volume" "club privè" torrent OR download')]:
    u = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    raw = fetch(u)
    open("/tmp/s31_%s.txt" % name, "w").write(raw)
    print(name, len(raw))
