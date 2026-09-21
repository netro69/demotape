"""Session 33 — Prozac+ underground source fetch (TPB, 1337x, RuTracker, IA, Usenet, YouTube via Invidious)."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
OUT = "/home/ubuntu/Projects/demotape/research_output/s33_%s.txt"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


def save(name, content):
    with open(OUT % name, "w", encoding="utf-8") as f:
        f.write(content)
    print("saved s33_%s.txt (%d bytes)" % (name, len(content)))


# 1. TPB (tpb.party mirror — worked in s30/31/32)
for q in ["prozac+", "acido acida", "testa plastica"]:
    qe = urllib.parse.quote(q)
    raw = fetch("https://tpb.party/search/%s/1/99/0" % qe)
    save("tpb_%s" % q.replace(" ", "_").replace("+", "plus"), raw)

# 2. 1337x
raw = fetch("https://1337x.to/search/prozac/1/")
save("1337x_prozac", raw)

# 3. RuTracker (clearnet attempt)
raw = fetch("https://rutracker.org/forum/tracker.php?nm=prozac")
save("rutracker_prozac", raw)

# 4. Internet Archive — multiple queries
for q in ["prozac acido", "acido acida", "testa plastica 1996", "prozac pordenone", "vox pop pordenone"]:
    qe = urllib.parse.quote('"%s"' % q if " " in q else q)
    j = fetch("https://archive.org/advancedsearch.php?q=%s&fl%%5B%%5D=identifier&fl%%5B%%5D=title&rows=20&output=json" % qe)
    save("ia_%s" % q.replace(" ", "_"), j)

# 5. YouTube via Invidious (user's instance)
INV = "https://yt.chocolatemoo53.com"
for q in ["prozac+ acido acida", "prozac+ testa plastica", "prozac+ live 1996", "prozac+ live 1998",
          "prozac+ pordenone", "mago accusani", "elisabetta imelio prozac", "prozac accuso",
          "prozac+ demo 1995", "prozac+ rock tenda"]:
    qe = urllib.parse.quote(q)
    j = fetch("%s/api/v1/search?q=%s&type=video" % (INV, qe))
    save("yt_%s" % q.replace(" ", "_").replace("+", "plus").replace("'", ""), j)

print("ALL FETCHES DONE")
