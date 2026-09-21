import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Check ALL bands with their link counts - identify the current most under-researched
bands_with_counts = []
for band in Band.objects.all():
    link_count = band.links.count()
    release_count = band.releases.count()
    bands_with_counts.append((band, link_count, release_count))

bands_with_counts.sort(key=lambda x: (x[1], x[2]))

print("=== ALL Bands Sorted by Link Count (most under-researched first) ===")
for band, link_count, release_count in bands_with_counts[:30]:
    years = band.active_years or '—'
    print(f"{band.name} | links: {link_count} | releases: {release_count} | years: {years} | city: {band.city}")

# Check specifically for Italian 1985-2000 era bands with <10 links
print("\n=== Italian 1985-2000 Bands with <10 Links ===")
import re
for band, link_count, release_count in bands_with_counts:
    if link_count >= 10:
        break
    years = band.active_years or ''
    if years:
        match = re.search(r'(\d{4})', years)
        if match:
            year = int(match.group(1))
            if 1985 <= year <= 2000:
                print(f"{band.name} | links: {link_count} | releases: {release_count} | years: {years} | city: {band.city}")
