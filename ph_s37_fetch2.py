"""Session 37 — discover all page links on the Scisma fan site, then fetch them."""
import html
import os
import re
import urllib.request

OUT = os.path.expanduser("~/.hermes/profiles/amanda/cache/scratch/s37")
BASE = "https://www.paolofidanzati.it/sitoscisma/"

os.makedirs(OUT, exist_ok=True)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")


# 1. discover links
try:
    raw = get(BASE + "main.php")
    hrefs = sorted(set(re.findall(r'href=["\']?([^"\' >]+)', raw, flags=re.I)))
    print("HREFS on main.php:")
    for h in hrefs:
        print("  ", h)
except Exception as e:
    print("FAIL main.php:", e)
    hrefs = []

# 2. fetch every local page found
pages = [h for h in hrefs if not h.startswith("http") and "#" not in h]
texts = {}
for p in pages:
    url = BASE + p
    try:
        raw = get(url)
    except Exception as e:
        print(f"FAIL {p}: {e}")
        continue
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    name = re.sub(r"[^A-Za-z0-9_.()-]", "_", p) or "index"
    path = os.path.join(OUT, name + ".txt")
    with open(path, "w") as f:
        f.write(t)
    print(f"OK {p} -> {path} ({len(t)} chars)")
