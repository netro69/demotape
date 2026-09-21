"""Session 31 — dump existing Massimo Volume links + band detail."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link, Release, Fanzine, FanzineReview

b = Band.objects.get(id=47)
print("=== BAND:", b.name, "===")
print("active_years:", b.active_years)
print("city:", b.city)
print("bio:", (b.bio or "")[:400])
print("\n=== LINKS (%d) ===" % b.links.count())
for l in b.links.all():
    print(f"{l.id} | {l.link_type} | {l.title} | {l.url}")
print("\n=== RELEASES ===")
for r in getattr(b, "releases", None).all() if hasattr(b, "releases") else []:
    print(r)
print("\n=== CONNECTIONS ===")
for c in getattr(b, "connections_from", None).all() if hasattr(b, "connections_from") else []:
    print(c)
for c in getattr(b, "connections_to", None).all() if hasattr(b, "connections_to") else []:
    print(c)
print("\n=== FANZINE REVIEWS ===")
for fr in getattr(b, "fanzine_reviews", None).all() if hasattr(b, "fanzine_reviews") else []:
    print(fr)
