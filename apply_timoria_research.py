# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Apply all research findings for Timoria (Band ID: 77).

Adds: missing links, releases (discography), label references, band connections,
and updates band fields (active_years, bio_en, discogs_id).

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_timoria_research.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Release, Link, Label, BandConnection
from django.db.models import Count
from django.utils.text import slugify

changes = {
    "links_added": 0,
    "links_skipped": 0,
    "releases_added": 0,
    "releases_skipped": 0,
    "connections_added": 0,
    "connections_skipped": 0,
    "labels_added": 0,
    "labels_skipped": 0,
}


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
        print(f"  + LINK: {band.name} -> {link_type}: {url[:80]}")
    else:
        changes["links_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {url[:80]}")


def add_release(band, title, year, label_name="", description="", format_type="cd"):
    """Add a release if it doesn't already exist."""
    existing = Release.objects.filter(band=band, title=title).exists()
    if not existing:
        slug = slugify(f"{band.name}-{title}")
        # Ensure unique slug
        if Release.objects.filter(slug=slug).exists():
            slug = f"{slug}-{year}"
        Release.objects.create(
            band=band,
            title=title,
            slug=slug,
            format=format_type,
            year=year,
            label=label_name,
            description=description,
            status="published",
        )
        changes["releases_added"] += 1
        print(f"  + RELEASE: {band.name} - {title} ({year})")
    else:
        changes["releases_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} - {title}")


def get_or_create_label(name, city="", website=""):
    """Get or create a label."""
    slug = slugify(name)
    label, created = Label.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "city": city,
            "website": website,
            "status": "active",
        }
    )
    if created:
        changes["labels_added"] += 1
        print(f"  + LABEL: {name}")
    else:
        changes["labels_skipped"] += 1
        print(f"  = LABEL (exists): {name}")
    return label


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
        changes["connections_skipped"] += 1
        print(f"  = CONN (exists): {from_band.name} -> {to_band.name} ({connection_type})")


# =========================================================================
# MAIN
# =========================================================================

print("\n=== TIMORIA RESEARCH APPLICATION ===\n")

# Get the band
timoria = Band.objects.get(id=77)
print(f"Band: {timoria.name} (ID: {timoria.pk})\n")

# =========================================================================
# 1. Update Band Fields
# =========================================================================
print("--- Updating Band Fields ---")

timoria.active_years = "1985-2003"
timoria.bio_en = (
    "Timoria were an Italian rock group formed in Brescia in 1985 (originally as Precious Time). "
    "They released nine studio albums between 1990 and 2003, with their commercial peak coming "
    "in the mid-1990s with Viaggio senza vento (1993) and 2020 SpeedBall (1995). "
    "Original vocalist Francesco Renga left in 1998 due to tensions with guitarist/songwriter "
    "Omar Pedrini and was replaced by Sasha Torrisi. The band dissolved in 2003."
)
timoria.discogs_id = "361405"
timoria.website = "http://www.timoria.it/"
timoria.save()
print(f"  Updated: active_years=1985-2003, discogs_id=361405, bio_en, website")

# =========================================================================
# 2. Add Labels
# =========================================================================
print("\n--- Adding Labels ---")

polygram = get_or_create_label("PolyGram", city="Milan", website="https://www.polygram.com")
polydor = get_or_create_label("Polydor", city="Milan", website="https://www.polydor.com")
mescal = get_or_create_label("Mescal", city="Milan", website="https://www.mescal.it")
tribe = get_or_create_label("Tribe Magazine", city="Milan")

# Mercury Records already exists in DB
try:
    mercury = Label.objects.get(slug="mercury-records")
    changes["labels_skipped"] += 1
    print(f"  = LABEL (exists): Mercury Records")
except Label.DoesNotExist:
    mercury = get_or_create_label("Mercury Records", city="New York")

# =========================================================================
# 3. Add Missing Links
# =========================================================================
print("\n--- Adding Links ---")

