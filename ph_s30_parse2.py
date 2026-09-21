"""Session 30 — deeper TPB parse + 42 Records IA item + 1337x via TOR proxy."""
import re
import html
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"__FETCH_ERROR__ {e}"


print("=" * 20, "TPB raw href dump", "=" * 20)
raw = open("/tmp/tpb.html", encoding="utf-8", errors="ignore").read()
hrefs = re.findall(r'href="([^"]*torrent[^"]*)"', raw)
seen = set()
for h in hrefs:
    if h not in seen:
        seen.add(h)
        print("href:", h)
if not hrefs:
    # dump all links
    for h in re.findall(r'href="([^"]+)"', raw)[:40]:
        print("link:", h)

print()
print("=" * 20, "IA item: 42IlNuotatoreCheever", "=" * 20)
j = fetch("https://archive.org/metadata/42IlNuotatoreCheever")
if j.startswith("__FETCH_ERROR__"):
    print(j)
else:
    import json
    try:
        meta = json.loads(j)
        md = meta.get("metadata", {})
        print("title:", md.get("title"))
        print("desc:", str(md.get("description"))[:400])
        print("creator:", md.get("creator"))
        for f in meta.get("files", [])[:10]:
            print("file:", f.get("name"), f.get("format"))
    except Exception as e:
        print("parse error:", e)

print()
print("=" * 20, "IA item: la_citta_futura-5-6_2000 (check for MV content)", "=" * 20)
j = fetch("https://archive.org/metadata/la_citta_futura-5-6_2000")
if j.startswith("__FETCH_ERROR__"):
    print(j)
else:
    import json
    try:
        meta = json.loads(j)
        md = meta.get("metadata", {})
        print("title:", md.get("title"))
        print("desc:", str(md.get("description"))[:300])
    except Exception as e:
        print("parse error:", e)
