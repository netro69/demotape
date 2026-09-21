# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Apply Piero Pelù (id=97) research findings to Demotape database.
Adds links, connections, and updates the bio.
Run: cd ~/Projects/demotape && python manage.py shell < apply_piero_pelu_research.py
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
    piero = Band.objects.get(id=97)
except Band.DoesNotExist:
    print("ERROR: Piero Pelù (id=97) not found in DB")
    sys.exit(1)

try:
    litfiba = Band.objects.get(id=95)
except Band.DoesNotExist:
    litfiba = None

try:
    diaframma = Band.objects.get(id=98)
except Band.DoesNotExist:
    diaframma = None

try:
    cccp = Band.objects.get(id=63)
except Band.DoesNotExist:
    cccp = None

try:
    rockgalileo = Band.objects.get(id=86)
except Band.DoesNotExist:
    rockgalileo = None

try:
    pankow = Band.objects.get(id=99)
except Band.DoesNotExist:
    pankow = None

try:
    biagio_antonacci = Band.objects.get(id=94)
except Band.DoesNotExist:
    biagio_antonacci = None

print(f"\n=== Applying Piero Pelù Research ===\n")
print(f"Current links: {piero.links.count()}")
print(f"Current connections FROM: {piero.connections_from.count()}")
print(f"Current connections TO: {piero.connections_to.count()}")

# =========================================================================
# Update bio
# =========================================================================
bio = """Pietro "Piero" Pelù (born 10 February 1962, Florence) is an Italian singer-songwriter, co-founder and lead vocalist of Litfiba (1980–1999, 2010, 2013). Active as a solo artist since 1999. Key figure in the Florentine new wave/post-punk underground scene alongside Diaframma, Pankow, and Neon. His theatrical stage presence and politically charged lyrics made him one of Italy's most recognizable rock frontmen. Over 7 million records sold across his career.

Co-founded Litfiba in Florence in 1980. The band evolved from post-punk/new wave into hard rock and Mediterranean-inflected alternative rock. Commercial peak with El Diablo (1990, Platinum) and Infinito (1999, 1 million copies). Left Litfiba in 1999 for solo career. Collaborated with Diaframma (Amsterdam EP, 1985), Ligabue & Jovanotti ("Il mio nome è mai più," 1999), Anggun ("L'amore immaginato," #1 Italy), and Saverio Lanza (RockGalileo). Published autobiography "Spacca l'infinito" (2021). Competed at Sanremo 2020 with "Pugili fragili." Active supporter of Emergency NGO."""

piero.bio = bio
piero.city = "Firenze"
piero.active_years = "1980–present"
piero.website = "https://www.pieropeluofficial.it/"
piero.save()
print(f"  + Updated bio for {piero.name}")

# =========================================================================
# Add Links
# =========================================================================
print(f"\n--- Adding Links ---")

