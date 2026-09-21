#!/usr/bin/env python
"""Find most under-researched Italian band from 1985-2000 era."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from django.db.models import Count, Q
from apps.core.models import Band

# Exclude flagged, ghost records, labels, studios
exclude_names = [
    'one more cig', 'Giorgio Gee', 'Summer Is Calling', 'Claim', 
    'Last Vice', 'DROP', 'Ghost Records & Publishing S.n.C.',
    'Midfinger Records', 'La Sauna'
]

bands = Band.objects.exclude(status='flagged').exclude(name__in=exclude_names)

# Filter for Italian bands from 1985-2000 era
# Active years containing 1985-2000
era_bands = bands.filter(
    Q(active_years__regex=r'198[5-9]|199[0-9]|2000') &
    ~Q(city='Seattle (USA)') & ~Q(city__contains='USA') & ~Q(city__contains='UK')
).annotate(link_count=Count('links')).order_by('link_count')[:15]

print(f"{'ID':>4} | {'Links':>5} | {'Name':<30} | {'City':<25} | {'Active':<20}")
print("-" * 100)
for b in era_bands:
    city = (b.city or "")[:25]
    active = (b.active_years or "")[:20]
    print(f"{b.id:>4} | {b.link_count:>5} | {b.name:<30} | {city:<25} | {active:<20}")

# Get the top one
if era_bands:
    top = era_bands[0]
    print(f"\n{'='*60}")
    print(f"TARGET: {top.name} (ID={top.id})")
    print(f"City: {top.city}")
    print(f"Active: {top.active_years}")
    print(f"Links: {top.link_count}")
    print(f"Genres: {[g.name for g in top.genre_tags.all()]}")
    print(f"Website: {top.website}")
    print(f"Discogs: {top.discogs_id}")
    print(f"MusicBrainz: {top.musicbrainz_id}")
    print(f"Bio: {(top.bio or '')[:300]}")
