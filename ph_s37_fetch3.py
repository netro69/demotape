"""Session 37 — fetch release detail pages + setlists from fan site; MusicBrainz releases."""
import html
import json
import os
import re
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
BASE = "https://www.paolofidanzati.it/sitoscisma/"
OUT = os.path.expanduser("~/.hermes/profiles/amanda/cache/scratch/s37")

PAGES = [
    "pezzetti.php", "bombardano.php", "scismacass.php", "centro.php",
    "rosemary.php", "rosemarycds.php", "negligenza.php", "innocenza.php",
    "innocenzap.php", "viveleroi.php", "tungsteno.php", "armstrong.php",
    "scaletta_tunnel.php", "scaletta_cesenatico.php", "scaletta_ravenna.php",
    "scaletta_thelastwaltz.php", "unamore.php",
]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")


for p in PAGES:
    try:
        raw = get(BASE + p)
        t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        t = html.unescape(t)
        t = re.sub(r"[ \t]+", " ", t)
        t = re.sub(r"\n\s*\n+", "\n", t)
        # cut nav footer
        t = t.split("indietro .:.")[0]
        path = os.path.join(OUT, p + ".txt")
        with open(path, "w") as f:
            f.write(t)
        print(f"===== {p} =====")
        print(t.strip()[:900])
        print()
    except Exception as e:
        print(f"===== {p} FAILED: {e} =====")

print("===== MUSICBRAINZ RELEASES =====")
try:
    d = json.loads(get("https://musicbrainz.org/ws/2/release-group/?artist=d8c6383e-55f8-4375-8838-57ca2cbadbdd&fmt=json"))
    for rg in d.get("release-groups", []):
        print("  ", rg.get("id"), "|", rg.get("title"), "|", rg.get("primary-type"), "|", rg.get("first-release-date"))
except Exception as e:
    print("FAILED:", e)
