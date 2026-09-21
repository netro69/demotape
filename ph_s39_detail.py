"""Session 39 — inspect target: Brandelli D'Odio (id=69) full DB record."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Release, FanzineReview

b = Band.objects.get(id=69)
print("NAME:", b.name, "| status:", b.status, "| years:", b.active_years, "| city:", b.city)
print("SLUG:", b.slug, "| MB:", b.musicbrainz_id, "| discogs:", b.discogs_id)
print("GENRES:", [g.name for g in b.genre_tags.all()])
print("BIO:", (b.bio or "")[:800])
print("WEBSITE:", b.website)
print()
print("=== LINKS (%d) ===" % b.links.count())
for l in b.links.all():
    print("-", l.link_type, "|", (l.title or "")[:70], "|", l.url)
print()
print("=== RELEASES ===")
for r in Release.objects.filter(band=b):
    print("-", r.year, r.title, r.format, "|", (r.label.name if r.label_id else "-"))
print()
print("=== FANZINE REVIEWS ===")
for fr in FanzineReview.objects.filter(band=b):
    print("-", fr.fanzine.name, fr.issue_number, fr.year)
