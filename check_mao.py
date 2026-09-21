#!/usr/bin/env python3
"""Check Mao + Hiroshima Mon Amour link discrepancy."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link

for bid in [80, 32]:
    b = Band.objects.get(id=bid)
    print(f"=== {b.id}: {b.name} | {b.city} | {b.active_years} | status={b.status}")
    print(f"    bio: {b.bio[:300] if b.bio else '(empty)'}")
    print(f"    genres: {[g.name for g in b.genre_tags.all()]}")
    for l in b.links.all():
        print(f"    LINK [{l.link_type}] {l.title} -> {l.url}")
    for r in b.releases.all():
        print(f"    REL {r.year} {r.title} ({r.format}) {r.label}")
    print()

# Any links created around session 25 date (2026-09-19) for mao?
print("Links mentioning 'mao':")
for l in Link.objects.filter(title__icontains='mao')[:20]:
    print(f"  band={l.band_id} ({l.band.name}) [{l.link_type}] {l.title} -> {l.url} created={l.created_at}")

print("\nLinks with 'rivoluzione' in URL/title:")
for l in Link.objects.filter(url__icontains='rivoluzione')[:20]:
    print(f"  band={l.band_id} ({l.band.name}) [{l.link_type}] {l.title} -> {l.url} created={l.created_at}")
