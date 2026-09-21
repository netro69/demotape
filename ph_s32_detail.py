"""Session 32 — detail dump for candidate bands."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, Release, BandConnection

for bid in [6, 86, 69, 76, 89]:
    b = Band.objects.get(id=bid)
    print("=" * 70)
    print(f"[{b.id}] {b.name} | {b.city} | {b.active_years} | status={b.status}")
    gt = ", ".join(t.name for t in b.genre_tags.all())
    print(f"  genres: {gt}")
    print(f"  bio: {(b.bio or '')[:400]}")
    rels = b.releases.all()
    print(f"  releases ({rels.count()}):")
    for r in rels:
        print(f"    - {r.year} {r.title} ({r.format}) [{r.label}]")
    links = b.links.all()
    print(f"  links ({links.count()}):")
    for l in links:
        print(f"    - [{l.link_type}] {l.title} -> {l.url}")
    conns = list(b.connections_from.all()) + list(b.connections_to.all())
    print(f"  connections ({len(conns)}):")
    for c in conns:
        print(f"    - {c.from_band.name} -> {c.to_band.name} ({c.connection_type})")
    fr = b.fanzine_reviews.all()
    print(f"  fanzine reviews: {fr.count()}")
