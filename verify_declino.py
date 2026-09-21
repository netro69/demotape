#!/usr/bin/env python
"""Verify final state of Declino links in the database."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

band = Band.objects.get(pk=72)
links = Link.objects.filter(band=band)
print(f"=== FINAL STATE: {band.name} (ID={band.id}) ===")
print(f"Total links: {links.count()}")
for l in links:
    print(f"  [{l.link_type}] {l.title}")
    print(f"    {l.url}")
