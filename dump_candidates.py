#!/usr/bin/env python3
"""Dump existing data for under-researched candidates."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, Release, BandConnection

for bid in [42, 26, 11, 41]:
    b = Band.objects.get(id=bid)
    print(f"=== {b.id}: {b.name} | {b.city} | {b.active_years} | status={b.status}")
    print(f"    bio: {b.bio[:200] if b.bio else '(empty)'}")
    print(f"    website: {b.website} discogs: {b.discogs_id} mb: {b.musicbrainz_id}")
    print(f"    genres: {[g.name for g in b.genre_tags.all()]}")
    for l in b.links.all():
        print(f"    LINK [{l.link_type}] {l.title} -> {l.url}")
    for r in b.releases.all():
        print(f"    REL {r.year} {r.title} ({r.format}) {r.label}")
    for c in b.connections_from.all():
        print(f"    CONN -> {c.to_band.name} ({c.connection_type})")
    for c in b.connections_to.all():
        print(f"    CONN <- {c.from_band.name} ({c.connection_type})")
    print()
