"""Session 38 — inspect candidate under-researched bands."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link

for bid in [42, 26, 29, 11, 20]:
    b = Band.objects.get(id=bid)
    print("===", bid, b.name, "| status:", b.status, "| years:", b.active_years)
    print("    city:", b.city, "| genres:", [g.name for g in b.genre_tags.all()])
    print("    bio:", (b.bio or "")[:300].replace("\n", " "))
    for l in b.links.all():
        print("  -", l.link_type, "|", (l.title or "")[:60], "|", l.url[:100])
    print()
