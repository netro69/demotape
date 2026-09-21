# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Apply Biagio Antonacci (id=94) research findings to Demotape database.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_biagio_antonacci_research.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, BandConnection

changes = {"links_added": 0, "skipped": 0, "connections_added": 0, "conn_skipped": 0}


def add_link(band, link_type, url, title="", description="", is_primary=False):
    existing = Link.objects.filter(band=band, url=url).exists()
    if not existing:
        Link.objects.create(
            band=band,
            link_type=link_type,
            url=url,
            title=title,
            description=description,
            is_primary=is_primary,
        )
        changes["links_added"] += 1
        print(f"  + LINK: {band.name} -> {link_type}: {url[:70]}")
    else:
        changes["skipped"] += 1


def add_connection(from_band, to_band, connection_type, notes="", source=""):
    existing = BandConnection.objects.filter(
        from_band=from_band, to_band=to_band, connection_type=connection_type
    ).exists()
    reverse = BandConnection.objects.filter(
        from_band=to_band, to_band=from_band, connection_type=connection_type
    ).exists()
    if not existing and not reverse:
        BandConnection.objects.create(
            from_band=from_band,
            to_band=to_band,
            connection_type=connection_type,
            notes=notes,
            source=source,
        )
        changes["connections_added"] += 1
        print(f"  + CONN: {from_band.name} -> {to_band.name} ({connection_type})")
    else:
        changes["conn_skipped"] += 1


# =========================================================================
# Get bands
# =========================================================================
try:
    biagio = Band.objects.get(id=94)
except Band.DoesNotExist:
    print("ERROR: Biagio Antonacci (id=94) not found in DB")
    sys.exit(1)

try:
    rockgalileo = Band.objects.get(id=86)
except Band.DoesNotExist:
    rockgalileo = None

try:
    piero = Band.objects.get(id=97)
except Band.DoesNotExist:
    piero = None

try:
    litfiba = Band.objects.get(id=95)
except Band.DoesNotExist:
    litfiba = None

try:
    vasco = Band.objects.get(id=96)
except Band.DoesNotExist:
    vasco = None

try:
    diaframma = Band.objects.get(id=98)
except Band.DoesNotExist:
    diaframma = None

try:
    pankow = Band.objects.get(id=99)
except Band.DoesNotExist:
    pankow = None

print(f"\n=== Applying Biagio Antonacci Research ===\n")
print(f"Current links: {biagio.links.count()}")
print(f"Current connections FROM: {biagio.connections_from.count()}")
print(f"Current connections TO: {biagio.connections_to.count()}")

# =========================================================================
# Update bio
# =========================================================================
bio = """Biagio Antonacci (born 9 November 1963, Milan) is an Italian pop/rock singer-songwriter, one of Italy's most commercially successful modern artists (over 10 million records sold). Raised in Rozzano (Milan suburb). Studied geometry (surveting diploma) before pursuing music.

Debuted at the 38th Sanremo Music Festival in 1988 with "Voglio vivere in un attimo." Signed to record label in 1989; debut album "Sono cose che capitano" went unnoticed. Breakthrough with "Liberatemi" (1992, produced by Mauro Malavasi, 2× Platinum, 150,000+ copies). Major commercial success throughout the 1990s-2000s with albums like "Mi fai stare bene" (Diamond), "Convivendo" (Part I + II, over 1 million copies). Received World Music Award 2005 (Hollywood) as "Best-Selling Male Italian Artist."

Key connection to the Florentine underground scene: from 1996 onwards, Saverio Lanza (frontman of RockGalileo) collaborated extensively with Antonacci as guitarist, bassist, pianist, and songwriter. This creates a bridge between mainstream Italian pop and the Florentine underground scene (Litfiba, Diaframma, Pankow). Gianmarco Colzi (RockGalileo drummer) later joined Litfiba (2001-2006).

NOT an underground/noise rock artist. All releases on major labels (Mercury, BMG Ricordi). NO connection to Chaos Village label or Asphodel network."""

biagio.bio = bio
biagio.city = "Milan (Rozzano)"
biagio.active_years = "1988–present"
biagio.website = "https://www.biagioantonacci.it/"
biagio.discogs_id = "230620"
biagio.save()
print(f"  + Updated bio for {biagio.name}")

# =========================================================================
# Add Links
# =========================================================================
print(f"\n--- Adding Links ---")

links = [
    ("archive", "https://en.wikipedia.org/wiki/Biagio_Antonacci", "Wikipedia EN", "", False),
    ("archive", "https://it.wikipedia.org/wiki/Biagio_Antonacci", "Wikipedia IT", "", False),
    ("archive", "https://www.allmusic.com/artist/biagio-antonacci-mn0000064698", "AllMusic", "", False),
    ("archive", "https://www.discogs.com/artist/230620-Biagio-Antonacci", "Discogs", "", False),
    ("streaming", "https://open.spotify.com/artist/109mBfoOFCCjp8E3IS8cNv", "Spotify", "", False),
    ("streaming", "https://music.apple.com/us/artist/biagio-antonacci/5796164", "Apple Music", "", False),
    ("website", "https://www.biagioantonacci.it/", "Official Website", "", True),
]

for link_type, url, title, description, is_primary in links:
    add_link(biagio, link_type, url, title, description, is_primary)

# =========================================================================
# Add Band Connections
# =========================================================================
print(f"\n--- Adding Connections ---")

if rockgalileo:
    add_connection(
        biagio, rockgalileo, "collaboration",
        "Saverio Lanza (RockGalileo frontman) collaborated as guitarist, bassist, pianist, songwriter for Antonacci from 1996 onwards. Long-term ongoing collaboration."
    )

if piero:
    add_connection(
        biagio, piero, "collaboration",
        "Saverio Lanza (RockGalileo) worked with both Antonacci and Pelù. Cross-collaboration network."
    )

if litfiba:
    add_connection(
        biagio, litfiba, "scene_peer",
        "Gianmarco Colzi (RockGalileo drummer) later joined Litfiba (2001-2006). Saverio Lanza connected both scenes."
    )

if vasco:
    add_connection(
        biagio, vasco, "collaboration",
        "Saverio Lanza (RockGalileo) collaborated with both Antonacci and Vasco Rossi. Network hub connection."
    )

if diaframma:
    add_connection(
        biagio, diaframma, "scene_peer",
        "Same Florentine wave scene via Lanza/Pelù network. Indirect connection."
    )

if pankow:
    add_connection(
        biagio, pankow, "scene_peer",
        "Florentine underground peer scene via Lanza/Pelù network. Indirect connection."
    )

# =========================================================================
# Summary
# =========================================================================
print(f"\n{'=' * 60}")
print(f"LINKS ADDED: {changes['links_added']}")
print(f"LINKS SKIPPED: {changes['skipped']}")
print(f"CONNECTIONS ADDED: {changes['connections_added']}")
print(f"CONNECTIONS SKIPPED: {changes['conn_skipped']}")

# Final status
biagio.refresh_from_db()
print(f"\n=== Final Status for {biagio.name} ===")
print(f"Links: {biagio.links.count()}")
print(f"Connections FROM: {biagio.connections_from.count()}")
print(f"Connections TO: {biagio.connections_to.count()}")
print(f"City: {biagio.city}")
print(f"Active: {biagio.active_years}")
print(f"Bio length: {len(biagio.bio)} chars")
