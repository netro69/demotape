"""Session 37 — fetch + strip HTML to text for a list of URLs. Writes .txt files to scratch."""
import html
import os
import re
import sys
import urllib.request

OUT = os.path.expanduser("~/.hermes/profiles/amanda/cache/scratch/s37")

URLS = [
    "https://www.paolofidanzati.it/sitoscisma/",
    "https://www.paolofidanzati.it/sitoscisma/main.php",
    "https://www.paolofidanzati.it/sitoscisma/concerti.php",
    "https://www.paolofidanzati.it/sitoscisma/polacco.php",
    "https://www.paolofidanzati.it/sitoscisma/fading.php",
    "https://it.wikipedia.org/wiki/Scisma_(gruppo_musicale)",
    "https://it.wikipedia.org/wiki/Rosemary_Plexiglas",
]

os.makedirs(OUT, exist_ok=True)

for url in URLS:
    name = url.split("/")[-1] or "index"
    name = re.sub(r"[^A-Za-z0-9_.()-]", "_", name) or "index"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"FAIL {url}: {e}")
        continue
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    path = os.path.join(OUT, name + ".txt")
    with open(path, "w") as f:
        f.write(t)
    print(f"OK {url} -> {path} ({len(t)} chars)")
