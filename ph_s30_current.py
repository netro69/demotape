"""Session 30 — Massimo Volume (id 47) current state: existing links + fanzine reviews."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, Release, FanzineReview, BandConnection

b = Band.objects.get(id=47)
print("BAND:", b.name, "|", b.city, "|", b.active_years)
print("BIO (first 400):", (b.bio or "")[:400])
print()
print("=== EXISTING LINKS (%d) ===" % b.links.count())
for l in b.links.all():
    print(f"[{l.link_type}] {l.title} | {l.url}")
print()
print("=== RELEASES ===")
for r in b.releases.all():
    print(f"{r.year} | {r.title} | {r.get_format_display() if hasattr(r, 'get_format_display') else ''} | label: {getattr(r, 'label', None)}")
print()
print("=== FANZINE REVIEWS ===")
for fr in FanzineReview.objects.filter(band=b):
    print(f"{fr.fanzine.name} #{fr.issue_number} ({fr.year}) | {fr.digitized_url}")
print()
print("=== CONNECTIONS ===")
for c in BandConnection.objects.filter(from_band=b):
    print(f"-> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=b):
    print(f"<- {c.from_band.name} ({c.connection_type})")
