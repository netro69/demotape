#!/usr/bin/env python3
"""
Apply all research findings for Sinistri (Band ID: 35, formerly Starfuckers).

Adds: missing links, releases, label references, band connections,
and updates band fields (active_years, bio_en, discogs_id).

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_sinistri_research.py
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
    label, created = Label.objects.get_or_create(
        name=name,
        defaults={"city": city, "website": website}
    )
    if created:
        changes["labels_added"] += 1
        print(f"  + LABEL: {name}")
    else:
        changes["labels_skipped"] += 1
    return label


def add_connection(band, target_name, connection_type, notes=""):
    """Add a band connection if it doesn't already exist."""
    target = Band.objects.filter(name=target_name).first()
    if not target:
        print(f"  ! TARGET NOT FOUND: {target_name}")
        return
    existing = BandConnection.objects.filter(
        from_band=band, to_band=target, connection_type=connection_type
    ).exists() or BandConnection.objects.filter(
        from_band=target, to_band=band, connection_type=connection_type
    ).exists()
    if not existing:
        BandConnection.objects.create(
            from_band=band,
            to_band=target,
            connection_type=connection_type,
            notes=notes,
        )
        changes["connections_added"] += 1
        print(f"  + CONNECTION: {band.name} -> {connection_type}: {target_name}")
    else:
        changes["connections_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {connection_type}: {target_name}")


