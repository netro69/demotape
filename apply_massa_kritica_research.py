#!/usr/bin/env python3
"""Apply verified links and connections for Massakritica (band 12) to the Demotape database."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, BandConnection

# Track changes
changes = {"links_added": 0, "links_skipped": 0, "links_removed": 0, "conns_added": 0, "conns_skipped": 0}


def add_link(band, link_type, url, title="", description="", is_primary=False):
    """Add a link if it doesn't already exist for this band."""
    existing = Link.objects.filter(band=band, url=url).exists()
    if not existing:
        Link.objects.create(
            band=band,
            link_type=link_type,
            url=url,
            title=title,
            description=description,
            is_primary=is_primary
        )
        changes["links_added"] += 1
        print(f"  + LINK: {band.name} -> {link_type}: {url[:70]}")
    else:
        changes["links_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {url[:70]}")


def remove_link(band, url):
    """Remove a specific link."""
    link = Link.objects.filter(band=band, url=url).first()
    if link:
        link.delete()
        changes["links_removed"] += 1
        print(f"  - REMOVE: {band.name} -> {url[:70]}")
    else:
        print(f"  = NOT FOUND: {band.name} -> {url[:70]}")


def add_connection(from_band, to_band, conn_type, source="", notes=""):
    """Add a BandConnection if it doesn't exist."""
    if from_band == to_band:
        print(f"  [SKIP self] {from_band.name}")
        return
    existing = BandConnection.objects.filter(
        from_band=from_band, to_band=to_band, connection_type=conn_type
    ).first()
    if not existing:
        BandConnection.objects.create(
            from_band=from_band,
            to_band=to_band,
            connection_type=conn_type,
            source=source,
            notes=notes
        )
        changes["conns_added"] += 1
        print(f"  + CONN: {from_band.name} -> {to_band.name} ({conn_type})")
    else:
        changes["conns_skipped"] += 1
        print(f"  = SKIP conn (exists): {from_band.name} -> {to_band.name} ({conn_type})")


# Get Massa Kritica
massa = Band.objects.get(name="Massa Kritica")

print("=" * 60)
print(f"Band: {massa.name} (id={massa.id})")
print(f"Current links: {massa.links.count()}")
print(f"Current connections: {massa.connections_from.count()} out / {massa.connections_to.count()} in")
print("=" * 60)

# Remove wrong links (Ghost Records - unrelated to Massa Kritica)
print("\n--- Removing incorrect Ghost Records links ---")
remove_link(massa, "https://it.wikipedia.org/wiki/Ghost_Records")
remove_link(massa, "https://ghostrecords.bandcamp.com/")

# Add correct links from research
print("\n--- Adding verified links ---")
verified_links = [
    ("website", "https://www.rockit.it/massakritica/biografia", "Rock.it Biografia", "Official bio on Rock.it (authored by band)"),
    ("website", "https://www.rockit.it/massakritica", "Rock.it Artist Page", "Rock.it artist profile"),
    ("streaming", "https://massakritica.bandcamp.com/", "Bandcamp", "Altre Frequenze EP and more"),
    ("streaming", "https://open.spotify.com/album/5u57qg86LlDWxse99pGZf9", "Spotify - Altre Frequenze", "Debut EP on Spotify"),
    ("streaming", "https://www.last.fm/music/Massakritica", "Last.fm", "Scrobbles, tracks, bio"),
    ("archive", "https://www.discogs.com/artist/371442-Massa-Kritica", "Discogs - Massa Kritica", "Discography and releases"),
    ("archive", "https://www.discogs.com/artist/4653399-Amplessi-Komplessi", "Discogs - Amplessi Komplessi", "Former name discography"),
    ("archive", "https://www.musik-sammler.de/artist/amplessi-komplessi/", "Musik-Sammler - Amplessi Komplessi", "Collector archive for former name"),
    ("archive", "https://www.concertarchives.org/bands/massakritica", "Concert Archives", "Live performance history"),
    ("purchase", "https://www.ruderecords.com/collections/vendors?q=Massakritica", "Rude Records Shop", "Altre Frequenze CD available"),
    ("website", "http://www.massakritica.com/", "Official Website (archived)", "Legacy site with old downloads"),
]

for link_type, url, title, desc in verified_links:
    add_link(massa, link_type, url, title, desc)

# Add connections to related bands
print("\n--- Adding scene connections ---")

# Get related bands
related_bands = {
    "Porno*Riviste": ("label_mate", "Tube Records compilation", "Same label roster, shared 24-track compilation"),
    "Skruigners": ("label_mate", "Tube Records compilation", "Same label roster, shared 24-track compilation"),
    "Pensione Libano": ("label_mate", "Tube Records compilation", "Same label roster, shared 24-track compilation"),
    "Discarica Abusiva": ("shared_stage", "Festa della Birra, Induno Olona", "Shared stage at beer festival"),
    "Africa Unite": ("via_person", "Madaski production", "Madaski (Africa Unite) produced debut EP"),
}

for band_name, (conn_type, source, notes) in related_bands.items():
    try:
        other = Band.objects.get(name=band_name)
        add_connection(massa, other, conn_type, source, notes)
    except Band.DoesNotExist:
        print(f"  [SKIP] {band_name} not in database")

# Print summary
print("\n" + "=" * 60)
print("SUMMARY:")
print(f"  Links added: {changes['links_added']}")
print(f"  Links skipped (existing): {changes['links_skipped']}")
print(f"  Links removed (incorrect): {changes['links_removed']}")
print(f"  Connections added: {changes['conns_added']}")
print(f"  Connections skipped (existing): {changes['conns_skipped']}")
print("=" * 60)

# Verify final state
print(f"\nFinal state for {massa.name}:")
print(f"  Links: {massa.links.count()}")
for l in masa.links.all():
    print(f"    [{l.link_type}] {l.title}")
print(f"  Connections: {massa.connections_from.count()} out / {massa.connections_to.count()} in")
for c in masa.connections_from.all():
    print(f"    -> {c.to_band.name} ({c.connection_type})")