links = [
    ("video", "https://www.youtube.com/watch?v=ieYROv7yH-A", "DEMO-TAPE CASSETTE 1981 (First Litfiba album)", "", False),
    ("video", "https://www.youtube.com/watch?v=S57S3dNWaho", "Litfiba - Desaparecido (Full Album) 1985", "", False),
    ("video", "https://www.youtube.com/watch?v=ps2cY-AFWI0", "Litfiba - Guerra (1985)", "", False),
    ("video", "https://www.youtube.com/watch?v=inVP8pgzmYc", "Litfiba - Guerra (alternative mix 1985)", "", False),
    ("video", "https://www.youtube.com/watch?v=HfLn6b3W-hE", "Litfiba – Eneide Di Krypton (1983) Full Album", "", False),
    ("video", "https://www.youtube.com/watch?v=FUQewQef1ek", "Litfiba 1984 Yassassin EP", "", False),
    ("video", "https://www.youtube.com/watch?v=ZKlLiR9QySI", "Litfiba Live in Berlin 1984", "", False),
    ("video", "https://www.youtube.com/watch?v=pw3daqiF4l8", "Piero Pelù - Io Ci Sarò (official)", "", False),
    ("video", "https://www.youtube.com/playlist?list=PLzI2aWQX8QwA4gUCu37fAowJDi2J87nPy", "Litfiba Rarities Playlist", "", False),
    ("video", "https://www.youtube.com/watch?v=Dz-l6RBTq0Q", "DIAFRAMMA & LITFIBA - Amsterdam", "", False),
    ("video", "https://www.youtube.com/watch?v=MQBgCIFP3F0", "Fiumani Pelù (Sky Arte interview)", "", False),
    ("video", "https://www.youtube.com/watch?v=S1vo_rXNmY4", "Litfiba - Trilogia Del Potere tour 2013 (FULL)", "", False),
    ("archive", "https://en.wikipedia.org/wiki/Piero_Pel%C3%B9", "Wikipedia EN", "", False),
    ("archive", "https://it.wikipedia.org/wiki/Piero_Pel%C3%B9", "Wikipedia IT", "", False),
    ("archive", "https://en.wikipedia.org/wiki/Litfiba", "Wikipedia - Litfiba", "", False),
    ("archive", "https://www.allmusic.com/artist/piero-pel%C3%B9", "AllMusic", "", False),
    ("archive", "https://www.discogs.com/artist/Litfiba", "Discogs - Litfiba", "", False),
    ("archive", "https://www.discogs.com/artist/Piero-Pel%C3%B9", "Discogs - Piero Pelù", "", False),
    ("article", "https://en.debaser.it/litfiba/litfiba-3/review-effettonotte-87", "DeBaser - Litfiba 1982 Debut EP Review", "", False),
    ("article", "https://en.debaser.it/litfiba/live-al-manila-23-aprile-1983-bootleg/review", "DeBaser - Live al Manila 1983 Bootleg Review", "", False),
    ("article", "https://en.debaser.it/litfiba/12-5-87-aprite-i-vostri-occhi/review", "DeBaser - Live 12-5-87 Review", "", False),
    ("article", "https://en.debaser.it/litfiba/trilogia-1983-1989-live-2013/review-proscriptor", "DeBaser - Trilogia 1983-1989 Live Review", "", False),
    ("streaming", "https://open.spotify.com/artist/6gTrPTTb3XgiLt7GGcmf8j", "Spotify", "", False),
    ("streaming", "https://music.apple.com/artist/piero-pelù", "Apple Music", "", False),
    ("website", "https://www.pieropeluofficial.it/", "Official Website", "", True),
]

for link_type, url, title, description, is_primary in links:
    add_link(piero, link_type, url, title, description, is_primary)

# =========================================================================
# Add Band Connections
# =========================================================================
print(f"\n--- Adding Connections ---")

if litfiba:
    add_connection(
        piero, litfiba, "shared_member",
        "Piero Pelù is the lead singer and co-founder of Litfiba. This connection links the solo artist to his band."
    )

if diaframma:
    add_connection(
        piero, diaframma, "collaboration",
        "Amsterdam EP (1985) — shared vocal project with Diaframma. Federico Fiumani and Piero Pelù close friendship. Both foundational Florentine new wave bands."
    )

if cccp:
    add_connection(
        piero, cccp, "scene_peer",
        "Gianni Maroccolo (Litfiba bassist) later played on CCCP's final album. Ringo de Palma (Litfiba drummer) played with CCCP. Shared Florentine/Emilian punk underground origins."
    )

if pankow:
    add_connection(
        piero, pankow, "scene_peer",
        "Shared Florentine underground scene, 1980s. Both part of the Florentine new wave/post-punk network."
    )

if rockgalileo:
    add_connection(
        piero, rockgalileo, "collaboration",
        "Saverio Lanza (RockGalileo vocalist/guitarist) collaborated with Piero Pelù on solo projects. Gianmarco Colzi (RockGalileo drummer) later joined Litfiba (2001–2006)."
    )

if biagio_antonacci:
    add_connection(
        piero, biagio_antonacci, "collaboration",
        "Saverio Lanza (RockGalileo) worked with both Antonacci and Pelù. Cross-collaboration network."
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
piero.refresh_from_db()
print(f"\n=== Final Status for {piero.name} ===")
print(f"Links: {piero.links.count()}")
print(f"Connections FROM: {piero.connections_from.count()}")
print(f"Connections TO: {piero.connections_to.count()}")
print(f"City: {piero.city}")
print(f"Active: {piero.active_years}")
print(f"Bio length: {len(piero.bio)} chars")
