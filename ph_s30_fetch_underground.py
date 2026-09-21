"""Session 30 (resumed) — fetch underground sources for Massimo Volume, save raw to files."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11, Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


out = []

# 1. TPB search
raw = fetch("https://thepiratebay.org/search.php?q=massimo+volume&video=on&audio=on")
out.append(("tpb", raw))
print("TPB fetched:", len(raw))

# 2. 1337x search
raw = fetch("https://1337x.to/search/massimo+volume/1/")
out.append(("1337x", raw))
print("1337x fetched:", len(raw))

# 3. Archive.org advanced search — massimo volume
j = fetch("https://archive.org/advancedsearch.php?q=%22massimo+volume%22&fl%5B%5D=identifier&fl%5B%5D=title&rows=30&output=json")
out.append(("ia_search", j))
print("IA search fetched:", len(j))

# 4. Archive.org audio search — clementi / stanze / lungo i bordi
for q in ["clementi", "lungo i bordi", "massimo volume stanze"]:
    qe = urllib.parse.quote('"%s"' % q)
    j = fetch("https://archive.org/advancedsearch.php?q=%s&fl%%5B%%5D=identifier&fl%%5B%%5D=title&rows=10&output=json" % qe)
    out.append(("ia_%s" % q.replace(" ", "_"), j))
    print("IA '%s' fetched: %d" % (q, len(j)))

# 5. RuTracker search page (likely login-walled, try anyway)
raw = fetch("https://rutracker.org/forum/tracker.php?nm=massimo+volume")
out.append(("rutracker", raw))
print("RuTracker fetched:", len(raw))

# Save everything
for name, content in out:
    with open("/tmp/s30_%s.txt" % name, "w", encoding="utf-8") as f:
        f.write(content)
print("saved", len(out), "files")
