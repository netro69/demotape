import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, Fanzine, FanzineReview, Release, Label

# Get band
band = Band.objects.get(id=142)
print(f"Band: {band.name} (id={band.id})")
print(f"  City: {band.city}")
print(f"  Active years: {band.active_years}")
print(f"  Bio: {band.bio[:200] if band.bio else 'None'}...")
print(f"  Status: {band.status}")

# Get connections
conns = BandConnection.objects.filter(from_band=band) | BandConnection.objects.filter(to_band=band)
print(f"\nConnections ({conns.count()}):")
for c in conns:
    other = c.to_band if c.from_band == band else c.from_band
    print(f"  {c.connection_type}: {other.name} (id={other.id})")

# Get links
links = Link.objects.filter(band=band)
print(f"\nLinks ({links.count()}):")
for l in links:
    print(f"  [{l.link_type}] {l.url}")

# Get releases
releases = Release.objects.filter(band=band)
print(f"\nReleases ({releases.count()}):")
for r in releases:
    print(f"  {r.title} ({r.year}) - {r.label}")

# Check related bands
print("\n--- Related bands ---")
for name in ['Scarlet', 'Lunar Sex', 'Rockrose']:
    try:
        b = Band.objects.get(name__iexact=name)
        print(f"  {name}: id={b.id}, city={b.city}, years={b.active_years}")
    except Band.DoesNotExist:
        print(f"  {name}: NOT FOUND")
