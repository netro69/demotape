# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python
"""Show existing links for the top under-researched bands."""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, Label, GenreTag

priority_bands = [
    'Negrita', 'Ritmo Tribale', 'Scisma', 'Karma', 'C.S.I.',
    'Sinistri', 'Outsider', 'Mister Henry', 'Thee Stolen Cars', 'Il Genio'
]

for name in priority_bands:
    try:
        b = Band.objects.get(name=name)
        links = b.links.all()
        conns_from = b.connections_from.select_related('to_band').all()
        conns_to = b.connections_to.select_related('from_band').all()
        print(f'\n=== {b.name} ===')
        print(f'  active_years: {b.active_years}')
        print(f'  bio: {b.bio[:150] if b.bio else "[empty]"}')
        if b.genre_tags.exists():
            print(f'  genres: {list(b.genre_tags.values_list("name", flat=True))}')
        if b.website:
            print(f'  website: {b.website}')
        if b.discogs_id:
            print(f'  discogs_id: {b.discogs_id}')
        if b.musicbrainz_id:
            print(f'  musicbrainz_id: {b.musicbrainz_id}')
        print(f'  Links ({links.count()}):')
        for l in links:
            print(f'    [{l.link_type}] {l.title} -> {l.url}')
        print(f'  Connections from: {conns_from.count()}')
        for c in conns_from:
            print(f'    -> {c.to_band.name} ({c.connection_type})')
        print(f'  Connections to: {conns_to.count()}')
        for c in conns_to:
            print(f'    <- {c.from_band.name} ({c.connection_type})')
    except Band.DoesNotExist:
        print(f'\n=== {name} NOT FOUND ===')
