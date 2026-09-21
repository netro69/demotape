import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Get Negrita band
negrita = Band.objects.filter(slug='negrita').first()
if not negrita:
    negrita = Band.objects.filter(name__icontains='negrita').first()

if not negrita:
    print("Negrita not found!")
    sys.exit(1)

print(f"=== {negrita.name} ===")
print(f"City: {negrita.city}")
print(f"Years: {negrita.active_years}")
print(f"Bio: {negrita.bio[:500]}")
print(f"Website: {negrita.website}")
print(f"Discogs ID: {negrita.discogs_id}")
print(f"MusicBrainz ID: {negrita.musicbrainz_id}")
print(f"Genre tags: {', '.join(gt.name for gt in negrita.genre_tags.all())}")

print(f"\n--- Links ({negrita.links.count()}) ---")
for link in negrita.links.all():
    print(f"  [{link.link_type}] {link.title or '(no title)'}: {link.url}")

print(f"\n--- Releases ({negrita.releases.count()}) ---")
for release in negrita.releases.all():
    print(f"  {release.title} ({release.year}) - {release.format} - Label: {release.label}")

print(f"\n--- Fanzine Reviews ({negrita.fanzine_reviews.count()}) ---")
for review in negrita.fanzine_reviews.all():
    print(f"  {review.fanzine.name} #{review.issue_number} ({review.year})")
