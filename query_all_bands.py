#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count
from apps.core.models import Band, Link

# Get ALL bands with their link counts, sorted by fewest
bands = Band.objects.annotate(link_count=Count('links')).order_by('link_count')
print("=== ALL BANDS (sorted by fewest links) ===")
print(f"{'ID':>4} | {'Links':>5} | {'Name':<30} | {'City':<20} | {'Active':<15}")
print("-" * 90)
for b in bands:
    city = (b.city or "")[:20]
    active = (b.active_years or "")[:15]
    print(f"{b.id:>4} | {b.link_count:>5} | {b.name:<30} | {city:<20} | {active:<15}")
