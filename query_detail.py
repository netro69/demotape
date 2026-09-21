import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Get details on Plastik
plastik = Band.objects.filter(slug='plastik').first()
if not plastik:
    plastik = Band.objects.filter(name__icontains='plastik').first()

if plastik:
    print(f"=== {plastik.name} ===")
    print(f"City: {plastik.city}")
    print(f"Years: {plastik.active_years}")
    print(f"Bio: {plastik.bio}")
    print(f"Website: {plastik.website}")
    print(f"Discogs ID: {plastik.discogs_id}")
    print(f"MusicBrainz ID: {plastik.musicbrainz_id}")
    print(f"Genre tags: {', '.join(gt.name for gt in plastik.genre_tags.all())}")
    
    print(f"\n--- Links ({plastik.links.count()}) ---")
    for link in plastik.links.all():
        print(f"  [{link.link_type}] {link.title or '(no title)'}: {link.url}")
    
    print(f"\n--- Releases ({plastik.releases.count()}) ---")
    for release in plastik.releases.all():
        print(f"  {release.title} ({release.year}) - {release.format} - Label: {release.label}")
        print(f"    Description: {release.description[:200]}")
    
    print(f"\n--- Fanzine Reviews ({plastik.fanzine_reviews.count()}) ---")
    for review in plastik.fanzine_reviews.all():
        print(f"  {review.fanzine.name} #{review.issue_number} ({review.year})")
else:
    print("Plastik not found!")

# Also check the top candidates more carefully
print("\n\n=== Checking All 1985-2000 Bands with 0-5 Links ===")
import re
bands_with_counts = []
for band in Band.objects.all():
    link_count = band.links.count()
    release_count = band.releases.count()
    bands_with_counts.append((band, link_count, release_count))

bands_with_counts.sort(key=lambda x: (x[1], x[2]))

for band, link_count, release_count in bands_with_counts:
    if link_count > 5:
        break
    years = band.active_years or ''
    era_match = False
    if years:
        match = re.search(r'(\d{4})', years)
        if match:
            year = int(match.group(1))
            if 1985 <= year <= 2000:
                era_match = True
    if era_match or not years:
        print(f"{band.name} | links: {link_count} | releases: {release_count} | years: {years} | city: {band.city}")
        # Show bio snippet
        if band.bio:
            print(f"  Bio: {band.bio[:150]}...")
        if band.website:
            print(f"  Website: {band.website}")
        if band.discogs_id:
            print(f"  Discogs: {band.discogs_id}")
