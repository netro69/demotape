"""Session 37 — raw hrefs from fan site pages; MusicBrainz; RuTracker/1337x via search; DB fanzine check."""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
BASE = "https://www.paolofidanzati.it/sitoscisma/"


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")


print("=== RAW HREFS from fan-site pages ===")
for p in ["recensioni.php", "biografia.php", "lastwaltz.php", "curiosita.php", "interviste.php", "partecipazioni.php", "discografia.php", "credits.php"]:
    try:
        raw = get(BASE + p)
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', raw)
        local = [h for h in hrefs if h.endswith(".php") and not h.startswith("http") and h != p]
        print(f"\n-- {p}:")
        for h in sorted(set(local)):
            print("   ", h)
    except Exception as e:
        print(f"-- {p} FAILED: {e}")

print("\n=== MUSICBRAINZ ===")
try:
    q = urllib.parse.quote('artist:"Scisma" AND country:IT')
    d = json.loads(get(f"https://musicbrainz.org/ws/2/artist/?query={q}&fmt=json"))
    for a in d.get("artists", [])[:5]:
        print("  ", a.get("id"), "|", a.get("name"), "|", a.get("country"), "|", a.get("disambiguation", ""), "| score", a.get("score"))
except Exception as e:
    print("FAILED:", e)
try:
    d = json.loads(get("https://musicbrainz.org/ws/2/release-group/?artist=INSERT&fmt=json"))
except Exception:
    pass

print("\n=== 1337x (direct) ===")
try:
    raw = get("https://1337x.to/search/scisma/1/")
    rows = re.findall(r"<a href=\"/torrent/(\d+)/[^\"]*\">([^<]+)</a>", raw)
    print("  results:", len(rows))
    for t, title in rows[:10]:
        print("   ", t, title[:80])
except Exception as e:
    print("  FAILED:", e)

print("\n=== DB: existing Fanzines ===")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import django

django.setup()
from apps.core.models import Fanzine, Band, Link

for fz in Fanzine.objects.all():
    print("  ", fz.id, "|", fz.name, "|", fz.city, "|", fz.active_years)

print("\n=== DB: Scisma existing link URLs (for dedupe) ===")
b = Band.objects.get(id=78)
existing = list(b.links.values_list("url", flat=True))
for u in existing:
    print("  ", u)
with open(os.path.expanduser("~/.hermes/profiles/amanda/cache/scratch/s37/existing_links.json"), "w") as f:
    json.dump(existing, f, indent=1)
