"""Session 35 — check Fanzine objects + Scarlet releases + label field type."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Fanzine, Release, Band

print("=== FANZINES in DB ===")
for f in Fanzine.objects.all().order_by("name"):
    print(f"{f.id}|{f.name}|{f.city}|{f.active_years}|{f.slug}")

print()
print("=== Release model fields ===")
for fld in Release._meta.get_fields():
    print(fld.name, type(fld).__name__)

print()
print("=== Releases for Scarlett (135), Rock Rose (142) ===")
for b in [Band.objects.get(id=135), Band.objects.get(id=142)]:
    print(f"--- {b.name} (id {b.id})")
    for r in Release.objects.filter(band=b):
        lbl = r.label if isinstance(r.label, str) else (r.label.name if r.label else "?")
        print(f"  {r.year} | {r.title} | {r.format} | {lbl} | cat:{r.catalog_number}")

print()
print("=== Full bio of Scarlett ===")
b = Band.objects.get(id=135)
print(b.bio)
print()
print("=== Full bio of Rock Rose ===")
b2 = Band.objects.get(id=142)
print((b2.bio or "")[:1500])
