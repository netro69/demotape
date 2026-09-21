"""Session 31 — check Fanzine/FanzineReview models + existing fanzines."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Fanzine, FanzineReview, Link

print("=== Fanzine fields ===")
for f in Fanzine._meta.get_fields():
    print(" ", f.name, "|", f.get_internal_type())
print()
print("=== FanzineReview fields ===")
for f in FanzineReview._meta.get_fields():
    print(" ", f.name, "|", f.get_internal_type())
print()
print("=== Existing fanzines ===")
for fz in Fanzine.objects.all():
    n = FanzineReview.objects.filter(fanzine=fz).count()
    print(f"[{fz.id}] {fz.name} | city={fz.city} | years={fz.active_years} | website={fz.website} | reviews={n}")
print()
print("=== Link fields ===")
for f in Link._meta.get_fields():
    print(" ", f.name, "|", f.get_internal_type())
