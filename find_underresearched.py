#!/usr/bin/env python3
"""Find most under-researched Italian bands (fewest links, 1985-2000 era)."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, Release
from django.db.models import Count


def parse_start(years):
    try:
        return int(str(years).split('–')[0].split('-')[0].strip()[:4])
    except Exception:
        return None


bands = Band.objects.annotate(link_count=Count('links', distinct=True))
candidates = []
for b in bands:
    start = parse_start(b.active_years)
    if start is None:
        continue
    if 1985 <= start <= 2000:
        candidates.append((b, start))

candidates.sort(key=lambda x: (x[0].link_count, x[0].name))
print(f"Total bands 1985-2000 start: {len(candidates)}")
print(f"{'ID':<5} {'Links':<6} {'Rels':<5} {'Start':<6} {'Status':<10} Name")
for b, start in candidates[:40]:
    rels = b.releases.count()
    print(f"{b.id:<5} {b.link_count:<6} {rels:<5} {start:<6} {b.status:<10} {b.name} | {b.city}")