# Streaming links
add_link(timoria, "streaming", "https://music.apple.com/gb/artist/timoria/28980737", "Apple Music", "Official Apple Music artist page")
add_link(timoria, "streaming", "https://music.youtube.com/channel/UCIgK3lonzMPYTppvG0B4zJA", "YouTube Music", "YouTube Music channel")

# Bandcamp links
add_link(timoria, "purchase", "https://timoriast.bandcamp.com/", "1999 on Bandcamp", "1999 album on Bandcamp")
add_link(timoria, "purchase", "https://timoriand.bandcamp.com/", "Live Generazione Senza Vento", "Live album on Bandcamp")
add_link(timoria, "purchase", "https://timoriadm.bandcamp.com/", "Grand Hotel Timoria", "2002 live compilation on Bandcamp")

# Archive/Reference links
add_link(timoria, "archive", "https://rateyourmusic.com/artist/timoria", "RateYourMusic", "Complete discography")
add_link(timoria, "archive", "https://www.estatica.it/it/musica/timoria/discografia", "Estatica.it Discography", "Complete 18-release discography")
add_link(timoria, "archive", "https://www.spirit-of-rock.com/en/discography/Timoria/1", "Spirit of Rock", "Album/song data")
add_link(timoria, "archive", "https://www.viberate.com/artist/timoria/", "Viberate", "Song stats and analytics")
add_link(timoria, "archive", "https://genius.com/artists/Timoria/albums", "Genius", "Lyrics and tracklists")
add_link(timoria, "archive", "https://it.wikipedia.org/wiki/Timoria", "Wikipedia IT", "Italian Wikipedia article")
add_link(timoria, "archive", "https://www.albumoftheyear.org/artist/199823-timoria/", "Album of the Year", "Complete discography")

# Discogs release links
add_link(timoria, "archive", "https://www.discogs.com/master/288469-Timoria-2020-SpeedBall", "2020 SpeedBall on Discogs", "Discogs master release")
add_link(timoria, "archive", "https://www.discogs.com/master/394164-Timoria-Eta-Beta", "Eta Beta on Discogs", "Discogs master release")
add_link(timoria, "archive", "https://www.discogs.com/master/1089682-Timoria-El-Topo-Grand-Hotel", "El Topo Grand Hotel on Discogs", "Discogs master release")
add_link(timoria, "archive", "https://www.discogs.com/master/880239-Timoria-Viaggio-Senza-Vento", "Viaggio Senza Vento on Discogs", "Discogs master release")

# Video links
add_link(timoria, "video", "https://www.youtube.com/watch?v=ConkkS8I98c", "Sole Spento (Official Video)", "Official music video for Sole Spento")
add_link(timoria, "video", "https://www.youtube.com/watch?v=l42cMRZY__Y", "Sole Spento (Live MTV Day)", "Live performance")
add_link(timoria, "video", "https://www.youtube.com/watch?v=Hq_acEKujRY", "Sangue Impazzito (Live)", "Sasha Torrisi live performance")
add_link(timoria, "video", "https://www.youtube.com/watch?v=B2BcUfagb-4", "C'è tutto un mondo intorno (feat. Timoria)", "Antonella Ruggiero collaboration")

# =========================================================================
# 4. Add Releases (Discography)
# =========================================================================
print("\n--- Adding Releases ---")

# Studio Albums
add_release(timoria, "Colori che esplodono", 1990, "PolyGram", "Debut album; produced by Gianni Moroccolo (ex-CCCP)")
add_release(timoria, "Ritmo e dolore", 1991, "Polydor", "Second album")
add_release(timoria, "Storie per vivere", 1992, "Polydor", "First gold record (50,000+ copies); singles: Senza vento, Sangue impazzito")
add_release(timoria, "Viaggio senza vento", 1993, "PolyGram", "Concept album; collabs with Finardi, Pagani, Cabezas; gold record")
add_release(timoria, "2020 SpeedBall", 1995, "PolyGram", "Major commercial album; reissued 2020 for 25th anniversary")
add_release(timoria, "Eta Beta", 1997, "PolyGram", "Renga's final album")
add_release(timoria, "1999", 1999, "PolyGram", "Seventh studio album; first with Sasha Torrisi")
add_release(timoria, "El Topo Grand Hotel", 2001, "Tribe Magazine", "Includes Sole Spento (most famous later-era track)")
add_release(timoria, "Un Aldo qualunque sul treno magico", 2002, "", "Final studio album")

