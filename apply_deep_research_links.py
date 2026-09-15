#!/usr/bin/env python3
"""
Apply all remaining verified URLs and connections from the deep research pass
(band-research-pass-2026-09-16.md) that were not already in the database.

Also adds Ghost Town compilation connections and Carlo Rizzi cross-band connections.

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_deep_research_links.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, BandConnection
from django.db.models import Count

changes = {"links_added": 0, "skipped": 0, "connections_added": 0, "conn_skipped": 0}

def add_link(band, link_type, url, title="", description=""):
    """Add a link if it doesn't already exist for this band."""
    existing = Link.objects.filter(band=band, url=url).exists()
    if not existing:
        Link.objects.create(
            band=band,
            link_type=link_type,
            url=url,
            title=title,
            description=description,
        )
        changes["links_added"] += 1
        print(f"  + LINK: {band.name} -> {link_type}: {url[:70]}")
    else:
        changes["skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {url[:70]}")

def add_connection(from_band, to_band, connection_type, notes=""):
    """Add a band connection if it doesn't already exist."""
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
        )
        changes["connections_added"] += 1
        print(f"  + CONN: {from_band.name} -> {to_band.name} ({connection_type})")
    else:
        changes["conn_skipped"] += 1

# =========================================================================
# NEW LINKS from deep research pass
# =========================================================================

# Andrea Fornari (Varese) — currently 4 links, add YouTube Music
try:
    b = Band.objects.get(name="Andrea Fornari")
    add_link(b, "video", "https://music.youtube.com/channel/UCFykzONe9IowBwkJZZ8PFsA", "YouTube Music")
except Band.DoesNotExist:
    pass

# Casa Del Mirto (Varese) — currently 4 links, add Bandcamp, YouTube, Wikipedia
try:
    b = Band.objects.get(name="Casa Del Mirto")
    add_link(b, "purchase", "https://ghostrecords.bandcamp.com/album/still-2", "Still (2014) on Bandcamp")
    add_link(b, "video", "https://www.youtube.com/watch?v=4xA3kzflwPk", "Ultimatum (from The Nature)")
    add_link(b, "archive", "https://it.wikipedia.org/wiki/Casa_del_mirto", "Wikipedia IT")
except Band.DoesNotExist:
    pass

# EgoP (Varese) — currently 4 links, add Spotify, Shazam
try:
    b = Band.objects.get(name="EgoP")
    add_link(b, "streaming", "https://open.spotify.com/intl-de/artist/1nmJ6mWHt04LSNWkG44YnW", "Spotify")
    add_link(b, "streaming", "https://www.shazam.com/artist/-/893055599", "Shazam")
except Band.DoesNotExist:
    pass

# Hormiga (Varese) — currently 3 links, add Internet Archive, Shazam
try:
    b = Band.objects.get(name="Hormiga")
    add_link(b, "archive", "https://archive.org/details/HormigayouListenBeforeBeingBorn", "Internet Archive")
    add_link(b, "streaming", "https://www.shazam.com/ja-jp/song/368837249/in-partegora", "Shazam (In Partegora)")
except Band.DoesNotExist:
    pass

# Frozen Farmer (Varese) — currently 6 links, add Bandcamp, Rockit, YouTube
try:
    b = Band.objects.get(name="Frozen Farmer")
    add_link(b, "purchase", "https://ghostrecords.bandcamp.com/track/snow", "Snow on Bandcamp")
    add_link(b, "article", "https://www.rockit.it/frozenfarmer", "Rockit")
    add_link(b, "video", "https://www.youtube.com/watch?v=dwxzF1XuSxo", "Death (2012) on YouTube")
except Band.DoesNotExist:
    pass

# Hot Gossip (Varese) — currently 5 links, add Bandcamp, Spotify, Echoes And Dust
try:
    b = Band.objects.get(name="Hot Gossip")
    add_link(b, "purchase", "https://ghostrecords.bandcamp.com/track/things-happen-on-a-tuesday", "Things Happen On A Tuesday on Bandcamp")
    add_link(b, "streaming", "https://open.spotify.com/artist/30AoEGNkGOgAbUi65zT2P3", "Spotify")
    add_link(b, "article", "https://echoesanddust.com/2009/01/hot-gossip-you-look-faster-when-you-are-young/", "Echoes And Dust review")
except Band.DoesNotExist:
    pass

# Various Artists (Varese) — currently 1 link, add Genius, Discogs, Spotify
try:
    b = Band.objects.get(name="Various Artists")
    add_link(b, "archive", "https://genius.com/albums/Various-artists/Demotape-intermezzo", "Genius (DEMOTAPE intermezzo)")
    add_link(b, "archive", "https://www.discogs.com/master/1147178-Various-Demo-Tape-1-", "Discogs (Demo Tape 1)")
    add_link(b, "streaming", "https://open.spotify.com/album/7xopGsVTmBBgIEroj7JiPJ", "Spotify (Cover Project Vol. 1)")
except Band.DoesNotExist:
    pass

# Fiel Garvie (Varese) — currently 4 links, add Spotify
try:
    b = Band.objects.get(name="Fiel Garvie")
    add_link(b, "streaming", "https://open.spotify.com/intl-it/artist/4z1dEs0XiSvHDkL4JdIw0x", "Spotify")
except Band.DoesNotExist:
    pass

