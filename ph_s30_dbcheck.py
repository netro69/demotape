"""Session 30 — check DB state: fanzines, Soviet Soviet, link types, dedupe list."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, Fanzine, FanzineReview, BandConnection

# 1. All fanzines
print("=== FANZINES in DB ===")
for fz in Fanzine.objects.all():
    n = FanzineReview.objects.filter(fanzine=fz).count()
    print(f"[{fz.id}] {fz.name} | reviews: {n}")

# 2. Soviet Soviet / related bands in DB?
print()
print("=== Related bands search ===")
for name in ["Soviet", "Bachi", "Giardini", "Santo Niente", "Allison", "Ugly Things", "Detriti", "Splatterpink"]:
    qs = Band.objects.filter(name__icontains=name)
    for b in qs:
        print(f"[{b.id}] {b.name} | {b.city} | {b.active_years} | status={b.status}")

# 3. Link type choices
print()
print("=== LINK model ===")
for f in Link._meta.get_fields():
    if hasattr(f, "choices") and f.choices:
        print(f.name, "choices:", [c[0] for c in f.choices])
    else:
        print(f.name, f.get_internal_type())

# 4. FanzineReview fields
print()
print("=== FANZINEREVIEW fields ===")
for f in FanzineReview._meta.get_fields():
    print(f.name, f.get_internal_type())

# 5. Existing MV link URLs (for dedupe)
print()
print("=== MV existing URLs ===")
b = Band.objects.get(id=47)
for l in b.links.all():
    print(l.url)
