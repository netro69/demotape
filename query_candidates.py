#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count
from apps.core.models import Band

# Find Italian bands from 1985-2000 era with the fewest links
# Exclude non-Italian cities (Seattle, etc.)
bands = Band.objects.annotate(link_count=Count('links')).order_by('link_count')[:40]
print("=== ALL BANDS WITH LINK COUNT ===")
for b in bands:
    city = b.city or ""
    active = b.active_years or ""
    # Skip non-Italian cities
    if "USA" in city or "Berlin" in city or "London" in city or "Paris" in city or "Barcelona" in city:
        continue
    # Focus on 1985-2000 era or empty (unknown)
    # Check if active years contain 1980s, 1990s
    has_80s = '198' in active
    has_90s = '199' in active
    has_early_00s = '2000' in active and ('2000' == active[:4] or '2001' in active[:4] or '2002' in active[:4] or '2003' in active[:4] or '2004' in active[:4])
    is_candidate = has_80s or has_90s or has_early_00s or not active
    if is_candidate:
        print(f"CANDIDATE | ID={b.id} | Name={b.name} | City={city} | Active={active} | Links={b.link_count}")
