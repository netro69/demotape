#!/usr/bin/env python3
"""Strict query: published Italian bands with real 4-digit start year 1985-2000."""
import os
import re
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link
from django.db.models import Count

bands = Band.objects.filter(status='published').annotate(
    link_count=Count('links', distinct=True))

rows = []
for b in bands:
    m = re.match(r'^\s*(19[89]\d|2000)\b(?!\d)', str(b.active_years or ''))
    if not m:
        continue
    start = int(m.group(1))
    if 1985 <= start <= 2000:
        conns = b.connections_from.count() + b.connections_to.count()
        rows.append((b.link_count, conns, start, b.id, b.name, b.city, b.active_years))

rows.sort()
print(f"{'Links':<6} {'Conns':<6} {'Start':<6} {'ID':<5} Name | City | raw_active_years")
for lc, cc, start, bid, name, city, years in rows:
    print(f"{lc:<6} {cc:<6} {start:<6} {bid:<5} {name} | {city} | '{years}'")