# Iver & The Driver (Varese) — currently 5 links, add Bandcamp, Spotify, Rockit
try:
    b = Band.objects.get(name="Iver & The Driver")
    add_link(b, "purchase", "https://ghostrecords.bandcamp.com/album/iver-the-driver-samples-and-oranges", "Samples and Oranges on Bandcamp")
    add_link(b, "streaming", "https://open.spotify.com/intl-de/artist/26VWPcKRX9zfzbP7KRr7fK", "Spotify")
    add_link(b, "article", "https://www.rockit.it/recensione/6047/iverethedriver-samples-and-oranges", "Rockit review")
except Band.DoesNotExist:
    pass

# =========================================================================
# Bands with < 3 links that have Ghost Records roster as additional link
# These bands have NO dedicated online presence — add Ghost Records roster
# =========================================================================

ghost_records_roster = "https://ghostrecords.bandcamp.com/"

for name in [
    "Massa Kritica", "Santo", "Encode", "Freelance Co.",
    "Ritmo Tribale", "Roberto Dell'Era", "Il Genio",
    "Hiroshima Mon Amour", "One Dimensional Man", "Ocropoid",
    "L'Avversario", "To You Mom:", "Grand Transmitter",
    "Thee Stolen Cars", "Midwest", "Nerorgasmo", "Sinistri",
    "Plastik", "Merci Miss Monroe",
]:
    try:
        b = Band.objects.get(name=name)
        lc = b.links.count()
        if lc < 3:
            add_link(b, "purchase", ghost_records_roster, "Ghost Records roster")
    except Band.DoesNotExist:
        pass

# =========================================================================
# Ghost Town Compilation Connections (2002)
# "Ghost Town: 13 songs from the lakes county" — Varese scene compilation
# =========================================================================

print("\n--- Ghost Town Compilation Connections ---")

ghost_town_bands = [
    "Bartòk", "Midwest", "Hormiga", "Clark Nova", "Frozen Farmer",
    "Birø", "Casa Del Mirto", "EgoP", "Plankton Dada Wave",
    "Videodreams", "The Lonely Rat", "Green Like July",
    "Movie Star Junkies", "Ronin", "Santo", "There Will Be Blood",
    "Freelance Co.", "Il Triangolo",
]

# Connect all Ghost Town bands to each other as scene_peers
# We'll connect them as a chain to avoid O(n^2) and duplicate connections
ghost_town_in_db = []
for name in ghost_town_bands:
    try:
        b = Band.objects.get(name=name)
        ghost_town_in_db.append(b)
    except Band.DoesNotExist:
        pass

print(f"Ghost Town bands in DB: {len(ghost_town_in_db)}")
for i in range(len(ghost_town_in_db)):
    for j in range(i + 1, len(ghost_town_in_db)):
        add_connection(
            ghost_town_in_db[i], ghost_town_in_db[j],
            "scene_peer",
            "Ghost Town compilation (2002)"
        )

# =========================================================================
# Carlo Rizzi Cross-Band Connections
# Carlo Rizzi (bass) plays in Frozen Farmer AND Tsuna and the Shadowlands
# (which was formed by ex-Bartok members)
# =========================================================================

print("\n--- Carlo Rizzi Network ---")
try:
    frozen_farmer = Band.objects.get(name="Frozen Farmer")
    bartok = Band.objects.get(name="Bartòk")
    add_connection(
        frozen_farmer, bartok, "scene_peer",
        "Carlo Rizzi (bass) in Frozen Farmer + Tsuna & Shadowlands (ex-Bartok members)"
    )
except Band.DoesNotExist:
    pass

# =========================================================================
# Big Fish Booking Agency Connections
# Il Triangolo's tour organized by Big Fish, which also represents:
# Afterhours, Baustelle, Eugenio Finardi, Marlene Kuntz
# =========================================================================

print("\n--- Big Fish Booking Agency Connections ---")

big_fish_bands = ["Il Triangolo", "Marlene Kuntz", "Afterhours"]
big_fish_in_db = []
for name in big_fish_bands:
    try:
        b = Band.objects.get(name=name)
        big_fish_in_db.append(b)
    except Band.DoesNotExist:
        pass

print(f"Big Fish bands in DB: {len(big_fish_in_db)}")
for i in range(len(big_fish_in_db)):
    for j in range(i + 1, len(big_fish_in_db)):
        add_connection(
            big_fish_in_db[i], big_fish_in_db[j],
            "scene_peer",
            "Big Fish booking agency"
        )

# =========================================================================
# Summary
# =========================================================================

print("\n" + "=" * 60)
print(f"LINKS ADDED: {changes['links_added']}")
print(f"LINKS SKIPPED: {changes['skipped']}")
print(f"CONNECTIONS ADDED: {changes['connections_added']}")
print(f"CONNECTIONS SKIPPED: {changes['conn_skipped']}")

# Final count
final_counts = Band.objects.annotate(link_count=Count('links'))
still_few = final_counts.filter(link_count__lt=3).count()
print(f"\nBands still with < 3 links: {still_few}")
total_links = Link.objects.count()
print(f"Total links in DB: {total_links}")
total_connections = BandConnection.objects.count()
print(f"Total connections in DB: {total_connections}")

# Show bands still with < 3
print("\nBands with < 3 links:")
for b in final_counts.filter(link_count__lt=3):
    print(f"  {b.name}: {b.link_count} links")
