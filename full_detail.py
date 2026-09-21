import os
import sys
import re

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Get all bands with <10 links - print full details
bands_with_counts = []
for band in Band.objects.all():
    link_count = band.links.count()
    release_count = band.releases.count()
    bands_with_counts.append((band, link_count, release_count))

bands_with_counts.sort(key=lambda x: (x[1], x[2]))

print("=== ALL Bands with <10 Links (full details) ===\n")
for band, link_count, release_count in bands_with_counts:
    if link_count >= 10:
        break
    
    print(f"\n{'='*60}")
    print(f"BAND: {band.name} (ID={band.id}, slug={band.slug})")
    print(f"City: {band.city}")
    print(f"Years: {band.active_years or '(none)'}")
    print(f"Links: {link_count} | Releases: {release_count}")
    print(f"Bio: {band.bio[:300] if band.bio else '(no bio)'}")
    print(f"Website: {band.website}")
    print(f"Discogs: {band.discogs_id}")
    print(f"MusicBrainz: {band.musicbrainz_id}")
    print(f"Genre tags: {', '.join(gt.name for gt in band.genre_tags.all())}")
    print(f"Status: {band.status}")
    print(f"Created by: {band.created_by}")
    
    # Show existing links
    print(f"\n  Existing links ({link_count}):")
    for link in band.links.all():
        print(f"    [{link.link_type}] {link.title}: {link.url}")
    
    # Show releases
    print(f"\n  Releases ({release_count}):")
    for release in band.releases.all():
        print(f"    {release.title} ({release.year}) - {release.format} - Label: {release.label}")
