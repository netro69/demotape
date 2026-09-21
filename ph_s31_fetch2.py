"""Session 31 — fetch mvstanze blog + YouTube search for MV rips via HTML."""
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


# 1. mvstanze blog (dedicated MV blog)
raw = fetch("http://mvstanze.blogspot.com/2005/02/demo.html")
open("/tmp/s31_mvstanze.txt", "w").write(raw)
print("mvstanze:", len(raw))

# 2. YouTube search via HTML (works without API)
for q in ["massimo volume stanze 1993", "massimo volume demo nero",
          "massimo volume radio blackout", "massimo volume il primo dio live"]:
    u = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
    raw = fetch(u)
    open("/tmp/s31_yth_%s.txt" % q.replace(" ", "_"), "w").write(raw)
    print("yt-html", q, len(raw))

# 3. RuTracker via site search on Google cache alternative (duckduckgo html)
u = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote('rutracker massimo volume')
raw = fetch(u)
open("/tmp/s31_ddg_rutracker.txt", "w").write(raw)
print("ddg rutracker:", len(raw))

u = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote('"massimo volume" site:archive.org')
raw = fetch(u)
open("/tmp/s31_ddg_ia.txt", "w").write(raw)
print("ddg ia:", len(raw))