def main():
    print("=" * 60)
    print("APPLYING RESEARCH: Sinistri (Band ID: 35)")
    print("=" * 60)

    try:
        band = Band.objects.get(id=35)
    except Band.DoesNotExist:
        print("ERROR: Band id=35 not found")
        return

    print(f"\nBand: {band.name}")
    print(f"Slug: {band.slug}")
    print(f"Current links: {band.links.count()}")
    current_conns = BandConnection.objects.filter(from_band=band).count() + BandConnection.objects.filter(to_band=band).count()
    print(f"Current connections: {current_conns}")

    # ================================================================
    # UPDATE BAND FIELDS
    # ================================================================
    print("\n--- Updating band fields ---")

    band.discogs_id = "187884"
    band.active_years = "1987-present"
    band.bio_en = ("Sinistri is the continuation of Starfuckers, one of Italy's most important avant-garde "
                   "experimental rock bands. Originally formed in 1987 as Starfuckers in Lunigiana (Tuscany), "
                   "the group evolved from raw Stooges-inspired garage/noise-rock to musique concrete-influenced "
                   "'concrete rock' to free-jazz/cubist post-rock to dark electronic/intuitive music trio as "
                   "Sinistri (2000-2004). They reverted to the Starfuckers name in 2008. "
                   "Key members: Manuele Giannini, Roberto Bertacchini, Alessandro Bocci. "
                   "Labels include Electric Eye, Underground, Lessness, Dbk Works, Hapna, Utech, Sometimes Records.")
    band.save()
    print(f"  + Updated: discogs_id, active_years, bio_en")

    # ================================================================
    # ADD LINKS
    # ================================================================
    print("\n--- Adding links ---")

    # Official / Primary
    add_link(band, "official", "https://starfuckers-sinistri.bandcamp.com/",
             "Bandcamp (Official Hub)", "Starfuckers / Sinistri main Bandcamp page")

    # Bandcamp specific albums
    add_link(band, "purchase", "https://starfuckers-sinistri.bandcamp.com/album/sinistri-free-pulse",
             "Free Pulse (Bandcamp)", "Sinistri - Free Pulse album on Bandcamp")
    add_link(band, "purchase", "https://starfuckers-sinistri.bandcamp.com/album/infrantumi",
             "Infrantumi (Bandcamp)", "Starfuckers - Infrantumi album on Bandcamp")
    add_link(band, "purchase", "https://starfuckers-sinistri.bandcamp.com/album/infinitive-sessions-music-is-a-pollution-of-time",
             "Infinitive Sessions (Bandcamp)", "Starfuckers - Infinitive Sessions on Bandcamp")

    # Discogs
    add_link(band, "purchase", "https://www.discogs.com/artist/224817-Starfuckers",
             "Discogs: Starfuckers", "Starfuckers Discogs artist page")
    add_link(band, "purchase", "https://www.discogs.com/artist/187884-Sinistri",
             "Discogs: Sinistri", "Sinistri Discogs artist page")

    # Streaming
    add_link(band, "streaming", "https://music.apple.com/us/artist/starfuckers/63130754",
             "Apple Music", "Starfuckers on Apple Music")
    add_link(band, "streaming", "https://soundcloud.com/sinistri",
             "SoundCloud", "Sinistri on SoundCloud")

    # Wikipedia / References
    add_link(band, "archive", "https://en.wikipedia.org/wiki/Starfuckers",
             "Wikipedia EN", "Starfuckers Wikipedia article")
    add_link(band, "archive", "https://it.wikipedia.org/wiki/Starfuckers",
             "Wikipedia IT", "Starfuckers Italian Wikipedia article")
    add_link(band, "archive", "https://www.allmusic.com/artist/starfuckers-mn0000014924",
             "AllMusic", "Starfuckers AllMusic biography & discography")

    # Reviews & Press
    add_link(band, "review", "https://www.ondarock.it/recensioni/2005_sinistri/",
             "OndaRock Review (Free Pulse)", "Italian review of Sinistri's Free Pulse")
    add_link(band, "review", "https://www.scaruffi.com/vol6/starfuck.html",
             "Piero Scaruffi's History of Rock",
             "Detailed biographical essay on Starfuckers' musical evolution")
    add_link(band, "interview", "https://www.thenewnoise.it/libere-strategie-storia-degli-starfuckers/",
             "The New Noise Interview",
             "2017 extensive interview with Bertacchini, Bocci, and Giannini")

    # Retail / Label
    add_link(band, "purchase", "https://www.forcedexposure.com/Artists/STARFUCKERS.html",
             "Forced Exposure", "US distributor for Starfuckers releases")
    add_link(band, "purchase", "https://www.soundohm.com/artist/starfuckers",
             "Soundohm", "EU distributor, specialist in electronic/avantgarde")

    # Aggregators
    add_link(band, "streaming", "https://rateyourmusic.com/artist/starfuckers",
             "RateYourMusic", "Starfuckers discography & ratings")
    add_link(band, "streaming", "https://www.beatport.com/artist/starfuckers/218949",
             "Beatport", "Starfuckers on Beatport")

    # ================================================================
    # ADD LABELS
    # ================================================================
    print("\n--- Adding labels ---")

    labels = [
        ("Electric Eye Records", "Italy"),
        ("Helter Skelter Records", "Italy"),
        ("Underground Records", "Italy"),
        ("Lessness", "Italy"),
        ("Drunken Fish", "USA"),
        ("Dbk Works", "Italy"),
        ("Hapna", "Sweden"),
        ("Utech Records", "USA"),
        ("Sometimes Records", "Italy"),
        ("Holy Mountain", "USA"),
        ("Tlön Uqbar", "USA"),
        ("The New Noise", "Italy"),
    ]
    for name, city in labels:
        get_or_create_label(name, city=city)

    # ================================================================
    # ADD RELEASES
    # ================================================================
    print("\n--- Adding releases ---")

    releases = [
        ("Metallic Diseases", 1989, "Electric Eye Records", "Debut album; raw Stooges-inspired noise/garage", "vinyl"),
        ("Brodo Di Cagne Strategico", 1991, "Electric Eye / Helter Skelter", "Jazzy noise-rock mini-album", "vinyl"),
        ("Sinistri", 1994, "Underground Records", "Aesthetic manifesto; 20th-century compositional techniques", "cd"),
        ("Infrantumi", 1997, "Lessness / Drunken Fish", "Post-rock's cryptic works; free-jazz, cubism, musique concrete", "cd"),
        ("Infinitive Sessions", 2002, "Dbk Works", "All-instrumental; funk-jazz to noise; sampled by Matmos", "cd"),
        ("Ordine 91-96", 2010, "Sometimes Records", "Compilation of rare tracks from early years", "cd"),
        ("Free Pulse", 2005, "Hapna", "First release as Sinistri; intuitive music, non-metric rhythms", "cd"),
        ("Timing The 183K Pulse", 2006, "Utech Records", "Eleven Intuitive Acts on a Defined Vamp; experimental dub/funk", "cd"),
    ]
    for title, year, label, desc, fmt in releases:
        add_release(band, title, year, label_name=label, description=desc, format_type=fmt)

    # ================================================================
    # ADD CONNECTIONS
    # ================================================================
    print("\n--- Adding connections ---")

    # Direct collaborators / same continuum
    add_connection(band, "M16", "same_continuum",
                   "Alessandro Bocci's side project with Manuele Giannini & Roberto Bertacchini")

    # Scene peers & influences
    add_connection(band, "This Heat", "influence",
                   "Primary stylistic reference; Starfuckers compared to This Heat's deconstructed approach")
    add_connection(band, "Matmos", "influence",
                   "Matmos heavily sampled Infinitive Sessions on The Civil War (2003)")
    add_connection(band, "Sonic Youth", "scene_peer",
                   "Starfuckers contributed to Gioventu Sonica tribute (1991), covering Death Valley '69")
    add_connection(band, "Afterhours", "scene_peer",
                   "Xabier Iriondo (Afterhours experimental guitarist) runs Phonometak Labs; shared Bologna scene")
    add_connection(band, "C.S.I.", "scene_peer",
                   "Bologna alternative scene peers; same era, shared ethos")
    add_connection(band, "Massimo Volume", "scene_peer",
                   "Bologna peers; Dario Parisini (Dish-Is-Nein) also played with them")
    add_connection(band, "CCCP Fedeli alla linea", "scene_peer",
                   "Same Bologna punk/alternative scene; shared political/alternative ethos")
    add_connection(band, "Royal Trux", "influence",
                   "Debut Metallic Diseases compared to Royal Trux's retro-brainy garage-blues")
    add_connection(band, "Faust", "influence",
                   "Infrantumi blends free-jazz, dissonant avantgarde, Faust")

    # ================================================================
    # SUMMARY
    # ================================================================
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for k, v in changes.items():
        print(f"  {k}: {v}")

    print(f"\nFinal state:")
    print(f"  Links: {band.links.count()}")
    final_conns = BandConnection.objects.filter(from_band=band).count() + BandConnection.objects.filter(to_band=band).count()
    print(f"  Connections: {final_conns}")

    if band.links.count() >= 8 and final_conns >= 8:
        print("\nSinistri is now FULLY RESEARCHED (>=8 links AND >=8 connections)")
    else:
        print(f"\nSinistri still needs work (links={band.links.count()}, conns={final_conns})")


if __name__ == "__main__":
    main()
