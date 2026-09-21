# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python
"""Fix successor direction for CCCP <-> C.S.I., then verify DB state."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, BandConnection

# Fix: Remove the wrong-direction successor (C.S.I. -> CCCP)
# The correct one is CCCP -> C.S.I. (CCCP is the predecessor, C.S.I. the successor)
csi = Band.objects.get(name='C.S.I.')
cccp = Band.objects.get(name='CCCP Fedeli alla linea')

wrong = BandConnection.objects.filter(from_band=csi, to_band=cccp, connection_type='successor').first()
if wrong:
    print(f'Removing wrong-direction successor: {wrong.from_band.name} -> {wrong.to_band.name} (successor)')
    wrong.delete()
else:
    print('No wrong-direction successor found')

# Verify correct one still exists
right = BandConnection.objects.filter(from_band=cccp, to_band=csi, connection_type='successor').first()
if right:
    print(f'Correct successor preserved: {right.from_band.name} -> {right.to_band.name} (successor)')
else:
    print('WARNING: Correct successor missing!')

# Final verification query
from django.db.models import Count

bands = Band.objects.annotate(
    num_links=Count('links', distinct=True),
    num_conns=Count('connections_from', distinct=True) + Count('connections_to', distinct=True)
).order_by('num_links', 'num_conns')

print('\n=== FINAL STATE: TOP 15 UNDER-RESEARCHED ===')
for b in bands[:15]:
    print(f'  {b.name:35s} | links={b.num_links} | conns={b.num_conns}')

from apps.core.models import Link
from apps.core.models import Label as Lbl
print(f'\nTotal bands: {Band.objects.count()}')
print(f'Total links: {Link.objects.count()}')
print(f'Total connections: {BandConnection.objects.count()}')
print(f'Total labels: {Lbl.objects.count()}')