# Live Albums
add_release(timoria, "Timoria live: generazione senza vento", 2003, "", "Live album from farewell era")
add_release(timoria, "Grand Hotel Timoria", 2002, "Tribe Magazine", "Live compilation")

# EPs
add_release(timoria, "The Precious Time Demo", 1986, "", "Demo EP under original name", "demotape")
add_release(timoria, "Macchine e dollari", 1988, "PolyGram", "First major label EP", "vinyl")

# Compilation
add_release(timoria, "1985-1995", 1995, "", "Career retrospective compilation")
add_release(timoria, "Senzatempo: dieci anni", 1997, "", "10-year anniversary cassette compilation", "cassette")

# =========================================================================
# 5. Add Band Connections
# =========================================================================
print("\n--- Adding Connections ---")

# Antonella Ruggiero (collaboration on Registrazioni moderne 1997)
try:
    antonella = Band.objects.get(name__icontains="Antonella Ruggiero")
    add_connection(timoria, antonella, "collaboration", "Collaborated on 2 tracks for Registrazioni moderne (1997): Ti sento and C'è tutto un mondo intorno")
except Band.DoesNotExist:
    print(f"  = SKIP: Antonella Ruggiero not in DB")

# Gianni Moroccolo / CCCP Fedeli alla linea connection
try:
    cccp = Band.objects.get(name__icontains="CCCP")
    add_connection(timoria, cccp, "collaboration", "Gianni Moroccolo (ex-CCCP) produced Colori che esplodono (1990)")
except Band.DoesNotExist:
    print(f"  = SKIP: CCCP Fedeli alla linea not in DB")

# Subsonica - shared Antonella Ruggiero collaboration
try:
    subsonica = Band.objects.get(name__icontains="Subsonica")
    add_connection(timoria, subsonica, "scene_peer", "Both collaborated with Antonella Ruggiero; both 1990s Italian alternative rock acts")
except Band.DoesNotExist:
    print(f"  = SKIP: Subsonica not in DB")

# Litfiba - Italian rock peers
try:
    litfiba = Band.objects.get(name__icontains="Litfiba")
    add_connection(timoria, litfiba, "scene_peer", "Both major 1990s Italian rock acts; shared festival stages")
except Band.DoesNotExist:
    print(f"  = SKIP: Litfiba not in DB")

# Francesco Renga (solo career) - if in DB
try:
    renga = Band.objects.get(name__icontains="Francesco Renga")
    add_connection(timoria, renga, "shared_member", "Francesco Renga was Timoria's lead vocalist 1985-1998")
except Band.DoesNotExist:
    print(f"  = SKIP: Francesco Renga not in DB")

# =========================================================================
# 6. Summary
# =========================================================================
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print(f"  Links added:       {changes['links_added']}")
print(f"  Links skipped:     {changes['links_skipped']}")
print(f"  Releases added:    {changes['releases_added']}")
print(f"  Releases skipped:  {changes['releases_skipped']}")
print(f"  Connections added: {changes['connections_added']}")
print(f"  Connections skipped: {changes['connections_skipped']}")
print(f"  Labels added:      {changes['labels_added']}")
print(f"  Labels skipped:    {changes['labels_skipped']}")

# Final count check
timoria.refresh_from_db()
print(f"\nFinal counts for {timoria.name}:")
print(f"  Links: {timoria.links.count()}")
print(f"  Releases: {timoria.releases.count()}")
print(f"  Connections (from): {timoria.connections_from.count()}")
print(f"  Connections (to): {timoria.connections_to.count()}")
