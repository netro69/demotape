"""Session 33 — parse tpb.party HTML properly + retry Invidious with alternate instances."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"


def read(name):
    with open(BASE + name, encoding="utf-8") as f:
        return f.read()


def fetch(url, timeout=30, headers=None):
    try:
        h = {"User-Agent": UA}
        if headers:
            h.update(headers)
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# --- TPB: find result rows in the table ---
html = read("s33_tpb_prozacplus.txt")
# tpb.party rows: <div class="detName">...<a href="/torrent/ID/slug.html" class="detLink" title="...">
names = re.findall(r'<a href="(/torrent/\d+/[^"]+)"[^>]*class="detLink"[^>]*>(.*?)</a>', html, re.S)
print("=== TPB 'prozac+' — detLink matches: %d ===" % len(names))
for slug, title in names[:25]:
    print("  - https://thepiratebay.org%s | %s" % (slug, re.sub(r"<[^>]+>", "", title).strip()[:100]))

# broader: any /torrent/ link at all
anylinks = re.findall(r'(/torrent/\d+/[^"#]+)', html)
print("any /torrent/ links: %d" % len(set(anylinks)))

# check for "no results" indicator
if "No hits" in html or "no results" in html.lower():
    print(">>> TPB says NO HITS <<<")
# count table rows
rows = re.findall(r'<tr[^>]*>', html)
print("table rows:", len(rows))

# --- Retry Invidious with headers + alternate instances ---
INV_CANDIDATES = [
    "https://yt.chocolatemoo53.com",
    "https://invidious.nerdvpn.de",
    "https://iv.ggtyler.dev",
    "https://invidious.f5.si",
    "https://inv.tux.pizza",
]
qe = urllib.parse.quote("prozac+ acido acida")
for inv in INV_CANDIDATES:
    j = fetch("%s/api/v1/search?q=%s&type=video" % (inv, qe), headers={"Accept": "application/json"})
    ok = not j.startswith("__FETCH_ERROR__")
    print("=== %s -> %s ===" % (inv, "OK" if ok else j[:80]))
    if ok:
        try:
            items = json.loads(j)[:10]
            for it in items:
                print("  - %s | https://www.youtube.com/watch?v=%s | %ss | %s" % (
                    it.get("title", "")[:90], it.get("videoId"), it.get("lengthSeconds", 0), (it.get("author") or "")[:30]))
            with open(BASE + "s33_yt_test.json", "w") as f:
                f.write(j)
            break
        except Exception as e:
            print("  parse error:", e, "|", j[:150])
