#!/usr/bin/env python
"""Add digitized fanzine (TVOR) and Wikipedia links to Declino."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

BAND_ID = 72

new_links = [
    {
        'url': 'https://it.wikipedia.org/wiki/Declino',
        'link_type': 'archive',
        'title': 'Declino - Wikipedia Italiano',
        'description': 'Italian Wikipedia article about Declino (hardcore punk band from Torino, 1980s)',
    },
    {
        'url': 'https://archive.org/details/tvor-teste-vuote-ossa-rotte-issue-3-como-italy',
        'link_type': 'archive',
        'title': 'T.V.O.R. Teste Vuote Ossa Rotte Issue 3 (1983) - Internet Archive',
        'description': 'Digitized fanzine issue. TVOR was the primary Italian hardcore punk fanzine 1980-1985. May contain mentions or reviews of early Declino material',
    },
    {
        'url': 'https://archive.org/details/TVORTesteVuoteOssaRotteIssue4ComoItaly',
        'link_type': 'archive',
        'title': 'T.V.O.R. Teste Vuote Ossa Rotte Issue 4 (1984) - Internet Archive',
        'description': 'Digitized fanzine issue from 1984. Declino was active in the Torino HC scene which TVOR documented',
    },
    {
        'url': 'https://archive.org/details/tvor-teste-vuote-ossa-rotte-issue-5',
        'link_type': 'archive',
        'title': 'T.V.O.R. Teste Vuote Ossa Rotte Issue 5 (1985) - Internet Archive',
        'description': 'Digitized fanzine issue from 1985. May contain reviews of Declino\'s 1984 demo',
    },
]

try:
    band = Band.objects.get(pk=BAND_ID)
    existing_urls = set(Link.objects.filter(band=band).values_list('url', flat=True))
    print(f"Target: {band.name} (ID={band.id})")
    print(f"Existing links: {len(existing_urls)}")
    
    added = []
    for link_data in new_links:
        url = link_data['url']
        if url in existing_urls:
            print(f"  SKIP: {url}")
            continue
        try:
            link = Link.objects.create(
                band=band,
                url=url,
                link_type=link_data['link_type'],
                title=link_data['title'],
                description=link_data['description'],
            )
            added.append(url)
            print(f"  ADDED [{link.link_type}]: {url}")
        except Exception as e:
            print(f"  ERROR: {url} -> {e}")
    
    print(f"\nAdded {added} new links")
    total = Link.objects.filter(band=band).count()
    print(f"Total links for {band.name}: {total}")
    
except Exception as e:
    print(f"ERROR: {e}")
