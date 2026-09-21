"""Session 30 — check Fanzine records + related bands for connections."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Fanzine, FanzineReview, BandConnection

print("=== FANZINES IN DB ===")
for f in Fanzine.objects.all():
    n = f.reviews.count()
    print(f"{f.id} | {f.name} | {f.city} | {f.active_years} | reviews: {n} | {f.website}")
print()
print("=== FANZINE REVIEWS for Massimo Volume ===")
print(FanzineReview.objects.filter(band__id=47).count())
print()
print("=== Related bands present? ===")
for nm in ["Bachi da Pietra", "Bachi Da Pietra", "Giardini di Mirò", "Santo Niente", "Umberto Palazzo", "Offlaga Disco Pax", "Cesare Basile"]:
    qs = Band.objects.filter(name__icontains=nm.split()[0])
    for b in qs:
        if nm.lower() in b.name.lower():
            print(f"FOUND: {b.id} | {b.name} | {b.status}")
print()
print("=== MV connections detail ===")
for c in BandConnection.objects.filter(from_band__id=47):
    print(f"MV -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band__id=47):
    print(f"{c.from_band.name} -> MV ({c.connection_type})")
