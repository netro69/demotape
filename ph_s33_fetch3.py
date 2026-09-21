"""Session 33 — fetch fan-site sections, MusicBrainz, Discogs, Wayback for official site."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


def strip(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;?", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


# 1. Fan site sections (giovanniweb.it/prozac/*)
for name, path in [("storia", "prozacstor.htm"), ("concerti", "prozacconc.htm"), ("stampa", "prozacstamp.htm")]:
    for prefix in ["", "uk/"]:
        url = "https://www.giovanniweb.it/prozac/%s%s" % (prefix, path)
        raw = fetch(url)
        if not raw.startswith("__FETCH_ERROR__"):
            txt = strip(raw)
            with open(BASE + "s33_fan_%s.txt" % name, "w", encoding="utf-8") as f:
                f.write(txt)
            print("fan %s: %d chars (%s)" % (name, len(txt), url))
            break
    else:
        # try index to discover real filenames
        idx = fetch("https://www.giovanniweb.it/prozac/")
        links = sorted(set(re.findall(r'href="([^"]+)"', idx))) if not idx.startswith("__FETCH_ERROR__") else []
        print("fan %s: FAILED. Index links: %s" % (name, links[:40]))
        with open(BASE + "s33_fan_index.txt", "w", encoding="utf-8") as f:
            f.write(strip(idx) if not idx.startswith("__FETCH_ERROR__") else idx)
        break

# 2. MusicBrainz artist search
j = fetch("https://musicbrainz.org/ws/2/artist/?query=artist:%22Prozac%2B%22&fmt=json")
with open(BASE + "s33_mb_artist.json", "w") as f:
    f.write(j)
try:
    d = json.loads(j)
    for a in d.get("artists", [])[:5]:
        print("MB artist: %s | %s | %s | score=%d" % (a["id"], a["name"], a.get("country", "-"), a.get("score", 0)))
except Exception as e:
    print("MB parse err:", e, j[:120])

# 3. Wayback Machine — official site candidates
for site in ["prozacplus.com", "prozac.it", "prozacplus.it", "www.prozacplus.com"]:
    u = "http://archive.org/wayback/available?url=%s" % site
    j = fetch(u)
    print("WB %s -> %s" % (site, j[:200]))

# 4. Wayback CDX search for any prozac-related fan/official sites
u = ("http://web.archive.org/cdx/search/cdx?url=*.prozacplus.com&output=json&limit=20")
j = fetch(u)
print("CDX prozacplus.com:", j[:400])
