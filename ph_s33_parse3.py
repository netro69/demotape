"""Session 33 — TPB proper parse + full Invidious sweep via f5.si."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"
INV = "https://invidious.f5.si"


def read(name):
    with open(BASE + name, encoding="utf-8") as f:
        return f.read()


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# --- TPB parse with generic regex ---
for fname in ["s33_tpb_prozacplus.txt", "s33_tpb_acido_acida.txt", "s33_tpb_testa_plastica.txt"]:
    html = read(fname)
    # generic: any anchor to /torrent/
    links = re.findall(r'<a[^>]+href="(/torrent/(\d+)/([^"]+))"[^>]*>(.*?)</a>', html, re.S)
    # dedupe by id, keep title
    seen = {}
    for slug, tid, slugname, title in links:
        t = re.sub(r"<[^>]+>", "", title).strip()
        if tid not in seen or (t and not seen[tid][0]):
            seen[tid] = (t, slug)
    print("=== %s — %d unique torrents ===" % (fname, len(seen)))
    for tid, (t, slug) in list(seen.items())[:25]:
        print("  - [%s] %s | https://thepiratebay.org%s" % (tid, t[:90], slug))
    # also grab size/date info lines
    descs = re.findall(r'class="detDesc">(.*?)</font>', html, re.S)
    if descs:
        print("  (%d detDesc rows)" % len(descs))

# --- Full Invidious sweep ---
QUERIES = [
    "prozac+ acido acida", "prozac+ testa plastica", "prozac+ live 1996", "prozac+ live 1998",
    "prozac+ pordenone", "mago accusani", "elisabetta imelio prozac", "prozac accuso",
    "prozac+ demo 1995", "prozac+ rock tenda", "prozac+ acida live", "prozac+ betty tossica",
    "prozac+ vox pop", "prozac+ arezzo wave", "prozac+ mi ami",
]
all_results = {}
for q in QUERIES:
    qe = urllib.parse.quote(q)
    j = fetch("%s/api/v1/search?q=%s&type=video" % (INV, qe))
    if j.startswith("__FETCH_ERROR__"):
        print("ERR %-30s %s" % (q, j[:60]))
        continue
    try:
        items = json.loads(j)
    except Exception as e:
        print("ERR %-30s parse %s" % (q, e))
        continue
    keep = []
    for it in items:
        title = (it.get("title") or "").lower()
        author = (it.get("author") or "").lower()
        # relevance filter: must mention prozac or band-member names
        if any(k in title or k in author for k in ["prozac", "accusani", "imelio", "mangoni", "acida", "testa plastica", "accuso", "betty"]):
            keep.append(it)
    all_results[q] = keep
    print("Q: %-30s -> %2d/%d relevant" % (q, len(keep), len(items)))

with open(BASE + "s33_yt_all.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=1)
print("saved s33_yt_all.json")
