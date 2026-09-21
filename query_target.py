#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

# Detailed view of best under-researched Italian 1985-2000 candidates
candidates = [
    (70, "Blue Vomit"),
    (72, "Declino"),
    (69, "Brandelli D'Odio"),
    (142, "Rock Rose"),
    (66, "Contropotere"),
    (71, "Nerorgasmo"),
    (83, "Üstmamò"),
    (61, "Blak Vomit"),
]

for bid, name in candidates:
    try:
        b = Band.objects.get(pk=bid)
        links = Link.objects.filter(band=b)
        print(f"\n{'='*60}")
        print(f"ID={b.id} | {b.name}")
        print(f"  City: {b.city or '(none)'}")
        print(f"  Active: {b.active_years or '(none)'}")
        bio = b.bio or "(no bio)"
        print(f"  Bio: {bio[:400]}")
        print(f"  Status: {b.status}")
        print(f"  Existing Links ({links.count()}):")
        for l in links:
            print(f"    [{l.link_type}] {l.url}")
    except Exception as e:
        print(f"Error for {name} (ID={bid}): {e}")
