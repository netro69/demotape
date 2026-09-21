# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python
"""Query database for under-researched bands."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, Label, GenreTag
from django.db.models import Count

# Find bands with fewest links and connections
bands = Band.objects.annotate(
    num_links=Count('links', distinct=True),
    num_conns=Count('connections_from', distinct=True) + Count('connections_to', distinct=True)
).order_by('num_links', 'num_conns')

print('=== TOP 20 UNDER-RESEARCHED BANDS (fewest links+connections) ===')
for b in bands[:20]:
    print(f'  {b.name:35s} | links={b.num_links} | conns={b.num_conns} | active_years={b.active_years}')

print()
print(f'Total bands: {Band.objects.count()}')
print(f'Total links: {Link.objects.count()}')
print(f'Total connections: {BandConnection.objects.count()}')
print(f'Total labels: {Label.objects.count()}')
