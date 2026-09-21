"""Session 35 — detail dump for candidate targets (Scarlett, Üstmamò, Scisma, Thee Stolen Cars)."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, FanzineReview, Release

for bid in [135, 83, 78, 8]:
    b = Band.objects.get(id=bid)
    print(f"===== ID {b.id}: {b.name} | {b.city} | {b.active_years} | status={b.status}")
    print(f"BIO ({len(b.bio or '')} chars): {(b.bio or '')[:400]}")
    print("LINKS:")
    for l in b.links.all():
        print(f"  [{l.link_type}] {l.title[:60]} | {l.url[:100]}")
    print("RELEASES:")
    for r in Release.objects.filter(band=b):
        print(f"  {r.year} {r.title} ({r.format or '?'}) [{r.label.name if r.label else 'no label'}]")
    print("FANZINE REVIEWS:")
    for fr in FanzineReview.objects.filter(band=b):
        print(f"  {fr.fanzine.name} #{fr.issue_number} ({fr.year})")
    print()
