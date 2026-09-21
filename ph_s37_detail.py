"""Session 37 — inspect candidates: Scisma, Brandelli D'Odio, Julie's Haircut."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link

for bid in (78, 69, 10):
    b = Band.objects.get(id=bid)
    genres = ", ".join(g.name for g in b.genre_tags.all())
    print("=" * 70)
    print(b.id, b.name, "|", b.city, "|", b.active_years, "|", genres, "| status:", b.status)
    print("bio:", (b.bio or "")[:600])
    print("LINKS (%d):" % b.links.count())
    for l in b.links.all():
        print("  -", l.link_type, "|", l.url[:110], "|", (l.title or "")[:60])
    print("RELEASES:")
    for r in b.releases.all():
        print("  -", r.year, r.title, "|", r.format, "|", r.label)
    print("FANZINE REVIEWS:")
    for fr in b.fanzine_reviews.all():
        print("  -", fr.fanzine.name, fr.issue_number, fr.year)
