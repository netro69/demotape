import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Count totals
print(f"Total bands: {Band.objects.count()}")
print(f"Total releases: {Release.objects.count()}")
print(f"Total links: {Link.objects.count()}")
print(f"Total fanzines: {Fanzine.objects.count()}")
print(f"Total fanzine_reviews: {FanzineReview.objects.count()}")

# Get all bands with link count, sorted ascending
bands_with_counts = []
for band in Band.objects.all():
    link_count = band.links.count()
    release_count = band.releases.count()
    bands_with_counts.append((band, link_count, release_count))

bands_with_counts.sort(key=lambda x: (x[1], x[2]))  # Fewest links first

print("\n=== Bands with Fewest Links (all) ===")
for band, link_count, release_count in bands_with_counts[:15]:
    print(f"{band.name} | links: {link_count} | releases: {release_count} | years: {band.active_years} | city: {band.city}")

# Filter for Italian scene 1985-2000
print("\n=== Italian/Underground Bands 1985-2000 with Fewest Links ===")
import re
results = []
for band, link_count, release_count in bands_with_counts:
    years = band.active_years or ''
    if years:
        match = re.search(r'(\d{4})', years)
        if match:
            year = int(match.group(1))
            if 1985 <= year <= 2000:
                results.append((band, link_count, release_count))

for band, link_count, release_count in results[:20]:
    print(f"{band.name} | links: {link_count} | releases: {release_count} | years: {band.active_years} | city: {band.city}")
