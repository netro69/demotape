"""Session 33 — fan site sections round 2 (correct filenames) + MusicBrainz releases + MB artist detail."""
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


# 1. Fan site: try the section pages linked from the discography page
CANDIDATES = {
    "storia": ["prozacstor.htm", "stor.htm", "storia.htm", "PROZSTOR.HTM", "Storia.htm"],
    "concerti": ["prozacconc.htm", "conc.htm", "concerti.htm", "PROZCONC.HTM"],
    "testaplastica": ["prozactp.htm", "tp.htm", "testaplastica.htm"],
    "acidoacida": ["prozacaa.htm", "aa.htm", "acidoacida.htm"],
    "stampa": ["prozacstamp.htm", "stamp.htm", "stampa.htm"],
    "down": ["down.htm"],
    "dilemmi": ["dilemmi.htm"],
}
for name, cands in CANDIDATES.items():
    got = False
    for c in cands:
        for base in ["https://www.giovanniweb.it/prozac/", "https://www.giovanniweb.it/prozac+/"]:
            url = base + c
            raw = fetch(url)
            if not raw.startswith("__FETCH_ERROR__") and len(raw) > 500:
                txt = strip(raw)
                with open(BASE + "s33_fan_%s.txt" % name, "w", encoding="utf-8") as f:
                    f.write(txt)
                print("fan %-14s: %5d chars (%s)" % (name, len(txt), url))
                got = True
                break
        if got:
            break
    if not got:
        print("fan %-14s: not found" % name)

# 2. MusicBrainz releases for Prozac+ (40db1288)
mbid = "40db1288-885d-417b-8056-91d7a002ad0e"
j = fetch("https://musicbrainz.org/ws/2/artist/%s?inc=releases+release-groups&fmt=json" % mbid)
with open(BASE + "s33_mb_releases.json", "w") as f:
    f.write(j)
try:
    d = json.loads(j)
    print("\n=== MusicBrainz: %d release-groups ===" % len(d.get("release-groups", [])))
    for rg in d.get("release-groups", []):
        year = "-"
        for rel in rg.get("releases", [])[:1]:
            year = rel.get("date", "-")[:4]
        print("  %s | %s | %s | %s" % (rg.get("primary-type", "-"), (rg.get("title") or "")[:60], year, rg["id"][:8]))
except Exception as e:
    print("MB releases parse err:", e, j[:200])
