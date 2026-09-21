"""Session 33 — Prozac+ detail: current state before research."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, Release, FanzineReview, BandConnection

b = Band.objects.get(id=90)
print(f"=== {b.name} (id={b.id}) ===")
print(f"City: {b.city} | Active: {b.active_years} | Status: {b.status}")
print(f"Genres: {', '.join(t.name for t in b.genre_tags.all())}")
print(f"Bio ({len(b.bio)} chars):\n{b.bio[:2000]}\n")

print("--- Releases ---")
for r in b.releases.all().order_by("year"):
    print(f"  {r.year} | {r.title} | {r.get_format_display()} | {r.label} | {r.catalog_number} | {r.status}")

print("\n--- Links ({} total) ---".format(b.links.count()))
for l in b.links.all():
    print(f"  [{l.link_type}] {l.title or '-'} | {l.url}")

print("\n--- Fanzine reviews ---")
for fr in FanzineReview.objects.filter(band=b):
    print(f"  {fr.fanzine.name} #{fr.issue_number} ({fr.year})")

print("\n--- Connections ---")
for c in BandConnection.objects.filter(from_band=b):
    print(f"  -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=b):
    print(f"  <- {c.from_band.name} ({c.connection_type})")
