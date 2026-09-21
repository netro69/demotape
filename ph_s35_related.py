"""Session 35 — check related bands + connections for Scarlett."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, BandConnection

print("=== Bands matching Lunar/Sailor/Rose ===")
for b in Band.objects.filter(name__icontains="lunar") | Band.objects.filter(name__icontains="sailor") | Band.objects.filter(name__icontains="rose"):
    print(f"{b.id}|{b.name}|{b.city}|{b.active_years}|status={b.status}")

print()
print("=== Connections touching Scarlett (135) ===")
for c in BandConnection.objects.filter(from_band__id=135) | BandConnection.objects.filter(to_band__id=135):
    print(f"{c.from_band.name} -> {c.to_band.name} | {c.connection_type} | {c.notes[:80]}")

print()
print("=== Connections touching Rock Rose (142) ===")
for c in BandConnection.objects.filter(from_band__id=142) | BandConnection.objects.filter(to_band__id=142):
    print(f"{c.from_band.name} -> {c.to_band.name} | {c.connection_type} | {c.notes[:80]}")

print()
print("=== Total bands + links in DB ===")
from apps.core.models import Link
print("bands:", Band.objects.count(), "| published:", Band.objects.filter(status="published").count(), "| links:", Link.objects.count())
