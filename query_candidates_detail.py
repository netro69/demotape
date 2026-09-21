#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count
from apps.core.models import Band, Link

# Get detailed info on the most under-researched candidates
candidate_ids = [127, 123, 128, 129, 133]
for bid in candidate_ids:
    try:
        b = Band.objects.get(pk=bid)
        links = Link.objects.filter(band=b)
        print(f"\n=== ID={b.id} | Name={b.name} | Slug={b.slug} ===")
        print(f"   City: {b.city}")
        print(f"   Active: {b.active_years}")
        print(f"   Bio: {b.bio[:300] if b.bio else '(no bio)'}")
        print(f"   Links ({links.count()}):")
        for l in links:
            print(f"     - {l.link_type}: {l.url}")
    except Exception as e:
        print(f"Error for ID {bid}: {e}")
