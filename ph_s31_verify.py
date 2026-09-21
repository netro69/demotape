"""Session 31 — verify MV links in DB."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link

band = Band.objects.get(id=47)
links = list(band.links.all())
print("total links:", len(links))
by_type = {}
for l in links:
    by_type[l.link_type] = by_type.get(l.link_type, 0) + 1
print("by type:", by_type)
# spot check the key underground ones
for u in ["https://www.youtube.com/watch?v=qN-xpWFuL5I",
          "https://thepiratebay.org/torrent/4962192",
          "https://archive.org/details/massimo-volume-vittoria-burattini",
          "http://www.mediafire.com/file/9uq3w726frca5lw/massimo%20volume%20-%20demo%20%231992%20%5Bv2%5D.rar"]:
    hit = [l.id for l in links if l.url == u]
    print("OK" if hit else "MISSING", u[:80])
# no duplicate URLs?
urls = [l.url for l in links]
print("unique URLs:", len(set(urls)) == len(urls), f"({len(set(urls))}/{len(urls)})")
